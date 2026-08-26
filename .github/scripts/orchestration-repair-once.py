from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, got {n}")
    return text.replace(old, new, 1)


# 1) Frontier: exact file-level scope checks; historical one-shot is charter-local;
# incomplete auditor invocations are resumed as the SAME audit, never a new experiment.
p = Path('.github/workflows/frontier-research.yml')
t = p.read_text()
n = t.count('git status --porcelain')
if n < 3:
    raise SystemExit(f'frontier scope hardening: expected >=3 porcelain checks, got {n}')
t = t.replace('git status --porcelain', 'git status --porcelain -uall')

old = '''          cp /tmp/frontier_charter.json "frontier/$TEAM_ID/charters/cto_v${CHARTER_VERSION}.json"

      - name: Checkout rejected snapshot for same-cycle repair'''
new = '''          cp /tmp/frontier_charter.json "frontier/$TEAM_ID/charters/cto_v${CHARTER_VERSION}.json"

          # A human one-shot lock belongs ONLY to the exact charter being executed.
          # Never let an old historical one-shot silently contaminate a later normal CTO charter.
          mkdir -p "directives/frontier" "state/frontier"
          if [[ "$ONE_SHOT" == "true" ]]; then
            printf '# Frontier %s local directive\\n\\nHUMAN-FORCED ONE-SHOT FOR CURRENT CHARTER v%s ONLY. Execute exactly one TEAM→AUDIT cycle. No automatic repair or continuation for this charter. Preserve negative results and provenance. This lock MUST NOT be inherited by any later normal CTO charter.\\n' "$TEAM_ID" "$CHARTER_VERSION" > "directives/frontier/${TEAM_ID}.md"
            if [[ -f "state/frontier/${TEAM_ID}.json" ]]; then
              jq '.one_shot=true | .human_forced_one_shot=true | .current_charter_one_shot=true | .auto_continue_allowed=false | .continue_recommended=false' "state/frontier/${TEAM_ID}.json" > /tmp/frontier_lifecycle.json
              mv /tmp/frontier_lifecycle.json "state/frontier/${TEAM_ID}.json"
            fi
          else
            printf '# Frontier %s local directive\\n\\nNORMAL CTO-CHARTERED FRONTIER CYCLE v%s. Execute the exact current CTO charter under the elastic V3 lifecycle. Historical human one-shot locks from older charter versions do not apply. Preserve all prior evidence and claim ceilings.\\n' "$TEAM_ID" "$CHARTER_VERSION" > "directives/frontier/${TEAM_ID}.md"
            if [[ -f "state/frontier/${TEAM_ID}.json" ]]; then
              jq '.one_shot=false | .human_forced_one_shot=false | .current_charter_one_shot=false | .auto_continue_allowed=true' "state/frontier/${TEAM_ID}.json" > /tmp/frontier_lifecycle.json
              mv /tmp/frontier_lifecycle.json "state/frontier/${TEAM_ID}.json"
            fi
          fi

      - name: Checkout rejected snapshot for same-cycle repair'''
t = replace_once(t, old, new, 'frontier charter-local one-shot reset')

marker = '''      - name: Enforce audit-only writes
'''
recovery = '''      - name: Recover an incomplete Frontier audit invocation
        shell: bash
        env:
          TEAM_ID: ${{ inputs.team_id }}
        run: |
          set -euo pipefail
          GATE="results/audit/CYCLE_${GITHUB_RUN_ID}_FRONTIER_${TEAM_ID}_GATE.json"
          REPORT="reports/audit/CYCLE_${GITHUB_RUN_ID}_FRONTIER_${TEAM_ID}.md"
          if [[ ! -s "$GATE" || ! -s "$REPORT" ]]; then
            echo "::warning::Auditor invocation returned without mandatory deliverables; resuming the SAME audit on the SAME frozen team snapshot. No team experiment is rerun."
            bash /tmp/spider_control/run-opencode-with-retry.sh run \\
              --model "$SPIDER_MODEL" \\
              --agent frontier_research_auditor \\
              "RESUME THE SAME INDEPENDENT AUDIT for Frontier team ${TEAM_ID}, charter v${{ inputs.charter_version }}, GitHub run ${GITHUB_RUN_ID}, repair ${{ inputs.repair_round }}. The prior auditor invocation returned without both mandatory deliverables. Do NOT rerun or modify the TEAM experiment. Do NOT create secondary scratch worktrees. Read TEAM directly at /tmp/spider_frontier_team and charter at /tmp/frontier_charter.json. Current checkout is the accepted audit base and you may write ONLY reports/audit/ and results/audit/. Finish the audit and MUST write exactly ${REPORT} plus ${GATE} with gate PASS, REVISE, or BLOCKED, safe_to_integrate, required_fixes, evidence/limitations and honest claim ceiling."
          fi
          test -s "$REPORT" || { echo "::error::Frontier auditor still omitted mandatory report after same-audit recovery"; exit 1; }
          test -s "$GATE" || { echo "::error::Frontier auditor still omitted mandatory gate after same-audit recovery"; exit 1; }

'''
t = replace_once(t, marker, recovery + marker, 'frontier mandatory audit recovery')

