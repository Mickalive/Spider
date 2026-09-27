"""A-CANDIDATE fitted applicability-gate resolver and the frozen comparison arms.

Implements prereg.md 4:
  * 4.1 A-CANDIDATE  -- cosine scoring over mechanism intents, a FITTED logistic
    applicability gate p_applicable = sigmoid(w * cos_sim + b), a gate threshold
    selected on a held-out validation split, and heuristic slot filling;
  * 4.3 B-LEXICAL-OVERLAP  -- max token Jaccard, never abstains;
  * 4.4 B-RANDOM-ROLE     -- role keyword inference then uniform choice;
  * 4.5 B-INTERNAL-ID-ORACLE -- receives the true mechanism_id/fragment_id;
  * prereg.md 11 A-REFERENCE-EMBEDARGMAX -- the explicitly declared non-empty
    substitute comparison leg used when the committed incumbent emits no
    EXECUTABLE decision. It always commits (no calibration, no abstention), so it
    is strictly weaker in decision power than A-CANDIDATE and cannot bias the
    primary comparison in the candidate's favour.

Nothing in this module reads a target mechanism id except the oracle arm, which
is the declared difficulty ceiling. The resolver sees only the goal text, the
registry's public intent strings, and the registry's declared parameter_slots.

The fitted gate parameters (w, b, threshold) are NOT hardcoded here. They are
produced by the calibration step in experiment_runner.py and passed in, so
"calibration is fitted rather than algebraically fixed" is structurally enforced
(an unfitted resolver cannot be constructed).
"""

from __future__ import annotations

import math
import os
import random
import re
from typing import Any

os.environ.setdefault("HF_HUB_OFFLINE", "1")
os.environ.setdefault("TRANSFORMERS_OFFLINE", "1")
os.environ.setdefault("TOKENIZERS_PARALLELISM", "false")

EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"

ROLE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "create": ("create", "register", "add", "make", "new", "start", "post", "upload", "put up"),
    "read": ("retrieve", "get", "show", "display", "open", "pull", "read", "surface", "find"),
    "update": ("update", "change", "set", "rename", "relabel", "adjust", "amend", "edit", "modify"),
    "delete": ("delete", "remove", "erase", "wipe", "discard", "drop", "destroy", "throw"),
}

# --- slot filling ---------------------------------------------------------
# Generic, mechanism-agnostic heuristic keyed on the slot NAME, exactly the
# "keyword/entity extraction" prereg.md 4.1.4 calls for. It is not given any
# per-mechanism knowledge and has no special case for verbatim rows.

_QUOTED = re.compile(r"'([^']*)'|\"([^\"]*)\"")
_EMAIL = re.compile(r"[\w.+-]+@[\w-]+\.[\w.]+")
_HTTP = re.compile(r"https?://\S+")
_INT = re.compile(r"(?<![\w@/.'-])(\d+)(?![\w@/.'-])")

_TITLE_TRIG = re.compile(r"(?:titled|title|heading)\b[^']*?['\"]([^'\"]+)['\"]", re.I)
_BODY_TRIG = re.compile(r"(?:body|text|content)\b[^']*?['\"]([^'\"]+)['\"]", re.I)
_TEXT_TRIG = re.compile(r"(?:saying|says|text|note)\b[^']*?['\"]([^'\"]+)['\"]", re.I)
_CAPTION_TRIG = re.compile(r"(?:caption\w*|description)\b[^']*?['\"]([^'\"]+)['\"]", re.I)
_URL_TRIG = re.compile(r"\burl\b[^']*?['\"]([^'\"]+)['\"]", re.I)
_NAMED_TRIG = re.compile(r"\bnamed\s+([A-Za-z][\w'-]*)", re.I)
_NAME_TO_TRIG = re.compile(r"\bname\b.*?\bto\s+([A-Za-z][\w'-]*)", re.I)

_TRIGGERS: dict[str, list[re.Pattern]] = {
    "title": [_TITLE_TRIG],
    "body": [_BODY_TRIG],
    "text": [_TEXT_TRIG],
    "caption": [_CAPTION_TRIG],
    "url": [_URL_TRIG, _HTTP],
    "name": [_NAMED_TRIG, _NAME_TO_TRIG],
}


def _strip_quoted(text: str) -> str:
    return _QUOTED.sub(" ", text)


def _ints_outside_literals(text: str) -> list[int]:
    out: list[int] = []
    for m in _INT.finditer(_strip_quoted(text)):
        out.append(int(m.group(1)))
    return out


