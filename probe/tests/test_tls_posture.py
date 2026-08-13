"""
test_tls_posture.py — Tier 2.4: cipher-suite classification + TLS posture grading.

Pure logic (no network): given cipher names and accepted protocol versions, flag
weak cryptography and grade the overall posture. The live enumeration in
tls_scanner is exercised separately against a loopback TLS server.
"""

from __future__ import annotations

import pytest

from scanner.tls_scanner import classify_cipher, grade_tls_posture


# ── cipher classification ─────────────────────────────────────────────────────

class TestClassifyCipher:
    def test_modern_aead_pfs(self):
        c = classify_cipher("ECDHE-RSA-AES256-GCM-SHA384")
        assert c["forward_secrecy"] is True
        assert c["aead"] is True
        assert c["cbc"] is False
        assert c["weak"] is False

    def test_rsa_cbc_no_pfs(self):
        c = classify_cipher("AES128-SHA")
        assert c["forward_secrecy"] is False
        assert c["cbc"] is True
        assert c["aead"] is False
        assert c["weak"] is False        # CBC alone isn't flagged weak, just no PFS

    def test_rc4_is_weak(self):
        c = classify_cipher("ECDHE-RSA-RC4-SHA")
        assert c["weak"] is True
        assert any("RC4" in r for r in c["weak_reasons"])

    def test_null_cipher_is_weak(self):
        c = classify_cipher("ECDHE-RSA-NULL-SHA")
        assert c["weak"] is True
        assert any("NULL" in r for r in c["weak_reasons"])

    def test_3des_is_weak(self):
        c = classify_cipher("DES-CBC3-SHA")
        assert c["weak"] is True
        assert any("3DES" in r for r in c["weak_reasons"])

    def test_export_and_md5_are_weak(self):
        c = classify_cipher("EXP-RC4-MD5")
        assert c["weak"] is True
        reasons = " ".join(c["weak_reasons"])
        assert "EXPORT" in reasons
        assert "MD5" in reasons

    def test_anonymous_is_weak(self):
        c = classify_cipher("ADH-AES256-SHA")
        assert c["weak"] is True
        assert any("anon" in r.lower() for r in c["weak_reasons"])

    def test_chacha20_is_aead(self):
        c = classify_cipher("ECDHE-RSA-CHACHA20-POLY1305")
        assert c["aead"] is True
        assert c["forward_secrecy"] is True


# ── posture grading ───────────────────────────────────────────────────────────

def _modern():
    return [classify_cipher("ECDHE-RSA-AES256-GCM-SHA384")]


class TestGradeTlsPosture:
    def test_grade_a_modern(self):
        g = grade_tls_posture(["TLSv1_3", "TLSv1_2"], _modern())
        assert g["grade"] == "A"
        assert g["findings"] == []

    def test_grade_b_no_tls13(self):
        g = grade_tls_posture(["TLSv1_2"], _modern())
        assert g["grade"] == "B"
        assert any("1.3" in f for f in g["findings"])

    def test_grade_c_tls11(self):
        g = grade_tls_posture(["TLSv1_2", "TLSv1_1"], _modern())
        assert g["grade"] == "C"
        assert any("1.1" in f for f in g["findings"])

    def test_grade_c_no_forward_secrecy(self):
        g = grade_tls_posture(["TLSv1_3", "TLSv1_2"],
                              [classify_cipher("AES128-SHA")])
        assert g["grade"] == "C"
        assert any("forward secrecy" in f for f in g["findings"])

    def test_grade_f_tls10(self):
        g = grade_tls_posture(["TLSv1_2", "TLSv1_0"], _modern())
        assert g["grade"] == "F"
        assert any("TLS1.0" in f or "1.0" in f for f in g["findings"])

    def test_grade_f_weak_cipher(self):
        g = grade_tls_posture(["TLSv1_2"],
                              [classify_cipher("ECDHE-RSA-RC4-SHA")])
        assert g["grade"] == "F"

    def test_empty_cipher_details_still_grades_protocols(self):
        g = grade_tls_posture(["TLSv1_0"], [])
        assert g["grade"] == "F"
