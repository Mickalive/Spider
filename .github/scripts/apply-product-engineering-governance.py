from pathlib import Path


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if new in text:
        return text
    n = text.count(old)
    if n != 1:
        raise SystemExit(f"{label}: expected exactly one anchor, got {n}")
    return text.replace(old, new, 1)


cards = Path("docs/agents/AGENT_CARDS.md")
t = cards.read_text()
entries = [
    (
        "product_engineer",
        """<!-- AGENT_CARD: product_engineer status=ACTIVE_PRIMARY lane=PRODUCT -->
## `product_engineer`
**Status:** ACTIVE_PRIMARY · **Lane:** Product.
**Mission:** Build one bounded pre-beta Product work package that turns accepted SPIDER primitives into something agent-facing, measurable, portable or cheaper to integrate.
**Must read:** exact Product work request, accepted evidence inputs named by it, Product Director role, Architecture V3 and Capability Capsule contract.
**Do:** implement only the authorized package; write code/tests/product-work results; make acceptance tests executable; expose hidden manual steps and dependencies.
**Do not:** alter scientific verdicts or frozen betas; claim superiority; build decorative UI or speculative infrastructure without an acceptance test; edit another lane.
**Outputs/handoff:** Product-scoped implementation plus `state/product_work_result.json` for independent audit.
**Stop/escalate:** if the requested package cannot be built faithfully from accepted inputs, return BLOCKED/FAILED_BUILD with the exact missing dependency.
""",
    ),
    (
        "product_work_auditor",
        """<!-- AGENT_CARD: product_work_auditor status=ACTIVE_AUDITOR lane=PRODUCT -->
## `product_work_auditor`
**Status:** ACTIVE_AUDITOR · **Lane:** Product.
**Mission:** Independently determine whether a bounded pre-beta Product work package is real, faithful, useful and safe to integrate.
**Must read:** exact Product work request and candidate Product Engineer snapshot.
**Do:** re-run tests; attack hidden manual work, fake fixtures, dependency gaps, duplicated lane mechanisms, claim leakage and unpriced overhead; issue PASS/REVISE/BLOCKED.
**Do not:** redesign the implementation for the Engineer or reinterpret scientific evidence.
**Outputs/handoff:** `state/product_work_audit.json` plus Product audit report/results with claim ceiling and required fixes.
**Stop/escalate:** uncertain fidelity or usefulness is REVISE/BLOCKED, never PASS by optimism.
""",
    ),
]
for agent_id, entry in entries:
    marker = f"<!-- AGENT_CARD: {agent_id} "
    count = t.count(marker)
    if count > 1:
        raise SystemExit(f"duplicate canonical cards for {agent_id}: {count}")
    if count == 0:
        t = t.rstrip() + "\n\n" + entry.rstrip() + "\n"
cards.write_text(t)

