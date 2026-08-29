import struct
from scanner.smb_scanner import parse_smb2_security_mode, _smb2_negotiate


def _smb2_negotiate_response(security_mode: int, dialect: int) -> bytes:
    # 4-byte Direct-TCP transport header + 64-byte SMB2 header + NEGOTIATE body.
    # A SUCCESSFUL NEGOTIATE response: header Status=0, Command=0, body StructSize=65.
    nbt = b"\x00\x00\x00\x80"
    header = b"\xfeSMB" + b"\x00" * 60            # 64-byte SMB2 header (status/cmd = 0)
    body = struct.pack("<HHH", 65, security_mode, dialect)  # StructSize, SecMode, Dialect
    return nbt + header + body


def _smb2_error_response(status: int) -> bytes:
    """An SMB2 ERROR response (e.g. STATUS_INVALID_PARAMETER). Windows returns
    this when SMB 3.1.1 is offered without a preauth-integrity negotiate context.
    Its body StructureSize is 9 (not 65) and it carries NO SecurityMode/dialect."""
    nbt = b"\x00\x00\x00\x48"
    header = (b"\xfeSMB" + struct.pack("<H", 64) + b"\x00" * 2 +  # proto, structsize, credit
              struct.pack("<I", status) +                         # Status  (abs offset 12)
              struct.pack("<H", 0x0000) +                         # Command NEGOTIATE (abs 16)
              b"\x00" * 2 + b"\x00" * 4 + b"\x00" * 4 +           # creditresp, flags, next
              b"\x00" * 8 + b"\x00" * 4 + b"\x00" * 4 +           # msgid, reserved, treeid
              b"\x00" * 8 + b"\x00" * 16)                          # sessionid, signature
    body = struct.pack("<H", 9) + b"\x00\x00" + struct.pack("<I", 0)  # ERROR body StructSize=9
    return nbt + header + body


def test_signing_required_smb311():
    resp = _smb2_negotiate_response(0x0003, 0x0311)  # enabled + required
    out = parse_smb2_security_mode(resp)
    assert out["signing_parsed"] is True
    assert out["signing_enabled"] is True
    assert out["signing_required"] is True
    assert out["negotiated_dialect"] == "0x0311"


def test_signing_not_required():
    resp = _smb2_negotiate_response(0x0001, 0x0210)  # enabled, NOT required
    out = parse_smb2_security_mode(resp)
    assert out["signing_required"] is False


def test_garbage_response():
    assert parse_smb2_security_mode(b"nope")["signing_parsed"] is False


# --- regression tests for the confirmed signing/dialect bug ----------------- #

def test_error_response_not_parsed_as_signing():
    """The confirmed bug: an SMB2 error response (STATUS_INVALID_PARAMETER) was
    read as a negotiate response, yielding bogus signing=false + dialect 0x0000.
    It must be rejected, not mislabelled."""
    resp = _smb2_error_response(0xC000000D)  # STATUS_INVALID_PARAMETER
    out = parse_smb2_security_mode(resp)
    assert out["signing_parsed"] is False
    # And it must NOT claim a (bogus) dialect/signing posture.
    assert out.get("negotiated_dialect") != "0x0000"
    assert "signing_required" not in out or out.get("signing_required") is None


def test_truncated_negotiate_body_not_parsed():
    """A response with the wrong body StructureSize is not a valid NEGOTIATE."""
    nbt = b"\x00\x00\x00\x44"
    header = b"\xfeSMB" + b"\x00" * 60
    body = struct.pack("<HHH", 9, 0x0003, 0x0311)  # StructSize 9, not 65
    out = parse_smb2_security_mode(nbt + header + body)
    assert out["signing_parsed"] is False


def test_signing_supported_field_present():
    """Step 13: expose signing_supported (protocol-precise), not only the
    ambiguous signing_enabled alias."""
    resp = _smb2_negotiate_response(0x0003, 0x0311)
    out = parse_smb2_security_mode(resp)
    assert out["signing_supported"] is True
    assert out["signing_required"] is True


def test_request_offers_311_with_preauth_context():
    """FIX 4: 3.1.1 IS now advertised, together with the mandatory preauth-integrity
    negotiate context — so Windows selects 3.1.1 (MS-SMB2 3.3.5.4) instead of being
    forced down to 3.0.2, and does NOT reject with STATUS_INVALID_PARAMETER."""
    req = _smb2_negotiate()
    assert b"\x11\x03" in req                                   # 0x0311 little-endian offered
    ctx_off = struct.unpack_from("<I", req, 64 + 28)[0]         # NegotiateContextOffset
    ctx_count = struct.unpack_from("<H", req, 64 + 32)[0]       # NegotiateContextCount
    assert ctx_count == 2 and ctx_off % 8 == 0
    assert struct.unpack_from("<H", req, ctx_off)[0] == 0x0001  # PREAUTH_INTEGRITY context
