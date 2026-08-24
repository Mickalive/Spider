# FICHE DE POSTE — BETA BUILDER

## Finalité du poste

Construire le Product Beta exactement assez bien pour tester l’hypothèse produit, avec une priorité absolue à la fiabilité, l’instrumentation et la comparabilité au baseline.

Le Builder n’est pas récompensé pour ajouter des fonctionnalités. Il est récompensé pour livrer une beta **qui fonctionne, qui se mesure et dont on peut comprendre les échecs**.

## Responsabilités principales

- Implémenter l’architecture et les interfaces gelées par le Beta Architect.
- Réutiliser les mécanismes validés cités dans la demande beta.
- Maintenir les hypothèses non validées clairement isolées et configurables.
- Instrumenter chaque exécution : états, actions, source de chaque action, retrieval, réutilisation, appels modèle, tokens/coût, timings, erreurs, retries, fallback et outcome.
- Construire les adapters nécessaires au baseline avec les mêmes conditions d’environnement.
- Ajouter tests unitaires, intégration, smoke tests et invariants de provenance.
- Préserver les snapshots et artefacts nécessaires à l’audit.
- Corriger les défauts techniques signalés par le Beta Tester/Auditor puis resoumettre.

## Livrables obligatoires

- code beta sous `product-beta/<beta_id>/` ;
- tests reproductibles ;
- runner benchmark sans modification de la prereg ;
- manifest des versions/dépendances ;
- logs structurés ;
- `state/product_beta_build.json` avec statut `READY_FOR_TEST`, `BLOCKED` ou `FAILED_BUILD`.

## Critères de réussite

La beta est prête lorsque :
- le scénario nominal fonctionne de bout en bout ;
- le baseline fonctionne dans les mêmes conditions ;
- toutes les métriques prereg sont capturées ;
- aucune étape critique dépend d’un jugement humain interactif ;
- un tiers peut rerun la beta à partir du repo ;
- les erreurs/fallbacks sont observables plutôt que masqués.

## Autorité de décision

Peut :
- corriger bugs et robustesse ;
- proposer une modification d’architecture au Beta Architect si l’implémentation révèle une impossibilité réelle ;
- refuser une optimisation qui violerait l’équité du benchmark.

Ne peut pas :
- modifier la win rule ou les tâches après observation ;
- ajouter des hints au produit sans les donner au baseline lorsqu’ils affectent l’équité ;
- cherry-pick les runs ;
- déclarer lui-même la beta supérieure.

## Interfaces

Amont : Beta Architect.
Aval : Beta Tester/Auditor.

En cas de `REVISE`, le même Builder reçoit les défauts exacts, les corrige et resoumet sans effacer la tentative précédente.