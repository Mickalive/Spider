# Report — EXP-PRODUCT-37385633334 (product, C-LLM-INHERIT)

## Outcome

`status=MEASUREMENT_INVALID`, `outcome=NOT_APPLICABLE`. The frozen readiness
certificate failed on all three checks, so the experiment terminated at the
gate exactly as the frozen decision rule requires. No arm executed.

## Readiness certificate (Gate 0)

1. **Model endpoint reachable — FAIL.** No model credentials
   (`OPENAI_API_KEY`, `ANTHROPIC_API_KEY` unset), no configured endpoint
   URL, no local model server listening (only DNS :53 and ssh :22), no
   programmatic access to any model. `config/models.json` lists only
   opencode free-model routing identities, which are not the frozen
   gpt-4o-mini and confer no endpoint.
2. **≥30 credential-free real-Web tasks with mechanical verifiers — FAIL.**
   No task bank or mechanical verifier is committed to this experiment's
   directory; prereg section 10 required it committed before freeze and it
   is absent.
3. **Accounting-fidelity control (PC-ACCOUNTING-FIDELITY) — FAIL.**
   `src/spider/kernel.py` (132 lines) implements observe/distill/resolve/
   verify/invalidate but contains no per-trajectory honest counters
   (`model_calls`, `model_tokens`, `browser_actions`, `http_requests`,
   `retrieval_calls`, `verification_calls`, `repair_attempts`,
   `latency_ms`); `playwright` and `httpx` are not installed; the seeded
   trajectory cannot run.

Raw certificate artifact:
`research/experiments/EXP-PRODUCT-37385633334/raw_readiness/readiness_certificate.json`
(sha256 `f87f51fdca39f07ae17cfbc99d83718f60226563c2b7fea642d357a1a906f737`).

## Metrics

All scientific metrics are `null` (not measured); zero model calls, zero
browser actions, zero HTTP/retrieval/verification/repair calls. This is not
a negative result about SPIDER's inheritance economics: the product thesis
was never tested because the required substrate is absent.

## Controls

- `PC-ACCOUNTING-FIDELITY`: not runnable (no counter instrumentation, no
  substrate).
- `NC-SHUFFLED-RETRIEVAL`, `B-COLD`, `B-INSTRUCTIONS`, `B-RETRIEVAL`,
  `A-SPIDER`: not evaluated — gate failed before arms.

## Hygiene obligation (recorded, done)

The mandatory non-experiment obligation — revert the committed four-file
1466-line insertion-variability kernel delta (`src/spider/variability.py`,
`tests/test_variability.py`, `src/spider/kernel.py`, `src/spider/models.py`)
per Automation invariant 13 — was verified complete at git commit
`39fcfd96f5eea0fe9a7d548f869428b617dedd08` (verdict commit of
EXP-PRODUCT-36314204238): the two new files are deleted, kernel.py/models.py
restored; current `src/spider/` holds only `__init__.py`, `kernel.py`,
`models.py`, `registry.py`; `tests/` holds only `test_kernel.py`.

## Interpretation

The readiness gate did its job: it converted missing substrate into a cheap,
honest early abort rather than an expensive invalid packet. The same three
blockers (model key, browser/Playwright, GHCR pull) are the recorded
blockers for C-LLM-INHERIT in `codex/claim_state.json`, so this packet
confirms they persist unchanged. The claim stays at HYPOTHESIS with zero
admissible evidence.

## Unresolved / smallest unblocking actions

Provision a model endpoint credential, install Playwright+httpx, implement
and demonstrate per-trajectory honest counters in `src/spider`, and commit
a frozen 30-task mechanical-verifier bank before any re-freeze.