marker = '''      - name: Enforce Frontier Director scope
'''
unlock = '''      - name: Clear historical one-shot lock after normal CTO integration
        if: ${{ inputs.one_shot != true }}
        shell: bash
        env:
          TEAM_ID: ${{ inputs.team_id }}
        run: |
          set -euo pipefail
          F="state/frontier/${TEAM_ID}.json"
          test -f "$F" || { echo "::error::Missing Frontier state after normal Director integration"; exit 1; }
          jq '.one_shot=false | .human_forced_one_shot=false | .current_charter_one_shot=false | .auto_continue_allowed=true' "$F" > /tmp/frontier_state.normal.json
          mv /tmp/frontier_state.normal.json "$F"

'''
t = replace_once(t, marker, unlock + marker, 'frontier normal lifecycle unlock')
p.write_text(t)

# 2) Product: preserve durable request history while proving any launch request is fresh.
p = Path('.github/workflows/product-loop.yml')
t = p.read_text()
old = '''      - name: Clear ephemeral launch state before fresh Product decision
        shell: bash
        run: |
          rm -f state/product_beta_request.json
          if [[ -f state/product_direction.json ]]; then
            jq '.beta_launch=false' state/product_direction.json > /tmp/product_direction.json
            mv /tmp/product_direction.json state/product_direction.json
          fi
'''
new = '''      - name: Snapshot prior Product request and clear only the ephemeral launch decision
        shell: bash
        run: |
          PRE_SHA=""
          if [[ -f state/product_beta_request.json ]]; then
            PRE_SHA=$(sha256sum state/product_beta_request.json | awk '{print $1}')
          fi
          echo "PRODUCT_REQUEST_PRE_SHA=$PRE_SHA" >> "$GITHUB_ENV"
          if [[ -f state/product_direction.json ]]; then
            jq '.beta_launch=false' state/product_direction.json > /tmp/product_direction.json
            mv /tmp/product_direction.json state/product_direction.json
          fi
'''
t = replace_once(t, old, new, 'product durable request preservation')
old = '''            test -f state/product_beta_request.json || { echo "::error::beta_launch requires a fresh product_beta_request"; exit 1; }
            BETA=$(jq -r '.beta_id // empty' state/product_beta_request.json)
            test -n "$BETA" || exit 1
'''
new = '''            test -f state/product_beta_request.json || { echo "::error::beta_launch requires a product_beta_request"; exit 1; }
            CURRENT_SHA=$(sha256sum state/product_beta_request.json | awk '{print $1}')
            if [[ -n "${PRODUCT_REQUEST_PRE_SHA:-}" && "$CURRENT_SHA" == "$PRODUCT_REQUEST_PRE_SHA" ]]; then
              echo "::error::beta_launch requires a freshly changed request; refusing stale durable authorization"
              exit 1
            fi
            BETA=$(jq -r '.beta_id // empty' state/product_beta_request.json)
            test -n "$BETA" || exit 1
'''
t = replace_once(t, old, new, 'product fresh request proof')
p.write_text(t)

# 3) Governance: historical human one-shot is not hereditary by team_id/domain.
p = Path('docs/roles/CHIEF_CTO.md')
t = p.read_text()
anchor = '''Les charters doivent être réellement distincts. Plusieurs équipes ne doivent pas simplement tester la même hypothèse sur le même instrument avec des formulations différentes.
'''
addition = '''Les charters doivent être réellement distincts. Plusieurs équipes ne doivent pas simplement tester la même hypothèse sur le même instrument avec des formulations différentes.

### Portée des one-shots humains

Un `one_shot` humain est une propriété **locale de l'instance exacte de charter** qui l'autorise (au minimum `team_id` + `charter_version` + provenance d'autorité). Il n'est JAMAIS héréditaire au `team_id`, au domaine scientifique, ni à un futur charter CTO normal.

Le lot historique `HISTORICAL_CTO25_ONE_SHOT_2026-08-26` devait exécuter une fois les six charters de récupération puis s'arrêter : aucune réparation, continuation ou répétition automatique de CES charters n'est autorisée. En revanche, un futur charter CTO normal et matériellement distinct relève à nouveau du cycle élastique V3 et ne doit pas recopier `ONE-CYCLE DISCIPLINE`, `one_shot=true` ou `auto_continue_allowed=false` depuis l'historique, sauf **nouvelle autorisation humaine explicite** visant ce nouveau charter.

Le CTO doit donc distinguer : **arrêt du charter one-shot consommé** ≠ **verrou permanent du domaine ou de l'identité d'équipe**.
'''
t = replace_once(t, anchor, addition, 'CTO one-shot scope rule')
p.write_text(t)

p = Path('.opencode/agents/chief_cto.md')
t = p.read_text()
anchor = '''When an important question is uncovered and does not belong cleanly inside an existing lane, write a complete machine-readable Frontier charter in `state/cto_direction.json.research_portfolio.frontier_team_charters`. You may create multiple independent teams in parallel. Use CREATE for a new team, CONTINUE with a higher charter_version when an accepted Frontier team deserves another materially distinct cycle, and PAUSE/TERMINATE/MERGE when appropriate.
'''
addition = anchor + '''
A human `one_shot` applies only to the exact charter instance that carries that human authorization. Never inherit a historical one-shot lock into a later normal CTO charter merely because the `team_id` or research topic is reused. Historical one-shot recovery charters stop after their one cycle; later materially distinct normal charters return to the elastic V3 lifecycle unless a fresh human authorization explicitly makes them one-shot too.
'''
t = replace_once(t, anchor, addition, 'chief CTO agent one-shot scope')
p.write_text(t)
