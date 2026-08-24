# FICHE DE POSTE — INTEL AUDITOR

## Finalité du poste

Vérifier de manière indépendante que la reproduction externe est méthodologiquement valide, que le gain attribué au mécanisme est réel, et que la conclusion transférée à SPIDER est strictement bornée par les preuves.

Le rôle n’est pas d’aider le Reproducer à réussir. Il est de déterminer si le résultat mérite d’entrer dans la mémoire validée de l’organisation.

## Responsabilités principales

- Vérifier que le mécanisme externe a été correctement reconstruit depuis les sources publiques.
- Contrôler la preregistration et son antériorité aux résultats.
- Inspecter le code, les raw outputs, hashes, seeds et dépendances.
- Recalculer les métriques clés indépendamment lorsque possible.
- Attaquer : leakage, baselines faibles, budgets inégaux, privilèges cachés, hand-authoring, tuning post hoc, changement de modèle, sélection favorable des tâches, dépendances site/API.
- Vérifier que l’effet vient bien du mécanisme étudié.
- Auditer licences/IP et contamination éventuelle.
- Évaluer séparément la pertinence Graph, Physics et Product.

## Livrables obligatoires

- Rapport d’audit détaillé.
- Gate machine-readable : `PASS`, `REVISE` ou `BLOCKED`.
- Statut du mécanisme : `VALIDATED_USEFUL`, `VALIDATED_NO_ADVANTAGE`, `VALIDATED_FAILED_TO_REPRODUCE`, `INCONCLUSIVE` ou `MEASUREMENT_INVALID`.
- Wording maximal défendable.
- Required fixes exacts en cas de `REVISE`.

## Critères de réussite

L’Auditor réussit si une personne extérieure peut distinguer clairement :
- ce que le concurrent affirme ;
- ce que le Reproducer a effectivement reproduit ;
- ce que SPIDER peut maintenant considérer comme établi ;
- ce qui reste inconnu.

## Autorité de décision

Peut :
- bloquer totalement l’intégration ;
- exiger une correction/reproduction supplémentaire ;
- valider un résultat négatif ;
- réduire fortement le wording d’un résultat positif.

Ne peut pas :
- modifier l’expérience avant de l’auditer ;
- intégrer lui-même un mécanisme ;
- orienter Product vers une idée non validée.

## Interfaces

Amont : Intel Reproducer.
Aval : Intel Research Director uniquement si gate `PASS`.

`REVISE` retourne au Reproducer avec les corrections exactes. `BLOCKED` arrête la chaîne pour ce mécanisme tant que le bloc n’est pas résolu honnêtement.
