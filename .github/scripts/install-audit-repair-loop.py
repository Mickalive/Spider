from pathlib import Path
import re


def replace_once(text: str, old: str, new: str, label: str) -> str:
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 match, found {count}")
    return text.replace(old, new, 1)


def replace_regex_once(text: str, pattern: str, replacement: str, label: str) -> str:
    out, count = re.subn(pattern, replacement, text, count=1, flags=re.S)
    if count != 1:
        raise SystemExit(f"{label}: expected exactly 1 regex match, found {count}")
    return out


def patch_graph(path: Path):
    text = path.read_text()

    inputs_old = '''      max_cycles:\n        description: "Optional numeric cap; 0 = continue until Lane Director stops"\n        required: false\n        type: number\n        default: 0\n'''
    inputs_new = inputs_old + '''      repair_from_run_id:\n        description: "Prior rejected Graph run to repair; empty = fresh scientific cycle"\n        required: false\n        type: string\n        default: ""\n      repair_round:\n        description: "Same-cycle audit repair round; provenance only, no arbitrary cap"\n        required: false\n        type: number\n        default: 0\n'''
    text = replace_once(text, inputs_old, inputs_new, 'graph inputs')

    checkout_old = '''      - name: Checkout or initialize accepted Graph lane\n        shell: bash\n        run: |\n          if git ls-remote --exit-code --heads origin "refs/heads/$LANE_BRANCH" >/dev/null 2>&1; then\n            git fetch origin "$LANE_BRANCH"\n            git switch -C "$LANE_BRANCH" "origin/$LANE_BRANCH"\n          else\n            git switch -C "$LANE_BRANCH"\n            git push origin "HEAD:refs/heads/$LANE_BRANCH"\n          fi\n'''
    checkout_new = '''      - name: Checkout or initialize accepted Graph lane\n        if: ${{ inputs.repair_from_run_id == '' }}\n        shell: bash\n        run: |\n          if git ls-remote --exit-code --heads origin "refs/heads/$LANE_BRANCH" >/dev/null 2>&1; then\n            git fetch origin "$LANE_BRANCH"\n            git switch -C "$LANE_BRANCH" "origin/$LANE_BRANCH"\n          else\n            git switch -C "$LANE_BRANCH"\n            git push origin "HEAD:refs/heads/$LANE_BRANCH"\n          fi\n\n      - name: Checkout rejected Graph snapshot and audit for repair\n        if: ${{ inputs.repair_from_run_id != '' }}\n        shell: bash\n        run: |\n          SOURCE_TEAM="cycle/graph/${{ inputs.repair_from_run_id }}/team"\n          SOURCE_AUDIT="cycle/graph/${{ inputs.repair_from_run_id }}/audit"\n          git fetch origin "$SOURCE_TEAM:refs/remotes/origin/$SOURCE_TEAM"\n          git fetch origin "$SOURCE_AUDIT:refs/remotes/origin/$SOURCE_AUDIT"\n          git switch -C graph-repair-base "origin/$SOURCE_TEAM"\n          git worktree add --detach /tmp/spider_graph_repair_audit "origin/$SOURCE_AUDIT"\n'''
    text = replace_once(text, checkout_old, checkout_new, 'graph checkout')

    team_pattern = r'''      - name: Run TEAM GRAPH\n.*?(?=      - name: Enforce Graph scope\n)'''
    team_new = '''      - name: Run TEAM GRAPH — fresh scientific cycle\n        if: ${{ inputs.repair_from_run_id == '' }}\n        env:\n          HUMAN_NOTE: ${{ inputs.human_note }}\n        shell: bash\n        run: |\n          opencode run \\\n            --model "$SPIDER_MODEL" \\\n            --agent graph_runner \\\n            "Run Graph lane cycle ${{ inputs.cycle_index }} (GitHub run ${GITHUB_RUN_ID}). Read SPIDER_MASTER_PROMPT.md, directives/GRAPH.md, directives/AUDITOR_GRAPH.md, docs/NEXT_GRAPH.md, docs/GRAPH_LEDGER.md and relevant accepted Graph evidence. Do real empirical work. Do not work on Physics. Do not edit SPIDER_MASTER_PROMPT.md or workflows. Never ask for interactive approval. Human steering note, subordinate to the constitution: ${HUMAN_NOTE}"\n\n      - name: Run TEAM GRAPH — repair audited defects\n        if: ${{ inputs.repair_from_run_id != '' }}\n        env:\n          HUMAN_NOTE: ${{ inputs.human_note }}\n        shell: bash\n        run: |\n          opencode run \\\n            --model "$SPIDER_MODEL" \\\n            --agent graph_runner \\\n            "REPAIR Graph lane cycle ${{ inputs.cycle_index }}, repair round ${{ inputs.repair_round }} (GitHub run ${GITHUB_RUN_ID}). The current checkout is the exact rejected team snapshot from run ${{ inputs.repair_from_run_id }}. The independent audit workspace is /tmp/spider_graph_repair_audit. Read SPIDER_MASTER_PROMPT.md, directives/GRAPH.md, directives/AUDITOR.md, directives/AUDITOR_GRAPH.md, the prior audit report and its *_GRAPH_GATE.json. Fix EVERY item in required_fixes concretely, rerun every affected test/experiment, and preserve the rejected attempt as provenance. Do not evade the audit by weakening tests, changing targets post hoc without labeling them exploratory, deleting contrary evidence, or merely rewriting claims when the defect is in code/measurement. Do not work on Physics or workflows. Human note: ${HUMAN_NOTE}"\n\n'''
    text = replace_regex_once(text, team_pattern, team_new, 'graph team steps')

    audit_header_old = '''  audit_graph:\n    name: INDEPENDENT AUDITOR — GRAPH\n    needs: [team_graph]\n    if: needs.team_graph.result == 'success'\n    runs-on: ubuntu-latest\n    timeout-minutes: 240\n'''
    audit_header_new = audit_header_old + '''    outputs:\n      gate: ${{ steps.audit_gate.outputs.gate }}\n      safe_to_integrate: ${{ steps.audit_gate.outputs.safe_to_integrate }}\n'''
    text = replace_once(text, audit_header_old, audit_header_new, 'graph audit outputs')

    audit_pattern = r'''      - name: Audit Graph immediately\n.*?(?=      - name: Enforce audit-only writes\n)'''
    audit_new = '''      - name: Audit Graph immediately\n        shell: bash\n        run: |\n          opencode run \\\n            --model "$SPIDER_MODEL" \\\n            --agent independent_auditor \\\n            "Audit Graph lane cycle ${{ inputs.cycle_index }} (GitHub run ${GITHUB_RUN_ID}), repair round ${{ inputs.repair_round }}. Completed team workspace: /tmp/spider_graph_team. Current checkout is the untouched accepted Graph base and is where you may write ONLY audit outputs. Read SPIDER_MASTER_PROMPT.md, directives/AUDITOR.md and directives/AUDITOR_GRAPH.md. Recompute claims and attack leakage, hand-coded decomposition, mismatched timing, weak baselines, denominator tricks, retrieval cost and transfer claims. Write reports/audit/CYCLE_${GITHUB_RUN_ID}_GRAPH.md AND mandatory results/audit/CYCLE_${GITHUB_RUN_ID}_GRAPH_GATE.json with gate PASS, REVISE, or BLOCKED and exact required_fixes. A valid negative/null/downgraded result may PASS. Use REVISE only for concrete same-cycle repairable defects and BLOCKED when another repair would be dishonest/repetitive or requires unavailable data/external decision. Do not edit team files, workflows or constitution."\n\n'''
    text = replace_regex_once(text, audit_pattern, audit_new, 'graph audit prompt')

    gate_step = '''      - name: Validate Graph audit integration gate\n        id: audit_gate\n        shell: bash\n        run: |\n          FILE="results/audit/CYCLE_${GITHUB_RUN_ID}_GRAPH_GATE.json"\n          test -f "$FILE" || { echo "::error::Auditor omitted mandatory Graph gate file"; exit 1; }\n          GATE=$(jq -r '.gate // empty' "$FILE")\n          SAFE=$(jq -r '.safe_to_integrate // false' "$FILE")\n          case "$GATE" in\n            PASS)\n              [ "$SAFE" = "true" ] || { echo "::error::PASS requires safe_to_integrate=true"; exit 1; }\n              ;;\n            REVISE)\n              [ "$SAFE" = "false" ] || { echo "::error::REVISE requires safe_to_integrate=false"; exit 1; }\n              FIXES=$(jq '.required_fixes | if type == "array" then length else 0 end' "$FILE")\n              [ "$FIXES" -gt 0 ] || { echo "::error::REVISE requires actionable required_fixes"; exit 1; }\n              ;;\n            BLOCKED)\n              [ "$SAFE" = "false" ] || { echo "::error::BLOCKED requires safe_to_integrate=false"; exit 1; }\n              ;;\n            *) echo "::error::Invalid Graph audit gate: $GATE"; exit 1 ;;\n          esac\n          echo "gate=$GATE" >> "$GITHUB_OUTPUT"\n          echo "safe_to_integrate=$SAFE" >> "$GITHUB_OUTPUT"\n          echo "Graph audit gate=$GATE safe=$SAFE"\n\n'''
    marker = '      - name: Persist Graph audit branch\n'
    text = replace_once(text, marker, gate_step + marker, 'graph gate parser')

    director_if_old = "    if: needs.audit_graph.result == 'success'\n"
    director_if_new = "    if: needs.audit_graph.result == 'success' && needs.audit_graph.outputs.gate == 'PASS'\n"
    # Only director currently has this exact line after audit header was already handled? audit header has team condition.
    # Assert one occurrence.
    text = replace_once(text, director_if_old, director_if_new, 'graph director gate')

    router = '''  graph_repair_router:\n    name: GRAPH AUDIT → RETURN TO CODER\n    needs: [audit_graph]\n    if: needs.audit_graph.result == 'success' && needs.audit_graph.outputs.gate == 'REVISE'\n    runs-on: ubuntu-latest\n    timeout-minutes: 10\n    steps:\n      - name: Dispatch same-cycle Graph repair with exact audit\n        env:\n          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}\n          HUMAN_NOTE: ${{ inputs.human_note }}\n          CYCLE_INDEX: ${{ inputs.cycle_index }}\n          MAX_CYCLES: ${{ inputs.max_cycles }}\n          REPAIR_ROUND: ${{ inputs.repair_round }}\n        shell: bash\n        run: |\n          NEXT_REPAIR=$((REPAIR_ROUND + 1))\n          echo "Audit requested REVISE; returning run ${GITHUB_RUN_ID} to graph_runner as repair round ${NEXT_REPAIR}."\n          gh workflow run graph-loop.yml --ref main \\\n            -f human_note="$HUMAN_NOTE" \\\n            -f cycle_index="$CYCLE_INDEX" \\\n            -f max_cycles="$MAX_CYCLES" \\\n            -f repair_from_run_id="$GITHUB_RUN_ID" \\\n            -f repair_round="$NEXT_REPAIR"\n\n  graph_audit_blocked:\n    name: GRAPH AUDIT — BLOCKED\n    needs: [audit_graph]\n    if: needs.audit_graph.result == 'success' && needs.audit_graph.outputs.gate == 'BLOCKED'\n    runs-on: ubuntu-latest\n    timeout-minutes: 5\n    steps:\n      - name: Stop without integrating rejected snapshot\n        shell: bash\n        run: |\n          echo "::warning::Graph audit is BLOCKED. No integration and no blind repair loop. Rejected snapshot remains provenance."\n\n'''
    text = replace_once(text, '  graph_director:\n', router + '  graph_director:\n', 'graph repair router')

    path.write_text(text)


