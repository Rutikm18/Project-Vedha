"""Typed, optional LangGraph orchestration for passive verification.

The graph is compiled once at module import and keeps model adapters out of graph
state. Its deterministic node always runs first; a conditional edge invokes the
optional LLM review only for high-value triage. If LangGraph is unavailable (or
the orchestration layer itself fails), the same core seam preserves result parity.
"""
from __future__ import annotations

from typing import Any, Literal, TypedDict

import structlog

from app.detection.verification import (
    VerificationLlm,
    VerificationVerdict,
    compute_verdict,
    needs_llm_review,
    review_verdict,
    verify_finding,
)

logger = structlog.get_logger()

try:
    from langchain_core.runnables import RunnableConfig  # type: ignore
    from langgraph.graph import END, START, StateGraph  # type: ignore

    _HAS_LANGGRAPH = True
except ImportError:  # pragma: no cover - exercised only where langgraph is absent
    RunnableConfig = dict[str, Any]  # type: ignore[misc,assignment]
    StateGraph = None  # type: ignore[assignment]
    START = END = None  # type: ignore[assignment]
    _HAS_LANGGRAPH = False


class VerificationGraphState(TypedDict, total=False):
    """Serializable workflow state; runtime adapters deliberately stay outside it."""

    evidence: dict[str, Any]
    review_requested: bool
    verdict: VerificationVerdict


async def _deterministic_node(
    state: VerificationGraphState,
) -> dict[str, VerificationVerdict]:
    return {"verdict": compute_verdict(state["evidence"])}


def _route_after_deterministic(
    state: VerificationGraphState,
) -> Literal["llm_review", "done"]:
    verdict = state["verdict"]
    if state.get("review_requested") and needs_llm_review(verdict, state["evidence"]):
        return "llm_review"
    return "done"


async def _llm_review_node(
    state: VerificationGraphState,
    config: RunnableConfig,
) -> dict[str, VerificationVerdict]:
    configurable = config.get("configurable", {})
    llm = configurable.get("verification_llm") if isinstance(configurable, dict) else None
    verdict = await review_verdict(state["verdict"], state["evidence"], llm)
    return {"verdict": verdict}


def _compile_graph():
    if not _HAS_LANGGRAPH:
        return None
    graph = StateGraph(VerificationGraphState)
    graph.add_node("deterministic_verdict", _deterministic_node)
    graph.add_node("llm_review", _llm_review_node)
    graph.add_edge(START, "deterministic_verdict")
    graph.add_conditional_edges(
        "deterministic_verdict",
        _route_after_deterministic,
        {"llm_review": "llm_review", "done": END},
    )
    graph.add_edge("llm_review", END)
    return graph.compile()


try:
    _VERIFICATION_GRAPH = _compile_graph()
except Exception as exc:  # pragma: no cover - dependency/version safety net
    logger.warning("verification.graph_compile_failed", error=str(exc))
    _VERIFICATION_GRAPH = None


def graph_available() -> bool:
    return _VERIFICATION_GRAPH is not None


async def run_verification(
    evidence: dict[str, Any],
    llm: VerificationLlm | None = None,
) -> VerificationVerdict:
    """Run deterministic verification and conditionally apply model review."""
    if _VERIFICATION_GRAPH is None:
        return await verify_finding(evidence, llm=llm)

    state: VerificationGraphState = {
        "evidence": evidence,
        "review_requested": llm is not None,
    }
    config: RunnableConfig = {"configurable": {"verification_llm": llm}}
    try:
        result = await _VERIFICATION_GRAPH.ainvoke(state, config=config)
        return result["verdict"]
    except Exception as exc:  # noqa: BLE001 — orchestration must not break ingestion
        logger.warning("verification.graph_failed", error=str(exc))
        return await verify_finding(evidence, llm=llm)
