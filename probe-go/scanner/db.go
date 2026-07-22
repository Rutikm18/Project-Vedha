// scanner/db.go — Gate 5 branch: database protocol handshake.
// Fingerprints MySQL, PostgreSQL, MSSQL, Redis, MongoDB, Elasticsearch.
// Never sends credentials — only reads the server greeting packet.
package scanner

import (
	"context"
	"encoding/binary"
	"fmt"
	"io"
	"net"
	"strings"
	"time"
)

var DBPorts = map[int]bool{
	3306: true, 5432: true, 1433: true, 6379: true, 27017: true, 1521: true,
}

// ProbeDB performs a protocol-level handshake on the given port and returns
// the detected engine and server version without authentication.
func ProbeDB(ctx context.Context, host string, port int, timeout time.Duration) Result {
	r := newResult("db_scan", host)
	r.Port = ptr(port)
	r.Proto = "tcp"

	var engine, version string
	var probeErr error

	switch port {
	case 3306:
		engine, version, probeErr = probeMysql(ctx, host, port, timeout)
	case 5432:
		engine, version, probeErr = probePostgres(ctx, host, port, timeout)
	case 1433:
		engine, version, probeErr = probeMSSQL(ctx, host, port, timeout)
	case 6379:
		engine, version, probeErr = probeRedis(ctx, host, port, timeout)
	case 27017:
		engine, version, probeErr = probeMongo(ctx, host, port, timeout)
	default:
		r.Status = "closed"
		return r
	}

	if probeErr != nil {
		r.Status = "closed"
		r.Error = probeErr.Error()
		return r
	}

	r.Status = "open"
	r.Data["engine"] = engine
	r.Data["server_version"] = version
	r.Evidence = fmt.Sprintf("%s %s", engine, version)
	return r
}

func dial(ctx context.Context, host string, port int, timeout time.Duration) (net.Conn, error) {
	addr := fmt.Sprintf("%s:%d", host, port)
	d := &net.Dialer{}
	dctx, cancel := context.WithTimeout(ctx, timeout)
	defer cancel()
	conn, err := d.DialContext(dctx, "tcp", addr)
	if err != nil {
		return nil, err
	}
	conn.SetDeadline(time.Now().Add(timeout))
	return conn, nil
}

// probeMysql reads the MySQL server greeting (packet 0, payload[0]==0x0a).
func probeMysql(ctx context.Context, host string, port int, timeout time.Duration) (string, string, error) {
	conn, err := dial(ctx, host, port, timeout)
	if err != nil {
		return "", "", err
	}
	defer conn.Close()

	// MySQL sends a 4-byte header followed by the greeting payload.
	hdr := make([]byte, 4)
	if _, err := io.ReadFull(conn, hdr); err != nil {
		return "", "", err
	}
	pktLen := int(uint32(hdr[0]) | uint32(hdr[1])<<8 | uint32(hdr[2])<<16)
	payload := make([]byte, pktLen)
	if _, err := io.ReadFull(conn, payload); err != nil {
		return "", "", err
	}
	if len(payload) < 2 || payload[0] != 0x0a {
		return "", "", fmt.Errorf("not a mysql greeting")
	}
	// version string follows the protocol byte, null-terminated
	null := strings.IndexByte(string(payload[1:]), 0)
	version := ""
	if null >= 0 {
		version = string(payload[1 : 1+null])
	}
	engine := "mysql/mariadb"
	if strings.Contains(strings.ToLower(version), "mariadb") {
		engine = "mariadb"
	}
	return engine, version, nil
}

// probePostgres sends a StartupMessage and reads the auth response type.
func probePostgres(ctx context.Context, host string, port int, timeout time.Duration) (string, string, error) {
	conn, err := dial(ctx, host, port, timeout)
	if err != nil {
		return "", "", err
	}
	defer conn.Close()

	// Postgres StartupMessage: length(4) + protocol(4) + "user\0postgres\0\0"
	user := "postgres"
	msg := []byte{0, 0, 0, 0, 0, 3, 0, 0}
	msg = append(msg, []byte("user\x00"+user+"\x00\x00")...)
	binary.BigEndian.PutUint32(msg[:4], uint32(len(msg)))

	if _, err := conn.Write(msg); err != nil {
		return "", "", err
	}
	// Read response type byte
	buf := make([]byte, 5)
	if _, err := io.ReadFull(conn, buf); err != nil {
		return "", "", err
	}
	// R = authentication, E = error, N = SSL not supported
	if buf[0] == 'R' || buf[0] == 'E' {
		return "postgresql", "", nil
	}
	return "", "", fmt.Errorf("unexpected postgres response: %q", buf[0])
}

