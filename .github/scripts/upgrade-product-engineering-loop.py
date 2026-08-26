from pathlib import Path

p = Path('.github/workflows/product-loop.yml')
t = p.read_text()


def replace_once(old: str, new: str, label: str):
    global t
    if new in t:
        return
    n = t.count(old)
    if n != 1:
        raise SystemExit(f'{label}: expected exactly one anchor, got {n}')
    t = t.replace(old, new, 1)


replace_once(
    "on:\n  workflow_dispatch:\n  workflow_run:\n",
    "on:\n  workflow_dispatch:\n  push:\n    branches: [main]\n    paths:\n      - '.github/workflows/product-loop.yml'\n  workflow_run:\n",
    'one-time activation trigger',
)

replace_once(
    "    outputs:\n      beta_launch: ${{ steps.direction.outputs.beta_launch }}\n      beta_id: ${{ steps.direction.outputs.beta_id }}\n",
    "    outputs:\n      beta_launch: ${{ steps.direction.outputs.beta_launch }}\n      beta_id: ${{ steps.direction.outputs.beta_id }}\n      work_launch: ${{ steps.direction.outputs.work_launch }}\n      work_id: ${{ steps.direction.outputs.work_id }}\n",
    'director outputs',
)

replace_once(
    """      - name: Snapshot prior Product request and clear only the ephemeral launch decision
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
""",
    """      - name: Snapshot prior Product requests and clear only ephemeral launch decisions
        shell: bash
        run: |
          BETA_PRE_SHA=""
          WORK_PRE_SHA=""
          if [[ -f state/product_beta_request.json ]]; then
            BETA_PRE_SHA=$(sha256sum state/product_beta_request.json | awk '{print $1}')
          fi
          if [[ -f state/product_work_request.json ]]; then
            WORK_PRE_SHA=$(sha256sum state/product_work_request.json | awk '{print $1}')
          fi
          echo "PRODUCT_REQUEST_PRE_SHA=$BETA_PRE_SHA" >> "$GITHUB_ENV"
          echo "PRODUCT_WORK_PRE_SHA=$WORK_PRE_SHA" >> "$GITHUB_ENV"
          if [[ -f state/product_direction.json ]]; then
            jq '.beta_launch=false | .work_launch=false' state/product_direction.json > /tmp/product_direction.json
            mv /tmp/product_direction.json state/product_direction.json
          fi
""",
    'request snapshot',
)

replace_once(
    """            \"Review accepted Graph=/tmp/spider_graph, Physics=/tmp/spider_physics, Intel=/tmp/spider_intel, Runtime=/tmp/spider_runtime and critical CTO=/tmp/spider_cto plus persistent Product state. Your formal job description is binding. Optimize toward verified future work avoided, not feature count. If a minimal product can now fairly test whether SPIDER beats a credible current agent on a useful task class after full overhead, authorize exactly one Product Beta and write state/product_beta_request.json; otherwise keep beta_launch=false.\"
""",
    """            \"Review accepted Graph=/tmp/spider_graph, Physics=/tmp/spider_physics, Intel=/tmp/spider_intel, Runtime=/tmp/spider_runtime and critical CTO=/tmp/spider_cto plus persistent Product state. Your formal job description is binding. Optimize toward verified future work avoided, not feature count. Choose exactly one honest mode: (A) if a minimal product can fairly test whether SPIDER beats a credible current agent on a useful task class after full overhead, authorize exactly one Product Beta; (B) otherwise, if concrete pre-beta engineering can make accepted primitives agent-facing, executable, instrumented, composable or cheaper to integrate, authorize exactly one bounded Product Engineering work package with mechanical acceptance tests; (C) only when neither has positive value, WAIT_FOR_EVIDENCE. Never build decorative UI or claim superiority without the frozen beta benchmark.\"
""",
    'director prompt',
)

