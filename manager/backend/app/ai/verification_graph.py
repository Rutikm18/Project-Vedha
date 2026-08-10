"""
verification_graph.py — optional LangGraph orchestration for passive verification.

The substance lives in app/detection/verification.py (pure core + optional LLM
rationale). This module wraps it in a LangGraph StateGraph so the SAME wiring
carries forward to P3, where active validation adds a checkpointed, human-in-the-
loop node. LangGraph is an OPTIONAL dependency: if it's not installed,
run_verification() calls the core directly and results are identical.
"""
from __future__ import annotations

from app.detection.verification import VerificationVerdict, verify_finding

try:
    from langgraph.graph import END, START, StateGraph  # type: ignore

    _HAS_LANGGRAPH = True
except ImportError:  # pragma: no cover - exercised only where langgraph is absent
    StateGraph = None  # type: ignore
    START = END = None  # type: ignore
    _HAS_LANGGRAPH = False


def graph_available() -> bool:
    return _HAS_LANGGRAPH


async def run_verification(evidence: dict, llm=None) -> VerificationVerdict:
    """Run passive verification. Uses the LangGraph StateGraph when available;
    otherwise the deterministic/LLM core directly (identical result)."""
    if not _HAS_LANGGRAPH:
        return await verify_finding(evidence, llm=llm)

    async def _corroborate(state: dict) -> dict:
        verdict = await verify_finding(state["evidence"], llm=state.get("llm"))
        return {"verdict": verdict}

    graph = StateGraph(dict)
    graph.add_node("corroborate", _corroborate)
    graph.add_edge(START, "corroborate")
    graph.add_edge("corroborate", END)
    compiled = graph.compile()
    result = await compiled.ainvoke({"evidence": evidence, "llm": llm})
    return result["verdict"]
