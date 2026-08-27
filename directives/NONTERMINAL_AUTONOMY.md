# HUMAN-AUTHORIZED NONTERMINAL AUTONOMY AMENDMENT

This file records the human-authorized operational interpretation adopted on 2026-08-27.

Until `lab/product:state/product_final.json` satisfies the Final Product gate, SPIDER is non-terminal by default.

A local research or engineering **program** may end because it is complete, falsified, blocked, exhausted, data-limited, or marked `continue=false`. That local stop does **not** terminate its lane. The control plane must preserve the result and then repair the same frozen cycle when the independent gate is `REVISE`, or select/re-charter a genuinely different bounded question when the prior program is `BLOCKED`, falsified, complete, exhausted, or otherwise locally terminal.

No failure may be rewritten as success merely to preserve liveness. `PASS`, `REVISE`, `BLOCKED`, negative results, falsifications, invalid measurements and operational failures retain their exact provenance and claim ceilings.

The only autonomous terminal condition is the Final Product gate defined in `docs/roles/PRODUCT_FINAL_GATE.md`: a real agent-facing executable product, independently audited, with a credible audited baseline win, durable evidence, installation/tests, recovery behavior and documented limits, represented by `state/product_final.json` on `lab/product`.

Provider/model availability is operational infrastructure, never scientific evidence. A model outage pauses physical execution only as long as no healthy free model is available; it must not terminate a lane or change a scientific/product verdict.

This amendment resolves the older wording in the autonomous relaunch section of `SPIDER_MASTER_PROMPT.md`: references there to “stop the lane” are to be read as **stop the current local program and replan the lane**, unless the Final Product gate is satisfied.
