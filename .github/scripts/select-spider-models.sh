#!/usr/bin/env bash
set -euo pipefail
probe_root="${1:?probe root required}"
out="${2:-${RUNNER_TEMP:-/tmp}/spider-model-selection}"
mkdir -p "$out"
selection="$out/router.json"
mapfile -t probe_files < <(find "$probe_root" -type f -name probe.json -print | sort)
(( ${#probe_files[@]} > 0 )) || { echo "::error::No model probe files found" >&2; exit 64; }
healthy=(); responsive=()
for file in "${probe_files[@]}"; do
  if jq -e '.healthy==true' "$file" >/dev/null; then
    model=$(jq -r '.model' "$file"); elapsed=$(jq -r '.elapsedSeconds // 9999' "$file")
    healthy+=("$model")
    [[ "$elapsed" =~ ^[0-9]+$ ]] && (( elapsed <= 30 )) && responsive+=("$model")
  fi
done
healthy_count=${#healthy[@]}; responsive_count=${#responsive[@]}
contains(){ local n="$1"; shift; local x; for x in "$@"; do [[ "$x" == "$n" ]] && return 0; done; return 1; }
is_healthy(){ contains "$1" "${healthy[@]}"; }; is_responsive(){ contains "$1" "${responsive[@]}"; }
science_pref=(mimo-v2.5-free muse-spark-1.2-contributor-free hy3-free nemotron-3-ultra-free nemotron-3.5-lightning-free deepseek-v4-flash-free north-mini-code-free laguna-s-2.1-free ling-3.0-flash-free ling-3.0-tiny-free big-pickle x-preview-f-free)
science_audit_pref=(hy3-free muse-spark-1.2-contributor-free mimo-v2.5-free nemotron-3-ultra-free nemotron-3.5-lightning-free deepseek-v4-flash-free north-mini-code-free laguna-s-2.1-free ling-3.0-flash-free ling-3.0-tiny-free big-pickle x-preview-f-free)
coding_pref=(mimo-v2.5-free hy3-free muse-spark-1.2-contributor-free big-pickle nemotron-3-ultra-free nemotron-3.5-lightning-free deepseek-v4-flash-free north-mini-code-free laguna-s-2.1-free ling-3.0-flash-free ling-3.0-tiny-free x-preview-f-free)
coding_audit_pref=(hy3-free muse-spark-1.2-contributor-free mimo-v2.5-free nemotron-3-ultra-free nemotron-3.5-lightning-free deepseek-v4-flash-free north-mini-code-free laguna-s-2.1-free ling-3.0-flash-free ling-3.0-tiny-free big-pickle x-preview-f-free)
scout_pref=(muse-spark-1.2-contributor-free mimo-v2.5-free hy3-free deepseek-v4-flash-free nemotron-3-ultra-free nemotron-3.5-lightning-free north-mini-code-free laguna-s-2.1-free ling-3.0-flash-free ling-3.0-tiny-free big-pickle x-preview-f-free)
director_pref=(mimo-v2.5-free muse-spark-1.2-contributor-free hy3-free nemotron-3-ultra-free nemotron-3.5-lightning-free deepseek-v4-flash-free north-mini-code-free laguna-s-2.1-free ling-3.0-flash-free ling-3.0-tiny-free big-pickle x-preview-f-free)
architect_pref=(mimo-v2.5-free hy3-free muse-spark-1.2-contributor-free nemotron-3-ultra-free nemotron-3.5-lightning-free deepseek-v4-flash-free north-mini-code-free laguna-s-2.1-free ling-3.0-flash-free ling-3.0-tiny-free big-pickle x-preview-f-free)
curator_pref=(muse-spark-1.2-contributor-free hy3-free mimo-v2.5-free nemotron-3-ultra-free nemotron-3.5-lightning-free deepseek-v4-flash-free north-mini-code-free laguna-s-2.1-free ling-3.0-flash-free ling-3.0-tiny-free big-pickle x-preview-f-free)
general_pref=(mimo-v2.5-free hy3-free muse-spark-1.2-contributor-free nemotron-3-ultra-free nemotron-3.5-lightning-free deepseek-v4-flash-free north-mini-code-free laguna-s-2.1-free ling-3.0-flash-free ling-3.0-tiny-free big-pickle x-preview-f-free)
ranked(){ local prefname="$1"; shift; local -n pref="$prefname"; local tier c e bad; for tier in responsive healthy; do for c in "${pref[@]}"; do if [[ "$tier" == responsive ]]; then is_responsive "$c" || continue; else is_healthy "$c" || continue; fi; bad=false; for e in "$@"; do [[ -n "$e" && "$c" == "$e" ]] && bad=true; done; [[ "$bad" == false ]] && echo "$c"; done; done | awk '!seen[$0]++'; }
pick(){ local p="$1"; shift; local x; x=$(ranked "$p" "$@" | head -n1 || true); [[ -n "$x" ]] || x=$(ranked "$p" | head -n1 || true); printf '%s' "$x"; }
fb(){ local p="$1"; shift; (( healthy_count > 0 )) || { printf '[]'; return; }; ranked "$p" "$@" | jq -R . | jq -s .; }
science=$(pick science_pref); science_audit=$(pick science_audit_pref "$science"); coding=$(pick coding_pref); coding_audit=$(pick coding_audit_pref "$coding"); scout=$(pick scout_pref); director=$(pick director_pref); architect=$(pick architect_pref); curator=$(pick curator_pref); general=$(pick general_pref)
science_fb=$(fb science_pref); science_audit_fb=$(fb science_audit_pref "$science"); coding_fb=$(fb coding_pref); coding_audit_fb=$(fb coding_audit_pref "$coding"); scout_fb=$(fb scout_pref); director_fb=$(fb director_pref); architect_fb=$(fb architect_pref); curator_fb=$(fb curator_pref); general_fb=$(fb general_pref)
degraded=false; (( healthy_count >= 2 )) || degraded=true
jq -n --arg generatedAt "$(date -u +%Y-%m-%dT%H:%M:%SZ)" --arg sourceRunId "${GITHUB_RUN_ID:-local}" --argjson healthyCount "$healthy_count" --argjson responsiveCount "$responsive_count" --argjson degraded "$degraded" --arg science "$science" --arg scienceAudit "$science_audit" --arg coding "$coding" --arg codingAudit "$coding_audit" --arg scout "$scout" --arg director "$director" --arg architect "$architect" --arg curator "$curator" --arg general "$general" --argjson scienceFb "$science_fb" --argjson scienceAuditFb "$science_audit_fb" --argjson codingFb "$coding_fb" --argjson codingAuditFb "$coding_audit_fb" --argjson scoutFb "$scout_fb" --argjson directorFb "$director_fb" --argjson architectFb "$architect_fb" --argjson curatorFb "$curator_fb" --argjson generalFb "$general_fb" --slurpfile probes <(jq -s '.' "${probe_files[@]}") '{schemaVersion:2,generatedAt:$generatedAt,sourceRunId:$sourceRunId,healthProof:"real headless bash tool-call nonce round-trip",healthyCount:$healthyCount,responsiveCount:$responsiveCount,responsiveThresholdSeconds:30,independenceDegraded:$degraded,selectionBasis:{health:"empirical current-cycle tool probe",roleRanking:"SPIDER role prior; not a model-quality scientific claim",auditDiversity:"different producer/auditor model whenever >=2 healthy models permit"},selected:{science:$science,science_audit:$scienceAudit,coding:$coding,coding_audit:$codingAudit,scout:$scout,director:$director,architect:$architect,curator:$curator,general:$general},fallbacks:{science:$scienceFb,science_audit:$scienceAuditFb,coding:$codingFb,coding_audit:$codingAuditFb,scout:$scoutFb,director:$directorFb,architect:$architectFb,curator:$curatorFb,general:$generalFb},probes:$probes[0]}' > "$selection"
cat "$selection"
[[ -z "${GITHUB_OUTPUT:-}" ]] || { echo "healthy_count=$healthy_count" >> "$GITHUB_OUTPUT"; echo "responsive_count=$responsive_count" >> "$GITHUB_OUTPUT"; }
