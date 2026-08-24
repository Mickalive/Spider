from pathlib import Path


def find_unique(lines, marker, label):
    hits = [i for i, line in enumerate(lines) if line == marker]
    if len(hits) != 1:
        raise SystemExit(f"{label}: expected 1 '{marker}', found {len(hits)}")
    return hits[0]


def replace_span(lines, start_marker, end_marker, new_lines, label):
    s = find_unique(lines, start_marker, label + ' start')
    e = next((i for i in range(s + 1, len(lines)) if lines[i] == end_marker), None)
    if e is None:
        raise SystemExit(f"{label}: end marker not found: {end_marker}")
    return lines[:s] + new_lines + lines[e:]


def patch_lane(path, lane):
    is_graph = lane == 'graph'
    Lane = 'Graph' if is_graph else 'Physics'
    upper = lane.upper()
    team_job = f'team_{lane}'
    audit_job = f'audit_{lane}'
    director_job = f'{lane}_director'
    team_name = f'TEAM {upper}'
    team_agent = 'graph_runner' if is_graph else 'physics_runner'
    enforce_name = f'Enforce {Lane} scope'
    audit_name = f'Audit {Lane} immediately'
    persist_audit_name = f'Persist {Lane} audit branch'
    repair_audit_workspace = f'/tmp/spider_{lane}_repair_audit'
    branch_prefix = f'cycle/{lane}'
    gate_file = f'results/audit/CYCLE_${{GITHUB_RUN_ID}}_{upper}_GATE.json'

    lines = path.read_text().splitlines()

    max_i = find_unique(lines, '      max_cycles:', f'{lane} max_cycles')
    default_i = next((i for i in range(max_i, min(max_i + 8, len(lines))) if lines[i] == '        default: 0'), None)
    if default_i is None:
        raise SystemExit(f'{lane}: max_cycles default not found')
    lines = lines[:default_i + 1] + [
        '      repair_from_run_id:',
        f'        description: "Prior rejected {Lane} run to repair; empty = fresh scientific cycle"',
        '        required: false',
        '        type: string',
        '        default: ""',
        '      repair_round:',
        '        description: "Same-cycle audit repair round; provenance only, no arbitrary cap"',
        '        required: false',
        '        type: number',
        '        default: 0',
    ] + lines[default_i + 1:]

    checkout_start = f'      - name: Checkout or initialize accepted {Lane} lane'
    checkout_end = '      - name: Install OpenCode'
    checkout_new = [
        checkout_start,
        "        if: ${{ inputs.repair_from_run_id == '' }}",
        '        shell: bash',
        '        run: |',
        '          if git ls-remote --exit-code --heads origin "refs/heads/$LANE_BRANCH" >/dev/null 2>&1; then',
        '            git fetch origin "$LANE_BRANCH"',
        '            git switch -C "$LANE_BRANCH" "origin/$LANE_BRANCH"',
        '          else',
        '            git switch -C "$LANE_BRANCH"',
        '            git push origin "HEAD:refs/heads/$LANE_BRANCH"',
        '          fi',
        '',
        f'      - name: Checkout rejected {Lane} snapshot and audit for repair',
        "        if: ${{ inputs.repair_from_run_id != '' }}",
        '        shell: bash',
        '        run: |',
        f'          SOURCE_TEAM="{branch_prefix}/${{{{ inputs.repair_from_run_id }}}}/team"',
        f'          SOURCE_AUDIT="{branch_prefix}/${{{{ inputs.repair_from_run_id }}}}/audit"',
        '          git fetch origin "$SOURCE_TEAM:refs/remotes/origin/$SOURCE_TEAM"',
        '          git fetch origin "$SOURCE_AUDIT:refs/remotes/origin/$SOURCE_AUDIT"',
        f'          git switch -C {lane}-repair-base "origin/$SOURCE_TEAM"',
        f'          git worktree add --detach {repair_audit_workspace} "origin/$SOURCE_AUDIT"',
        '',
    ]
    lines = replace_span(lines, checkout_start, checkout_end, checkout_new, f'{lane} checkout')

    team_start = f'      - name: Run {team_name}'
    team_end = f'      - name: {enforce_name}'
    if is_graph:
        fresh_prompt = 'Run Graph lane cycle ${{ inputs.cycle_index }} (GitHub run ${GITHUB_RUN_ID}). Read SPIDER_MASTER_PROMPT.md, directives/GRAPH.md, directives/AUDITOR_GRAPH.md, docs/NEXT_GRAPH.md, docs/GRAPH_LEDGER.md and relevant accepted Graph evidence. Do real empirical work. Do not work on Physics. Do not edit SPIDER_MASTER_PROMPT.md or workflows. Never ask for interactive approval. Human steering note, subordinate to the constitution: ${HUMAN_NOTE}'
        repair_prompt = f'REPAIR Graph lane cycle ${{{{ inputs.cycle_index }}}}, repair round ${{{{ inputs.repair_round }}}} (GitHub run ${{GITHUB_RUN_ID}}). The current checkout is the exact rejected team snapshot from run ${{{{ inputs.repair_from_run_id }}}}. The independent audit workspace is {repair_audit_workspace}. Read SPIDER_MASTER_PROMPT.md, directives/GRAPH.md, directives/AUDITOR.md, directives/AUDITOR_GRAPH.md, the prior audit report and its *_GRAPH_GATE.json. Fix EVERY item in required_fixes concretely, rerun every affected test/experiment, and preserve the rejected attempt as provenance. Do not evade the audit by weakening tests, changing targets post hoc without labeling them exploratory, deleting contrary evidence, or merely rewriting claims when the defect is in code/measurement. Do not work on Physics or workflows. Human note: ${{HUMAN_NOTE}}'
    else:
        fresh_prompt = 'Run Physics lane cycle ${{ inputs.cycle_index }} (GitHub run ${GITHUB_RUN_ID}). Read SPIDER_MASTER_PROMPT.md, directives/PHYSICS.md, directives/AUDITOR_PHYSICS.md, docs/NEXT_PHYSICS.md, docs/PHYSICS_LEDGER.md and relevant accepted Physics evidence. Do real falsifiable work with real data. Historical WP-003 is MEASUREMENT_INVALID. Prefer environment response P(S_next | S,A). Do not work on Graph. Do not edit SPIDER_MASTER_PROMPT.md or workflows. Never ask for interactive approval. Human steering note, subordinate to the constitution: ${HUMAN_NOTE}'
        repair_prompt = f'REPAIR Physics lane cycle ${{{{ inputs.cycle_index }}}}, repair round ${{{{ inputs.repair_round }}}} (GitHub run ${{GITHUB_RUN_ID}}). The current checkout is the exact rejected team snapshot from run ${{{{ inputs.repair_from_run_id }}}}. The independent audit workspace is {repair_audit_workspace}. Read SPIDER_MASTER_PROMPT.md, directives/PHYSICS.md, directives/AUDITOR.md, directives/AUDITOR_PHYSICS.md, the prior audit report and its *_PHYSICS_GATE.json. Fix EVERY item in required_fixes concretely, rerun every affected test/experiment, and preserve the rejected attempt as provenance. Do not evade the audit by weakening tests, changing targets post hoc without labeling them exploratory, deleting contrary evidence, or merely rewriting claims when the defect is in code/measurement. Do not work on Graph or workflows. Human note: ${{HUMAN_NOTE}}'

    team_new = [
        f'      - name: Run {team_name} — fresh scientific cycle',
        "        if: ${{ inputs.repair_from_run_id == '' }}",
        '        env:',
        '          HUMAN_NOTE: ${{ inputs.human_note }}',
        '        shell: bash',
        '        run: |',
        '          opencode run \\',
        '            --model "$SPIDER_MODEL" \\',
        f'            --agent {team_agent} \\',
        f'            "{fresh_prompt}"',
        '',
        f'      - name: Run {team_name} — repair audited defects',
        "        if: ${{ inputs.repair_from_run_id != '' }}",
        '        env:',
        '          HUMAN_NOTE: ${{ inputs.human_note }}',
        '        shell: bash',
        '        run: |',
        '          opencode run \\',
        '            --model "$SPIDER_MODEL" \\',
        f'            --agent {team_agent} \\',
        f'            "{repair_prompt}"',
        '',
    ]
    lines = replace_span(lines, team_start, team_end, team_new, f'{lane} producer steps')

    audit_i = find_unique(lines, f'  {audit_job}:', f'{lane} audit job')
    timeout_i = next((i for i in range(audit_i, min(audit_i + 12, len(lines))) if lines[i] == '    timeout-minutes: 240'), None)
    if timeout_i is None:
        raise SystemExit(f'{lane}: audit timeout marker missing')
    lines = lines[:timeout_i + 1] + [
        '    outputs:',
        '      gate: ${{ steps.audit_gate.outputs.gate }}',
        '      safe_to_integrate: ${{ steps.audit_gate.outputs.safe_to_integrate }}',
    ] + lines[timeout_i + 1:]

    audit_start = f'      - name: {audit_name}'
    audit_end = '      - name: Enforce audit-only writes'
    if is_graph:
        audit_prompt = 'Audit Graph lane cycle ${{ inputs.cycle_index }} (GitHub run ${GITHUB_RUN_ID}), repair round ${{ inputs.repair_round }}. Completed team workspace: /tmp/spider_graph_team. Current checkout is the untouched accepted Graph base and is where you may write ONLY audit outputs. Read SPIDER_MASTER_PROMPT.md, directives/AUDITOR.md and directives/AUDITOR_GRAPH.md. Recompute claims and attack leakage, hand-coded decomposition, mismatched timing, weak baselines, denominator tricks, retrieval cost and transfer claims. Write reports/audit/CYCLE_${GITHUB_RUN_ID}_GRAPH.md AND mandatory results/audit/CYCLE_${GITHUB_RUN_ID}_GRAPH_GATE.json with gate PASS, REVISE, or BLOCKED and exact required_fixes. A valid negative/null/downgraded result may PASS. Use REVISE only for concrete same-cycle repairable defects and BLOCKED when another repair would be dishonest/repetitive or requires unavailable data/external decision. Do not edit team files, workflows or constitution.'
    else:
        audit_prompt = 'Audit Physics lane cycle ${{ inputs.cycle_index }} (GitHub run ${GITHUB_RUN_ID}), repair round ${{ inputs.repair_round }}. Completed team workspace: /tmp/spider_physics_team. Current checkout is the untouched accepted Physics base and is where you may write ONLY audit outputs. Read SPIDER_MASTER_PROMPT.md, directives/AUDITOR.md and directives/AUDITOR_PHYSICS.md. Attack target leakage, temporal lags, split integrity, preprocessing leakage, policy confounding, uncertainty level, nulls, preregistration timing, identifiability and code/report consistency. Write reports/audit/CYCLE_${GITHUB_RUN_ID}_PHYSICS.md AND mandatory results/audit/CYCLE_${GITHUB_RUN_ID}_PHYSICS_GATE.json with gate PASS, REVISE, or BLOCKED and exact required_fixes. A valid negative/null/falsified/downgraded result may PASS. Use REVISE only for concrete same-cycle repairable defects and BLOCKED when another repair would be dishonest/repetitive or requires unavailable data/external decision. Do not edit team files, workflows or constitution.'
    audit_new = [
        audit_start,
        '        shell: bash',
        '        run: |',
        '          opencode run \\',
        '            --model "$SPIDER_MODEL" \\',
        '            --agent independent_auditor \\',
        f'            "{audit_prompt}"',
        '',
    ]
    lines = replace_span(lines, audit_start, audit_end, audit_new, f'{lane} audit prompt')

    gate_step = [
        f'      - name: Validate {Lane} audit integration gate',
        '        id: audit_gate',
        '        shell: bash',
        '        run: |',
        f'          FILE="{gate_file}"',
        f'          test -f "$FILE" || {{ echo "::error::Auditor omitted mandatory {Lane} gate file"; exit 1; }}',
        "          GATE=$(jq -r '.gate // empty' \"$FILE\")",
        "          SAFE=$(jq -r '.safe_to_integrate // false' \"$FILE\")",
        '          case "$GATE" in',
        '            PASS)',
        '              [ "$SAFE" = "true" ] || { echo "::error::PASS requires safe_to_integrate=true"; exit 1; }',
        '              ;;',
        '            REVISE)',
        '              [ "$SAFE" = "false" ] || { echo "::error::REVISE requires safe_to_integrate=false"; exit 1; }',
        "              FIXES=$(jq '.required_fixes | if type == \"array\" then length else 0 end' \"$FILE\")",
        '              [ "$FIXES" -gt 0 ] || { echo "::error::REVISE requires actionable required_fixes"; exit 1; }',
        '              ;;',
        '            BLOCKED)',
        '              [ "$SAFE" = "false" ] || { echo "::error::BLOCKED requires safe_to_integrate=false"; exit 1; }',
        '              ;;',
        f'            *) echo "::error::Invalid {Lane} audit gate: $GATE"; exit 1 ;;',
        '          esac',
        '          echo "gate=$GATE" >> "$GITHUB_OUTPUT"',
        '          echo "safe_to_integrate=$SAFE" >> "$GITHUB_OUTPUT"',
        f'          echo "{Lane} audit gate=$GATE safe=$SAFE"',
        '',
    ]
    persist_i = find_unique(lines, f'      - name: {persist_audit_name}', f'{lane} persist audit')
    lines = lines[:persist_i] + gate_step + lines[persist_i:]

    director_i = find_unique(lines, f'  {director_job}:', f'{lane} director')
    router = [
        f'  {lane}_repair_router:',
        f'    name: {upper} AUDIT → RETURN TO CODER',
        f'    needs: [{audit_job}]',
        f"    if: needs.{audit_job}.result == 'success' && needs.{audit_job}.outputs.gate == 'REVISE'",
        '    runs-on: ubuntu-latest',
        '    timeout-minutes: 10',
        '    steps:',
        f'      - name: Dispatch same-cycle {Lane} repair with exact audit',
        '        env:',
        '          GH_TOKEN: ${{ secrets.GITHUB_TOKEN }}',
        '          HUMAN_NOTE: ${{ inputs.human_note }}',
        '          CYCLE_INDEX: ${{ inputs.cycle_index }}',
        '          MAX_CYCLES: ${{ inputs.max_cycles }}',
        '          REPAIR_ROUND: ${{ inputs.repair_round }}',
        '        shell: bash',
        '        run: |',
        '          NEXT_REPAIR=$((REPAIR_ROUND + 1))',
        f'          echo "Audit requested REVISE; returning run ${{GITHUB_RUN_ID}} to {team_agent} as repair round ${{NEXT_REPAIR}}."',
        f'          gh workflow run {lane}-loop.yml --ref main \\',
        '            -f human_note="$HUMAN_NOTE" \\',
        '            -f cycle_index="$CYCLE_INDEX" \\',
        '            -f max_cycles="$MAX_CYCLES" \\',
        '            -f repair_from_run_id="$GITHUB_RUN_ID" \\',
        '            -f repair_round="$NEXT_REPAIR"',
        '',
        f'  {lane}_audit_blocked:',
        f'    name: {upper} AUDIT — BLOCKED',
        f'    needs: [{audit_job}]',
        f"    if: needs.{audit_job}.result == 'success' && needs.{audit_job}.outputs.gate == 'BLOCKED'",
        '    runs-on: ubuntu-latest',
        '    timeout-minutes: 5',
        '    steps:',
        '      - name: Stop without integrating rejected snapshot',
        '        shell: bash',
        '        run: |',
        f'          echo "::warning::{Lane} audit is BLOCKED. No integration and no blind repair loop. Rejected snapshot remains provenance."',
        '',
    ]
    lines = lines[:director_i] + router + lines[director_i:]

    director_i = find_unique(lines, f'  {director_job}:', f'{lane} director after router')
    cond_i = next((i for i in range(director_i, min(director_i + 8, len(lines))) if lines[i].startswith('    if: ')), None)
    if cond_i is None:
        raise SystemExit(f'{lane}: director if condition missing')
    lines[cond_i] = f"    if: needs.{audit_job}.result == 'success' && needs.{audit_job}.outputs.gate == 'PASS'"

    path.write_text('\n'.join(lines) + '\n')


patch_lane(Path('.github/workflows/graph-loop.yml'), 'graph')
patch_lane(Path('.github/workflows/physics-loop.yml'), 'physics')

for p, lane in [(Path('.github/workflows/graph-loop.yml'), 'GRAPH'), (Path('.github/workflows/physics-loop.yml'), 'PHYSICS')]:
    text = p.read_text()
    assert 'repair_from_run_id:' in text
    assert 'repair_round:' in text
    assert f'{lane} AUDIT → RETURN TO CODER' in text
    assert "outputs.gate == 'PASS'" in text
    assert "outputs.gate == 'REVISE'" in text
    assert "outputs.gate == 'BLOCKED'" in text
    assert '_GATE.json' in text

Path('.github/scripts/install-audit-repair-loop.py').unlink(missing_ok=True)
Path('.github/workflows/_install-audit-repair-loop.yml').unlink(missing_ok=True)
Path('.spider/maintenance/install-audit-repair-loop.json').unlink(missing_ok=True)
print('Audit repair-loop patch passed all assertions.')
