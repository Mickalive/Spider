# COMMIT-SCOPE DISCLOSURE — R0-2 (run 32908002333)

Status: provenance disclosure by runtime_runner. No action requested.

Commit `8ed968d` ("R0-2 harness v2") contains, BESIDES the intended
Runtime lane files (runtime/, tests/runtime/, tools/), 18 repository-level
control-plane documents that were ALREADY STAGED IN THE GIT INDEX when the
session started (environment-provisioned V3 control-plane overlay):
`.opencode/agents/*`, `AGENTS.md`, `SPIDER_ARCHITECTURE_V3.md`,
`docs/agents/AGENT_CARDS.md`, `directives/LAB_DIRECTOR.md`,
`directives/LANE_DIRECTOR.md`, `docs/roles/*`.

Facts for auditors:
1. None of these files are Runtime-lane evidence or other-lane evidence;
   they contain no outcomes, no results, no lane ledgers.
2. They were staged by the orchestration environment before substantive
   work began; the runner's commit (made with explicit `git add` of its
   own files) also flushed the pre-existing index contents.
3. The runner did not author or modify these documents in this session.
4. Rewriting pushed history to strip them was rejected: force-push is out
   of bounds without explicit authorization. This note is the durable
   disclosure instead.

Commits `42eb66d` (frozen prereg + probe evidence) and `e172e16`
(outcomes) contain exactly their intended path scopes.
