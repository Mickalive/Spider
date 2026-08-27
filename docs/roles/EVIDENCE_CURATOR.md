# FICHE DE POSTE — RUN EVIDENCE CURATOR

## Finalité

Empêcher qu'une découverte, mesure, anomalie, résultat négatif, coût, limitation ou décision expérimentale n'existe uniquement dans un run GitHub Actions.

Le Curator récupère les anciens runs vers les **mêmes surfaces canoniques que les découvertes normales du projet**. Il ne crée jamais de silo de récupération parallèle.

## Ontologie de stockage obligatoire

Le repo a quatre couches distinctes :

1. **`results/` = résultats canoniques.** Toute donnée de résultat scientifique, runtime, produit, audit ou frontier vit ici, sous la lane appropriée. C'est l'unique home des résultats.
2. **`reports/` = narration et interprétation.** Un rapport peut expliquer un résultat, mais il ne remplace jamais le fichier résultat canonique.
3. **`docs/*_LEDGER.md` = mémoire cumulative et index raisonné.** Les ledgers résument, relient et bornent les claims ; ils ne sont pas le stockage primaire du résultat.
4. **`evidence/` = provenance.** Logs bruts, metadata Actions, artefacts récupérés, run-memory et receipts de suppression vivent ici.

Il est interdit de créer `reports/<lane>/recovered/` comme second stockage de résultats ou de mettre un JSON de résultat sous `evidence/`.

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

Chaque finding conserve exactement l'un des statuts : `AUDITED_DURABLE`, `DURABLE_UNAUDITED`, `LOG_ONLY_UNAUDITED`, `OPERATIONAL_DIAGNOSTIC`, ou `DUPLICATE`.

Ne jamais transformer une panne d'infrastructure en résultat scientifique. Ne jamais renforcer une claim par rapport à l'audit ou au claim ceiling original. Les falsifications, `BLOCKED`, `DATA_INSUFFICIENT`, `MEASUREMENT_INVALID` et résultats négatifs sont des données de premier rang et doivent être conservés.

## Destination canonique par run

Chaque run substantif doit finir avec quatre couches durables :

### 1. Résultat(s) canonique(s) sous `results/`

- Si le run avait produit un fichier sous `results/<lane>/...` sur une branche encore récupérable, conserver/copier ce fichier tel quel vers `main/results/<lane>/...` quand il n'existe pas déjà.
- Si un chemin identique existe déjà avec le même contenu, le référencer sans duplication.
- Si le même chemin existe avec un contenu différent, préserver l'ancienne variante sous un nom lié au run plutôt que d'écraser silencieusement un résultat canonique plus récent.
- Si la substance n'existe plus que dans les logs/artefacts et qu'aucun fichier de résultat adéquat n'existe, créer `results/<lane>/run_<run_id>_recovered.json` avec les mesures exactes récupérables, verdicts, provenance, statut épistémique et claim ceiling.

Tous les chemins de résultat liés au run doivent être listés dans `canonical_result_paths` du run-memory.

### 2. Rapport narratif

Créer `reports/<lane>/run_<run_id>_recovery.md` si une analyse de récupération est nécessaire. Le rapport doit nommer l'exact run id, expliquer ce qui a été récupéré ou perdu, et pointer vers les fichiers canoniques sous `results/`.

### 3. Ledger(s) cumulatif(s)

Intégrer le contenu substantif dans le ou les ledgers propriétaires :
- `docs/GRAPH_LEDGER.md`
- `docs/PHYSICS_LEDGER.md`
- `docs/INTEL_LEDGER.md`
- `docs/RUNTIME_LEDGER.md`
- `docs/PRODUCT_LEDGER.md`
- `docs/CTO_LEDGER.md`
- `docs/FRONTIER_LEDGER.md`

Toute entrée de récupération cite l'exact `run_id`. Si le résultat est déjà durable, ne pas dupliquer inutilement : vérifier, référencer puis ajouter seulement la provenance ou les données manquantes.

### 4. Provenance et index

Les données brutes récupérées vont sous `evidence/actions-runs/<run_id>/` : metadata, logs, artefacts et autres sources brutes raisonnablement stockables.

Maintenir :
- `evidence/run-memory/runs/<run_id>.json`
- `evidence/run-memory/INDEX.md`
- `evidence/run-memory/CTO_FEED.json`
- `evidence/run-memory/PRODUCT_FEED.json`

Chaque run-memory doit contenir au minimum : `run_id`, `canonical_result_paths`, `report_path`, `ledger_paths`, statut épistémique et provenance.

Le receipt `evidence/ledger-integration/runs/<run_id>.json` est généré **déterministiquement par le workflow**, après le travail du Curator. Le Curator ne décide jamais lui-même qu'un run Actions est supprimable.

## Suppression

Un ancien run ne devient supprimable que si :
1. au moins un fichier canonique sous `results/` est lié au run ;
2. son rapport narratif requis existe et cite le run ;
3. le ou les ledgers pertinents citent le run ;
4. la provenance brute récupérable est durable sous `evidence/` ;
5. aucune donnée utile ne reste uniquement dans Actions ou le staging temporaire ;
6. aucun blocker pertinent ne subsiste ;
7. le receipt déterministe porte `integration_complete=true`, `all_substantive_data_copied_to_repo=true` et `safe_to_delete_actions_run=true`.

En cas de doute : ne pas supprimer. Un état partiel est un état durable normal, pas une raison de jeter le batch.

## Runs déjà supprimés

Ne jamais inventer leur contenu perdu. Récupérer uniquement ce qui reste démontrable par Git, staging temporaire, branches, rapports, résultats et ledgers. `evidence/run-memory/DELETED_RUNS_RECOVERY.json` reste le registre de l'incident historique. Les trous de provenance restent explicitement marqués tant qu'aucune source nouvelle ne les résout.

## Feeds CTO / Product

Les feeds sont reconstruits à partir de l'ensemble des records durables. Ils transportent les résultats utiles sans changer leur statut épistémique. Seul `AUDITED_DURABLE` peut être traité comme brique validée ; tout le reste reste avertissement, contrainte, piste ou besoin de validation.