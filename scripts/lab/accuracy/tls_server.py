"""Minimal HTTPS listener for the accuracy lab (stdlib only, no third-party code).

  weak    TLS 1.0 - 1.2, every cipher OpenSSL will still offer at security level 0
          (3DES included), the 1024-bit key and the expired certificate
  anon    TLS 1.2 with anonymous ECDH (AECDH-AES256-SHA) as the only cipher
  strong  TLS 1.2 - 1.3, ECDHE with AES-GCM / ChaCha20 only, 2048-bit, in date

Answers every request with a fixed page. Lab use only.
"""
import http.server
import ssl
import sys

MODE = sys.argv[1] if len(sys.argv) > 1 else "strong"
ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
if MODE == "weak":
    ctx.minimum_version = ssl.TLSVersion.TLSv1
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    ctx.set_ciphers("ALL:@SECLEVEL=0")
    ctx.load_cert_chain("/srv/certs/weak.crt", "/srv/certs/weak.key")
elif MODE == "anon":
    # Anonymous DH: no server authentication, so anyone in the path can impersonate
    # the server. (3DES would be the classic choice, but OpenSSL 3.5 no longer ships it.)
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.maximum_version = ssl.TLSVersion.TLSv1_2
    ctx.set_ciphers("AECDH-AES256-SHA:@SECLEVEL=0")
    ctx.load_cert_chain("/srv/certs/strong.crt", "/srv/certs/strong.key")
else:
    ctx.minimum_version = ssl.TLSVersion.TLSv1_2
    ctx.set_ciphers("ECDHE+AESGCM:ECDHE+CHACHA20")
    ctx.load_cert_chain("/srv/certs/strong.crt", "/srv/certs/strong.key")


class Page(http.server.BaseHTTPRequestHandler):
    server_version = "lab"
    sys_version = ""

    def do_GET(self):
        body = b"accuracy lab\n"
        self.send_response(200)
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def log_message(self, *args):
        pass


srv = http.server.ThreadingHTTPServer(("0.0.0.0", 443), Page)
srv.socket = ctx.wrap_socket(srv.socket, server_side=True)
srv.serve_forever()
