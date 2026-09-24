"""Regulatory citation grounding: control references the packs don't contain are flagged."""
from __future__ import annotations

from app.compliance.citations import check_citations, extract_citations


def test_extracts_common_citation_shapes():
    text = ("See GDPR Art. 32(1)(a), NYDFS §500.17, RBI Annex 1 §7, 16 CFR 314.4(c)(5), "
            "PCI Req 4.2.1, ISO A.8.24, NIST SC-8 and SAMA 3.3.17.")
    found = extract_citations(text)
    for c in ("art. 32(1)(a)", "§500.17", "annex 1 §7", "16 cfr 314.4(c)(5)", "req 4.2.1",
              "a.8.24", "sc-8", "3.3.17"):
        assert c in found, c


def test_known_citations_are_verified():
    out = check_citations("Under Art. 33 notify within 72h; RBI Annex 1 §19 and §500.17 also apply.")
    assert out["unverified"] == []
    assert set(out["verified"]) >= {"art. 33", "annex 1 §19", "§500.17"}


def test_invented_citations_are_flagged():
    out = check_citations("This breaches DORA Art. 99(7) and NYDFS §500.99 and RBI Annex 1 §41.")
    assert set(out["unverified"]) == {"art. 99(7)", "§500.99", "annex 1 §41"}


def test_article_spelled_out_is_normalized():
    assert check_citations("Article 32 applies")["verified"] == ["art. 32"]


def test_non_citation_text_is_ignored():
    out = check_citations("Upgrade OpenSSH to 9.8, disable TLS 1.0, CVE-2024-6387, CVSS 8.1, port 445.")
    assert out == {"verified": [], "unverified": []}


def test_parent_article_of_known_subclause_is_accepted():
    # The packs cite Art. 32(1)(a); a model citing plain "Art. 32" is still grounded.
    assert check_citations("GDPR Art. 32")["unverified"] == []