replace_once(
    """          LAUNCH=$(jq -r '.beta_launch // false' state/product_direction.json)
          if [[ "$LAUNCH" == true ]]; then
            test -f state/product_beta_request.json || { echo "::error::beta_launch requires a product_beta_request"; exit 1; }
            CURRENT_SHA=$(sha256sum state/product_beta_request.json | awk '{print $1}')
            if [[ -n "${PRODUCT_REQUEST_PRE_SHA:-}" && "$CURRENT_SHA" == "$PRODUCT_REQUEST_PRE_SHA" ]]; then
              echo "::error::beta_launch requires a freshly changed request; refusing stale durable authorization"
              exit 1
            fi
            BETA=$(jq -r '.beta_id // empty' state/product_beta_request.json)
            test -n "$BETA" || exit 1
          else
            BETA=""
          fi
          echo "beta_launch=$LAUNCH" >> "$GITHUB_OUTPUT"
          echo "beta_id=$BETA" >> "$GITHUB_OUTPUT"
""",
    """          LAUNCH=$(jq -r '.beta_launch // false' state/product_direction.json)
          WORK=$(jq -r '.work_launch // false' state/product_direction.json)
          if [[ "$LAUNCH" == true && "$WORK" == true ]]; then
            echo "::error::Product Director may authorize a beta OR one pre-beta work package, never both in the same decision"
            exit 1
          fi
          if [[ "$LAUNCH" == true ]]; then
            test -f state/product_beta_request.json || { echo "::error::beta_launch requires a product_beta_request"; exit 1; }
            CURRENT_SHA=$(sha256sum state/product_beta_request.json | awk '{print $1}')
            if [[ -n "${PRODUCT_REQUEST_PRE_SHA:-}" && "$CURRENT_SHA" == "$PRODUCT_REQUEST_PRE_SHA" ]]; then
              echo "::error::beta_launch requires a freshly changed request; refusing stale durable authorization"
              exit 1
            fi
            BETA=$(jq -r '.beta_id // empty' state/product_beta_request.json)
            test -n "$BETA" || exit 1
          else
            BETA=""
          fi
          if [[ "$WORK" == true ]]; then
            test -f state/product_work_request.json || { echo "::error::work_launch requires state/product_work_request.json"; exit 1; }
            CURRENT_WORK_SHA=$(sha256sum state/product_work_request.json | awk '{print $1}')
            if [[ -n "${PRODUCT_WORK_PRE_SHA:-}" && "$CURRENT_WORK_SHA" == "$PRODUCT_WORK_PRE_SHA" ]]; then
              echo "::error::work_launch requires a freshly changed work request; refusing stale authorization"
              exit 1
            fi
            WORK_ID=$(jq -r '.work_id // empty' state/product_work_request.json)
            test -n "$WORK_ID" || { echo "::error::work request missing work_id"; exit 1; }
            test "$(jq -r '.work_launch // false' state/product_work_request.json)" == true || { echo "::error::work request must declare work_launch=true"; exit 1; }
            test "$(jq '.acceptance_tests // [] | length' state/product_work_request.json)" -gt 0 || { echo "::error::work request requires executable acceptance_tests"; exit 1; }
            test -n "$(jq -r '.kill_condition // empty' state/product_work_request.json)" || { echo "::error::work request requires kill_condition"; exit 1; }
          else
            WORK_ID=""
          fi
          echo "beta_launch=$LAUNCH" >> "$GITHUB_OUTPUT"
          echo "beta_id=$BETA" >> "$GITHUB_OUTPUT"
          echo "work_launch=$WORK" >> "$GITHUB_OUTPUT"
          echo "work_id=$WORK_ID" >> "$GITHUB_OUTPUT"
""",
    'direction validation',
)

