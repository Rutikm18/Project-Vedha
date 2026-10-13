"""Small independently expressed finite oracle, not human-reviewed ground truth."""

import itertools
import json
from pathlib import Path

from app.graph.local_rule import (
    LocalRuleInput,
    RuleBindingError,
    evaluate_local_data_read,
)


def test_finite_binding_worlds_against_requirement_oracle():
    p = (
        Path(__file__).resolve().parents[3]
        / "docs/planning/2026-10-13-attack-path-local-rule.example.json"
    )
    base = json.loads(p.read_text())
    truths = ["supported_true", "supported_false", "unknown", "conflicted"]
    checked = 0
    for (
        reachable,
        readable,
        same_service,
        same_context,
        same_instance,
        accepted,
    ) in itertools.product(
        truths, truths, [False, True], [False, True], [False, True], [False, True]
    ):
        data = json.loads(json.dumps(base))
        data["assertions"][0]["truth"] = reachable
        data["assertions"][1]["truth"] = readable
        if not same_service:
            data["assertions"][1]["target_id"] = data["asset"]["id"]
        if not same_context:
            data["assertions"][1]["context_ref"] = "other-scenario"
        if not same_instance:
            data["assertions"][1]["service_instance_ref"] = "replaced-listener"
        data["finding"]["lifecycle"] = "accepted" if accepted else "open"
        expected = (
            reachable == readable == "supported_true"
            and same_service
            and same_context
            and same_instance
        )
        try:
            evaluate_local_data_read(LocalRuleInput.model_validate(data))
            actual = True
        except RuleBindingError:
            actual = False
        assert actual == expected, (
            reachable,
            readable,
            same_service,
            same_context,
            same_instance,
            accepted,
        )
        checked += 1
    assert checked == 256
