# Research provider access: fail closed, zero paid tokens (12 Oct 2026)

## Observed incident

After PR #44, fresh GitHub Actions on 12 October 2026 reported:
- `opencode/big-pickle`: `Upstream request failed: Invalid credential`
  in several independent lane and Global Director jobs;
- `opencode/mimo-v2.5-free`: OpenCode `UnknownError / Unexpected server error`;
- `opencode/ling-3.0-flash-fin-free`: `Model is unavailable`.

These are **external provider/authentication failures**, not falsified
SPIDER hypotheses or ordinary code unit-test failures. A model ID ending
`-free` does not prove that the CI account can presently authenticate.

## Automated behavior

Before any new scientific dispatch the Factory executes
`scripts/probe_free_provider.py`, which submits at most three very short
prompts to **explicitly reviewed zero-price OpenCode models only**.
The probe agent has **no tools, no filesystem privileges, no browser
privileges, no ability to edit or read the repo**.

- A verified response: the normal Scout/Director/lanes may run.
- An authentication error, access-policy denial, timeout or unavailable
  pool: new work is **parked, not retried across six lanes**.
  No experiment is marked FAILED by this preflight.
- The structured `.spider-runtime/provider_preflight.json` receipt is
  uploaded in Factory artifacts with category and tried model IDs only.
  It contains **no API key, raw model output or research data**.
- Frozen packets remain immutable and the Codex remains intact.
- All agents continue to use the explicit `config/models.json` free
  allowlist. No auto-discovery, no paid substitution.

A green unit-test/CI run means the safeguards work. The **live provider
probe** must say `ready: true` before calling the research factory
**operational**. An Actions run shown as successful with
`SPIDER_PROVIDER_GATE_BLOCKED` is a *safe parked factory*, not a
completed science cycle.

## If the gate reports AUTH_INVALID

1. Verify your existing free-tier OpenCode credentials/provider access
   from the **official OpenCode account**. The provider may require
   a valid API key even for a model whose unit price is zero.
2. Ensure credentials are securely available to the GitHub runner
   through a supported provider mechanism. Do not commit keys or paste
   them in logs. Do not buy credits simply to quiet this health gate.
3. Run the next scheduled probe, or inspect the Factory run artifacts,
   before concluding that the CI environment can call free models.
4. Check upstream OpenCode client/provider status for
   `Invalid credential` affecting a current CLI version. A server-side
   error can persist with an apparently valid stored key.

If no genuinely free authenticated route can be made to work, **keep
scientific automation parked**. Improve local deterministic tests and
the existing Spider Product kernel without silently paying for inference.

## Product independence

The separate browser-pilot draft PR #42 is not made production-ready by
a restored research credential. It must independently pass an end-to-end
nontrivial task with a capable genuinely free agent, plus baseline and
safety/economics reviews.
