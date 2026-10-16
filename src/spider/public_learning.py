"""Very narrow public-page learning gate for two allowlisted read-only tasks.

Two verified agent-visited web pages of separate identifiers are needed before
a reusable relative pattern exists. Canonical route template is only admitted
for a known site family; never invent an arbitrary endpoint. Scope is explicit.
"""
from __future__ import annotations

import hashlib
import json
from urllib.parse import urlsplit

from .models import Mechanism
from .public_tasks import TRAIN, PublicTask, VERS


def learn_public_route(family: str, examples: list[dict]) -> Mechanism:
    if family not in TRAIN or len(examples) != 2:
        raise ValueError("two allowlisted independent training examples required")
    seen = []
    refs = []
    for ex in examples:
        task = PublicTask(family, ex["identifier"])
        if task.identifier not in TRAIN[family] or task.identifier in seen:
            raise ValueError("duplicate or out-of-training identifier")
        if ex.get("verified_against_independent_oracle") is not True:
            raise ValueError("independent oracle success is mandatory")
        visited = ex.get("visited_urls") or []
        if not isinstance(visited, list) or not visited:
            raise ValueError("missing agent-observed web history")
        valid_urls = {u for u in visited if isinstance(u, str)}
        if family == "pypi":
            witnessed = task.target_url in valid_urls
        else:
            expected = task.target_url
            prefix = f"https://github.com/{task.identifier}/releases/tag/"
            witnessed = any(
                u == expected or (u.startswith(prefix) and
                 urlsplit(u).scheme == "https" and urlsplit(u).hostname == "github.com"
                 and not urlsplit(u).query and not urlsplit(u).fragment
                 and VERS.fullmatch(u[len(prefix):]) is not None)
                for u in valid_urls
            )
        if not witnessed:
            raise ValueError("no observed exact task page or latest-release tag")
        if not isinstance(ex.get("answer"), str) or not VERS.fullmatch(ex["answer"]):
            raise ValueError("invalid claimed answer")
        seen.append(task.identifier)
        refs.append(hashlib.sha256(json.dumps(
            {"id": task.identifier, "answer": ex["answer"], "task_url": task.target_url},
            sort_keys=True,
        ).encode()).hexdigest())
    template = (
        "https://pypi.org/project/${id}/" if family == "pypi"
        else "https://github.com/${id}/releases/latest"
    )
    return Mechanism(
        mechanism_id=f"PUBLIC-LEARNED-{family}-TWO-SAMPLES",
        intent=f"latest-{family}",
        preconditions={"family": family, "surface": "allowlisted-public-v1"},
        applicability_guards={"read_only": True},
        action_template={"method": "GET", "url": template},
        postconditions={"verified": True},
        parameter_slots=["id"],
        verification_rule={"replay_safe": True, "requires_fresh_oracle": True},
        evidence=refs,
        confidence=0.85,
    )
