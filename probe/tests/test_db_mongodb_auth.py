"""
test_db_mongodb_auth.py — MongoDB auth posture, and the two ways to get it wrong.

WHY. db_scan identified MongoDB and stopped. An internet-reachable MongoDB with
no authentication is one of the highest-severity findings in a network
assessment, and Vedha reported it identically to a locked-down one.

TRAP 1 — isMaster proves nothing. hello/isMaster is answered WITHOUT credentials
even on a fully hardened server. Deriving exposure from it would flag every
MongoDB in the estate.

TRAP 2 — OP_QUERY is dead. MongoDB 5.1 removed OP_QUERY for everything but the
handshake. An auth probe sent as OP_QUERY fails on every modern server, and
reading that wire failure as "auth enforced" is a false NEGATIVE on exactly the
exposed instances the rule exists to catch. Hence OP_MSG.
"""
from __future__ import annotations

import struct

from scanner.db_scanner import build_op_msg_command, interpret_mongodb_auth


class TestOpMsgFraming:
    def test_declared_length_matches_actual(self):
        msg = build_op_msg_command("serverStatus")
        assert struct.unpack("<i", msg[:4])[0] == len(msg)

    def test_opcode_is_op_msg_not_op_query(self):
        """2013 = OP_MSG. 2004 = OP_QUERY, which modern servers reject."""
        msg = build_op_msg_command("serverStatus")
        assert struct.unpack("<i", msg[12:16])[0] == 2013

    def test_bson_document_is_self_consistent(self):
        msg = build_op_msg_command("serverStatus")
        doc = msg[21:]                       # header(16) + flagBits(4) + kind(1)
        assert struct.unpack("<i", doc[:4])[0] == len(doc)
        assert doc.endswith(b"\x00")

    def test_db_field_is_present(self):
        """OP_MSG requires $db inside the command document."""
        assert b"$db\x00" in build_op_msg_command("serverStatus", db="admin")
        assert b"admin\x00" in build_op_msg_command("serverStatus", db="admin")


class TestAuthInterpretation:
    def test_unauthorized_means_auth_enforced(self):
        out = interpret_mongodb_auth(
            b"\x01\x00errmsg\x00not authorized on admin to execute command")
        assert out["auth_required"] is True
        assert out["unauthenticated_read"] is False

    def test_unauthorized_codename(self):
        out = interpret_mongodb_auth(b"codeName\x00Unauthorized\x00")
        assert out["auth_required"] is True

    def test_successful_serverstatus_means_exposed(self):
        out = interpret_mongodb_auth(
            b"\x10uptime\x00\x2c\x01\x00\x00\x03connections\x00")
        assert out["unauthenticated_read"] is True
        assert out["auth_required"] is False

    def test_silence_claims_nothing(self):
        """Neither exposed nor hardened — an empty dict keeps the rule honest
        instead of inventing a posture."""
        assert interpret_mongodb_auth(b"") == {}
        assert interpret_mongodb_auth(b"\x00\x00\x00\x00garbage") == {}

    def test_auth_marker_wins_over_ok_marker(self):
        """A reply containing both must be read as enforced — the error path is
        the definitive statement."""
        out = interpret_mongodb_auth(b"uptime\x00 ... not authorized ...")
        assert out["auth_required"] is True
        assert out["unauthenticated_read"] is False
