# SPIDER Actions Run Archive

This directory is the durable index for GitHub Actions runs whose raw Actions history may eventually be deleted.

## Non-negotiable invariant

**NO ACTIONS RUN MAY BE DELETED BEFORE ITS DATA IS SAFE ELSEWHERE.**

A completed substantive run is deletable only when BOTH independent conditions are true:

1. **Lossless Actions archive complete**
   - `evidence/run-archive/manifests/<run_id>.json` exists;
   - raw GitHub Actions log ZIP is archived;
   - every still-downloadable GitHub Actions artifact is archived as its raw ZIP, or the run had none;
   - every branch/tag ref containing the run id is captured in a verified Git bundle, or there were none;
   - the complete archive is stored as a checksum-verified asset on repository Release `spider-actions-data-archive-v1`;
   - `archive_complete=true` and `actions_payload_complete=true`.

2. **Semantic/data integration complete**
   - `evidence/run-memory/runs/<run_id>.json` exists on `main`;
   - `distillation_complete=true`;
   - useful results, negatives, anomalies, costs, limits, provenance and research/product implications have been integrated into durable SPIDER memory at their exact epistemic status;
   - aggregated feeds/indexes are rebuilt from the durable records.

`repo-hygiene.yml` enforces both gates mechanically. A historical `safe_to_prune=true` flag by itself is never sufficient.

## Storage model

Large raw payloads do **not** live in the normal Git working tree because doing so would bloat every clone. They live as immutable-by-checksum repository Release assets:

`run-<run_id>.tar.gz`

Each bundle contains the original run metadata, job metadata, raw Actions logs ZIP, artifact metadata and raw artifact ZIPs, related Git refs/bundle, readable logs when available, checksums, and the semantic record as it existed at archive time when one already existed.

The Git repository keeps the compact durable control plane:

- `manifests/<run_id>.json` — per-run archive proof;
- `DATA_CATALOG.json` — machine-readable inventory of archived substantive runs;
- `../run-memory/runs/<run_id>.json` — semantic distillation;
- `../run-memory/INDEX.md`, `CTO_FEED.json`, `PRODUCT_FEED.json` — accumulated knowledge routed to downstream teams.

## Failure rule

If raw logs or a still-listed artifact cannot be downloaded, checksum verification fails, a Git bundle cannot be verified, or semantic distillation is missing, the run stays in GitHub Actions. The migration must report the blocker; it must never delete around it.
