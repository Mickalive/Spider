# NEXT RUN — COMPATIBILITY HANDOFF

SPIDER no longer has one global research cycle in which Graph, Physics and one Auditor all wait for each other.

Use the lane handoffs instead:

- Graph: `docs/NEXT_GRAPH.md` + `directives/GRAPH.md`
- Physics: `docs/NEXT_PHYSICS.md` + `directives/PHYSICS.md`
- Common audit standard: `directives/AUDITOR.md`
- Lane Director contract: `directives/LANE_DIRECTOR.md`
- Global snapshot/meta integration: `directives/LAB_DIRECTOR.md`

## CURRENT ACCEPTED STATUS

Graph: PROOF OF CONCEPT only. Exact matched replay removed novel decisions/actions in the tested scripted routes; ~69.6% composition reuse remains a small hand-structured POC; the old 8.5x wall-clock claim is withdrawn.

Physics: historical WP-003 is MEASUREMENT_INVALID because of target leakage, invalid uncertainty construction and non-deterministic process hashing. Its numerical falsification claim is not accepted evidence.

## EXECUTION MODEL

Graph lane:

TEAM GRAPH -> GRAPH AUDIT -> GRAPH LANE DIRECTOR -> optional immediate next Graph cycle

Physics lane:

TEAM PHYSICS -> PHYSICS AUDIT -> PHYSICS LANE DIRECTOR -> optional immediate next Physics cycle

The two lanes do not wait for each other.
They advance on persistent accepted branches `lab/graph` and `lab/physics`.

`main` is only the human-reviewed stable snapshot.
The global Lab Director / Meta-Director may periodically reconcile the latest accepted lane snapshots without blocking either lane.

Historical invalid artifacts remain provenance and must not be rewritten into clean-looking history.