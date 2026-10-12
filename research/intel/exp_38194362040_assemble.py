#!/usr/bin/env python3
"""EXECUTE assembler for EXP-INTEL-38194362040 (intel lane).

Part of the evaluator family (prereg.md Appendix A.6): reads the frozen raw
evidence produced by the EXECUTE transaction and writes the canonical packet
files result.json and provenance.json. No model calls; deterministic given the
raw evidence. report.md is authored separately as explanatory prose.
"""
import hashlib
import json
import os
import platform
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
EXP = os.path.join(REPO, "research", "experiments", "EXP-INTEL-38194362040")


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 22), b""):
            h.update(chunk)
    return h.hexdigest()


def rel(path):
    return os.path.relpath(path, REPO)


def artifact(path, role):
    p = os.path.join(REPO, path) if not os.path.isabs(path) else path
    return {"path": rel(p), "sha256": sha256_file(p), "role": role}


def main():
    decision = json.load(open(os.path.join(EXP, "raw", "decision.json")))
    controls = json.load(open(os.path.join(EXP, "raw", "controls.json")))
    preflight = json.load(open(os.path.join(EXP, "raw", "preflight.json")))
    prov = json.load(open(os.path.join(EXP, "raw", "provisioning_evidence.json")))
    census = json.load(open(os.path.join(EXP, "raw", "endpoint_census.json")))
    comparators = json.load(open(os.path.join(EXP, "raw", "external_comparators.json")))
    mat = json.load(open(os.path.join(EXP, "raw", "materialized_configs.json")))

    cells = decision["cells"]
    q = cells["M-14B-QWEN"]
    l = cells["M-8B-LLAMA"]
    qm, lm = q["metrics"], l["metrics"]

    def m4(v, k, n, unit, reason=None):
        d = {"value": v, "k": k, "n": n, "unit": unit}
        if reason:
            d["reason"] = reason
        return d

    metrics = {
        "M-14B-QWEN": {
            "positive_control_pass_rate": m4(qm["positive_control_pass_rate"], qm["positive_control_n_pass"], qm["positive_control_n_total"], "fraction"),
            "parseable_action_rate_step1": m4(qm["parseable_action_rate_step1"], round(qm["parseable_action_rate_step1"] * 5), 5, "fraction"),
            "answer_action_emission_rate": m4(qm["answer_action_emission_rate"], round(qm["answer_action_emission_rate"] * 5), 5, "fraction"),
            "task_success_rate": m4(qm["task_success_rate"], round(qm["task_success_rate"] * 5), 5, "fraction"),
            "mean_inference_latency_s": {"value": qm["mean_inference_latency_s"], "n_calls": qm["n_calls_latency"], "unit": "s"},
            "mean_completion_tokens": {"value": qm["mean_completion_tokens"], "n_calls": qm["n_calls_tokens"], "unit": "tokens"},
            "served_body_digest_verified": {"value": 1, "unit": "bool"},
            "gguf_metadata_fingerprint_matched": {"value": 1, "unit": "bool"},
            "cell_state": q["cell_state"],
            "clears": q["clears"],
        },
        "M-8B-LLAMA": {
            "positive_control_pass_rate": m4(lm["positive_control_pass_rate"], lm["positive_control_n_pass"], lm["positive_control_n_total"], "fraction"),
            "parseable_action_rate_step1": m4(lm["parseable_action_rate_step1"], round(lm["parseable_action_rate_step1"] * 5), 5, "fraction"),
            "answer_action_emission_rate": m4(lm["answer_action_emission_rate"], round(lm["answer_action_emission_rate"] * 5), 5, "fraction"),
            "task_success_rate": m4(lm["task_success_rate"], round(lm["task_success_rate"] * 5), 5, "fraction"),
            "mean_inference_latency_s": {"value": lm["mean_inference_latency_s"], "n_calls": lm["n_calls_latency"], "unit": "s"},
            "mean_completion_tokens": {"value": lm["mean_completion_tokens"], "n_calls": lm["n_calls_tokens"], "unit": "tokens"},
            "served_body_digest_verified": {"value": 1, "unit": "bool"},
            "gguf_metadata_fingerprint_matched": {"value": 1, "unit": "bool"},
            "cell_state": l["cell_state"],
            "clears": l["clears"],
        },
        "PC-ORACLE-EPISODE": {
            "task_success_rate": {"value": controls["PC-ORACLE-EPISODE"]["task_success_rate"], "k": 5, "n": 5, "unit": "fraction"},
            "parseable_action_rate_step1": {"value": controls["PC-ORACLE-EPISODE"]["parseable_action_rate_step1"], "k": 5, "n": 5, "unit": "fraction"},
        },
        "NC-NO-MODEL-ACTION": {
            "task_success_rate": {"value": controls["NC-NO-MODEL-ACTION"]["task_success_rate"], "k": 0, "n": 5, "unit": "fraction"},
            "parseable_action_rate_step1": {"value": controls["NC-NO-MODEL-ACTION"]["parseable_action_rate_step1"], "k": 0, "n": 5, "unit": "fraction"},
        },
        "B-RANDOM-ACTION": {
            "task_success_rate": {"value": controls["B-RANDOM-ACTION"]["task_success_rate"], "k": round(controls["B-RANDOM-ACTION"]["task_success_rate"] * 5), "n": 5, "unit": "fraction"},
            "parseable_action_rate_step1": {"value": controls["B-RANDOM-ACTION"]["parseable_action_rate_step1"], "k": 5, "n": 5, "unit": "fraction"},
        },
        "capability_bar": {"task_success_rate": 0.6, "parseable_action_rate_step1": 0.6, "episodes": 5, "unit": "fraction"},
        "candidates_measured_complete": {"value": 2, "n": 2, "unit": "cells"},
        "served_body_digest_verified": {"value": 2, "n": 2, "unit": "candidates"},
        "gguf_metadata_fingerprint_matched": {"value": 2, "n": 2, "unit": "candidates"},
        "b3_status": decision["b3_status"],
        "providers_credential_required": {"value": census["counts"]["CREDENTIAL_REQUIRED"], "unit": "providers"},
        "providers_credential_free_operationally_capped": {"value": census["counts"]["CREDENTIAL_FREE_OPERATIONALLY_CAPPED"], "unit": "providers"},
        "providers_provisionable_credentialed": {"value": census["counts"]["PROVISIONABLE_CREDENTIATED"], "unit": "providers"},
        "providers_unreachable": {"value": census["counts"]["UNREACHABLE"], "unit": "providers"},
        "comparators_enumerated": {"value": comparators["comparators_enumerated"], "unit": "entries",
                                   "primary_sources_pinned": comparators["comparators_enumerated"],
                                   "evidence_label": "CANDIDATE_NOT_EVIDENCE"},
        "comparators_not_pinned": {"value": comparators["comparators_not_pinned"], "unit": "entries"},
        "preflight_pass": preflight["pass"],
        "outcome": decision["outcome"],
        "status": decision["status"],
        "decision_trace": decision["decision_trace"],
    }

    ctl = {
        "PC-SUITE-EXP-INTEL-38194362040": {
            "role": "positive_control_suite",
            "members": ["PC-JSON-CONSTRAINED-DECODING", "PC-ORACLE-EPISODE"],
            "expected": "PC-JSON-CONSTRAINED-DECODING 10/10 per candidate; PC-ORACLE-EPISODE 5/5",
            "observed": "PC-JSON-CONSTRAINED-DECODING 10/10 on both candidates; PC-ORACLE-EPISODE 5/5",
            "verdict": "PASS",
            "evidence_ref": "raw/controls.json, cells/M-14B-QWEN/raw/model_receipts.json, cells/M-8B-LLAMA/raw/model_receipts.json",
        },
        "PC-JSON-CONSTRAINED-DECODING": {
            "role": "positive_control_per_candidate_constrained_decoding_gate",
            "expected": "10/10 parseable constrained-JSON probes per loaded candidate",
            "observed": "10/10 for M-14B-QWEN and 10/10 for M-8B-LLAMA",
            "verdict": "PASS",
            "evidence_ref": "cells/M-14B-QWEN/raw/model_receipts.json#positive_control, cells/M-8B-LLAMA/raw/model_receipts.json#positive_control",
        },
        "PC-ORACLE-EPISODE": {
            "role": "positive_control_episode",
            "expected": "5/5 task_success=true through the real frozen run_episode scorer against the served page",
            "observed": "5/5 task_success=true; parseable_action_rate_step1=1.0",
            "verdict": "PASS",
            "evidence_ref": "raw/controls.json#PC-ORACLE-EPISODE",
        },
        "NC-NO-MODEL-ACTION": {
            "role": "null_control_no_model",
            "expected": "parseable_action_rate_step1=0.0 AND task_success_rate=0.0",
            "observed": "parseable_action_rate_step1=0.0, task_success_rate=0.0",
            "verdict": "PASS",
            "evidence_ref": "raw/controls.json#NC-NO-MODEL-ACTION",
        },
        "B-RANDOM-ACTION": {
            "role": "negative_baseline_random_actions",
            "expected": "parseable_action_rate_step1=1.0 AND task_success_rate<0.6",
            "observed": "parseable_action_rate_step1=1.0, task_success_rate=0.2 (1/5, <0.6)",
            "verdict": "PASS",
            "evidence_ref": "raw/controls.json#B-RANDOM-ACTION",
        },
        "B-CARRIED-3B-8B-QWEN-GOAL-SCHEMA": {
            "role": "carried_reference_baseline_protocol_hardness",
            "status": "CARRIED_NOT_RERUN",
            "expected": "carried FAIL: M-7B-QWEN 0/5 and M-3B-QWEN 0/5, parseable_action_rate_step1=1.0",
            "observed": "carried from EXP-INTEL-38164607941; used only to certify protocol hardness/decoding liveness, not as a comparator arm",
            "verdict": "NOT_APPLICABLE",
            "evidence_ref": "research/experiments/EXP-INTEL-38164607941/result.json#metrics",
        },
        "B-POLLINATIONS-CARRIED": {
            "role": "carried_hosted_credential_free_proxy_baseline",
            "status": "CARRIED_NOT_RERUN",
            "expected": "credential-free but operationally capped (reasoning-only, ~197-token cap, intermittent 402, no pinning/SLA)",
            "observed": "census classified Pollinations CREDENTIAL_FREE_OPERATIONALLY_CAPPED (HTTP 200); not invoked for capability",
            "verdict": "NOT_APPLICABLE",
            "evidence_ref": "raw/endpoint_census.json#providers.Pollinations",
        },
    }

    artifacts = [
        artifact("research/experiments/EXP-INTEL-38194362040/raw/preflight.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/raw/run_resources.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/raw/controls.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/raw/materialized_configs.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/raw/provisioning_evidence.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/raw/endpoint_census.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/raw/external_comparators.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/raw/decision.json", "derived"),
        artifact("research/experiments/EXP-INTEL-38194362040/cells/M-14B-QWEN/raw/harness_config.json", "fixture"),
        artifact("research/experiments/EXP-INTEL-38194362040/cells/M-14B-QWEN/raw/provisioning_receipt.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/cells/M-14B-QWEN/raw/model_receipts.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/cells/M-8B-LLAMA/raw/harness_config.json", "fixture"),
        artifact("research/experiments/EXP-INTEL-38194362040/cells/M-8B-LLAMA/raw/provisioning_receipt.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/cells/M-8B-LLAMA/raw/model_receipts.json", "raw"),
        artifact("research/experiments/EXP-INTEL-38194362040/configs/config_M-14B-QWEN.json", "fixture"),
        artifact("research/experiments/EXP-INTEL-38194362040/configs/config_M-8B-LLAMA.json", "fixture"),
        artifact("research/intel/exp_38194362040_materialize.py", "code"),
        artifact("research/intel/exp_38194362040_provision.py", "code"),
        artifact("research/intel/exp_38194362040_controls.py", "code"),
        artifact("research/intel/exp_38194362040_census.py", "code"),
        artifact("research/intel/exp_38194362040_comparators.py", "code"),
        artifact("research/intel/exp_38194362040_eval.py", "code"),
        artifact("research/intel/exp_38194362040_assemble.py", "code"),
        artifact("research/intel/run_exp_37982024058.py", "code"),
        artifact("research/experiments/EXP-INTEL-37982024058/raw/harness_config.json", "fixture"),
        artifact("research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py", "fixture"),
    ]

    observations = [
        "PREFLIGHT PASS (frozen rule 1) with all five checks true: PC-ORACLE-EPISODE 5/5 task_success and parseable_action_rate_step1=1.0; NC-NO-MODEL-ACTION parseable_action_rate_step1=0.0 and task_success_rate=0.0; B-RANDOM-ACTION parseable_action_rate_step1=1.0 and task_success_rate=0.2 (<0.6); all freeze_artifact sha256 checks match; required stack imports (llama_cpp 0.2.90, playwright, frozen runner producer symbols) succeed.",
        "CONTENT-IDENTITY REPAIR CONFIRMED: at EXECUTE each candidate's revision-pinned served body was fully downloaded and its sha256 equals the frozen served_body_sha256 pin and the HF tree-API lfs.oid - M-14B-QWEN 8,988,110,976 bytes / e47ad95dad6ff848b431053b375adb5d39321290ea2c638682577dafca87c008; M-8B-LLAMA 4,920,739,232 bytes / 7b064f5842bf9532c91456deda288a1b672397a54fa729aa665952863033557c. The parsed GGUF header fingerprints also equal the frozen fingerprints. Both candidates IDENTITY-PASS; the parent's metadata-vs-body mismatch did not recur.",
        "M-14B-QWEN (Qwen2.5-14B-Instruct Q4_K_M, chat_format=qwen): loaded (load_time_s=0.543, max RSS ~9.4 GB); PC-JSON-CONSTRAINED-DECODING 10/10; 5/5 episode records -> COMPLETE. task_success_rate=0.0 (0/5), parseable_action_rate_step1=1.0 (5/5), answer_action_emission_rate=0.0 (0/5). Every episode clicked #reveal-btn at step 0 (revealing TARGET-42) and then re-clicked the now-hidden #reveal-btn for all remaining steps, never emitting an answer action. mean latency 12.535 s/call (35 calls), mean completion tokens 15.0.",
        "M-8B-LLAMA (Meta-Llama-3.1-8B-Instruct Q4_K_M, chat_format=llama-3): loaded (load_time_s=15.1, max RSS ~5.2 GB); PC-JSON-CONSTRAINED-DECODING 10/10; 5/5 episode records -> COMPLETE. task_success_rate=0.0 (0/5), parseable_action_rate_step1=1.0 (5/5), answer_action_emission_rate=0.0 (0/5). Same behavioural mode: reveal click at step 0, then repeated re-clicks of the hidden reveal button; no answer action in any episode. mean latency 5.726 s/call (35 calls), mean completion tokens 10.57.",
        "Both candidate cells COMPLETE and neither CLEARS (task_success_rate 0.0 < 0.6 in both), so frozen rule 4 yields OUTCOME=FALSIFIES with B3_STATUS=NOT_SATISFIED (every predeclared hosted provider is CREDENTIAL_REQUIRED / UNREACHABLE / CREDENTIAL_FREE_OPERATIONALLY_CAPPED). status=COMPLETE.",
        "ENDPOINT CENSUS (non-gating): 12 providers. PROVISIONABLE_CREDENTIATED=0; CREDENTIAL_REQUIRED=10 (OpenAI 401, Anthropic 401, Google Gemini 403, Mistral 401, Groq 401, Together 401, OpenRouter 200, DeepSeek 401, Fireworks 401, Cohere 401); CREDENTIAL_FREE_OPERATIONALLY_CAPPED=1 (Pollinations HTTP 200); UNREACHABLE=1 (HuggingFace Inference, connection error). No credential environment variable was present.",
        "EXTERNAL COMPARATORS (non-gating readiness/reproducibility table): 3/3 entries enumerated with pinned primary sources, all labelled CANDIDATE_NOT_EVIDENCE (QCR arXiv:2608.12847; Agentic Compilation arXiv:2604.09718; site-memory/ColorBrowserAgent arXiv:2601.07262). No external number was reproduced and none is used as evidence.",
        "The observed failure mode (step-0 reveal succeeds, then hidden-button re-click loop, zero answer actions) is the same mode inherited from the audited 3B-8B Qwen prompt ablation (EXP-INTEL-38164607941) and reproduced here at 14B Qwen and 8B Llama under the frozen protocol.",
        "No claim is promoted or weakened by this transaction; the FALSIFIES outcome is bounded to the predeclared credential-free local Q4_K_M classes tested and the recorded non-provisionable hosted census.",
    ]

    validity_notes = [
        "Bounded negative scope: FALSIFIES is asserted only over the COMPLETE predeclared credential-free local Q4_K_M candidate set tested (Qwen2.5-14B-Instruct, Meta-Llama-3.1-8B-Instruct) plus the carried Qwen 3B-8B anchors and the recorded non-provisionable hosted census. It does not close hosted frontier classes (blocked, not tested), other quantisations, other tasks or other domains, and does not globally reject C-LLM-INHERIT.",
        "Deterministic protocol / no variance: temperature=0.0 + fixed seeds (42-46). The 3/5 (0.6) rule is a pre-declared capability-gate adequacy rule, not a statistical threshold; n=5 per candidate affords no variance estimate. This limitation is inherited from the frozen design and disclosed.",
        "Representation loss (inherited): state is a simplified text observation (PAGE_TEXT 300 chars, ELEMENTS over button/a/input, HISTORY), not a full accessibility tree. After the reveal, PAGE_TEXT contains TARGET-42 and ELEMENTS still lists the (now hidden) reveal button; both tested classes re-click it rather than answering. This packet changes only the model class, not the observation representation, so the failure may partly reflect representation/affordance reasoning rather than raw capacity.",
        "Grammar admission vs parse acceptance: the frozen GBNF admits any single-field object; liveness rests on the empirically verified PC 10/10 and 5/5 step-1 parseable behaviour. A candidate with parseable_action_rate_step1 < 0.6 cannot clear the bar, so this residual cannot manufacture a false SUPPORTS.",
        "Task-bank granularity: the frozen task is a single near-deterministic page; clearing the bar is necessary but not sufficient for Gate-3 readiness (comparator-at-ceiling and dynamic range are B2-owned by Runtime).",
        "Scale vs family are not separated within a candidate: both candidates failed, so the 14B scale test and the non-Qwen family test each individually bound those tested classes; this does not isolate scale from family-specific properties, and no interaction claim is made.",
        "The endpoint census is observational (env-var presence + unauthenticated HTTP status/reachability + carried receipts); it cannot prove a credentialed provider would clear the bar, only that it is provisionable. Hosted model numbers are CANDIDATE_NOT_EVIDENCE.",
        "The external-comparator readiness/reproducibility table is a literature-identity enumeration; no vendor number is SPIDER evidence and no external number is reproduced by this packet.",
        "The 14B GGUF (~9 GB) loaded successfully on this 15 GB box (max RSS ~9.4 GB); no load failure occurred. No candidate was UNMEASURED_LOAD_FAILED or EXCLUDED, so the FALSIFIES branch is not emptied by operational failure.",
        "The frozen runner and base fixture are byte-verified freeze_artifacts; the per-candidate overlays differ from the frozen base config only in prompts.system, sampling.chat_format and candidate_models_frozen.",
        "In DESIGN terminology this is the Product-targeting C-LLM-INHERIT experiment for Intel, which only owns priority_claim C-LLM-INHERIT among the relevant Product claim set; the treatment arm is a candidate model under the frozen protocol. No governed Product code was modified.",
    ]

    unresolved = [
        "Whether a hosted frontier class (credential-gated, not tested) clears the frozen minimal bar; no hosted model was invoked and no API credential exists in this factory.",
        "Whether the failure is intrinsic to raw multi-step control capacity or to the frozen simplified observation representation (ELEMENTS exposes the hidden reveal button after reveal); this packet cannot separate those, and a representation-level follow-up (accessibility tree / hidden-element suppression) is a different factor.",
        "Whether the tested classes could clear the bar under any prompt or decoding variation; the frozen single-factor protocol uses one fixed P-TREAT-GOAL-SCHEMA prompt, so prompt sensitivity is not explored here.",
        "Whether the HF Xet metadata/body mismatch documented by the parent experiment (xetHash/etag vs lfs.oid) affects other lanes' pinned GGUFs; not surveyed.",
        "Whether other quantisations or a different task would change the bounded negative; out of the frozen scope.",
    ]

    # frozen input verification
    frozen = {}
    for name, exp_path in [("request.json", "request.json"), ("spec.json", "spec.json"),
                           ("prereg.md", "prereg.md"), ("freeze.json", "freeze.json"),
                           ("design_review.json", "design_review.json")]:
        p = os.path.join(EXP, exp_path)
        frozen[name] = {"path": rel(p), "sha256": sha256_file(p)}
    frz = json.load(open(os.path.join(EXP, "freeze.json")))
    frozen["freeze_hashes_match"] = {
        "request.json": frozen["request.json"]["sha256"] == frz["hashes"]["request.json"],
        "spec.json": frozen["spec.json"]["sha256"] == frz["hashes"]["spec.json"],
        "prereg.md": frozen["prereg.md"]["sha256"] == frz["hashes"]["prereg.md"],
        "design_review.json": frozen["design_review.json"]["sha256"] == frz["hashes"]["design_review.json"],
    }
    frozen["freeze_artifacts_all_match"] = all(
        v.get("match") for v in preflight["freeze_artifact_hashes"].values()
    )

    result = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-38194362040",
        "lane": "intel",
        "status": "COMPLETE",
        "outcome": "FALSIFIES",
        "claim_ids": ["C-LLM-INHERIT"],
        "summary": (
            "Corrected byte-verified credential-free capable-endpoint capability ladder. Content-identity repair "
            "succeeded: both predeclared candidates were fully downloaded, their served-body sha256+bytes and GGUF "
            "header fingerprints match the frozen pins (IDENTITY-PASS), and both loaded. Each cell is COMPLETE "
            "(PC-JSON-CONSTRAINED-DECODING 10/10; 5/5 episodes) and neither CLEARS: M-14B-QWEN task_success_rate=0.0 "
            "(0/5) and M-8B-LLAMA task_success_rate=0.0 (0/5), both parseable_action_rate_step1=1.0, "
            "answer_action_emission_rate=0.0. Both classes click #reveal-btn at step 0 (revealing TARGET-42) then "
            "re-click the now-hidden button for all remaining steps, never answering. The endpoint census "
            "(non-gating) finds 0 PROVISIONABLE_CREDENTIATED, 10 CREDENTIAL_REQUIRED, 1 CREDENTIAL_FREE_OPERATIONALLY_CAPPED "
            "(Pollinations) and 1 UNREACHABLE (HuggingFace Inference). Frozen rule 4 therefore yields OUTCOME=FALSIFIES "
            "and B3_STATUS=NOT_SATISFIED: no currently-provisionable credential-free same-protocol endpoint clears the "
            "frozen minimal multi-step Web-agent bar, so readiness condition (3) is not satisfied. The 3-entry external-comparator "
            "readiness table is recorded as CANDIDATE_NOT_EVIDENCE. This is a valid scientific negative over the predeclared "
            "credential-free Q4_K_M classes tested; it is not a global rejection of C-LLM-INHERIT and does not close hosted frontier classes."
        ),
        "metrics": metrics,
        "controls": ctl,
        "artifacts": artifacts,
        "observations": observations,
        "validity_notes": validity_notes,
        "unresolved": unresolved,
        "frozen_input_verification": frozen,
    }

    with open(os.path.join(EXP, "result.json"), "w") as f:
        json.dump(result, f, indent=2, sort_keys=False)

    # ---- provenance.json ----
    mem_gb = None
    try:
        with open("/proc/meminfo") as mf:
            for line in mf:
                if line.startswith("MemTotal:"):
                    mem_gb = round(int(line.split()[1]) / (1024 * 1024), 1)
                    break
    except OSError:
        mem_gb = None
    env = {
        "os": platform.platform(),
        "python": platform.python_version(),
        "venv": "/tmp/opencode/venv",
        "llama_cpp_python": "0.2.90",
        "playwright": "1.63.0",
        "chrome_path": "/usr/bin/google-chrome",
        "cpu_cores": os.cpu_count(),
        "mem_total_gb": mem_gb,
        "n_threads": 4,
        "network": "huggingface.co (GGUF bodies) and PyPI reachable; no hosted-provider credentials present",
    }
    provenance = {
        "schema_version": 1,
        "experiment_id": "EXP-INTEL-38194362040",
        "lane": "intel",
        "run": {
            "kind": "github_actions",
            "run_id": os.environ.get("GITHUB_RUN_ID"),
            "run_attempt": os.environ.get("GITHUB_RUN_ATTEMPT"),
            "repository": os.environ.get("GITHUB_REPOSITORY"),
            "server_url": os.environ.get("GITHUB_SERVER_URL"),
            "github_sha": os.environ.get("GITHUB_SHA"),
            "repo_head": "50bc0c511cdc81e8100857903d428d780328c930",
            "branch": "lab2/intel",
            "execution_checkpoint": {
                "path": "research/experiments/EXP-INTEL-38194362040/execution_checkpoint.json",
                "github_run_id": "38194362040",
                "pre_execute_sha": "80662c80feb21351aaca63073f74b6b505e0b570",
                "note": "Prior EXECUTE attempts failed with exit 75 (transient model-pool exhaustion) before producing evidence; this transaction ran the frozen design to completion.",
            },
        },
        "frozen_inputs": frozen,
        "freeze_artifacts": {
            "note": "All hashes in freeze.json.artifact_hashes were re-verified on disk before EXECUTE; match status is derived from raw/preflight.json.",
            "entries": [
                {
                    "path": p,
                    "match": v.get("match"),
                    "expected_sha256": v.get("expected_sha256"),
                    "observed_sha256": v.get("observed_sha256"),
                }
                for p, v in preflight["freeze_artifact_hashes"].items()
            ],
        },
        "prompt_strings": {
            "P-TREAT-GOAL-SCHEMA": {
                "sha256": "36a4240aba96e46797c16aebbedcc548778a0c1097b4ce4432608148758c5716",
                "note": "frozen prompt treatment applied to both candidate cells; contains neither '#reveal-btn' nor 'TARGET-42'",
            }
        },
        "harness_config_hashes": {
            "base_config": mat["base_config_path"],
            "base_config_sha256": mat["base_config_sha256"],
            "M-14B-QWEN_overlay_sha256": mat["cells"]["M-14B-QWEN"]["overlay_sha256"],
            "M-8B-LLAMA_overlay_sha256": mat["cells"]["M-8B-LLAMA"]["overlay_sha256"],
            "M-14B-QWEN_diff_paths": mat["cells"]["M-14B-QWEN"]["diff_paths"],
            "M-8B-LLAMA_diff_paths": mat["cells"]["M-8B-LLAMA"]["diff_paths"],
        },
        "models": {},
        "environment": env,
        "commands": [
            "/tmp/opencode/venv/bin/python research/intel/exp_38194362040_materialize.py",
            "/tmp/opencode/venv/bin/python research/intel/exp_38194362040_provision.py",
            "/tmp/opencode/venv/bin/python research/intel/exp_38194362040_controls.py --outdir research/experiments/EXP-INTEL-38194362040 --config research/experiments/EXP-INTEL-37982024058/raw/harness_config.json --chrome /usr/bin/google-chrome",
            "/tmp/opencode/venv/bin/python research/intel/run_exp_37982024058.py --mode probe-candidate --outdir research/experiments/EXP-INTEL-38194362040/cells/M-14B-QWEN --candidate M-14B-QWEN --gguf /tmp/opencode/gguf/Qwen2.5-14B-Instruct-Q4_K_M.gguf --chrome /usr/bin/google-chrome --n-threads 4",
            "/tmp/opencode/venv/bin/python research/intel/run_exp_37982024058.py --mode probe-candidate --outdir research/experiments/EXP-INTEL-38194362040/cells/M-8B-LLAMA --candidate M-8B-LLAMA --gguf /tmp/opencode/gguf/Meta-Llama-3.1-8B-Instruct-Q4_K_M.gguf --chrome /usr/bin/google-chrome --n-threads 4",
            "/tmp/opencode/venv/bin/python research/intel/exp_38194362040_census.py research/experiments/EXP-INTEL-38194362040",
            "/tmp/opencode/venv/bin/python research/intel/exp_38194362040_comparators.py research/experiments/EXP-INTEL-38194362040",
            "/tmp/opencode/venv/bin/python research/intel/exp_38194362040_eval.py",
            "/tmp/opencode/venv/bin/python research/intel/exp_38194362040_assemble.py",
        ],
        "authored_code": [
            artifact("research/intel/exp_38194362040_materialize.py", "code"),
            artifact("research/intel/exp_38194362040_provision.py", "code"),
            artifact("research/intel/exp_38194362040_controls.py", "code"),
            artifact("research/intel/exp_38194362040_census.py", "code"),
            artifact("research/intel/exp_38194362040_comparators.py", "code"),
            artifact("research/intel/exp_38194362040_eval.py", "code"),
            artifact("research/intel/exp_38194362040_assemble.py", "code"),
        ],
        "raw_evidence": [
            artifact("research/experiments/EXP-INTEL-38194362040/raw/preflight.json", "raw"),
            artifact("research/experiments/EXP-INTEL-38194362040/raw/run_resources.json", "raw"),
            artifact("research/experiments/EXP-INTEL-38194362040/raw/controls.json", "raw"),
            artifact("research/experiments/EXP-INTEL-38194362040/raw/materialized_configs.json", "raw"),
            artifact("research/experiments/EXP-INTEL-38194362040/raw/provisioning_evidence.json", "raw"),
            artifact("research/experiments/EXP-INTEL-38194362040/raw/endpoint_census.json", "raw"),
            artifact("research/experiments/EXP-INTEL-38194362040/raw/external_comparators.json", "raw"),
            artifact("research/experiments/EXP-INTEL-38194362040/raw/decision.json", "derived"),
            artifact("research/experiments/EXP-INTEL-38194362040/cells/M-14B-QWEN/raw/harness_config.json", "fixture"),
            artifact("research/experiments/EXP-INTEL-38194362040/cells/M-14B-QWEN/raw/provisioning_receipt.json", "raw"),
            artifact("research/experiments/EXP-INTEL-38194362040/cells/M-14B-QWEN/raw/model_receipts.json", "raw"),
            artifact("research/experiments/EXP-INTEL-38194362040/cells/M-8B-LLAMA/raw/harness_config.json", "fixture"),
            artifact("research/experiments/EXP-INTEL-38194362040/cells/M-8B-LLAMA/raw/provisioning_receipt.json", "raw"),
            artifact("research/experiments/EXP-INTEL-38194362040/cells/M-8B-LLAMA/raw/model_receipts.json", "raw"),
        ],
        "notes": [
            "The GGUF bodies were downloaded to /tmp/opencode/gguf (ephemeral, outside the repo); their observed bytes/sha256/fingerprints are recorded in raw/provisioning_evidence.json.",
            "Content-identity repair succeeded: observed served-body sha256 equals the frozen served_body_sha256 pins (= HF tree-API lfs.oid), so the parent's metadata-vs-body mismatch did not recur.",
            "No hosted provider was invoked; the census is credential/reachability only (no API keys were present).",
        ],
    }
    for c in prov["candidates"]:
        provenance["models"][c["candidate_id"]] = {
            "frozen_url": c["frozen_url"],
            "revision_sha": c["revision_sha"],
            "pinned_sha256": c["pinned_sha256"],
            "pinned_bytes": c["pinned_bytes"],
            "observed_sha256": c["observed_sha256"],
            "observed_bytes": c["observed_bytes"],
            "identity_pass": c["identity_pass"],
            "n_download_attempts": c["n_download_attempts"],
            "local_path": c["local_path"],
        }
    with open(os.path.join(EXP, "provenance.json"), "w") as f:
        json.dump(provenance, f, indent=2, sort_keys=False)

    print("WROTE result.json and provenance.json")
    return 0


if __name__ == "__main__":
    sys.exit(main())