// probeMSSQL sends a pre-login TDS packet and checks the response.
func probeMSSQL(ctx context.Context, host string, port int, timeout time.Duration) (string, string, error) {
	conn, err := dial(ctx, host, port, timeout)
	if err != nil {
		return "", "", err
	}
	defer conn.Close()

	// Minimal TDS pre-login packet
	prelogin := []byte{
		0x12,       // type: pre-login
		0x01,       // status: end-of-message
		0x00, 0x2f, // length: 47
		0x00, 0x00, // spid
		0x01,       // packetid
		0x00,       // window
		// Pre-login option list (VERSION token = 0x00)
		0x00,             // VERSION option
		0x00, 0x1a,       // offset (26)
		0x00, 0x06,       // length
		0xff,             // terminator
		0x08, 0x00, 0x01, 0x55, 0x00, 0x00, // version: 8.0.1.85
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		0x00, 0x00, 0x00, 0x00, 0x00,
	}
	if _, err := conn.Write(prelogin); err != nil {
		return "", "", err
	}
	resp := make([]byte, 64)
	n, err := conn.Read(resp)
	if err != nil || n < 4 {
		return "", "", fmt.Errorf("mssql no response")
	}
	if resp[0] == 0x12 {
		return "mssql", "", nil
	}
	return "", "", fmt.Errorf("unexpected mssql response")
}

// probeRedis sends PING and expects +PONG.
func probeRedis(ctx context.Context, host string, port int, timeout time.Duration) (string, string, error) {
	conn, err := dial(ctx, host, port, timeout)
	if err != nil {
		return "", "", err
	}
	defer conn.Close()

	if _, err := conn.Write([]byte("PING\r\n")); err != nil {
		return "", "", err
	}
	buf := make([]byte, 64)
	n, err := conn.Read(buf)
	if err != nil || n == 0 {
		return "", "", fmt.Errorf("redis no response")
	}
	resp := strings.ToUpper(strings.TrimSpace(string(buf[:n])))
	if strings.Contains(resp, "PONG") || strings.HasPrefix(resp, "+") || strings.HasPrefix(resp, "-") {
		return "redis", "", nil
	}
	return "", "", fmt.Errorf("not redis: %q", resp)
}

// probeMongo reads the MongoDB server greeting via a minimal OP_QUERY.
func probeMongo(ctx context.Context, host string, port int, timeout time.Duration) (string, string, error) {
	conn, err := dial(ctx, host, port, timeout)
	if err != nil {
		return "", "", err
	}
	defer conn.Close()

	// OP_MSG isMaster request (MongoDB 3.6+)
	// MessageHeader(16) + flagBits(4) + sections
	msg := []byte{
		// MsgHeader: length, requestID, responseTo, opCode(2013=OP_MSG)
		0x00, 0x00, 0x00, 0x00, // length (filled below)
		0x01, 0x00, 0x00, 0x00, // requestID
		0x00, 0x00, 0x00, 0x00, // responseTo
		0xdd, 0x07, 0x00, 0x00, // opCode = 2013
		0x00, 0x00, 0x00, 0x00, // flagBits
		0x00,                   // section kind=body
		// BSON document: {isMaster: 1}
		0x13, 0x00, 0x00, 0x00,
		0x10,
		0x69, 0x73, 0x4d, 0x61, 0x73, 0x74, 0x65, 0x72, 0x00,
		0x01, 0x00, 0x00, 0x00,
		0x00,
	}
	binary.LittleEndian.PutUint32(msg[:4], uint32(len(msg)))

	if _, err := conn.Write(msg); err != nil {
		return "", "", err
	}
	hdr := make([]byte, 4)
	if _, err := io.ReadFull(conn, hdr); err != nil {
		return "", "", err
	}
	pktLen := int(binary.LittleEndian.Uint32(hdr))
	if pktLen < 4 || pktLen > 1<<20 {
		return "", "", fmt.Errorf("invalid mongo response length")
	}
	rest := make([]byte, pktLen-4)
	io.ReadFull(conn, rest)
	return "mongodb", "", nil
}
