from pathlib import Path
import re

lane_files = {
    Path('.github/workflows/graph-loop.yml'): 3,
    Path('.github/workflows/physics-loop.yml'): 3,
    Path('.github/workflows/meta-sync.yml'): 1,
}

pattern = re.compile(
    r'''(?ms)^      - name: Add OpenCode to PATH with transient network retry\n'''
    r'''        shell: bash\n'''
    r'''        run: \|\n'''
    r'''          echo "\$HOME/\.opencode/bin" >> "\$GITHUB_PATH"\n'''
    r'''          cat >> "\$BASH_ENV" <<'SPIDER_OPENCODE_RETRY'\n'''
    r'''          opencode\(\) \{\n'''
    r'''.*?'''
    r'''^          SPIDER_OPENCODE_RETRY\n'''
)

replacement = '''      - name: Add OpenCode to PATH with bounded local retry
        shell: bash
        run: |
          echo "$HOME/.opencode/bin" >> "$GITHUB_PATH"
          cat >> "$BASH_ENV" <<'SPIDER_OPENCODE_RETRY'
          opencode() {
            local real="$HOME/.opencode/bin/opencode"
            local log rc attempt
            local max_attempts=6
            local retry_delay=300
            log="$(mktemp)"
            for ((attempt = 1; attempt <= max_attempts; attempt++)); do
              : > "$log"
              echo "OpenCode/Ox attempt ${attempt}/${max_attempts}."
              set +e
              "$real" "$@" 2>&1 | tee "$log"
              rc=${PIPESTATUS[0]}
              set -e
              if [ "$rc" -eq 0 ]; then
                rm -f "$log"
                return 0
              fi
              if ! grep -Eiq '(network_error|NetworkError|network error|fetch failed|APIConnectionError|ECONNRESET|ECONNREFUSED|EAI_AGAIN|ENETUNREACH|ENOTFOUND|ETIMEDOUT|timed out|timeout|socket hang up|connection (reset|refused|closed|error)|upstream.*(reset|closed|unavailable|error)|HTTP[^0-9]*(429|500|502|503|504)|status[^0-9]*(429|500|502|503|504)|too many requests|rate.?limit|service unavailable|bad gateway|gateway timeout|temporar(y|ily) unavailable|TLS|SSL.*error)' "$log"; then
                echo "::error::SPIDER_OX_NONTRANSIENT exit=$rc; watchdog will not retry this failure." >&2
                rm -f "$log"
                return "$rc"
              fi
              if [ "$attempt" -eq "$max_attempts" ]; then
                echo "::error::SPIDER_TRANSIENT_OX_EXHAUSTED attempts=$max_attempts exit=$rc" >&2
                rm -f "$log"
                return "$rc"
              fi
              echo "::warning::Transient OpenCode/Ox outage; retrying in ${retry_delay}s." >&2
              sleep "$retry_delay"
            done
          }
          SPIDER_OPENCODE_RETRY
'''

for path, expected in lane_files.items():
    text = path.read_text()
    text, count = pattern.subn(replacement, text)
    if count != expected:
        raise SystemExit(f'{path}: expected {expected} retry blocks, patched {count}')
    path.write_text(text)

graph = Path('.github/workflows/graph-loop.yml')
text = graph.read_text()
for old, new in {
    "    if: always() && needs.team_graph.result != 'cancelled'": "    if: needs.team_graph.result == 'success'",
    "    if: always() && needs.audit_graph.result != 'cancelled'": "    if: needs.audit_graph.result == 'success'",
}.items():
    if text.count(old) != 1:
        raise SystemExit(f'graph condition mismatch: {old}')
    text = text.replace(old, new)
old_push = '          git push --force origin "HEAD:refs/heads/$BRANCH"'
if text.count(old_push) != 2:
    raise SystemExit('graph push count mismatch')
text = text.replace(old_push, '          ATTEMPT_BRANCH="${BRANCH}-attempt-${GITHUB_RUN_ATTEMPT}"\n          git push --force origin "HEAD:refs/heads/$ATTEMPT_BRANCH"\n          git push --force origin "HEAD:refs/heads/$BRANCH"')
graph.write_text(text)

physics = Path('.github/workflows/physics-loop.yml')
text = physics.read_text()
for old, new in {
    "    if: always() && needs.team_physics.result != 'cancelled'": "    if: needs.team_physics.result == 'success'",
    "    if: always() && needs.audit_physics.result != 'cancelled'": "    if: needs.audit_physics.result == 'success'",
}.items():
    if text.count(old) != 1:
        raise SystemExit(f'physics condition mismatch: {old}')
    text = text.replace(old, new)
if text.count(old_push) != 2:
    raise SystemExit('physics push count mismatch')
text = text.replace(old_push, '          ATTEMPT_BRANCH="${BRANCH}-attempt-${GITHUB_RUN_ATTEMPT}"\n          git push --force origin "HEAD:refs/heads/$ATTEMPT_BRANCH"\n          git push --force origin "HEAD:refs/heads/$BRANCH"')
physics.write_text(text)

for p, n in {
    '.github/workflows/graph-loop.yml': 3,
    '.github/workflows/physics-loop.yml': 3,
    '.github/workflows/meta-sync.yml': 1,
}.items():
    t = Path(p).read_text()
    assert t.count('SPIDER_TRANSIENT_OX_EXHAUSTED') == n
    assert t.count('local max_attempts=6') == n
    assert t.count('local retry_delay=300') == n

assert "if: needs.team_graph.result == 'success'" in graph.read_text()
assert "if: needs.audit_graph.result == 'success'" in graph.read_text()
assert "if: needs.team_physics.result == 'success'" in physics.read_text()
assert "if: needs.audit_physics.result == 'success'" in physics.read_text()

Path('.github/workflows/_install-ox-watchdog-hardening.yml').unlink(missing_ok=True)
Path('.github/scripts/install-ox-watchdog-hardening.py').unlink(missing_ok=True)
Path('.spider/maintenance/install-ox-watchdog.json').unlink(missing_ok=True)
print('SPIDER Ox watchdog hardening installed successfully')
