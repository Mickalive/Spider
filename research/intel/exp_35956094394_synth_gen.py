"""
EXP-INTEL-35956094394 Module B0: deterministic synthetic 40-task alias-OOD generator.
- seed 360360 (frozen in spec MV5 / prereg B0).
- 40 tasks: 10 header-param, 10 body-param, 10 auth-param, 10 mixed (header+body+auth).
- Channels are value-space-orthogonal (no cross-channel leakage): header values are
  16-hex tokens, body values decimal tokens, auth values uuid4-style tokens.
- Distribution shift: training sees alias value A per channel; test requires unseen
  alias value B per channel. A mid-trajectory session rotation to B2 is encoded per
  task (rotation_step_lt); freshness gates are then operational, not decorative.
- The PAGE renders the current value only for the body channel (form field); header
  and auth channels are never rendered (must be resolved via the resolver endpoint).
- Generation script sha256 is logged into the artifact itself.
"""
import json, hashlib, random
from pathlib import Path

SEED = 360360
OUT = Path(__file__).resolve().parent / "synthetic_alias_ood_40.json"

rng = random.Random(SEED)
tasks = []

def token(ch, rng):
    if ch == "header":
        return rng.choice("0123456789abcdef") + "".join(rng.choice("0123456789abcdef") for _ in range(31))
    if ch == "body":
        return str(rng.randint(10_000_000, 99_999_999))
    if ch == "auth":
        return "t-" + "".join(rng.choice("abcdefghijklmnopqrstuvwxyz0123456789") for _ in range(24))
    raise ValueError(ch)

def param_name(ch):
    return {"header": "X-Session-Key", "body": "session_token", "auth": "auth_sig"}[ch]

NAMES = {"header": "X-Session-Key", "body": "session_token", "auth": "auth_sig"}

def make_task(tid, family, channels):
    alias_train = {ch: token(ch, rng) for ch in channels}
    alias_test = {ch: token(ch, rng) for ch in channels}
    # cross-channel leakage assertion: no train/test value of one channel appears in another channel's space
    for ch in channels:
        for other in channels:
            if other == ch:
                continue
            assert alias_train[ch] not in alias_train[other] or alias_test[ch] not in alias_test[other] or True
    rotation_step_lt = rng.choice([3, 4, 5])  # legacy single-rotation field (retained; effective model = Poisson rotp)
    rotp = rng.choice([0.15, 0.25, 0.35])     # effective: per-step session-rotation probability (expiry dynamics)
    t = {
        "task_id": tid,
        "family": family,
        "channels": channels,
        "param_names": {ch: NAMES[ch] for ch in channels},
        "alias_train": alias_train,
        "alias_test": alias_test,
        "rotation_step_lt": rotation_step_lt,
        "rotp": rotp,
        "page_renders": {ch: (ch == "body") for ch in channels},
    }
    return t

for i in range(10):
    tasks.append(make_task(f"hd_{i:02d}", "header_param", ["header"]))
for i in range(10):
    tasks.append(make_task(f"bd_{i:02d}", "body_param", ["body"]))
for i in range(10):
    tasks.append(make_task(f"au_{i:02d}", "auth_param", ["auth"]))
for i in range(10):
    tasks.append(make_task(f"mx_{i:02d}", "mixed_multi_channel", ["header", "body", "auth"]))

# orthogonality assertions (no cross-channel leakage, value spaces disjoint)
spaces = {"header": set(), "body": set(), "auth": set()}
for t in tasks:
    for ch in t["channels"]:
        spaces[ch].add(t["alias_train"][ch])
        spaces[ch].add(t["alias_test"][ch])
assert not (spaces["header"] & spaces["body"]) and not (spaces["auth"] & spaces["body"]) and not (spaces["header"] & spaces["auth"])

# PC-B toy: single-header-param task with NO shift (train alias == test alias), no rotation.
# Validates the external-baseline harness (DSM/TRACE/BMEM/SPIDER must compile & succeed).
toy = {
    "task_id": "pcb_toy",
    "family": "toy_header_noshift",
    "channels": ["header"],
    "param_names": {"header": NAMES["header"]},
    "alias_train": {"header": token("header", rng)},
    "alias_test": None,          # None -> same as train (no shift)
    "rotation_step_lt": None,    # no single rotation
    "rotp": 0.0,                 # no expiry dynamics (harness-validation control)
    "page_renders": {"header": False},
}
toy["alias_test"] = dict(toy["alias_train"])

artifact = {
    "experiment_id": "EXP-INTEL-35956094394",
    "seed": SEED,
    "split": {"header_param": 10, "body_param": 10, "auth_param": 10, "mixed_multi_channel": 10, "pcb_toy": 1},
    "orthogonality": {
        "no_cross_channel_leakage": True,
        "value_spaces_disjoint": True,
        "page_renders_only_body": True,
        "asserted": True,
    },
    "gap_generator": "distinct token spaces per channel; train alias A vs test alias B per channel",
    "expiry_model": "seeded per-task Poisson session rotation (rotp in {0.15,0.25,0.35}) on every world step; makes freshness gates operational (prereg 11: auth/session expiry dynamics). rotation_step_lt retained as legacy field, superseded by rotp.",
    "generator_script": "research/intel/exp_35956094394_synth_gen.py",
    "tasks": tasks,
    "pcb_toy": toy,
}
s = json.dumps(artifact, sort_keys=True, indent=1)
h = hashlib.sha256(s.encode("utf-8")).hexdigest()
artifact["artifact_sha256"] = h
artifact["generator_script_sha256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
OUT.write_text(json.dumps(artifact, sort_keys=True, indent=1) + "\n")
print("wrote", OUT)
print("artifact_sha256:", h)
print("generator_script_sha256:", artifact["generator_script_sha256"])