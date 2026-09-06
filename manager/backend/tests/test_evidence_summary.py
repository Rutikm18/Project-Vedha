"""evidence_summary — turn the messy evidence JSONB into a short, plain fact list.

The goal is human-at-a-glance: friendly labels, priority ordering, no raw JSON, no
internal noise. These tests pin that behaviour against the real shapes the engine
emits (top-level service facts + a nested ``enrichment`` block).
"""
from __future__ import annotations

from app.services.evidence_summary import summarize_evidence


def test_none_and_non_dict_inputs_are_empty():
    assert summarize_evidence(None) == []
    assert summarize_evidence("nope") == []
    assert summarize_evidence(123) == []


def test_passthrough_of_already_shaped_list():
    shaped = [{"label": "Port", "value": "443"}]
    assert summarize_evidence(shaped) == shaped


def test_common_keys_get_friendly_labels_in_priority_order():
    facts = summarize_evidence({"version": "1.0", "service": "https", "port": 443})
    labels = [f["label"] for f in facts]
    assert labels.index("Port") < labels.index("Service") < labels.index("Version")


def test_booleans_render_yes_no_with_exposure_labels():
    facts = {f["label"]: f["value"] for f in summarize_evidence(
        {"internet_facing": True, "auth_enforced": False})}
    assert facts["Internet-facing"] == "Yes"
    assert facts["Authentication required"] == "No"


def test_enrichment_kev_and_epss_are_surfaced_simply():
    facts = {f["label"]: f["value"] for f in summarize_evidence(
        {"enrichment": {"kev": True, "epss_percentile": 0.92}})}
    assert "Listed" in facts["CISA KEV"]
    assert "92" in facts["EPSS percentile"]


def test_lists_are_joined_not_json():
    facts = {f["label"]: f["value"] for f in summarize_evidence(
        {"weak_algorithms": ["arcfour", "hmac-md5"]})}
    assert "arcfour" in facts["Weak algorithms"]
    assert "hmac-md5" in facts["Weak algorithms"]
    assert "[" not in facts["Weak algorithms"]  # not JSON


def test_noise_and_internal_keys_are_skipped():
    labels = {f["label"] for f in summarize_evidence(
        {"title": "x", "remediation": "y", "correlation": True, "port": 22})}
    assert "Port" in labels
    assert not any(lbl.lower() in {"title", "remediation", "correlation"} for lbl in labels)


def test_unknown_scalar_keys_fall_back_to_sentence_case():
    facts = {f["label"]: f["value"] for f in summarize_evidence({"cipher_suite": "TLS_RSA_WITH_RC4"})}
    assert facts["Cipher suite"] == "TLS_RSA_WITH_RC4"


def test_output_is_capped_for_readability():
    big = {f"field_{i}": i for i in range(100)}
    assert len(summarize_evidence(big)) <= 24


def test_nested_dicts_do_not_leak_raw_json():
    facts = summarize_evidence({"port": 22, "raw_blob": {"a": {"b": 1}}})
    for f in facts:
        assert "{" not in f["value"]
