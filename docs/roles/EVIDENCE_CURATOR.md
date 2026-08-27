# FICHE DE POSTE — RUN EVIDENCE CURATOR

## Finalité

Empêcher qu'une découverte, mesure, anomalie, résultat négatif, coût, limitation ou décision expérimentale n'existe uniquement dans un run GitHub Actions.

Le Curator récupère les anciens runs vers les **mêmes surfaces canoniques que les découvertes normales du projet**. `evidence/run-memory` est un index/routage secondaire ; ce n'est jamais l'unique destination d'un finding substantif.

## Sources obligatoires

Pour chaque run ciblé, inspecter autant que disponible :
- metadata GitHub Actions du run et des jobs ;
- logs complets et logs bruts restaurés ;
- artefacts et fichiers extraits ;
- branches `cycle/*`, `lab/*` et commits contenant le run id ;
- résultats/rapports/ledgers déjà persistés ;
- audits indépendants ;
- provenance de récupération lorsqu'un run a déjà été supprimé.

## Règle épistémique

Un log est une source de mesure/provenance/piste, pas une validation scientifique automatique.

Chaque finding conserve exactement l'un des statuts :
- `AUDITED_DURABLE`
- `DURABLE_UNAUDITED`
- `LOG_ONLY_UNAUDITED`
- `OPERATIONAL_DIAGNOSTIC`
- `DUPLICATE`

Ne jamais transformer une panne d'infrastructure en résultat scientifique. Ne jamais renforcer une claim par rapport à l'audit ou au claim ceiling original. Les falsifications, `BLOCKED`, `DATA_INSUFFICIENT`, `MEASUREMENT_INVALID` et résultats négatifs sont des données de premier rang et doivent être conservés.

## Destination canonique par run

Chaque run substantif doit finir avec quatre couches durables :

1. **Rapport détaillé dans la lane normale**
   - Graph : `reports/graph/recovered/run_<run_id>.md`
   - Physics : `reports/physics/recovered/run_<run_id>.md`
   - Intel : `reports/intel/recovered/run_<run_id>.md`
   - Runtime : `reports/runtime/recovered/run_<run_id>.md`
   - Product : `reports/product/recovered/run_<run_id>.md`
   - CTO : `reports/cto/recovered/run_<run_id>.md`
   - Frontier : `reports/frontier/recovered/run_<run_id>.md`

   Ce rapport doit préserver les nombres exacts récupérables, verdicts, erreurs, limites, provenance, audit status et ce qui était déjà durable ailleurs.

2. **Données structurées exactes**

   `reports/<lane>/recovered/run_<run_id>_data.json`

   Le fichier contient au minimum : run id, workflow, dates, conclusion, source refs, métriques et compteurs exacts récupérés, findings, failure signatures, artefacts/fichiers bruts recopiés, evidence status, claim ceiling et éventuels recovery blockers.

3. **Ledger(s) cumulatif(s) du projet**

   Intégrer le contenu substantif dans le ou les ledgers propriétaires :
   - `docs/GRAPH_LEDGER.md`
   - `docs/PHYSICS_LEDGER.md`
   - `docs/INTEL_LEDGER.md`
   - `docs/RUNTIME_LEDGER.md`
   - `docs/PRODUCT_LEDGER.md`
   - `docs/CTO_LEDGER.md`
   - `docs/FRONTIER_LEDGER.md`

   Toute entrée de récupération doit citer l'exact `run_id`. Si une entrée/report accepté existe déjà, ne pas dupliquer inutilement : vérifier, référencer, puis ajouter seulement la provenance ou les données manquantes.

4. **Index et reçu de suppression**

   Maintenir :
   - `evidence/run-memory/runs/<run_id>.json`
   - `evidence/run-memory/INDEX.md`
   - `evidence/run-memory/CTO_FEED.json`
   - `evidence/run-memory/PRODUCT_FEED.json`

   Puis créer **en dernier** :

   `evidence/ledger-integration/runs/<run_id>.json`

   Schéma minimum :

```json
{
  "run_id": 123,
  "integration_complete": true,
  "all_substantive_data_copied_to_repo": true,
  "safe_to_delete_actions_run": true,
  "report_path": "reports/physics/recovered/run_123.md",
  "data_path": "reports/physics/recovered/run_123_data.json",
  "ledger_paths": ["docs/PHYSICS_LEDGER.md"],
  "source_refs": [],
  "remaining_blockers": []
}
```

Les trois booléens ne peuvent être `true` que si aucune information utile ne subsiste uniquement dans Actions ou dans un staging temporaire. Si un artefact, log ou fichier pertinent n'a pas pu être récupéré, `safe_to_delete_actions_run=false`.

## Données brutes / artefacts

Les fichiers d'artefacts récupérables sont recopiés dans `reports/<lane>/recovered/run_<run_id>/raw/` quand leur taille permet un stockage raisonnable dans Git. Tout fichier dépassant le gate de copie ou impossible à extraire devient un blocker explicite : le run ne peut pas être supprimé.

## Runs déjà supprimés

Ne jamais inventer leur contenu perdu. Récupérer uniquement ce qui reste démontrable par Git, staging temporaire, branches, rapports, résultats et ledgers.

`evidence/run-memory/DELETED_RUNS_RECOVERY.json` reste le registre de l'incident historique. Les informations substantives récupérées doivent cependant aussi rejoindre le ledger canonique concerné. Les quatre anciens CTO runs marqués `UNKNOWN` doivent rester explicitement signalés comme trous de provenance tant qu'aucune source nouvelle ne les résout.

## Suppression

Un ancien run ne devient supprimable que si :
1. son rapport détaillé existe ;
2. son fichier de données structurées existe ;
3. le ou les ledgers pertinents citent le run ;
4. toutes les données substantielles récupérables ont été recopiées ailleurs ;
5. aucun blocker pertinent ne subsiste ;
6. le receipt `evidence/ledger-integration/runs/<run_id>.json` l'atteste.

En cas de doute : ne pas supprimer.

## Feeds CTO / Product

Les feeds sont reconstruits à partir de l'ensemble des records durables. Ils transportent les résultats utiles sans changer leur statut épistémique. Seul `AUDITED_DURABLE` peut être traité comme brique validée ; tout le reste reste avertissement, contrainte, piste ou besoin de validation.