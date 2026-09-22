from __future__ import annotations

import hashlib
import json
import math
import re
from typing import Any

from .models import Mechanism, Observation, Resolution, ResolutionStatus
from .registry import MechanismRegistry


_PARAMETER = re.compile(r"\$\{([A-Za-z_][A-Za-z0-9_]*)\}")

# Reconstruction adapter constants (port of Frontier RECONSTRUCTION-RULE,
# reference harness sha256 4db542a727d35b5fee7c36cb842e6abff61ba6c51f5a1fa7f1c67a884d24da6f,
# audit PASS on EXP-FRONTIER-35766532429).
ALLOWED_STATE_KEYS = {
    "url", "method", "url_path", "url_query", "url_segments",
    "headers_observed", "body_observed",
    "ax_tree_snapshot", "ax_nodes_count", "viewport_observed",
}
_STANDARD_HEADERS = {
    "host", "user-agent", "accept", "accept-encoding", "accept-language",
    "connection", "content-length", "content-type", "referer", "origin", "cache-control",
}


def _matches(required: dict[str, Any], actual: dict[str, Any]) -> bool:
    return all(actual.get(k) == v for k, v in required.items())


def _template_slots(value: Any) -> set[str]:
    if isinstance(value, str):
        return set(_PARAMETER.findall(value))
    if isinstance(value, dict):
        out: set[str] = set()
        for item in value.values():
            out.update(_template_slots(item))
        return out
    if isinstance(value, list):
        out: set[str] = set()
        for item in value:
            out.update(_template_slots(item))
        return out
    return set()


def _bind(value: Any, params: dict[str, Any]) -> Any:
    if isinstance(value, str):
        full = _PARAMETER.fullmatch(value)
        if full:
            return params[full.group(1)]

        def replace(match: re.Match[str]) -> str:
            return str(params[match.group(1)])

        return _PARAMETER.sub(replace, value)
    if isinstance(value, dict):
        return {k: _bind(v, params) for k, v in value.items()}
    if isinstance(value, list):
        return [_bind(v, params) for v in value]
    return value


# ---------------------------------------------------------------- reconstruction adapter
# Faithful port of the audit-PASS Frontier RECONSTRUCTION-RULE (EXP-FRONTIER-35766532429).
# Pure-stdlib transcription: identical arithmetic to the reference numpy implementation
# (softmax subtracts the max before exp; argmax keeps the first index on ties).

def _sha1_hex(s: str) -> str:
    return hashlib.sha1(s.encode("utf-8")).hexdigest()


def _norm_key(k: str) -> str:
    return re.sub(r"[^a-z0-9]", "", k.lower())


def _template_components(template: dict) -> dict:
    url = template.get("url", "")
    headers = template.get("headers", {})
    body = template.get("body", {})
    url_path = url.split("?", 1)[0] if "?" in url else url
    query_str = url.split("?", 1)[1] if "?" in url else ""
    qkeys: list[str] = []
    if query_str:
        for kv in query_str.split("&"):
            if not kv:
                continue
            k = kv.split("=", 1)[0] if "=" in kv else kv
            qkeys.append(k)
    segs = [s for s in url_path.split("/") if s]
    static = [s for s in segs if not _PARAMETER.search(s)]
    return {"url": url, "url_path": url_path, "query_str": query_str, "qkeys": qkeys,
            "segs": segs, "static": static, "headers": dict(headers), "body": dict(body)}


def _value_shape_ok(template_value: str, observed_value: Any) -> bool:
    if not isinstance(observed_value, str):
        return False
    slots = _PARAMETER.findall(template_value)
    if slots:
        m = _PARAMETER.search(template_value)
        prefix = template_value[: m.start()]
        if len(observed_value) <= len(prefix):
            return False
        return observed_value.startswith(prefix) and not _PARAMETER.fullmatch(observed_value)
    return observed_value == template_value


def _channel_present(cand_keys_vals: dict, observed_raw_to_val: dict) -> tuple[bool, bool]:
    if not cand_keys_vals:
        return True, True
    all_present = True
    any_signal = False
    for raw_k, tv in cand_keys_vals.items():
        if raw_k in observed_raw_to_val:
            any_signal = True
            if not _value_shape_ok(tv, observed_raw_to_val[raw_k]):
                all_present = False
        else:
            all_present = False
    return all_present, any_signal


def _candidate_present(m: Mechanism, derived: dict) -> bool:
    comps = _template_components(m.action_template)
    hdr = comps["headers"]
    bdy = comps["body"]
    qkeys = comps["qkeys"]
    obs_hdr_raw = derived["headers_observed"] or {}
    obs_bdy_raw = derived["body_observed"] or {}
    obs_query_raw = derived["url_query"] or {}
    h_ok, _h_sig = _channel_present(hdr, obs_hdr_raw)
    b_ok, _b_sig = _channel_present(bdy, obs_bdy_raw)
    q_ok = True
    for qk in qkeys:
        if qk not in obs_query_raw:
            q_ok = False
    return h_ok and b_ok and q_ok


