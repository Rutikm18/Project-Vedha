"""openai_tools.py — OpenAI tool calling behind the Anthropic SDK's shape.

AgentDecisionEngine keeps its conversation in Anthropic's block format
(``tool_use`` / ``tool_result``) and calls ``client.messages.create(...)``. This
client exposes that same surface over OpenAI chat-completions tool calling,
translating the WHOLE history on every call. So the agent can fail over from
Claude to OpenAI mid-run — even between two tool iterations — without its loop
knowing which provider answered.
"""
from __future__ import annotations

import json
from types import SimpleNamespace
from typing import Any

from app.services.llm_http_client import AsyncLlmHttpClient

_STOP_REASONS = {"tool_calls": "tool_use", "stop": "end_turn", "length": "max_tokens",
                 "content_filter": "refusal"}


def _get(block: Any, name: str, default: Any = None) -> Any:
    return block.get(name, default) if isinstance(block, dict) else getattr(block, name, default)


def _text_of(content: Any) -> str:
    if isinstance(content, str):
        return content
    return "\n".join(str(_get(b, "text", "")) for b in content or [] if _get(b, "type") == "text")


def to_openai_tool(tool: dict) -> dict:
    return {"type": "function", "function": {
        "name": tool["name"],
        "description": tool.get("description", ""),
        "parameters": tool.get("input_schema") or {"type": "object", "properties": {}},
    }}


def to_openai_messages(system: Any, messages: list[dict]) -> list[dict]:
    out: list[dict] = [{"role": "system", "content": _text_of(system)}]
    for message in messages:
        role, content = message["role"], message["content"]
        if isinstance(content, str):
            out.append({"role": role, "content": content})
            continue
        if role == "assistant":
            calls = [{
                "id": _get(block, "id"), "type": "function",
                "function": {"name": _get(block, "name"),
                             "arguments": json.dumps(_get(block, "input") or {})},
            } for block in content if _get(block, "type") == "tool_use"]
            turn: dict = {"role": "assistant", "content": _text_of(content) or None}
            if calls:
                turn["tool_calls"] = calls
            out.append(turn)
            continue
        # A user turn: tool results become `tool` messages (OpenAI requires them
        # directly after the assistant turn that issued the calls), text stays user.
        for block in content:
            if _get(block, "type") == "tool_result":
                out.append({"role": "tool", "tool_call_id": _get(block, "tool_use_id"),
                            "content": _text_of(_get(block, "content", ""))})
        text = _text_of(content)
        if text:
            out.append({"role": "user", "content": text})
    return out


def from_openai_response(data: dict) -> SimpleNamespace:
    choice = data["choices"][0]
    message = choice.get("message") or {}
    blocks: list[SimpleNamespace] = []
    if message.get("content"):
        blocks.append(SimpleNamespace(type="text", text=str(message["content"])))
    for call in message.get("tool_calls") or []:
        function = call.get("function") or {}
        try:
            arguments = json.loads(function.get("arguments") or "{}")
        except ValueError:
            arguments = {}
        blocks.append(SimpleNamespace(type="tool_use", id=call.get("id"), name=function.get("name"),
                                      input=arguments if isinstance(arguments, dict) else {}))
    return SimpleNamespace(content=blocks, stop_details=None,
                           stop_reason=_STOP_REASONS.get(choice.get("finish_reason"), "end_turn"))


class OpenAiToolClient:
    def __init__(self, settings, *, http: AsyncLlmHttpClient | None = None) -> None:
        self._settings = settings
        self._http = http or AsyncLlmHttpClient(timeout_seconds=settings.llm_request_timeout_seconds)
        self.messages = SimpleNamespace(create=self.create)

    async def create(self, *, model: str, max_tokens: int, system: Any, messages: list[dict],
                     tools: list[dict] | None = None, **_anthropic_only: Any) -> SimpleNamespace:
        # **_anthropic_only swallows output_config / cache hints OpenAI has no use for.
        body: dict = {"model": model, "max_tokens": max_tokens,
                      "messages": to_openai_messages(system, messages)}
        if tools:
            body["tools"] = [to_openai_tool(tool) for tool in tools]
        async with self._http.open() as client:
            response = await client.post(
                f"{self._settings.openai_base_url.rstrip('/')}/chat/completions",
                headers={"Authorization": f"Bearer {self._settings.openai_api_key}"},
                json=body,
            )
            response.raise_for_status()
            return from_openai_response(response.json())
