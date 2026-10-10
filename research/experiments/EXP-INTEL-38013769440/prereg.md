# EXP-INTEL-38013769440 preregistration

Lane: `intel`. Claim: `C-LLM-INHERIT` (intel priority claim; director_mandate cycle `38013054267`, action `REOPEN`).
Status line: DESIGN v2 — preregistered before any confirmatory episode and before any model load.
This file is frozen together with `spec.json`; both are immutable after `freeze.json` exists.

## 1. Objective and the decision it can change

Readiness condition (3) of the four-arm `C-LLM-INHERIT` benchmark requires at least one credential-free,
CPU-quantized, same-model driver that can complete the minimal multi-step Web-agent task. The parent
experiment (`EXP-INTEL-37982024058`) produced a bounded FALSIFIES: under an underspecified system prompt
(no goal, no action-schema enumeration) Qwen2.5 3B/7B passed constrained-decoding positive controls 10/10
and step-1 parsing 5/5, yet failed the task 0/5 and 0/5, looping on a click of the now-hidden `#reveal-btn`.

This experiment asks the single decision-changing question named by the audit (`VF-01`):

> Does supplying the task **goal and action schema** in the system prompt convert the step-0 reveal-click
> into a full click-then-answer completion for the largest obtainable credential-free models — and if not,
> what is the demonstrable capability ceiling for the minimal Web-agent task across the credential-free
> endpoints and local models actually available to the factory?

Both outcomes change a program decision: a proven driver unblocks the flagship four-arm benchmark;
exhaustion licenses an explicit close/re-scope off the credential-free path. The mandate licenses both
directions, and both branches below are reachable.

## 2. Frozen task (byte-identical to the parent fixture)

The task HTML, GBNF grammar, user template, sampling and verifier are byte-identical to
`research/experiments/EXP-INTEL-37982024058/raw/harness_config.json`
(sha256 `7aba9dc899c40dd29f87b4265835eea6dc0b889c66271a983e4b82b8f5bc7adb`).

Task HTML (`task.page_html`):

```html
<!DOCTYPE html>
<html>
<body>
  <button id="reveal-btn">Reveal</button>
  <div id="target" style="display:none">TARGET-42</div>
  <script>
    document.getElementById('reveal-btn').onclick = () => {
      document.getElementById('target').style.display = 'block';
      document.getElementById('reveal-btn').style.display = 'none';
    };
  </script>
</body>
</html>
```

Success predicate (mechanical, unchanged): `clicked_reveal == True` AND `revealed_value == "TARGET-42"`
AND a final `answer` action whose text is exactly `"TARGET-42"`.

Constraint: **every episode of every arm — including every control — must navigate to the served task URL
before the episode begins.** This fixes the parent control bug (see §7).

GBNF grammar (`gbnf_grammar`, byte-for-byte from the fixture):

```
root ::= ws "{" ws "\"action\"" ws ":" ws action ws "," ws field ws "}" ws
ws ::= [ \t\n]*
action ::= "\"click\"" | "\"answer\""
field ::= "\"selector\"" ws ":" ws string | "\"text\"" ws ":" ws string
string ::= "\"" strchars "\""
strchars ::= strchar strchars | strchar
strchar ::= [^"\\] | "\\" (["\\/bfnrt] | "u" [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F] [0-9a-fA-F])
```

Sampling / runtime (frozen): `temperature=0.0`, `max_tokens=512`, `n_ctx=2048`, `llama_seed=42`,
`chat_format="qwen"`, episode seed `= 42 + episode_idx`, 5 episodes per arm, `n_threads=4`, CPU-only,
`llama-cpp-python==0.2.90` (primary; the identical build ran in the parent EXECUTE), Playwright 1.63.0
with `/usr/bin/google-chrome` (154.0.8037.97). User template (frozen):
`PAGE_TEXT: {page_text}\nELEMENTS: {elements_json}\nHISTORY: {history}\nNext action (JSON only): `.

## 3. Treatment and comparator (single frozen variable)

Both prompts are constructed by the harness from the frozen literals below with no discretion.

**PR-UNDERSPEC** (comparator; the parent `prompts.system` literal, verbatim):