def _candidate_score(m: Mechanism, derived: dict, use_channels: tuple = ("url", "headers", "body")) -> float:
    comps = _template_components(m.action_template)
    derived_hdr = derived["headers_observed"] or {}
    derived_bdy = derived["body_observed"] or {}
    derived_query = derived["url_query"] or {}
    use_url = "url" in use_channels
    use_hdr = "headers" in use_channels
    use_bdy = "body" in use_channels
    if use_url and comps["qkeys"]:
        obs_norms = {_norm_key(k): k for k in derived_query}
        cand_norms = {_norm_key(k) for k in comps["qkeys"]}
        if cand_norms:
            inter = len(cand_norms & set(obs_norms))
            union = len(cand_norms | set(obs_norms))
            query_hit = inter / union
        else:
            query_hit = 1.0
    else:
        query_hit = 1.0
    if use_url:
        obs_segs = derived["url_segments"]
        t_static = comps["static"]
        if not t_static and not obs_segs:
            path_score = 1.0
        elif not t_static or not obs_segs:
            path_score = 0.0
        else:
            inter = len(set(t_static) & set(obs_segs))
            union = len(set(t_static) | set(obs_segs))
            jacc = inter / union if union else 0
            seq = 0
            for a, b in zip(t_static, obs_segs):
                if a == b:
                    seq += 1
                else:
                    break
            seq_score = seq / max(len(t_static), len(obs_segs)) if max(len(t_static), len(obs_segs)) else 0
            path_score = 0.6 * jacc + 0.4 * seq_score
    else:
        path_score = 1.0
    url_score = 0.5 * query_hit + 0.5 * path_score

    def chan_score(cand_vals: dict, obs_raw: dict):
        if not cand_vals:
            return None
        scores = []
        for raw_k, tv in cand_vals.items():
            if raw_k in obs_raw and _value_shape_ok(tv, obs_raw[raw_k]):
                scores.append(1.0)
            else:
                scores.append(0.0)
        return float(sum(scores) / len(scores))

    h_score = chan_score(comps["headers"], derived_hdr) if use_hdr else None
    b_score = chan_score(comps["body"], derived_bdy) if use_bdy else None
    w_url = 0.35
    w_hdr = 0.35 if h_score is not None else 0.0
    w_bdy = 0.30 if b_score is not None else 0.0
    total_w = w_url + w_hdr + w_bdy
    if total_w == 0:
        return 0.5
    num = w_url * url_score
    if h_score is not None:
        num += w_hdr * h_score
    if b_score is not None:
        num += w_bdy * b_score
    return num / total_w


def _softmax(arr: list[float], temp: float = 0.15) -> list[float]:
    a = [x / temp for x in arr]
    m = max(a)
    e = [math.exp(x - m) for x in a]
    s = sum(e)
    return [x / s for x in e]


def _deterministic_jitter(intent: str, derived: dict) -> float:
    j = ((int(_sha1_hex(derived["url"]), 16) % 7) * 0.003 +
         ((len(derived["url_segments"])) % 3) * 0.002 +
         (int(_sha1_hex(intent), 16) % 5) * 0.001)
    return j


def _adoption_value_template(observed_value: Any, params: dict) -> str | None:
    if not isinstance(observed_value, str):
        return None
    ordered = sorted(params.items(), key=lambda kv: -len(str(kv[1]))) if params else []
    tv = observed_value
    for pk, pv in ordered:
        pvs = str(pv)
        if pvs and pvs in tv:
            tv = tv.replace(pvs, "${%s}" % pk)
    return tv


def _choose_adoptions(derived: dict, candidates: list[Mechanism], params: dict) -> list[tuple]:
    comps_all = [_template_components(m.action_template) for m in candidates]
    cand_hdr_keys: set[str] = set()
    cand_bdy_keys: set[str] = set()
    cand_query_keys: set[str] = set()
    for c in comps_all:
        cand_hdr_keys |= set(c["headers"].keys())
        cand_bdy_keys |= set(c["body"].keys())
        cand_query_keys |= set(c["qkeys"])
    obs_hdr = derived["headers_observed"] or {}
    obs_bdy = derived["body_observed"] or {}
    obs_query = derived["url_query"] or {}
    adoptions: list[tuple] = []
    for k, v in sorted(obs_query.items(), key=lambda kv: kv[0].lower()):
        if k in cand_query_keys:
            continue
        tv = _adoption_value_template(v, params)
        if tv is not None:
            adoptions.append(("query", k, tv))
    for k, v in sorted(obs_hdr.items(), key=lambda kv: kv[0].lower()):
        if k in cand_hdr_keys or _norm_key(k).lower() in _STANDARD_HEADERS:
            continue
        tv = _adoption_value_template(v, params)
        if tv is not None:
            adoptions.append(("headers", k, tv))
    for k, v in sorted(obs_bdy.items(), key=lambda kv: kv[0].lower()):
        if k in cand_bdy_keys:
            continue
        if not isinstance(v, str) or not v:
            continue
        tv = _adoption_value_template(v, params)
        if tv is not None:
            adoptions.append(("body", k, tv))
    return adoptions


