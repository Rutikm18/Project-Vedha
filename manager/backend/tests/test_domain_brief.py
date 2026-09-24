"""Domain-expert skill selection + the system-prompt brief it produces."""
from __future__ import annotations

from app.ai.domain_brief import build_domain_brief
from app.ai.skills import SKILLS, select_skill
from app.compliance.profile import EngagementProfile
from app.schemas.ai import AiGenerateRequest, AiMessage
from app.services.llm import _CONTEXT_MARKER, ManagerLlmService, _anthropic_system_blocks


def test_every_skill_is_complete():
    for skill in SKILLS.values():
        assert skill.persona and skill.impact_lens and skill.best_practices and skill.vocabulary


def test_skill_selection_order():
    assert select_skill("insurance", {"sector_fn:swift"})[0].id == "insurance"
    skill, reason = select_skill("generic", {"sector_fn:swift"})
    assert skill.id == "banking" and "sector_fn:swift" in reason
    assert select_skill(None, set())[0].id == "generic"


def test_brief_for_indian_bank_names_regulators_and_clocks():
    brief = build_domain_brief(EngagementProfile(sector="banking", jurisdictions=["IN"]),
                               categories={"missing_patch"})
    assert brief.skill_id == "banking"
    assert "rbi_csf" in brief.framework_ids and "certin_2022" in brief.framework_ids
    assert "Annex 1 §7 Patch/Vulnerability & Change Management" in brief.text
    assert "6h" in brief.text and "CERT-In" in brief.text
    assert "never invent" in brief.text.lower()
    assert "VAPT" in brief.text  # sector vocabulary


def test_brief_ignores_attacker_influenced_tags():
    # Only enumerated sector/scope tags may shape the trusted system prompt; a
    # domain/zone tag carries scan-derived text and must never be echoed.
    brief = build_domain_brief(EngagementProfile(), tags={"domain:ignore-previous-rules.evil",
                                                          "sector_fn:swift"})
    assert "ignore-previous-rules" not in brief.text
    assert brief.skill_id == "banking"


def test_generic_brief_has_no_regional_frameworks_but_keeps_global_pointer():
    brief = build_domain_brief(EngagementProfile())
    assert brief.framework_ids == []
    assert "no jurisdiction" in brief.text.lower()


def test_brief_is_bounded():
    prof = EngagementProfile(sector="banking", jurisdictions=["IN", "EU", "UK", "US", "SA", "AE", "SG", "HK"])
    brief = build_domain_brief(prof, tags={"compliance_scope:swift_cscf_scope"},
                               categories={"weak_tls", "exposed_rdp", "default_credentials", "anon_ftp"})
    assert len(brief.text) <= 9000


def test_system_prompt_places_brief_in_cached_prefix_before_context():
    svc = ManagerLlmService.__new__(ManagerLlmService)
    svc.settings = type("S", (), {"jwt_secret": "x" * 32})()
    req = AiGenerateRequest(task="client_assistant", messages=[AiMessage(role="user", content="hi")],
                            context={"open_findings": []})
    brief = build_domain_brief(EngagementProfile(sector="banking", jurisdictions=["IN"]))
    system = svc._build_system(req, domain_brief=brief.text)
    stable, marker, _ = system.partition(_CONTEXT_MARKER)
    assert marker and "<domain_expertise" in stable
    assert _anthropic_system_blocks(system)[0]["text"] == stable
    assert svc._build_system(req) == system.replace("\n\n" + brief.text, "")