```
You are a web agent. Reply with ONLY a valid JSON action per the schema. No prose, no reasoning, no markdown.
```

**PR-SPECIFIED** (treatment) is PR-UNDERSPEC with exactly one appended suffix:

```
 Actions available: {"action":"click","selector":"<css selector>"} or {"action":"answer","text":"<code>"}. Click the button to reveal the code, then answer it.
```

Thus `PR-SPECIFIED = PR-UNDERSPEC + " " + suffix`. The opening instruction sentence is **byte-identical**
across the two arms; the only difference is the presence of the action-schema enumeration and the goal
sentence. This removes the prior-design confound in which the opening instruction sentence also changed.
The schema keys `selector`/`text` match the frozen grammar. The goal sentence
`Click the button to reveal the code, then answer it.` is reproduced **verbatim** from the grand-parent
census `SYS` literal in `research/experiments/EXP-INTEL-37973264582/raw/code/min_webagent.py`
(sha256 `4e2b6710c78f4e4399a8ed5ae78e0231563fb832b780b80a955bcbc16b046862`); only the schema token
`ref`→`selector` and placeholder `<id>`→`<css selector>` are adapted to the frozen grammar.

**Leak guard (P2-BLIND-COMPOSITION):** neither prompt contains the substring `#reveal-btn` nor `TARGET-42`.
The treatment states the goal without naming the selector or the answer.

Component-wise isolation (schema-only vs goal-only) is out of scope for this packet; comparing the
goal+schema bundle against its no-goal/no-schema comparator is the preregistered single variable.

## 4. Candidates

Obtainable primary set `S_primary` (E-LOCAL-LLAMA, huggingface.co resolve-redirect GGUF):

| id | model | quant | bytes (live-verified at DESIGN) |
|----|-------|-------|---------------------------------|
| M-0.5B-QWEN | Qwen2.5-0.5B-Instruct | Q4_K_M | 491,400,032 |
| M-3B-QWEN | Qwen2.5-3B-Instruct | Q4_K_M | 2,104,932,768 |
| M-7B-QWEN | Qwen2.5-7B-Instruct | Q4_K_M | 3,993,201,344 + 689,872,288 (2 shards) |
| M-14B-QWEN | Qwen2.5-14B-Instruct | Q4_K_M | 3,991,999,872 + 3,989,373,504 + 1,006,737,120 (3 shards) |

Pinned sha256 (from `raw/gguf_sha256.txt`, census receipts): M-3B `626b4a66…15c62d`;
M-7B shard1 `dfce12e3…0580db`, shard2 `539cf93f…df3d72a`; M-0.5B `74a4da8c…d7a9db`.
M-14B shas and the probe shas are recomputed at download. A shard hash/size mismatch is `NOT_MEASURED`
with reason `SHA-MISMATCH`, never a substitution.

`M-14B-QWEN` joins `S_primary` iff all shards download with the pinned content-lengths AND available RAM
`>= 11 GiB` at load time; otherwise it is `NOT_IN_OBTAINABLE_SET` (reason RAM/PROVISIONING). Qwen2.5-32B
Q4_K_M (~18.49 GiB weights; first shard 3,961,498,272 B, HTTP-verified at DESIGN) and 72B exceed the
runner's ~16 GiB RAM and are `NOT_IN_OBTAINABLE_SET` by the same pre-declared memory definition; the
E-LOCAL-LLAMA runnable range ends at 14B.

**Architecture-diversity probe (secondary, non-gating):** `M-LLAMA-3.2-3B` (Q4_K_M, 2,019,377,696 B,
same ~3B size class as M-3B-QWEN), to separate a Qwen-specific ceiling from a small-model ceiling. Gated
on the frozen runtime exposing a usable chat template; if not, `NOT_MEASURED-RUNTIME`, never a negative.
Its result is reported as generalization evidence and does not change the primary decision.

Other reachable-but-not-measured GGUFs (declared scope boundary, not an availability claim):
Llama-3.1-8B (4,920,739,232 B), Gemma-2-2B (1,708,582,752 B), Gemma-2-9B (5,761,057,728 B),
Phi-3.5-mini (2,393,232,672 B) — all HTTP-verified live at DESIGN via the same route.

## 5. Arms per candidate

