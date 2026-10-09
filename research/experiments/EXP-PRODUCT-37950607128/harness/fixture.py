"""SYNTH-INDUCTION-BANK-v1 and its deterministic, credential-free executor.

This module is the executable reconstruction of the fixture bank frozen in
``prereg.md`` section 5 of EXP-PRODUCT-37950607128. It is standard-library only,
deterministic and offline. The certificate harness records the sha256 of the
serialized bank so AUDIT can rebuild it independently.

Interpretation notes (recorded so the reconstruction is unambiguous):

* The prereg denotes induction ranges compactly (e.g. ``itm-0001..itm-0004``).
  EXECUTE expands each range to four concrete, distinct values; the expansion
  is recorded verbatim in the serialized bank.
* ``F5-TWO-SLOT`` induction values are the four distinct in-grammar pairs
  ``(t1,i1) .. (t4,i4)``; the held-out pair is ``(t9,i9)``.
* The prereg names three noise fields (``trace_id``, ``seq``, ``ts``) and then
  refers to "all four noise fields" for ``F6-NOISE-STRESS``. EXECUTE therefore
  carries four noise fields (``trace_id``, ``seq``, ``ts``, ``nonce``) in every
  family's state and next_state, all varying, all absent from the action
  template. They must never become parameter slots.
"""

from __future__ import annotations

import re
from typing import Any, Callable

from spider.models import Observation

SEED = 37950607128

NOISE_FIELDS = ("trace_id", "seq", "ts", "nonce")

INDUCTION_COUNT = 4


def _noise(index: int) -> dict[str, Any]:
    return {
        "trace_id": f"tr-{SEED % 100000}-{index}",
        "seq": index,
        "ts": 1700000000 + 7 * index,
        "nonce": (SEED + 131 * index) % 9973,
    }


# --------------------------------------------------------------------------
# Family builders
# --------------------------------------------------------------------------


def _f1_action(p: dict[str, Any]) -> dict[str, Any]:
    return {"method": "GET", "url": f"https://fixture.invalid/v1/items/{p['item']}"}


def _f2_action(p: dict[str, Any]) -> dict[str, Any]:
    return {
        "method": "GET",
        "url": "https://fixture.invalid/v1/search",
        "params": {"q": p["query"]},
    }


def _f3_action(p: dict[str, Any]) -> dict[str, Any]:
    return {
        "method": "POST",
        "url": "https://fixture.invalid/v1/echo",
        "json": {"token": p["token"]},
    }


def _f4_action(p: dict[str, Any]) -> dict[str, Any]:
    return {
        "method": "POST",
        "url": "https://fixture.invalid/v1/verify",
        "headers": {"X-Resource": p["resource"]},
    }


def _f5_action(p: dict[str, Any]) -> dict[str, Any]:
    return {
        "method": "POST",
        "url": f"https://fixture.invalid/v1/tenants/{p['tenant']}/items",
        "json": {"item_id": p["item_id"]},
    }


def _f6_action(p: dict[str, Any]) -> dict[str, Any]:
    return {"method": "GET", "url": f"https://fixture.invalid/v1/nodes/{p['node']}"}


def _simple_next(value: Any) -> Callable[[dict[str, Any], int], dict[str, Any]]:
    def build(_p: dict[str, Any], index: int) -> dict[str, Any]:
        return {"status": 200, "resource_echo": value(_p), **_noise(index)}

    return build


def _f1_next(p: dict[str, Any], index: int) -> dict[str, Any]:
    return {"status": 200, "resource_echo": p["item"], **_noise(index)}


def _f2_next(p: dict[str, Any], index: int) -> dict[str, Any]:
    return {"status": 200, "resource_echo": p["query"], **_noise(index)}


def _f3_next(p: dict[str, Any], index: int) -> dict[str, Any]:
    return {"status": 200, "resource_echo": p["token"], **_noise(index)}


def _f4_next(p: dict[str, Any], index: int) -> dict[str, Any]:
    return {"status": 200, "resource_echo": p["resource"], **_noise(index)}


def _f5_next(p: dict[str, Any], index: int) -> dict[str, Any]:
    return {
        "status": 200,
        "resource_echo": {"tenant": p["tenant"], "item_id": p["item_id"]},
        **_noise(index),
    }