def _rewrite_template_multi(base: Mechanism, adoptions: list[tuple], derived: dict) -> dict:
    comps = _template_components(base.action_template)
    obs_hdr = derived["headers_observed"] or {}
    obs_bdy = derived["body_observed"] or {}
    obs_query = derived["url_query"] or {}
    base_path = comps["url_path"]
    query_adopts = [(k, tv) for ch, k, tv in adoptions if ch == "query"]
    header_adopts = [(k, tv) for ch, k, tv in adoptions if ch == "headers"]
    body_adopts = [(k, tv) for ch, k, tv in adoptions if ch == "body"]
    qparts: list[str] = []
    for qk in comps["qkeys"]:
        if qk in obs_query:
            qs = comps["query_str"]
            for kv in qs.split("&"):
                if "=" in kv:
                    kk, vv = kv.split("=", 1)
                    if kk == qk:
                        qparts.append(f"{qk}={vv}")
                        break
                elif kv == qk:
                    qparts.append(qk)
                    break
    for k, tv in query_adopts:
        if k not in [p.split("=")[0] for p in qparts]:
            qparts.append(f"{k}={tv}")
    url = base_path + ("?" + "&".join(qparts) if qparts else "")
    new_headers = {}
    for k, tv in comps["headers"].items():
        if k in obs_hdr:
            new_headers[k] = tv
    for k, tv in header_adopts:
        new_headers[k] = tv
    new_body = {}
    for k, tv in comps["body"].items():
        if k in obs_bdy:
            new_body[k] = tv
    for k, tv in body_adopts:
        new_body[k] = tv
    out = {"url": url}
    if new_headers:
        out["headers"] = new_headers
    if new_body:
        out["body"] = new_body
    return out


def _reconstruct_resolve(intent: str, derived_context: dict, retrieved_candidates: list[Mechanism],
                         params: dict, use_channels: tuple = ("url", "headers", "body")) -> Resolution:
    """Genuine non-oracle reconstruction adapter with multi-channel support."""
    if not retrieved_candidates:
        score = 0.05 + (int(_sha1_hex(intent), 16) % 10) * 0.002
        return Resolution(ResolutionStatus.UNKNOWN, None,
                          "no applicable mechanism - abstain", confidence=float(score))
    work = dict(derived_context)
    work["headers_observed"] = dict(derived_context["headers_observed"] or {}) if "headers" in use_channels else {}
    work["body_observed"] = dict(derived_context["body_observed"] or {}) if "body" in use_channels else {}
    scores = [_candidate_score(m, work, use_channels=use_channels) for m in retrieved_candidates]
    best_sel = max(range(len(scores)), key=lambda i: scores[i])
    adoptions = _choose_adoptions(work, retrieved_candidates, params)
    if not adoptions and _candidate_present(retrieved_candidates[best_sel], work):
        m = retrieved_candidates[best_sel]
        probs = _softmax(scores, temp=0.15)
        conf = float(max(probs))
        jitter = _deterministic_jitter(intent, work)
        conf = min(0.98, max(0.02, conf * 0.85 + 0.12 + jitter))
        if conf < 0.80:
            return Resolution(ResolutionStatus.UNKNOWN, None,
                              f"low confidence {conf:.3f} abstain", confidence=conf)
        required = _template_slots(m.action_template)
        if any(s not in params for s in required):
            return Resolution(ResolutionStatus.UNKNOWN, None, "missing slots after selection",
                              confidence=float(0.3 + len(required) * 0.01))
        bound = _bind(m.action_template, params)
        return Resolution(ResolutionStatus.EXECUTABLE, m.mechanism_id,
                          f"selected structurally matching candidate score {scores[best_sel]:.3f} conf {conf:.3f}",
                          bound_action=bound, confidence=conf)
    if not adoptions:
        conf = 0.2 + (int(_sha1_hex(intent), 16) % 10) * 0.01
        return Resolution(ResolutionStatus.UNKNOWN, None,
                          "cannot reconstruct - no adoptable signal", confidence=float(conf))
    base = retrieved_candidates[best_sel]
    new_template = _rewrite_template_multi(base, adoptions, work)
    rewrite_score = 1.0
    probs = _softmax(scores + [rewrite_score], temp=0.15)
    conf = float(max(probs))
    jitter = _deterministic_jitter(intent, work)
    conf = min(0.98, max(0.02, conf * 0.85 + 0.12 + jitter))
    if conf < 0.80:
        return Resolution(ResolutionStatus.UNKNOWN, None,
                          f"low confidence {conf:.3f} abstain", confidence=conf)
    required = _template_slots(new_template)
    if any(s not in params for s in required):
        return Resolution(ResolutionStatus.UNKNOWN, None, "missing slots after rewrite",
                          confidence=float(0.3 + len(required) * 0.01))
    bound = _bind(new_template, params)
    return Resolution(ResolutionStatus.EXECUTABLE, base.mechanism_id,
                      f"rewrote base template adopting {len(adoptions)} observed keys {adoptions} conf {conf:.3f}",
                      bound_action=bound, confidence=conf)