Per candidate, in order: `PC-JSON-CONSTRAINED-DECODING` (10/10) → `PR-UNDERSPEC` (5 episodes) →
`PR-SPECIFIED` (5 episodes). PR-UNDERSPEC is run for M-7B-QWEN and M-3B-QWEN (the two parent models) and
for M-LLAMA-3.2-3B if measured; M-14B-QWEN and M-0.5B-QWEN run PR-SPECIFIED only, after PC.
`PC-SCRIPTED-ORACLE` runs once before any model episode.

## 6. Controls (frozen ids)

- **PC-SCRIPTED-ORACLE** (positive ceiling, 5/5): a non-model policy clicks `#reveal-btn` then answers
  `TARGET-42` through the identical pipeline. `< 5/5` ⇒ `MEASUREMENT_INVALID`.
- **PC-JSON-CONSTRAINED-DECODING** (positive, 10/10 per candidate): isolates decoding from reasoning.
  A candidate failing this is `NOT_MEASURED-PC-FAIL`; both 7B and 3B failing ⇒ `MEASUREMENT_INVALID`.
- **NC-NO-MODEL-ACTION** (null, 0 parseable / 0 success on the loaded page): verifier rejects non-actions.
- **B-RANDOM-ACTION** (null, chance floor): per-step uniform draw from the fixture `action_space`
  (`click #reveal-btn`, `answer TARGET-41`, `answer TARGET-42`, `answer TARGET-43`, `answer unknown`),
  base_seed 42, on the loaded page. This is the **true parent semantics** (`make_random_producer` draws
  `rng.choice` at every step). Analytical per-episode success `= r/(1-q) = (1/5)/(4/5) = 0.25`, so the
  probability of clearing the ≥3/5 bar by chance is ≈0.104; the realized value is reported as the floor.
  Guard: if B-RANDOM clears the bar, a clearing model must reach `task_success_rate ≥ 0.8` to count.
- **B-ANSWER-NO-REVEAL** (null, floor-exact): deterministically emits `answer TARGET-42` without clicking,
  5 episodes; `0/5` success with `5/5` parseable. `> 0/5` success ⇒ `MEASUREMENT_INVALID`.
- **CV-UNDERSPEC-REPLICATION** (continuity): for each of M-7B-QWEN, M-3B-QWEN under PR-UNDERSPEC,
  PASS iff `task_success_rate == 0/5` AND `step0_reveal_click_rate ≥ 0.8` AND `loop_signature_rate ≥ 0.2`
  AND `parseable_action_rate_step1 ≥ 0.8`. Any deviation ⇒ `REPLICATION-DEVIATION` ⇒ `MEASUREMENT_INVALID`.

## 7. Corrections relative to the parent and prior attempt

1. **Parent control bug (verified from `raw/control_episodes.json`).** `mode_null_random` created the page
   but never called `page.goto`, and `run_episode` reloads `page.url` (= `about:blank`). Every B-RANDOM
   click recorded `click_ok=False` and `final_target_visible=False`. The parent's "B-RANDOM 5/5 valid JSON,
   0/5 success" is therefore **not** a valid chance bound. This experiment runs NC and B-RANDOM on the
   loaded task page, records the realized random floor, and adds the floor-exact `B-ANSWER-NO-REVEAL`.
2. **B-RANDOM semantics.** The prior attempt redefined B-RANDOM as one action per episode and attributed
   that to the parent. The parent samples uniformly **per step**; this prereg restores the true semantics
   and documents the resulting ~0.25 per-episode chance level and its bar-clearing guard.
3. **Treatment identity.** PR-SPECIFIED is now a strict suffix append to the byte-identical PR-UNDERSPEC
   opening sentence, removing the prior confound in which the opening instruction also changed.
4. **Non-Qwen obtainability.** The prior attempt claimed non-Qwen models were "not obtainable"; they are
   reachable via the same resolve route (verified live). They are now an explicit bounded-scope boundary,
   plus one same-size cross-architecture probe.

## 8. Decision rule

**Bar (parent-comparable):** `parseable_action_rate_step1 ≥ 0.6` AND `task_success_rate ≥ 0.6` over the
5-episode PR-SPECIFIED arm (≥ 3/5 both). Ordered evaluation:

