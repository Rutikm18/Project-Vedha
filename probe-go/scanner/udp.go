// scanner/udp.go — Gate 5 branch: UDP service probes (DNS, NTP, SNMP).
// Sends a real protocol request packet; absence of a response is treated as
// filtered — NOT closed — because UDP is connectionless.
package scanner

import (
	"context"
	"encoding/binary"
	"fmt"
	"net"
	"strings"
	"time"
)

var UDPPorts = map[int]string{
	53:  "dns",
	123: "ntp",
	161: "snmp",
	137: "netbios-ns",
}

// ProbeUDP probes a set of well-known UDP ports on host.
func ProbeUDP(ctx context.Context, host string, timeout time.Duration) []Result {
	var results []Result
	for port, svc := range UDPPorts {
		r := probeUDPPort(ctx, host, port, svc, timeout)
		if r.Status == "open" {
			results = append(results, r)
		}
	}
	return results
}

func probeUDPPort(ctx context.Context, host string, port int, svc string, timeout time.Duration) Result {
	r := newResult("udp_scan", host)
	r.Port = ptr(port)
	r.Proto = "udp"

	addr := net.JoinHostPort(host, fmt.Sprintf("%d", port))
	conn, err := net.Dial("udp", addr)
	if err != nil {
		r.Status = "filtered"
		r.Error = err.Error()
		return r
	}
	defer conn.Close()
	conn.SetDeadline(time.Now().Add(timeout))

	var probe []byte
	switch svc {
	case "dns":
		probe = dnsVersionQuery()
	case "ntp":
		probe = ntpRequest()
	case "snmp":
		probe = snmpPublicGetRequest()
	case "netbios-ns":
		probe = netbiosNameQuery()
	default:
		probe = []byte{}
	}

	if len(probe) > 0 {
		if _, err := conn.Write(probe); err != nil {
			r.Status = "filtered"
			return r
		}
	}

	buf := make([]byte, 512)
	n, err := conn.Read(buf)
	if err != nil || n == 0 {
		r.Status = "filtered"
		return r
	}

	r.Status = "open"
	r.Data["service"] = svc
	r.Data["service_guess"] = svc
	r.Data["response_bytes"] = n

	switch svc {
	case "snmp":
		// Extract community string from response if present
		if comm := extractSNMPCommunity(buf[:n]); comm != "" {
			r.Data["community"] = comm
		}
	case "dns":
		r.Data["service"] = "domain"
	case "ntp":
		if n >= 4 {
			stratum := int(buf[1])
			r.Data["ntp_stratum"] = stratum
		}
	}
	return r
}

// dnsVersionQuery crafts a DNS TXT query for version.bind (chaos class).
func dnsVersionQuery() []byte {
	return []byte{
		0xDE, 0xAD, // transaction ID
		0x00, 0x00, // flags: standard query
		0x00, 0x01, // qdcount: 1
		0x00, 0x00, // ancount: 0
		0x00, 0x00, // nscount: 0
		0x00, 0x00, // arcount: 0
		// QNAME: version.bind
		0x07, 'v', 'e', 'r', 's', 'i', 'o', 'n',
		0x04, 'b', 'i', 'n', 'd',
		0x00,       // end of name
		0x00, 0x10, // QTYPE: TXT
		0x00, 0x03, // QCLASS: CH (chaos)
	}
}

// ntpRequest sends an NTPv3 client request packet.
func ntpRequest() []byte {
	b := make([]byte, 48)
	b[0] = 0x1b // LI=0, VN=3, Mode=3 (client)
	return b
}