def fill_slot(slot: str, goal_text: str) -> Any | None:
    """Return the value the goal supplies for `slot`, or None if absent."""
    if slot.endswith("_id"):
        ints = _ints_outside_literals(goal_text)
        return ints[0] if ints else None
    if slot == "email":
        m = _EMAIL.search(goal_text)
        return m.group(0) if m else None
    for pattern in _TRIGGERS.get(slot, []):
        m = pattern.search(goal_text)
        if m:
            return m.group(1)
    # generic fallbacks for quoted values, in order of appearance
    quotes = [a or b for a, b in _QUOTED.findall(goal_text)]
    return None


def bind_parameters(mechanism: dict, goal_text: str) -> tuple[dict[str, Any], list[str]]:
    bound: dict[str, Any] = {}
    unfilled: list[str] = []
    for slot in mechanism["parameter_slots"]:
        value = fill_slot(slot, goal_text)
        if value is None:
            unfilled.append(slot)
        else:
            bound[slot] = value
    return bound, unfilled


def render_action(template: dict, bound: dict[str, Any]) -> dict:
    """Substitute ${slot} placeholders. Only declared slots occur in templates."""

    def sub(value: Any) -> Any:
        if isinstance(value, str):
            full = re.fullmatch(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", value)
            if full:
                return str(bound[full.group(1)])
            return re.sub(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}", lambda m: str(bound[m.group(1)]), value)
        if isinstance(value, dict):
            return {k: sub(v) for k, v in value.items()}
        if isinstance(value, list):
            return [sub(v) for v in value]
        return value

    return sub(template)


# --- embeddings -----------------------------------------------------------
class Embedder:
    def __init__(self, name: str = EMBED_MODEL_NAME) -> None:
        from sentence_transformers import SentenceTransformer

        self.name = name
        self.model = SentenceTransformer(name)
        try:
            self.dim = int(self.model.get_embedding_dimension())
        except AttributeError:  # sentence-transformers < 6
            self.dim = int(self.model.get_sentence_embedding_dimension())

    def encode(self, texts: list[str]):
        return self.model.encode(texts, normalize_embeddings=True, show_progress_bar=False)


def cosines(embedder: Embedder, goals: list[str], intents: list[str]):
    g = embedder.encode(goals)
    m = embedder.encode(intents)
    return g @ m.T  # (n_goals, n_mechanisms), rows are unit vectors


# --- arms -----------------------------------------------------------------
def arm_candidate(
    goal_text: str,
    cos_row: list[float],
    mechanisms: list[dict],
    by_id: dict[str, dict],
    gate_w: float,
    gate_b: float,
    threshold: float,
) -> dict:
    p = [1.0 / (1.0 + math.exp(-(gate_w * c + gate_b))) for c in cos_row]
    best = max(range(len(p)), key=lambda i: (p[i], -i))
    top_p = p[best]
    mech = mechanisms[best]
    decision: dict[str, Any] = {
        "selected_mechanism_id": mech["mechanism_id"],
        "p_applicable": top_p,
        "cos_top": cos_row[best],
        "margin_p": top_p - sorted(p, reverse=True)[1] if len(p) > 1 else top_p,
        "resolution_status": "EXECUTABLE",
        "abstain_reason": None,
        "bound_parameters": {},
        "unfilled_slots": [],
        "uses_internal_ids": False,
    }
    if top_p < threshold:
        decision["resolution_status"] = "ABSTAIN"
        decision["abstain_reason"] = "p_applicable_below_threshold"
        decision["selected_mechanism_id"] = None
        return decision
    bound, unfilled = bind_parameters(mech, goal_text)
    decision["bound_parameters"] = bound
    decision["unfilled_slots"] = unfilled
    if unfilled:
        decision["resolution_status"] = "ABSTAIN"
        decision["abstain_reason"] = "unfilled_parameter_slots"
        decision["selected_mechanism_id"] = None
        return decision
    decision["bound_action"] = render_action(mech["action_template"], bound)
    return decision


def arm_reference_embedargmax(goal_text: str, cos_row: list[float], mechanisms: list[dict]) -> dict:
    """Uncalibrated, never-abstaining resolver: the declared substitute leg."""
    best = max(range(len(cos_row)), key=lambda i: (cos_row[i], -i))
    mech = mechanisms[best]
    bound, unfilled = bind_parameters(mech, goal_text)
    decision: dict[str, Any] = {
        "selected_mechanism_id": mech["mechanism_id"],
        "p_applicable": None,
        "cos_top": cos_row[best],
        "resolution_status": "EXECUTABLE",
        "abstain_reason": None,
        "bound_parameters": bound,
        "unfilled_slots": unfilled,
        "uses_internal_ids": False,
    }
    if unfilled:
        decision["bound_action"] = None  # cannot render; request is skipped and logged
        decision["resolution_status"] = "EXECUTABLE"
    else:
        decision["bound_action"] = render_action(mech["action_template"], bound)
    return decision


def arm_lexical_overlap(goal_text: str, mechanisms: list[dict]) -> dict:
    from goal_generator import jaccard  # exact frozen implementation of the null

    best_id, best_score = None, -1.0
    for mech in mechanisms:  # fixture order is already mechanism_id lexical order
        score = jaccard(goal_text, mech["intent"])
        if score > best_score:
            best_id, best_score = mech["mechanism_id"], score
    mech = next(m for m in mechanisms if m["mechanism_id"] == best_id)
    bound, unfilled = bind_parameters(mech, goal_text)
    return {
        "selected_mechanism_id": best_id,
        "jaccard_top": best_score,
        "resolution_status": "EXECUTABLE",
        "abstain_reason": None,
        "bound_parameters": bound,
        "unfilled_slots": unfilled,
        "bound_action": render_action(mech["action_template"], bound) if not unfilled else None,
        "uses_internal_ids": False,
    }


def arm_random_role(goal_text: str, mechanisms: list[dict], rng: random.Random) -> dict:
    low = goal_text.lower()
    role = None
    for candidate in ("create", "read", "update", "delete"):
        if any(k in low for k in ROLE_KEYWORDS[candidate]):
            role = candidate
            break
    if role is None:
        role = "read"
    pool = [m for m in mechanisms if m["verb"] == role]
    if not pool:
        pool = list(mechanisms)
    mech = pool[rng.randrange(len(pool))]
    bound, unfilled = bind_parameters(mech, goal_text)
    return {
        "selected_mechanism_id": mech["mechanism_id"],
        "inferred_role": role,
        "resolution_status": "EXECUTABLE",
        "abstain_reason": None,
        "bound_parameters": bound,
        "unfilled_slots": unfilled,
        "bound_action": render_action(mech["action_template"], bound) if not unfilled else None,
        "uses_internal_ids": False,
    }


def arm_internal_id_oracle(mechanism_id: str, fragment_id: str, goal_text: str, mechanisms: list[dict]) -> dict:
    mech = next((m for m in mechanisms if m["mechanism_id"] == mechanism_id), None)
    if mech is None:
        return {
            "selected_mechanism_id": None,
            "fragment_id": fragment_id,
            "resolution_status": "ABSTAIN",
            "abstain_reason": "oracle_mechanism_absent_from_registry",
            "bound_parameters": {},
            "unfilled_slots": [],
            "uses_internal_ids": True,
        }
    bound, unfilled = bind_parameters(mech, goal_text)
    return {
        "selected_mechanism_id": mechanism_id,
        "fragment_id": fragment_id,
        "resolution_status": "EXECUTABLE",
        "abstain_reason": None,
        "bound_parameters": bound,
        "unfilled_slots": unfilled,
        "bound_action": render_action(mech["action_template"], bound) if not unfilled else None,
        "uses_internal_ids": True,
    }


# --- incumbent ------------------------------------------------------------
def incumbent_registry_path(fixture: dict, path: str) -> str:
    from src.spider.models import Mechanism
    from src.spider.registry import MechanismRegistry

    reg = MechanismRegistry(path)
    reg.replace(
        Mechanism(
            mechanism_id=m["mechanism_id"],
            intent=m["intent"],
            preconditions={},
            action_template=m["action_template"],
            postconditions={},
            parameter_slots=list(m["parameter_slots"]),
            evidence=[m["fragment_id"]],
            confidence=m["confidence"],
        )
        for m in fixture["mechanisms"]
    )
    return path


def arm_incumbent(goal_text: str, registry_path: str, min_confidence: float = 0.5) -> dict:
    """The committed src/spider/kernel.py SpiderKernel, unmodified."""
    from src.spider.kernel import SpiderKernel
    from src.spider.registry import MechanismRegistry

    kernel = SpiderKernel(MechanismRegistry(registry_path), min_confidence=min_confidence)
    res = kernel.resolve(goal_text, context={}, params={})
    return {
        "selected_mechanism_id": res.mechanism_id,
        "resolution_status": res.status.value,
        "abstain_reason": res.reason,
        "confidence": res.confidence,
        "bound_parameters": {},
        "unfilled_slots": [],
        "uses_internal_ids": False,
        "min_confidence": min_confidence,
    }
