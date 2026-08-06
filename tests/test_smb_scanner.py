import struct
from scanner.smb_scanner import parse_smb2_security_mode


def _smb2_negotiate_response(security_mode: int, dialect: int) -> bytes:
    # 4-byte Direct-TCP transport header + 64-byte SMB2 header + NEGOTIATE body.
    nbt = b"\x00\x00\x00\x80"
    header = b"\xfeSMB" + b"\x00" * 60            # 64-byte SMB2 header
    body = struct.pack("<HHH", 65, security_mode, dialect)  # StructSize, SecMode, Dialect
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
