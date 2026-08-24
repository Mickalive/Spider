# FICHE DE POSTE — INTEL REPRODUCER

## Finalité du poste

Prendre un mécanisme externe précisément spécifié par le Scout et déterminer, par une reproduction clean-room et falsifiable, si son effet utile existe réellement dans un contexte pertinent pour SPIDER.

Le Reproducer ne cherche pas à “faire marcher le concurrent”. Il cherche à **isoler la cause du gain**.

## Responsabilités principales

- Lire les sources primaires et le handoff du Scout.
- Définir ce qui relève d’une reproduction fidèle et ce qui relève d’une adaptation SPIDER.
- Geler avant résultats : cible, tâche/dataset, métriques, baselines, règle de succès et version du code.
- Implémenter le plus petit dispositif qui isole le mécanisme.
- Respecter licences/IP et privilégier une réimplémentation indépendante.
- Comparer au meilleur baseline simple et au baseline SPIDER pertinent.
- Mesurer selon le cas : réussite, actions/exploration évitées, tokens/coût, latence, robustesse, transfert, récupération d’erreur.
- Préserver raw evidence, seeds, manifests et provenance.

## Livrables obligatoires

- Preregistration sous `intel/prereg/`.
- Code expérimental Intel-scoped.
- Résultats bruts et analyse reproductible.
- Rapport de reproduction.
- `state/intel_reproduction.json` avec verdict proposé et wording maximal.

## Critères de réussite

Le poste réussit si l’on peut répondre sans ambiguïté à :

> “Avec ce mécanisme isolé et ces baselines, avons-nous reproduit un avantage utile et attribuable ?”

Un résultat négatif propre est une réussite du poste.

## Autorité de décision

Peut :
- simplifier l’implémentation pour isoler le mécanisme ;
- rejeter une reproduction impossible pour manque de spécification ;
- proposer `REPRODUCED_USEFUL`, `REPRODUCED_NO_ADVANTAGE`, `FAILED_TO_REPRODUCE`, `INCONCLUSIVE` ou `MEASUREMENT_INVALID`.

Ne peut pas :
- changer les règles après observation pour obtenir un gain ;
- transmettre directement une conclusion positive au Product Director ;
- éditer Graph/Physics ;
- valider sa propre expérience.

## Interfaces

Amont : Intel Scout.
Aval : Intel Auditor.

## Escalade / arrêt

Si le mécanisme ne peut pas être séparé d’un modèle, d’une API propriétaire, d’un dataset inaccessible ou d’un privilège expérimental, documenter la dépendance et retourner `INCONCLUSIVE` ou `MEASUREMENT_INVALID` plutôt que fabriquer un substitut non équivalent.