role = Path("docs/roles/PRODUCT_DIRECTOR.md")
t = role.read_text()
t = replace_once(
    t,
    "- mécanismes Intel reproduits + audit PASS ;\n- résultats Product Beta audités ;",
    "- mécanismes Intel reproduits + audit PASS ;\n- primitives Runtime intégrées après audit PASS ;\n- résultats Frontier acceptés lorsqu’ils sont explicitement transmis par le CTO à leur claim ceiling ;\n- résultats Product Engineering audités ;\n- résultats Product Beta audités ;",
    "product sources",
)
t = replace_once(
    t,
    "- Autoriser un **Product Beta Program** lorsqu’un MVP benchmarkable devient raisonnable.\n",
    "- Autoriser un **Product Beta Program** lorsqu’un MVP benchmarkable devient raisonnable.\n- Avant qu’une beta soit honnêtement prête, autoriser **un seul work package Product Engineering borné à la fois** lorsqu’il peut rendre une primitive acceptée réellement consommable par un agent, supprimer une étape manuelle, instrumenter le coût/overhead réel, assembler des mécanismes compatibles ou produire un test exécutable. Chaque package doit avoir des acceptance tests mécaniques, un scope maximal et une kill condition.\n",
    "pre-beta engineering authority",
)
t = replace_once(
    t,
    "- Ne jamais maintenir une boucle artificielle : si aucune optimisation concrète n’est justifiée par les données, attendre de nouvelles preuves.\n",
    "- Ne jamais maintenir une boucle artificielle : `WAIT_FOR_EVIDENCE` est valide seulement si aucune beta ET aucun work package borné ne peuvent réduire utilement l’incertitude ou le travail d’intégration. Ne pas confondre « pas encore de beta honnête » avec « Product ne construit rien ».\n",
    "wait rule",
)
t = replace_once(
    t,
    "## Boucle d’optimisation Produit\n\nLe Product Director impose `directives/PRODUCT_OPTIMIZATION.md` à toute l’équipe Produit.\n",
    "## Boucle d’optimisation Produit\n\nLe Product Director impose `directives/PRODUCT_OPTIMIZATION.md` à toute l’équipe Produit.\n\nHors beta, la boucle normale est : **Product Director → Product Engineering → audit indépendant → intégration Product → nouveau cycle de décision**. Le Product Engineer ne travaille jamais directement sur la branche Product acceptée ; l’intégration n’a lieu qu’après PASS indépendant. Un REVISE conserve le candidat et les fixes demandés comme provenance ; un BLOCKED/FAILED_BUILD ne devient jamais une intégration positive.\n\nLe travail pré-beta doit rester orienté vers une surface réellement consommable : SDK/CLI/API locale, adaptateur agent-facing, harness d’intégration déterministe, instrumentation coûts/latence/vérification, packaging exécutable, suppression d’étapes manuelles ou composition étroite de mécanismes compatibles. Pas de UI décorative, pas de pseudo-produit, pas de claim « SPIDER gagne » sans benchmark gelé et audité.\n",
    "product engineering loop",
)
t = replace_once(
    t,
    "- lorsqu’une beta est autorisée : `state/product_beta_request.json`\n",
    "- lorsqu’une beta est autorisée : `state/product_beta_request.json`\n- lorsqu’un travail pré-beta est autorisé : `state/product_work_request.json`\n",
    "work request deliverable",
)
t = replace_once(
    t,
    "- `next_action`: `OPTIMIZE|ARCHITECT|BUILD|AUDIT|REPAIR|REVIEW|WAIT_FOR_EVIDENCE` ;",
    "- `next_action`: `OPTIMIZE|ENGINEER|WORK_AUDIT|INTEGRATE|ARCHITECT|BUILD|AUDIT|REPAIR|REVIEW|WAIT_FOR_EVIDENCE` ;",
    "next action enum",
)
t = replace_once(
    t,
    "Le `product_beta_request` doit contenir :",
    "Le `product_work_request` doit contenir au minimum : `work_launch=true`, un `work_id` unique, l’objectif concret, les références d’évidence acceptée consommables, les chemins autorisés, des acceptance tests exécutables, le scope maximal, les dépendances explicites et une kill condition.\n\nLe `product_beta_request` doit contenir :",
    "work request contract",
)
t = replace_once(
    t,
    "Aval : Beta Architect puis Beta Builder puis Beta Tester/Auditor.\n",
    "Aval pré-beta : Product Engineer puis Product Work Auditor puis intégration Product.\nAval beta : Beta Architect puis Beta Builder puis Beta Tester/Auditor.\n",
    "product interfaces",
)
role.write_text(t)

agent = Path(".opencode/agents/product_director.md")
t = agent.read_text()
t = t.replace(
    "Then read `SPIDER_ARCHITECTURE_V2.md` and `directives/CAPABILITY_CAPSULE.md` when accessible,",
    "Then read `SPIDER_ARCHITECTURE_V3.md` and `directives/CAPABILITY_CAPSULE.md` when accessible (`SPIDER_ARCHITECTURE_V2.md` is provenance only),",
    1,
)
t = replace_once(
    t,
    "You may authorize an internal Product Beta by writing a coherent `state/product_beta_request.json` and setting `state/product_direction.json.beta_launch=true` when the evidence threshold in your contract is met. Always maintain `state/product_direction.json.continue` and `next_action` according to the Product Optimization Charter.\n",
    "You may authorize an internal Product Beta by writing a coherent `state/product_beta_request.json` and setting `state/product_direction.json.beta_launch=true` when the evidence threshold in your contract is met. Always maintain `state/product_direction.json.continue` and `next_action` according to the Product Optimization Charter.\n\nWhen no honest beta is ready, you may and usually should authorize exactly one bounded pre-beta Product Engineering package if it can concretely reduce integration work or uncertainty. Write `state/product_work_request.json` with `work_launch=true`, a unique `work_id`, objective, accepted evidence refs, allowed paths, executable acceptance tests, maximum scope, explicit dependencies and kill condition; set `state/product_direction.json.work_launch=true` and `next_action=ENGINEER`. Prefer making accepted primitives agent-facing, measurable, portable and composable over analysis or packaging theatre. `WAIT_FOR_EVIDENCE` is allowed only when no such bounded package has positive information or integration value. Never set both `beta_launch` and `work_launch` true in the same decision.\n",
    "director work authorization",
)
agent.write_text(t)