def _f6_next(p: dict[str, Any], index: int) -> dict[str, Any]:
    return {"status": 200, "resource_echo": p["node"], **_noise(index)}


FAMILIES: list[dict[str, Any]] = [
    {
        "family": "F1-PATH-ID",
        "intent": "fetch_item",
        "route": "items",
        "expected_slot_count": 1,
        "slot_keys": ["item"],
        "grammar": {"item": r"^[a-z]+-[0-9]{4}$"},
        "induction": [{"item": f"itm-000{k}"} for k in (1, 2, 3, 4)],
        "held_out": {"item": "itm-0009"},
        "build_action": _f1_action,
        "build_next": _f1_next,
        "bound_identifier": lambda a: a["url"].rsplit("/", 1)[-1],
    },
    {
        "family": "F2-QUERY-ID",
        "intent": "search",
        "route": "search",
        "expected_slot_count": 1,
        "slot_keys": ["query"],
        "grammar": {"query": r"^[a-z]{4,8}$"},
        "induction": [{"query": v} for v in ("alpha", "beta", "gamma", "delta")],
        "held_out": {"query": "epsilon"},
        "build_action": _f2_action,
        "build_next": _f2_next,
        "bound_identifier": lambda a: a["params"]["q"],
    },
    {
        "family": "F3-BODY-FIELD",
        "intent": "echo",
        "route": "echo",
        "expected_slot_count": 1,
        "slot_keys": ["token"],
        "grammar": {"token": r"^tok-[0-9]{2}$"},
        "induction": [{"token": f"tok-{k}{k}"} for k in (1, 2, 3, 4)],
        "held_out": {"token": "tok-99"},
        "build_action": _f3_action,
        "build_next": _f3_next,
        "bound_identifier": lambda a: a["json"]["token"],
    },
    {
        "family": "F4-HEADER-FIELD",
        "intent": "verify_header",
        "route": "verify",
        "expected_slot_count": 1,
        "slot_keys": ["resource"],
        "grammar": {"resource": r"^res-[a-z]$"},
        "induction": [{"resource": f"res-{c}"} for c in ("a", "b", "c", "d")],
        "held_out": {"resource": "res-z"},
        "build_action": _f4_action,
        "build_next": _f4_next,
        "bound_identifier": lambda a: a["headers"]["X-Resource"],
    },
    {
        "family": "F5-TWO-SLOT",
        "intent": "write_item",
        "route": "tenants",
        "expected_slot_count": 2,
        "slot_keys": ["tenant", "item_id"],
        "grammar": {"tenant": r"^t[0-9]$", "item_id": r"^i[0-9]$"},
        "induction": [
            {"tenant": f"t{k}", "item_id": f"i{k}"} for k in (1, 2, 3, 4)
        ],
        "held_out": {"tenant": "t9", "item_id": "i9"},
        "build_action": _f5_action,
        "build_next": _f5_next,
        "bound_identifier": lambda a: (a["url"].split("/tenants/", 1)[1].split("/", 1)[0], a["json"]["item_id"]),
    },
    {
        "family": "F6-NOISE-STRESS",
        "intent": "ping",
        "route": "nodes",
        "expected_slot_count": 1,
        "slot_keys": ["node"],
        "grammar": {"node": r"^n-[0-9]{2}$"},
        "induction": [{"node": f"n-0{k}"} for k in (1, 2, 3, 4)],
        "held_out": {"node": "n-09"},
        "build_action": _f6_action,
        "build_next": _f6_next,
        "bound_identifier": lambda a: a["url"].rsplit("/", 1)[-1],
    },
]


# --------------------------------------------------------------------------
# Deterministic fixture executor
# --------------------------------------------------------------------------

_PATH_PATTERNS: list[tuple[str, str, re.Pattern[str]]] = [
    ("F1-PATH-ID", "GET", re.compile(r"^/v1/items/(?P<item>[^/]+)$")),
    ("F2-QUERY-ID", "GET", re.compile(r"^/v1/search$")),
    ("F3-BODY-FIELD", "POST", re.compile(r"^/v1/echo$")),
    ("F4-HEADER-FIELD", "POST", re.compile(r"^/v1/verify$")),
    ("F5-TWO-SLOT", "POST", re.compile(r"^/v1/tenants/(?P<tenant>[^/]+)/items$")),
    ("F6-NOISE-STRESS", "GET", re.compile(r"^/v1/nodes/(?P<node>[^/]+)$")),
]