def patch_physics(path: Path):
    text = path.read_text()

    inputs_old = '''      max_cycles:\n        description: "Optional numeric cap; 0 = continue until Lane Director stops"\n        required: false\n        type: number\n        default: 0\n'''
    inputs_new = inputs_old + '''      repair_from_run_id:\n        description: "Prior rejected Physics run to repair; empty = fresh scientific cycle"\n        required: false\n        type: string\n        default: ""\n      repair_round:\n        description: "Same-cycle audit repair round; provenance only, no arbitrary cap"\n        required: false\n        type: number\n        default: 0\n'''
    text = replace_once(text, inputs_old, inputs_new, 'physics inputs')

    checkout_old = '''      - name: Checkout or initialize accepted Physics lane\n        shell: bash\n        run: |\n          if git ls-remote --exit-code --heads origin "refs/heads/$LANE_BRANCH" >/dev/null 2>&1; then\n            git fetch origin "$LANE_BRANCH"\n            git switch -C "$LANE_BRANCH" "origin/$LANE_BRANCH"\n          else\n            git switch -C "$LANE_BRANCH"\n            git push origin "HEAD:refs/heads/$LANE_BRANCH"\n          fi\n'''
    checkout_new = '''      - name: Checkout or initialize accepted Physics lane\n        if: ${{ inputs.repair_from_run_id == '' }}\n        shell: bash\n        run: |\n          if git ls-remote --exit-code --heads origin "refs/heads/$LANE_BRANCH" >/dev/null 2>&1; then\n            git fetch origin "$LANE_BRANCH"\n            git switch -C "$LANE_BRANCH" "origin/$LANE_BRANCH"\n          else\n            git switch -C "$LANE_BRANCH"\n            git push origin "HEAD:refs/heads/$LANE_BRANCH"\n          fi\n\n      - name: Checkout rejected Physics snapshot and audit for repair\n        if: ${{ inputs.repair_from_run_id != '' }}\n        shell: bash\n        run: |\n          SOURCE_TEAM="cycle/physics/${{ inputs.repair_from_run_id }}/team"\n          SOURCE_AUDIT="cycle/physics/${{ inputs.repair_from_run_id }}/audit"\n          git fetch origin "$SOURCE_TEAM:refs/remotes/origin/$SOURCE_TEAM"\n          git fetch origin "$SOURCE_AUDIT:refs/remotes/origin/$SOURCE_AUDIT"\n          git switch -C physics-repair-base "origin/$SOURCE_TEAM"\n          git worktree add --detach /tmp/spider_physics_repair_audit "origin/$SOURCE_AUDIT"\n'''
    text = replace_once(text, checkout_old, checkout_new, 'physics checkout')

    team_pattern = r'''      - name: Run TEAM PHYSICS\n.*?(?=      - name: Enforce Physics scope\n)'''
    team_new = '''      - name: Run TEAM PHYSICS — fresh scientific cycle\n        if: ${{ inputs.repair_from_run_id == '' }}\n        env:\n          HUMAN_NOTE: ${{ inputs.human_note }}\n        shell: bash\n        run: |\n          opencode run \\\n            --model "$SPIDER_MODEL" \\\n            --agent physics_runner \\\n            "Run Physics lane cycle ${{ inputs.cycle_index }} (GitHub run ${GITHUB_RUN_ID}). Read SPIDER_MASTER_PROMPT.md, directives/PHYSICS.md, directives/AUDITOR_PHYSICS.md, docs/NEXT_PHYSICS.md, docs/PHYSICS_LEDGER.md and relevant accepted Physics evidence. Do real falsifiable work with real data. Historical WP-003 is MEASUREMENT_INVALID. Prefer environment response P(S_next | S,A). Do not work on Graph. Do not edit SPIDER_MASTER_PROMPT.md or workflows. Never ask for interactive approval. Human steering note, subordinate to the constitution: ${HUMAN_NOTE}"\n\n      - name: Run TEAM PHYSICS — repair audited defects\n        if: ${{ inputs.repair_from_run_id != '' }}\n        env:\n          HUMAN_NOTE: ${{ inputs.human_note }}\n        shell: bash\n        run: |\n          opencode run \\\n            --model "$SPIDER_MODEL" \\\n            --agent physics_runner \\\n            "REPAIR Physics lane cycle ${{ inputs.cycle_index }}, repair round ${{ inputs.repair_round }} (GitHub run ${GITHUB_RUN_ID}). The current checkout is the exact rejected team snapshot from run ${{ inputs.repair_from_run_id }}. The independent audit workspace is /tmp/spider_physics_repair_audit. Read SPIDER_MASTER_PROMPT.md, directives/PHYSICS.md, directives/AUDITOR.md, directives/AUDITOR_PHYSICS.md, the prior audit report and its *_PHYSICS_GATE.json. Fix EVERY item in required_fixes concretely, rerun every affected test/experiment, and preserve the rejected attempt as provenance. Do not evade the audit by weakening tests, changing targets post hoc without labeling them exploratory, deleting contrary evidence, or merely rewriting claims when the defect is in code/measurement. Do not work on Graph or workflows. Human note: ${HUMAN_NOTE}"\n\n'''
    text = replace_regex_once(text, team_pattern, team_new, 'physics team steps')

    audit_header_old = '''  audit_physics:\n    name: INDEPENDENT AUDITOR — PHYSICS\n    needs: [team_physics]\n    if: needs.team_physics.result == 'success'\n    runs-on: ubuntu-latest\n    timeout-minutes: 240\n'''
    audit_header_new = audit_header_old + '''    outputs:\n      gate: ${{ steps.audit_gate.outputs.gate }}\n      safe_to_integrate: ${{ steps.audit_gate.outputs.safe_to_integrate }}\n'''
    text = replace_once(text, audit_header_old, audit_header_new, 'physics audit outputs')

    audit_pattern = r'''      - name: Audit Physics immediately\n.*?(?=      - name: Enforce audit-only writes\n)'''
    audit_new = '''      - name: Audit Physics immediately\n        shell: bash\n        run: |\n          opencode run \\\n            --model "$SPIDER_MODEL" \\\n            --agent independent_auditor \\\n            "Audit Physics lane cycle ${{ inputs.cycle_index }} (GitHub run ${GITHUB_RUN_ID}), repair round ${{ inputs.repair_round }}. Completed team workspace: /tmp/spider_physics_team. Current checkout is the untouched accepted Physics base and is where you may write ONLY audit outputs. Read SPIDER_MASTER_PROMPT.md, directives/AUDITOR.md and directives/AUDITOR_PHYSICS.md. Attack target leakage, temporal lags, split integrity, preprocessing leakage, policy confounding, uncertainty level, nulls, preregistration timing, identifiability and code/report consistency. Write reports/audit/CYCLE_${GITHUB_RUN_ID}_PHYSICS.md AND mandatory results/audit/CYCLE_${GITHUB_RUN_ID}_PHYSICS_GATE.json with gate PASS, REVISE, or BLOCKED and exact required_fixes. A valid negative/null/falsified/downgraded result may PASS. Use REVISE only for concrete same-cycle repairable defects and BLOCKED when another repair would be dishonest/repetitive or requires unavailable data/external decision. Do not edit team files, workflows or constitution."\n\n'''
    text = replace_regex_once(text, audit_pattern, audit_new, 'physics audit prompt')

    gate_step = '''      - name: Validate Physics audit integration gate\n        id: audit_gate\n        shell: bash\n        run: |\n          FILE="results/audit/CYCLE_${GITHUB_RUN_ID}_PHYSICS_GATE.json"\n          test -f "$FILE" || { echo "::error::Auditor omitted mandatory Physics gate file"; exit 1; }\n          GATE=$(jq -r '.gate // empty' "$FILE")\n          SAFE=$(jq -r '.safe_to_integrate // false' "$FILE")\n          case "$GATE" in\n            PASS)\n              [ "$SAFE" = "true" ] || { echo "::error::PASS requires safe_to_integrate=true"; exit 1; }\n              ;;\n            REVISE)\n              [ "$SAFE" = "false" ] || { echo "::error::REVISE requires safe_to_integrate=false"; exit 1; }\n              FIXES=$(jq '.required_fixes | if type == "array" then length else 0 end' "$FILE")\n              [ "$FIXES" -gt 0 ] || { echo "::error::REVISE requires actionable required_fixes"; exit 1; }\n              ;;\n            BLOCKED)\n              [ "$SAFE" = "false" ] || { echo "::error::BLOCKED requires safe_to_integrate=false"; exit 1; }\n              ;;\n            *) echo "::error::Invalid Physics audit gate: $GATE"; exit 1 ;;\n          esac\n          echo "gate=$GATE" >> "$GITHUB_OUTPUT"\n          echo "safe_to_integrate=$SAFE" >> "$GITHUB_OUTPUT"\n          echo "Physics audit gate=$GATE safe=$SAFE"\n\n'''
    marker = '      - name: Persist Physics audit branch\n'
    text = replace_once(text, marker, gate_step + marker, 'physics gate parser')

    director_if_old = "    if: needs.audit_physics.result == 'success'\n"
    director_if_new = "    if: needs.audit_physics.result == 'success' && needs.audit_physics.outputs.gate == 'PASS'\n"
    text = replace_once(text, director_if_old, director_if_new, 'physics director gate')

    router = '''  physics_repair_router:\n    name: PHYSICS AUDIT → RETURN TO CODER\n    needs: [audit_physics]\n    if: needs.audit_physics.result == 'success' && needs.audit_physics.outputs.gate == 'REVISE'\n    runs-on: ubuntu-latest\n    timeout-minutes: 10\n    steps:\n      - name: Dispatch same-cycle Physics repair with exact audit\n        env:\n          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}\n          HUMAN_NOTE: ${{ inputs.human_note }}\n          CYCLE_INDEX: ${{ inputs.cycle_index }}\n          MAX_CYCLES: ${{ inputs.max_cycles }}\n          REPAIR_ROUND: ${{ inputs.repair_round }}\n        shell: bash\n        run: |\n          NEXT_REPAIR=$((REPAIR_ROUND + 1))\n          echo "Audit requested REVISE; returning run ${GITHUB_RUN_ID} to physics_runner as repair round ${NEXT_REPAIR}."\n          gh workflow run physics-loop.yml --ref main \\\n            -f human_note="$HUMAN_NOTE" \\\n            -f cycle_index="$CYCLE_INDEX" \\\n            -f max_cycles="$MAX_CYCLES" \\\n            -f repair_from_run_id="$GITHUB_RUN_ID" \\\n            -f repair_round="$NEXT_REPAIR"\n\n  physics_audit_blocked:\n    name: PHYSICS AUDIT — BLOCKED\n    needs: [audit_physics]\n    if: needs.audit_physics.result == 'success' && needs.audit_physics.outputs.gate == 'BLOCKED'\n    runs-on: ubuntu-latest\n    timeout-minutes: 5\n    steps:\n      - name: Stop without integrating rejected snapshot\n        shell: bash\n        run: |\n          echo "::warning::Physics audit is BLOCKED. No integration and no blind repair loop. Rejected snapshot remains provenance."\n\n'''
    text = replace_once(text, '  physics_director:\n', router + '  physics_director:\n', 'physics repair router')

    path.write_text(text)


graph = Path('.github/workflows/graph-loop.yml')
physics = Path('.github/workflows/physics-loop.yml')
patch_graph(graph)
patch_physics(physics)

# Final invariants before allowing the maintenance commit.
g = graph.read_text()
p = physics.read_text()
for text, lane in [(g, 'Graph'), (p, 'Physics')]:
    assert 'repair_from_run_id:' in text
    assert 'repair_round:' in text
    assert f'{lane.upper()} AUDIT → RETURN TO CODER' in text
    assert 'required_fixes' in text
    assert "outputs.gate == 'PASS'" in text
    assert "outputs.gate == 'REVISE'" in text
    assert "outputs.gate == 'BLOCKED'" in text

# Remove this one-shot maintenance machinery in the same resulting commit.
Path('.github/scripts/install-audit-repair-loop.py').unlink(missing_ok=True)
Path('.github/workflows/_install-audit-repair-loop.yml').unlink(missing_ok=True)
Path('.spider/maintenance/install-audit-repair-loop.json').unlink(missing_ok=True)
print('Audit repair loop patch passed all assertions.')
