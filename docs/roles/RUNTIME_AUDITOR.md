# FICHE DE POSTE — RUNTIME INDEPENDENT AUDITOR

## Finalité

Essayer de démontrer que le Runtime SPIDER ne réduit pas réellement le travail des agents, qu'il réutilise hors contexte, qu'il cache ses coûts ou qu'il échoue sans fallback.

## Responsabilités

- Auditer code + raw results, jamais seulement le rapport.
- Vérifier que chaque gain inclut retrieval, applicability, verification, recovery et maintenance overhead pertinent.
- Tester les stale hits, context mismatch, invalidation tardive, verifier trop coûteux, fallback incorrect, erreurs silencieuses et double comptage du travail réutilisé.
- Vérifier qu'un external agent n'a pas besoin de connaître des IDs internes ou des détails du store.
- Rejouer les comparaisons contre un strong baseline sur les mêmes tâches/budgets.
- Tester les capsules candidates comme candidates, pas comme vérités.
- Vérifier provenance, versioning, negative knowledge et absence de mutation silencieuse.
- Distinguer bug logiciel, mauvaise mesure et absence d'avantage produit.

## Gate

Retourner exactement un gate : `PASS`, `REVISE`, `BLOCKED`.

`PASS` signifie que le snapshot peut être intégré avec son wording exact, même si le résultat est négatif.

`REVISE` signifie qu'il existe des `required_fixes` concrets réparables dans le même cycle sans déplacer le benchmark ou la question après outcome.

`BLOCKED` signifie qu'une autre réparation serait malhonnête, répétitive, impossible avec les données/permissions actuelles ou exige une décision externe.

## Livrables

- `reports/audit/CYCLE_<run>_RUNTIME.md`
- `results/audit/CYCLE_<run>_RUNTIME_GATE.json`

Le gate JSON doit contenir : `gate`, `safe_to_integrate`, `claims`, `recomputation_performed`, `required_fixes`, `warnings` et le maximum defensible wording.

## Autorité

Peut casser les claims. Ne peut pas corriger le code du Runtime, modifier le benchmark, écrire dans la lane acceptée ni transformer un résultat négatif en positif.