1. `PC-SCRIPTED-ORACLE != 5/5` ⇒ `MEASUREMENT_INVALID`; `B-ANSWER-NO-REVEAL != 0/5` success ⇒
   `MEASUREMENT_INVALID`; `NC-NO-MODEL-ACTION != 0` parseable ⇒ `MEASUREMENT_INVALID`;
   PC-JSON failing on both 7B and 3B ⇒ `MEASUREMENT_INVALID`.
2. `CV-UNDERSPEC-REPLICATION` must PASS (§6), else `MEASUREMENT_INVALID`.
3. **SUPPORTS** iff some `S_primary` model clears the bar (applying the B-RANDOM guard); record the driver
   id and shard hashes.
4. **FALSIFIES** iff all gates pass and every `S_primary` model is measured under PR-SPECIFIED and fails
   the bar. M-14B is either in `S_primary` and measured, or excluded by the pre-declared availability
   definition, so `S_primary` is always fully measurable when downloads succeed.
5. **MIXED** iff an `S_primary` model is unresolved for a non-capability reason while none clears.

`NOT_ATTEMPTED`, `NOT_IN_OBTAINABLE_SET`, `NOT_MEASURED` and infrastructure failures are census/operational
records, never scientific negatives; infrastructure failure is `MEASUREMENT_INVALID`, never FALSIFIES.

## 9. Validity threats

- **Low-`n` / deterministic protocol.** temp=0 and fixed seeds make traces near-duplicates; the 5-episode
  unit is an adequacy rule, not a variance estimate (inherited `VF-03`). Reported as counts, not p-values.
- **Chance floor.** The parent bar's per-step chance-clearing probability is ≈0.104; the B-RANDOM guard and
  the floor-exact control bound this, but the bar remains weak for stochastic policies.
- **Representation loss.** The observation truncates body text to 300 chars and element text to 40 chars
  (frozen from the parent). After reveal, `TARGET-42` appears in `PAGE_TEXT`; this was acknowledged in the
  parent and does not by itself explain the loop.
- **Prompt-arm asymmetry.** M-14B-QWEN and M-0.5B-QWEN are run under PR-SPECIFIED only, so their success is
  a capability result; the statement that the *prompt* converts the click rests on the 7B/3B
  `CV-UNDERSPEC-REPLICATION`. The two largest/smallest arms are therefore ceiling tests, not conversion
  attribution.
- **Runtime/chattemplate for non-Qwen.** The M-LLAMA-3.2-3B probe may be unavailable under the frozen
  runtime; it is then `NOT_MEASURED-RUNTIME`, and the Qwen-family result still stands as a bounded ceiling.
- **Scope.** Bounds only this minimal two-step synthetic task, these frozen prompts, this sampling and the
  measured credential-free candidates. No generalization to arbitrary multi-step web tasks.
- **External check is context only.** The published-envelope anchors (WebArena peer-reviewed: GPT-4 14.41%,
  human 78.24%; non-peer-reviewed vendor/community tool-calling snapshots) cannot alter the primary outcome.

## 10. Consequences

- **Positive (SUPPORTS):** readiness condition (3) is satisfied by a proven credential-free same-model
  driver; the four-arm `C-LLM-INHERIT` benchmark becomes executable as frozen; `C-LLM-INHERIT` advances
  from HYPOTHESIS toward EXPERIMENTAL (DIRECTOR decision).
- **Negative (FALSIFIES/MIXED):** readiness condition (3) is demonstrated not satisfiable on the
  credential-free path up to the measured ceiling; `C-LLM-INHERIT` must be re-scoped off it (drop Gate 3's
  same-model external anchor; internally re-run comparators on a task bank with demonstrable dynamic range,
  since readiness condition (2) / the mandate's B2 is also open). No credential-free endpoint is promoted
  into Product Core.

## 11. Relationship to pre-2.0 precedent

This is not a pre-2.0 replay and not a repeat of the prior invalid design. It is a controlled, within-
experiment prompt ablation with an in-experiment continuity replication, corrected controls, a floor-exact
null, a verifier-ceiling control, and a declared closest-model boundary — sufficient to convert the parent
bounded FALSIFIES into an identifiability-safe determination of readiness condition (3).