_GRAMMAR_BY_FAMILY = {f["family"]: f["grammar"] for f in FAMILIES}


def fixture_execute(bound_action: dict[str, Any]) -> dict[str, Any]:
    """Execute a bound action against the deterministic synthetic fixture.

    Returns 412 on host/method/path-schema mismatch and 422 when a bound
    identifier fails its family grammar (including empty, whitespace or ``/``);
    otherwise returns a 200 state echoing the bound identifier(s).
    """
    url = bound_action.get("url", "")
    method = bound_action.get("method")
    if not isinstance(url, str) or not url.startswith("https://fixture.invalid"):
        return {"status": 412, "error": "bad_request"}
    path = url[len("https://fixture.invalid"):]
    path = path.split("?", 1)[0]

    for family, expected_method, pattern in _PATH_PATTERNS:
        match = pattern.match(path)
        if not match:
            continue
        if method != expected_method:
            return {"status": 412, "error": "bad_request"}
        grammar = _GRAMMAR_BY_FAMILY[family]
        captured = match.groupdict()

        if family == "F2-QUERY-ID":
            value = bound_action.get("params", {}).get("q")
            if not isinstance(value, str) or re.fullmatch(grammar["query"], value) is None:
                return {"status": 422, "error": "unsupported_identifier"}
            return {"status": 200, "resource_echo": value}

        if family == "F3-BODY-FIELD":
            value = bound_action.get("json", {}).get("token")
            if not isinstance(value, str) or re.fullmatch(grammar["token"], value) is None:
                return {"status": 422, "error": "unsupported_identifier"}
            return {"status": 200, "resource_echo": value}

        if family == "F4-HEADER-FIELD":
            value = bound_action.get("headers", {}).get("X-Resource")
            if not isinstance(value, str) or re.fullmatch(grammar["resource"], value) is None:
                return {"status": 422, "error": "unsupported_identifier"}
            return {"status": 200, "resource_echo": value}

        if family == "F5-TWO-SLOT":
            tenant = captured.get("tenant")
            item_id = bound_action.get("json", {}).get("item_id")
            if (
                not isinstance(tenant, str)
                or not isinstance(item_id, str)
                or re.fullmatch(grammar["tenant"], tenant) is None
                or re.fullmatch(grammar["item_id"], item_id) is None
            ):
                return {"status": 422, "error": "unsupported_identifier"}
            return {"status": 200, "resource_echo": {"tenant": tenant, "item_id": item_id}}

        key = {"F1-PATH-ID": "item", "F6-NOISE-STRESS": "node"}[family]
        value = captured.get(key)
        if not isinstance(value, str) or re.fullmatch(grammar[key], value) is None:
            return {"status": 422, "error": "unsupported_identifier"}
        return {"status": 200, "resource_echo": value}

    return {"status": 412, "error": "bad_request"}


# --------------------------------------------------------------------------
# Retrieval-shaped comparator (B-RETRIEVAL-SHAPED)
# --------------------------------------------------------------------------


def _flat_keys(obj: Any, prefix: tuple[str, ...] = ()) -> set[tuple[str, ...]]:
    keys: set[tuple[str, ...]] = set()
    if isinstance(obj, dict):
        for key, value in obj.items():
            keys |= _flat_keys(value, prefix + (str(key),))
    elif isinstance(obj, (list, tuple)):
        for index, value in enumerate(obj):
            keys |= _flat_keys(value, prefix + (str(index),))
    else:
        if prefix:
            keys.add(prefix)
    return keys


def _target_features(intent: str, context: dict[str, Any]) -> set[tuple[str, ...]]:
    return {("intent", intent)} | {("state",) + path for path in _flat_keys(context)}


def _observation_features(observation: Observation) -> set[tuple[str, ...]]:
    return (
        {("intent", observation.intent)}
        | {("state",) + path for path in _flat_keys(observation.state)}
        | {("action",) + path for path in _flat_keys(observation.action)}
    )


def _jaccard(a: set[Any], b: set[Any]) -> float:
    if not a and not b:
        return 1.0
    union = a | b
    if not union:
        return 1.0
    return len(a & b) / len(union)


