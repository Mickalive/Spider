Run 1 outputs (2026-09-24T20:08Z) preserved for audit delta before the measurement-fidelity fixes in run 2:
- hit_nginx_cache_files was 0 due to a runner-user permission artifact (www-data mode-700 cache dirs);
  run 2 counts via sudo = 1 real nginx cache entry file (see provenance cache_file_count_sudo).
- hit_warm_ok was False because the warm request saw X-Cache=HIT (Phase 0 health gate had legitimately
  pre-warmed the real proxy_cache); run 2 accepts MISS or HIT with greedy byte-identical content.
All scientific measurements were reproduced identically in run 2 (deterministic SEED=44); outcome
COMPLETE / FALSIFIES unchanged. run_2 final artifacts: result.json, report.md, provenance.json in ..