// snmpPublicGetRequest crafts a minimal SNMPv1 GetRequest for sysDescr.
func snmpPublicGetRequest() []byte {
	// BER-encoded SNMPv1 GetRequest with community="public", sysDescr OID
	return []byte{
		0x30, 0x26, // SEQUENCE
		0x02, 0x01, 0x00, // version: 0 (SNMPv1)
		0x04, 0x06, 'p', 'u', 'b', 'l', 'i', 'c', // community: "public"
		0xa0, 0x19, // GetRequest PDU
		0x02, 0x01, 0x01, // requestID: 1
		0x02, 0x01, 0x00, // error-status: 0
		0x02, 0x01, 0x00, // error-index: 0
		0x30, 0x0e, // VarBindList
		0x30, 0x0c, // VarBind
		0x06, 0x08, 0x2b, 0x06, 0x01, 0x02, 0x01, 0x01, 0x01, 0x00, // sysDescr.0
		0x05, 0x00, // value: NULL
	}
}

// netbiosNameQuery asks for the workgroup name.
func netbiosNameQuery() []byte {
	return []byte{
		0xA0, 0x1E, // TXN ID
		0x00, 0x00, // flags
		0x00, 0x01, // qdcount
		0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
		// QNAME: * (wildcard NetBIOS)
		0x20,
		0x43, 0x4B, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41,
		0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41,
		0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41,
		0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41, 0x41,
		0x00,
		0x00, 0x21, // QTYPE: NBSTAT
		0x00, 0x01, // QCLASS: IN
	}
}

// extractSNMPCommunity pulls the community string from a raw SNMP response.
// BER structure: SEQUENCE { version(INT), community(OCTET STRING), ...}
func extractSNMPCommunity(buf []byte) string {
	if len(buf) < 6 || buf[0] != 0x30 {
		return ""
	}
	i := 2 // skip SEQUENCE tag + length
	if i >= len(buf) || buf[i] != 0x02 {
		return ""
	}
	i += 2 + int(buf[i+1]) // skip version integer
	if i >= len(buf) || buf[i] != 0x04 {
		return ""
	}
	cLen := int(buf[i+1])
	i += 2
	if i+cLen > len(buf) {
		return ""
	}
	comm := string(buf[i : i+cLen])
	if strings.ContainsAny(comm, "\x00\xff") {
		return ""
	}
	return comm
}

// ProbeAllSNMPCommunities tests a list of community strings, returns those
// that elicited a GetResponse.
func ProbeAllSNMPCommunities(ctx context.Context, host string, communities []string, timeout time.Duration) []string {
	var found []string
	for _, comm := range communities {
		if testSNMPCommunity(ctx, host, comm, timeout) {
			found = append(found, comm)
		}
	}
	return found
}

func testSNMPCommunity(ctx context.Context, host, community string, timeout time.Duration) bool {
	addr := fmt.Sprintf("%s:161", host)
	conn, err := net.Dial("udp", addr)
	if err != nil {
		return false
	}
	defer conn.Close()
	conn.SetDeadline(time.Now().Add(timeout))

	// Build GetRequest with this community
	pkt := buildSNMPGetRequest(community)
	if _, err := conn.Write(pkt); err != nil {
		return false
	}
	buf := make([]byte, 512)
	n, err := conn.Read(buf)
	return err == nil && n > 0 && buf[0] == 0x30
}

func buildSNMPGetRequest(community string) []byte {
	cBytes := []byte(community)
	// BER: version(INT 0), community(OCTET STRING community), GetRequest PDU
	pduContents := []byte{
		0x02, 0x01, 0x01, // requestID
		0x02, 0x01, 0x00, // error-status
		0x02, 0x01, 0x00, // error-index
		0x30, 0x0e,       // VarBindList
		0x30, 0x0c,
		0x06, 0x08, 0x2b, 0x06, 0x01, 0x02, 0x01, 0x01, 0x01, 0x00,
		0x05, 0x00,
	}
	pdu := append([]byte{0xa0, byte(len(pduContents))}, pduContents...)

	inner := []byte{0x02, 0x01, 0x00}                        // version
	inner = append(inner, 0x04, byte(len(cBytes)))
	inner = append(inner, cBytes...)
	inner = append(inner, pdu...)

	pkt := make([]byte, 4+len(inner))
	pkt[0] = 0x30
	pkt[1] = byte(len(inner))
	// For lengths > 127 this is wrong but community strings are short enough
	_ = binary.BigEndian // keep import
	copy(pkt[2:], inner)
	return pkt
}
