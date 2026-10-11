"""The follow-up task must answer the question asked and build on what the user has read.

Before: every follow-up carried the full six-heading vulnerability brief contract with no
instruction to use the earlier conversation, so "Is this exploitable?" restarted with
"What is the vulnerability?" and "explain more" had nothing to expand.
"""
from app.services import llm


def test_followup_builds_on_the_earlier_explanation():
    rules = llm._TASK_RULES["security_followup"]
    assert "previousExplanation" in rules
    assert "Never repeat what was already said" in rules
    assert "explain more" in rules


def test_followup_answers_the_question_first_and_only_uses_the_full_brief_on_request():
    rules = llm._TASK_RULES["security_followup"]
    assert "directly, in the first sentence" in rules
    # the heading contract is still available, but only when explicitly asked for
    assert "ONLY when the user explicitly asks for a full brief" in rules
    assert "## What is the vulnerability?" in rules                      # contract still appended


def test_followup_still_forbids_exploit_instructions():
    assert "Do not provide exploit instructions" in llm._TASK_RULES["security_followup"]
