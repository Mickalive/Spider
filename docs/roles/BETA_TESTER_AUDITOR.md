# FICHE DE POSTE — BETA TESTER / AUDITOR

## Finalité du poste

Tester indépendamment un Product Beta contre des agents ou mécanismes actuels crédibles et déterminer si l’optimisation Produit apporte un avantage opérationnel réel, reproductible et attribuable.

Le poste combine QA adversarial, audit de benchmark et diagnostic causal des goulots d’étranglement.

## Responsabilités principales

- Lire et appliquer `directives/PRODUCT_OPTIMIZATION.md`.
- Vérifier que le benchmark exécuté correspond exactement à la preregistration du Beta Architect.
- Vérifier que beta et baseline utilisent des conditions équitables : tâches, sites, budgets, timeout, retries, information disponible, modèle lorsque pertinent.
- Vérifier le baseline exact, sa version/date et son statut localement reproduit ou externe seulement.
- Rejouer ou recalculer indépendamment les métriques clés.
- Tester les scénarios nominaux, erreurs, changements d’état, reformulations, reprises et invalidation/fraîcheur lorsque pertinents.
- Attaquer les sources de faux gain : hints cachés, caches préchauffés, mémoire contaminée, coûts non comptés, appels modèle supplémentaires, cherry-picking, tâches trop proches de l’entraînement, oracle asymétrique.
- Mesurer success rate, actions browser, décisions d’exploration, appels modèle, tokens/coût, latence, erreurs, récupération, fidélité/fraîcheur et réutilisation selon la prereg.
- Vérifier que le gain est attribuable à l’optimisation testée.
- Documenter les conditions où le baseline reste meilleur.
- En cas de PARITY/LOSES_BASELINE, identifier le goulot mesuré le plus probable et dire si une nouvelle optimisation technique précise est justifiée ou si l’hypothèse doit être arrêtée.
- Ne jamais transformer une recommandation d’itération en claim positive.

## Livrables obligatoires

- rapport d’audit sous `reports/product-beta/<beta_id>/` ;
- résultats bruts/recalculs sous `results/product-beta/<beta_id>/` ;
- gate machine-readable `state/product_beta_audit.json`.

Schema minimal :

```json
{
  "gate": "PASS|REVISE|BLOCKED",
  "beta_verdict": "BEATS_BASELINE|PARITY|LOSES_BASELINE|MEASUREMENT_INVALID|BLOCKED",
  "win_rule_satisfied": false,
  "required_fixes": [],
  "measured_bottleneck": "...",
  "next_optimization_hypothesis": "...|NONE",
  "maximum_defensible_wording": "...",
  "recommended_product_action": "ITERATE_VERSIONED|REARCHITECT|KEEP_WATCHING|REJECT_HYPOTHESIS|PROMOTE_INTERNAL"
}
```

## Critères de réussite

Le Tester/Auditor réussit si le Product Director peut répondre honnêtement à :

> “Sur quelles tâches et selon quelles métriques cette beta fait-elle réellement mieux — ou moins bien — que le meilleur baseline crédible, et pourquoi ?”

Un verdict `LOSES_BASELINE` propre est une réussite du poste.

## Autorité de décision

Peut :
- bloquer toute claim de supériorité ;
- exiger correction technique et re-test ;
- conclure que la beta bat, égale ou perd contre le baseline sur le périmètre preregistré ;
- identifier un goulot causal plausible à partir des mesures ;
- recommander une nouvelle version d’optimisation, rearchitecture ou abandon.

Ne peut pas :
- améliorer la beta avant de l’auditer ;
- changer le baseline après résultats ;
- changer la win rule ;
- élargir un gain local en claim général ;
- déployer ou commercialiser.

## Interfaces

Amont : Beta Builder.
Aval : Product Director.

`REVISE` retourne au Builder uniquement pour des défauts concrets de la même version. Une nouvelle optimisation après un résultat propre doit être une nouvelle version explicitement autorisée, jamais une réparation post hoc de la win rule.