class SpiderKernel:
    """Conservative first execution-inheritance kernel.

    This kernel is deliberately not a browser agent. It stores and resolves validated mechanisms.
    It abstains when applicability is not demonstrated.
    """

    def __init__(self, registry: MechanismRegistry, min_confidence: float = 0.8):
        self.registry = registry
        self.min_confidence = min_confidence

    def observe(self, observation: Observation) -> str:
        raw = json.dumps({
            "intent": observation.intent,
            "state": observation.state,
            "action": observation.action,
            "next_state": observation.next_state,
            "success": observation.success,
            "provenance": observation.provenance,
        }, sort_keys=True, separators=(",", ":")).encode()
        return hashlib.sha256(raw).hexdigest()

    def distill(self, observation: Observation) -> Mechanism | None:
        """Create only a literal candidate mechanism.

        Generalization/parameter induction is intentionally not guessed here; Research 2.0 must
        earn that capability through C-PARAM-INHERIT and related gates.
        """
        if not observation.success:
            return None
        oid = self.observe(observation)[:16]
        return Mechanism(
            mechanism_id=f"obs-{oid}",
            intent=observation.intent,
            preconditions=dict(observation.state),
            action_template=dict(observation.action),
            postconditions=dict(observation.next_state),
            evidence=[oid],
            confidence=0.5,
        )

    def resolve(self, intent: str, context: dict[str, Any], params: dict[str, Any] | None = None,
                *, reconstruct: bool = False,
                use_channels: tuple[str, ...] = ("url", "headers", "body")) -> Resolution:
        """Resolve an intent against validated mechanisms.

        Default (reconstruct=False) is the mirror-faithful exact-match kernel: candidates are
        filtered by intent/preconditions/guards/slots and the highest-confidence mechanism wins.

        reconstruct=True exposes the reconstruction adapter (EXP-FRONTIER-35766532429 audit PASS):
        when the observed state carries keys/aliases absent from every candidate template, the
        adapter selects the structurally closest candidate and rewrites its action template with
        adoptions of the observed keys, abstaining (UNKNOWN) below the 0.80 confidence gate.
        The adapter reads ONLY the whitelisted ALLOWED_STATE_KEYS from context.
        """
        params = params or {}
        candidates = []
        for m in self.registry.all():
            if m.invalidated or m.intent != intent:
                continue
            if not _matches(m.preconditions, context):
                continue
            if not _matches(m.applicability_guards, context):
                continue

            required_slots = set(m.parameter_slots) | _template_slots(m.action_template)
            if any(slot not in params for slot in required_slots):
                continue
            candidates.append(m)

        if not candidates:
            return Resolution(ResolutionStatus.UNKNOWN, None, "no applicable validated mechanism")

        if reconstruct:
            derived = {k: context[k] for k in ALLOWED_STATE_KEYS if k in context}
            return _reconstruct_resolve(intent, derived, candidates, params, use_channels=use_channels)

        candidates.sort(key=lambda m: m.confidence, reverse=True)
        best = candidates[0]
        if best.confidence < self.min_confidence:
            return Resolution(ResolutionStatus.EXPLORE, best.mechanism_id, "candidate exists but confidence is below execution threshold", confidence=best.confidence)

        return Resolution(
            ResolutionStatus.EXECUTABLE,
            best.mechanism_id,
            "applicability guards and confidence threshold passed",
            bound_action=_bind(best.action_template, params),
            confidence=best.confidence,
        )

    def verify(self, mechanism_id: str, observed_state: dict[str, Any]) -> bool:
        mechanism = next((m for m in self.registry.all() if m.mechanism_id == mechanism_id), None)
        if mechanism is None or mechanism.invalidated:
            return False
        return _matches(mechanism.postconditions, observed_state)

    def invalidate(self, mechanism_id: str) -> bool:
        return self.registry.invalidate(mechanism_id)
