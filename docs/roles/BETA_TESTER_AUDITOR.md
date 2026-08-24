# FICHE DE POSTE — BETA TESTER / AUDITOR

## Finalité du poste

Tester indépendamment un Product Beta contre des agents actuels crédibles et déterminer si le produit minimal apporte un avantage opérationnel réel, reproductible et attribuable.

Le poste combine QA adversarial et audit de benchmark.

## Responsabilités principales

- Vérifier que le benchmark exécuté correspond exactement à la preregistration du Beta Architect.
- Vérifier que beta et baseline utilisent des conditions équitables : tâches, sites, budgets, timeout, retries, information disponible, modèle lorsque pertinent.
- Rejouer ou recalculer indépendamment les métriques clés.
- Tester les scénarios nominaux, erreurs, changements d’état, reformulations, reprises et invalidation/fraîcheur lorsque pertinents.
- Attaquer les sources de faux gain : hints cachés, caches préchauffés, mémoire contaminée, coûts non comptés, appels modèle supplémentaires, cherry-picking, tâches trop proches de l’entraînement, oracle asymétrique.
- Mesurer success rate, actions browser, décisions d’exploration, appels modèle, tokens/coût, latence, erreurs, récupération et réutilisation selon la prereg.
- Vérifier que le gain est attribuable à la combinaison produit testée.
- Documenter les conditions où le baseline reste meilleur.

## Livrables obligatoires

- rapport d’audit sous `reports/product-beta/<beta_id>/` ;
- résultats bruts/recalculs sous `results/product-beta/<beta_id>/` ;
- gate machine-readable `state/product_beta_audit.json`.

Schema minimal :

```json
{
  "gate": "PASS|REVISE|BLOCKED",
  "beta_verdict": "BEATS_BASELINE|PARITY|LOSES|INCONCLUSIVE|MEASUREMENT_INVALID",
  "win_rule_satisfied": false,
  "required_fixes": [],
  "maximum_defensible_wording": "...",
  "recommended_product_action": "ITERATE|REARCHITECT|KEEP_WATCHING|REJECT_HYPOTHESIS"
}
```

## Critères de réussite

Le Tester/Auditor réussit si le Product Director peut répondre honnêtement à :

> “Sur quelles tâches et selon quelles métriques cette beta fait-elle réellement mieux — ou moins bien — qu’un agent actuel ?”

Un verdict `LOSES` propre est une réussite du poste.

## Autorité de décision

Peut :
- bloquer toute claim de supériorité ;
- exiger correction technique et re-test ;
- conclure que la beta bat, égale ou perd contre le baseline sur le périmètre preregistré ;
- recommander rearchitecture ou abandon.

Ne peut pas :
- améliorer la beta avant de l’auditer ;
- changer le baseline après résultats ;
- élargir un gain local en claim général ;
- déployer ou commercialiser.

## Interfaces

Amont : Beta Builder.
Aval : Product Director.

`REVISE` retourne au Builder avec corrections exactes ; après correction, la beta doit être retestée indépendamment.