marker = "\n  beta_architect:\n"
if '  product_engineer:\n' not in t:
    if marker not in t:
        raise SystemExit('beta architect marker missing')
    jobs = r'''

  product_engineer:
    name: PRODUCT ENGINEERING
    needs: [product_director]
    if: needs.product_director.outputs.work_launch == 'true'
    runs-on: ubuntu-latest
    timeout-minutes: 330
    outputs:
      status: ${{ steps.work_state.outputs.status }}
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0

      - name: Checkout Product base and mount accepted evidence
        shell: bash
        run: |
          set -euo pipefail
          git fetch origin "$PRODUCT_BRANCH"
          git switch -C product-engineer-base "origin/$PRODUCT_BRANCH"
          for lane in graph physics intel runtime cto; do
            B="lab/$lane"
            if git ls-remote --exit-code --heads origin "refs/heads/$B" >/dev/null 2>&1; then
              git fetch origin "$B:refs/remotes/origin/$B"
              git worktree add --detach "/tmp/spider_$lane" "origin/$B"
            else
              mkdir -p "/tmp/spider_$lane"
            fi
          done
          mkdir -p /tmp/spider_frontier
          while IFS= read -r REF; do
            B="${REF#refs/heads/}"
            TEAM="${B#lab/frontier/}"
            [[ -n "$TEAM" && "$TEAM" != "$B" ]] || continue
            git fetch origin "$B:refs/remotes/origin/$B"
            git worktree add --detach "/tmp/spider_frontier/$TEAM" "origin/$B"
          done < <(git ls-remote --heads origin 'refs/heads/lab/frontier/*' | awk '{print $2}' | sort)
          rm -f state/product_work_result.json state/product_work_audit.json

      - name: Install OpenCode
        shell: bash
        run: curl --retry 3 --retry-all-errors --retry-delay 15 -fsSL https://opencode.ai/install | bash

      - name: Build bounded pre-beta Product work package
        shell: bash
        run: |
          bash .github/scripts/run-opencode-with-retry.sh run \
            --model "$SPIDER_MODEL" \
            --agent product_engineer \
            "Build Product work package ${{ needs.product_director.outputs.work_id }} exactly from state/product_work_request.json. Accepted Graph=/tmp/spider_graph Physics=/tmp/spider_physics Intel=/tmp/spider_intel Runtime=/tmp/spider_runtime CTO=/tmp/spider_cto and accepted Frontier snapshots=/tmp/spider_frontier. Your formal job description is binding. Produce executable integration work and real acceptance tests; no decorative UI, no scientific-claim promotion, no beta superiority claim."

      - name: Validate Product work result and scope
        id: work_state
        shell: bash
        run: |
          set -euo pipefail
          test -f state/product_work_result.json || { echo "::error::Missing product_work_result"; exit 1; }
          test "$(jq -r '.work_id // empty' state/product_work_result.json)" == "${{ needs.product_director.outputs.work_id }}" || { echo "::error::work_id mismatch"; exit 1; }
          STATUS=$(jq -r '.status // empty' state/product_work_result.json)
          case "$STATUS" in READY_FOR_AUDIT|BLOCKED|FAILED_BUILD) ;; *) echo "::error::Invalid Product work status $STATUS"; exit 1 ;; esac
          BAD=""
          while IFS= read -r line; do
            [[ -n "$line" ]] || continue
            p="${line:3}"
            case "$p" in
              product/*|tests/product/*|results/product/work/*|docs/product/*|state/product_work_result.json) ;;
              *) BAD+="$p\n" ;;
            esac
          done < <(git status --porcelain -uall)
          if [[ -n "$BAD" ]]; then
            echo -e "Product Engineer crossed protected scope:\n$BAD"
            exit 1
          fi
          echo "status=$STATUS" >> "$GITHUB_OUTPUT"

      - name: Persist Product Engineer candidate snapshot
        if: always()
        shell: bash
        run: |
          BRANCH="cycle/product/${GITHUB_RUN_ID}/work"
          git config user.name spider-product-engineer
          git config user.email spider-product-engineer@autonomous.local
          git switch -C "$BRANCH"
          git add -A
          git commit -m "Product work ${{ needs.product_director.outputs.work_id }}: engineering" || true
          git push --force origin "HEAD:refs/heads/$BRANCH"

  product_work_build_review:
    name: PRODUCT DIRECTOR — WORK BUILD REVIEW
    needs: [product_director, product_engineer]
    if: needs.product_engineer.outputs.status == 'BLOCKED' || needs.product_engineer.outputs.status == 'FAILED_BUILD'
    runs-on: ubuntu-latest
    timeout-minutes: 240
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - name: Mount failed Product work candidate
        shell: bash
        run: |
          git fetch origin "$PRODUCT_BRANCH"
          git switch -C "$PRODUCT_BRANCH" "origin/$PRODUCT_BRANCH"
          B="cycle/product/${GITHUB_RUN_ID}/work"
          git fetch origin "$B:refs/remotes/origin/$B"
          git worktree add --detach /tmp/spider_product_work "origin/$B"
      - name: Install OpenCode
        shell: bash
        run: curl --retry 3 --retry-all-errors --retry-delay 15 -fsSL https://opencode.ai/install | bash
      - name: Review blocked Product Engineering work
        shell: bash
        run: |
          bash .github/scripts/run-opencode-with-retry.sh run --model "$SPIDER_MODEL" --agent product_director \
            "Review Product work ${{ needs.product_director.outputs.work_id }} status=${{ needs.product_engineer.outputs.status }} at /tmp/spider_product_work. Preserve the negative result. Clear stale work_launch, record the exact blocker, and decide the next bounded engineering/evidence action. Do not integrate un-audited implementation and do not claim a product win."
      - name: Advance Product state and start a fresh decision cycle
        shell: bash
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          git config user.name spider-product-director
          git config user.email spider-product-director@autonomous.local
          git add -A
          git commit -m "Product work build review ${GITHUB_RUN_ID}" || true
          git push origin "HEAD:refs/heads/$PRODUCT_BRANCH"
          gh workflow run product-loop.yml --repo "$GITHUB_REPOSITORY" --ref main

  product_work_auditor:
    name: PRODUCT WORK AUDITOR
    needs: [product_director, product_engineer]
    if: needs.product_engineer.outputs.status == 'READY_FOR_AUDIT'
    runs-on: ubuntu-latest
    timeout-minutes: 300
    outputs:
      gate: ${{ steps.work_gate.outputs.gate }}
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - name: Mount accepted Product base and Engineer candidate
        shell: bash
        run: |
          set -euo pipefail
          git fetch origin "$PRODUCT_BRANCH"
          git switch -C product-work-audit-base "origin/$PRODUCT_BRANCH"
          rm -f state/product_work_audit.json
          B="cycle/product/${GITHUB_RUN_ID}/work"
          git fetch origin "$B:refs/remotes/origin/$B"
          git worktree add --detach /tmp/spider_product_work "origin/$B"
      - name: Install OpenCode
        shell: bash
        run: curl --retry 3 --retry-all-errors --retry-delay 15 -fsSL https://opencode.ai/install | bash
      - name: Run independent Product work audit
        shell: bash
        run: |
          bash .github/scripts/run-opencode-with-retry.sh run \
            --model "$SPIDER_MODEL" \
            --agent product_work_auditor \
            "Independently audit Product work ${{ needs.product_director.outputs.work_id }}. Exact request is on the accepted Product checkout; immutable Engineer candidate=/tmp/spider_product_work. Re-run its acceptance tests and attack hidden manual steps, fake fixtures, dependency gaps, duplicated lane mechanisms, claim leakage and omitted overhead. Do not redesign it to pass."
      - name: Validate Product work audit and scope
        id: work_gate
        shell: bash
        run: |
          set -euo pipefail
          test -f state/product_work_audit.json || { echo "::error::Missing product_work_audit"; exit 1; }
          test "$(jq -r '.work_id // empty' state/product_work_audit.json)" == "${{ needs.product_director.outputs.work_id }}" || { echo "::error::audit work_id mismatch"; exit 1; }
          GATE=$(jq -r '.gate // empty' state/product_work_audit.json)
          SAFE=$(jq -r '.safe_to_integrate // false' state/product_work_audit.json)
          case "$GATE" in PASS|REVISE|BLOCKED) ;; *) echo "::error::Invalid Product work audit gate $GATE"; exit 1 ;; esac
          if [[ "$GATE" == PASS ]]; then
            [[ "$SAFE" == true ]] || { echo "::error::PASS requires safe_to_integrate=true"; exit 1; }
          else
            [[ "$SAFE" == false ]] || { echo "::error::$GATE requires safe_to_integrate=false"; exit 1; }
          fi
          if [[ "$GATE" == REVISE ]]; then
            test "$(jq '.required_fixes // [] | length' state/product_work_audit.json)" -gt 0 || { echo "::error::REVISE requires required_fixes"; exit 1; }
          fi
          BAD=""
          while IFS= read -r line; do
            [[ -n "$line" ]] || continue
            p="${line:3}"
            case "$p" in
              reports/product/audit/*|results/product/audit/*|state/product_work_audit.json) ;;
              *) BAD+="$p\n" ;;
            esac
          done < <(git status --porcelain -uall)
          if [[ -n "$BAD" ]]; then
            echo -e "Product Work Auditor crossed protected scope:\n$BAD"
            exit 1
          fi
          echo "gate=$GATE" >> "$GITHUB_OUTPUT"
      - name: Persist independent Product work audit
        if: always()
        shell: bash
        run: |
          BRANCH="cycle/product/${GITHUB_RUN_ID}/work-audit"
          git config user.name spider-product-work-auditor
          git config user.email spider-product-work-auditor@autonomous.local
          git switch -C "$BRANCH"
          git add -A
          git commit -m "Product work ${{ needs.product_director.outputs.work_id }}: audit" || true
          git push --force origin "HEAD:refs/heads/$BRANCH"

  product_work_integration:
    name: PRODUCT WORK INTEGRATION
    needs: [product_director, product_engineer, product_work_auditor]
    if: needs.product_work_auditor.outputs.gate == 'PASS'
    runs-on: ubuntu-latest
    timeout-minutes: 240
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - name: Mount PASSed Product work and audit
        shell: bash
        run: |
          set -euo pipefail
          git fetch origin "$PRODUCT_BRANCH"
          git switch -C "$PRODUCT_BRANCH" "origin/$PRODUCT_BRANCH"
          for kind in work work-audit; do
            B="cycle/product/${GITHUB_RUN_ID}/$kind"
            git fetch origin "$B:refs/remotes/origin/$B"
            git worktree add --detach "/tmp/spider_product_$kind" "origin/$B"
          done
          for d in product tests/product results/product/work docs/product; do
            if [[ -d "/tmp/spider_product_work/$d" ]]; then
              mkdir -p "$d"
              cp -a "/tmp/spider_product_work/$d/." "$d/"
            fi
          done
          if [[ -f /tmp/spider_product_work/state/product_work_result.json ]]; then
            cp /tmp/spider_product_work/state/product_work_result.json state/product_work_result.json
          fi
          for d in reports/product/audit results/product/audit; do
            if [[ -d "/tmp/spider_product_work-audit/$d" ]]; then
              mkdir -p "$d"
              cp -a "/tmp/spider_product_work-audit/$d/." "$d/"
            fi
          done
          cp /tmp/spider_product_work-audit/state/product_work_audit.json state/product_work_audit.json
      - name: Install OpenCode
        shell: bash
        run: curl --retry 3 --retry-all-errors --retry-delay 15 -fsSL https://opencode.ai/install | bash
      - name: Integrate audited Product work into Product program
        shell: bash
        run: |
          bash .github/scripts/run-opencode-with-retry.sh run --model "$SPIDER_MODEL" --agent product_director \
            "Integrate independently PASSed Product work ${{ needs.product_director.outputs.work_id }} now present on the Product checkout. Engineer snapshot=/tmp/spider_product_work; Audit=/tmp/spider_product_work-audit. Preserve the audit claim ceiling, clear consumed work_launch, update Product ledger/hypotheses/state, and decide what concrete engineering or beta question should be considered next. PASS means safe to integrate, not evidence that SPIDER beats an external agent."
      - name: Persist accepted Product work and launch next decision cycle
        shell: bash
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          set -euo pipefail
          git config user.name spider-product-director
          git config user.email spider-product-director@autonomous.local
          git add -A
          git commit -m "Product work ${{ needs.product_director.outputs.work_id }}: integrate ${GITHUB_RUN_ID}" || true
          git push origin "HEAD:refs/heads/$PRODUCT_BRANCH"
          gh workflow run product-loop.yml --repo "$GITHUB_REPOSITORY" --ref main

  product_work_audit_review:
    name: PRODUCT DIRECTOR — WORK AUDIT REVIEW
    needs: [product_director, product_engineer, product_work_auditor]
    if: needs.product_work_auditor.outputs.gate == 'REVISE' || needs.product_work_auditor.outputs.gate == 'BLOCKED'
    runs-on: ubuntu-latest
    timeout-minutes: 240
    steps:
      - uses: actions/checkout@v6
        with:
          fetch-depth: 0
      - name: Mount rejected/revisable Product work evidence
        shell: bash
        run: |
          git fetch origin "$PRODUCT_BRANCH"
          git switch -C "$PRODUCT_BRANCH" "origin/$PRODUCT_BRANCH"
          for kind in work work-audit; do
            B="cycle/product/${GITHUB_RUN_ID}/$kind"
            git fetch origin "$B:refs/remotes/origin/$B"
            git worktree add --detach "/tmp/spider_product_$kind" "origin/$B"
          done
      - name: Install OpenCode
        shell: bash
        run: curl --retry 3 --retry-all-errors --retry-delay 15 -fsSL https://opencode.ai/install | bash
      - name: Review independent Product work rejection
        shell: bash
        run: |
          bash .github/scripts/run-opencode-with-retry.sh run --model "$SPIDER_MODEL" --agent product_director \
            "Review Product work ${{ needs.product_director.outputs.work_id }} after independent gate=${{ needs.product_work_auditor.outputs.gate }}. Candidate=/tmp/spider_product_work; Audit=/tmp/spider_product_work-audit. Do not integrate it. Preserve required fixes/blocker and negative evidence, clear stale work_launch, and decide the next bounded repair/rearchitecture/evidence action without claiming a Product win."
      - name: Advance Product state and launch next decision cycle
        shell: bash
        env:
          GH_TOKEN: ${{ github.token }}
        run: |
          git config user.name spider-product-director
          git config user.email spider-product-director@autonomous.local
          git add -A
          git commit -m "Product work audit review ${GITHUB_RUN_ID}" || true
          git push origin "HEAD:refs/heads/$PRODUCT_BRANCH"
          gh workflow run product-loop.yml --repo "$GITHUB_REPOSITORY" --ref main
'''
    t = t.replace(marker, jobs + marker, 1)

p.write_text(t)
