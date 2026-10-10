# SPIDER — one cumulative Codex

`SPIDER_CODEX.md` is the single human-readable scientific entry point. `codex/index.json` is the single machine-readable catalog, spanning **the original research and its Research 2.0 continuation**.

- `index.json.historical.artifacts`: 1,401 unique original source artifacts with original path, lane, role, SHA and exact line interval in the byte-identical evidence source `codex/sources/0000-historical-evidence.md`. These are NOT 1,401 independent experiments.
- `index.json.experiments`: subsequently finalized, independently audited experiment packets at `codex/experiments/<experiment_id>/`.
- `claim_state.json.historical_precedents_by_claim`: bounded prior evidence associated with the same ten claims whose later, audited events are in `events_by_claim`. Historical tags never automatically promote a claim.

The source historical Git blob `9bb76113aeaf46d9aecdd8a38349a3a7741e57c3` is also retained untouched on `archive/spider-codex-ultimate`.

`scripts/sync_codex.py` verifies the original historical blob and artifact inventory before regenerating this **one cumulative catalog**, ensuring later synchronized experiments do not erase the first era.