def retrieval_comparator_action(
    intent: str,
    context: dict[str, Any],
    observations: list[Observation],
    k: int = 5,
) -> dict[str, Any]:
    """Return the literal action of the K=5 nearest induction observation.

    Similarity is structural field-overlap (Jaccard over flattened key paths of
    intent+state+action). No model and no network are used.
    """
    target = _target_features(intent, context)
    ranked = sorted(
        (
            (-_jaccard(target, _observation_features(obs)), index, obs)
            for index, obs in enumerate(observations)
        ),
        key=lambda item: (item[0], item[1]),
    )
    nearest = ranked[:k][0][2]
    return nearest.action


# --------------------------------------------------------------------------
# Bank construction and serialization
# --------------------------------------------------------------------------


def build_observations() -> list[Observation]:
    observations: list[Observation] = []
    for family in FAMILIES:
        for index in range(INDUCTION_COUNT):
            params = family["induction"][index]
            state = {
                "site": "fixture.invalid",
                "route": family["route"],
                "auth": "public",
                **_noise(index),
            }
            observations.append(
                Observation(
                    intent=family["intent"],
                    state=state,
                    action=family["build_action"](params),
                    next_state=family["build_next"](params, index),
                    success=True,
                )
            )
    return observations


def observations_by_family() -> dict[str, list[Observation]]:
    out: dict[str, list[Observation]] = {family["family"]: [] for family in FAMILIES}
    all_obs = build_observations()
    index = 0
    for family in FAMILIES:
        out[family["family"]] = all_obs[index:index + INDUCTION_COUNT]
        index += INDUCTION_COUNT
    return out


def negative_cases() -> list[dict[str, Any]]:
    """Return the declared negative cases (must all be refused)."""
    cases: list[dict[str, Any]] = []
    for family in FAMILIES:
        intent = family["intent"]
        stable_state = {
            "site": "fixture.invalid",
            "route": family["route"],
            "auth": "public",
        }
        held = family["held_out"]

        if family["family"] == "F5-TWO-SLOT":
            cases.append({
                "family": family["family"], "kind": "missing_param", "slot": "tenant",
                "intent": intent, "context": stable_state,
                "params": {"item_id": held["item_id"]},
            })
            cases.append({
                "family": family["family"], "kind": "missing_param", "slot": "item_id",
                "intent": intent, "context": stable_state,
                "params": {"tenant": held["tenant"]},
            })
            cases.append({
                "family": family["family"], "kind": "out_of_support_pair",
                "intent": intent, "context": stable_state,
                "params": {"tenant": "t99", "item_id": "i99"},
            })
        else:
            key = family["slot_keys"][0]
            for label, value in (("empty", ""), ("space", "in valid"), ("slash", "in/valid")):
                cases.append({
                    "family": family["family"], "kind": f"out_of_support_{label}",
                    "intent": intent, "context": stable_state, "params": {key: value},
                })

        cases.append({
            "family": family["family"], "kind": "wrong_intent",
            "intent": f"wrong_intent__{intent}", "context": stable_state,
            "params": dict(held),
        })
    return cases


def build_bank(observations: list[Observation]) -> dict[str, Any]:
    families: list[dict[str, Any]] = []
    offset = 0
    for family in FAMILIES:
        family_obs = observations[offset:offset + INDUCTION_COUNT]
        offset += INDUCTION_COUNT
        families.append({
            "family": family["family"],
            "intent": family["intent"],
            "route": family["route"],
            "expected_slot_count": family["expected_slot_count"],
            "slot_keys": list(family["slot_keys"]),
            "grammar": dict(family["grammar"]),
            "induction_params": family["induction"],
            "held_out_params": family["held_out"],
            "induction_observations": [
                {
                    "intent": o.intent,
                    "state": o.state,
                    "action": o.action,
                    "next_state": o.next_state,
                    "success": o.success,
                }
                for o in family_obs
            ],
        })
    return {
        "bank_id": "SYNTH-INDUCTION-BANK-v1",
        "seed": SEED,
        "noise_fields": list(NOISE_FIELDS),
        "induction_count_per_family": INDUCTION_COUNT,
        "families": families,
        "negative_cases": negative_cases(),
    }
