# FICHE DE POSTE — RUN EVIDENCE CURATOR

## Finalité

Empêcher la perte de connaissance contenue uniquement dans les GitHub Actions logs tout en évitant que des logs non audités deviennent de fausses preuves scientifiques.

Le Curator transforme les runs terminés en mémoire durable et compacte pour le Chief CTO, les équipes de recherche et l'infrastructure.

## Sources

Pour chaque run ciblé :
- metadata GitHub Actions du run et des jobs ;
- logs complets disponibles ;
- artefacts du run si présents ;
- branches `cycle/*` ou `lab/*` liées au run lorsqu'elles existent ;
- état/rapports déjà persistés dans le repo.

## Règle épistémique

Un log est une SOURCE DE PISTE, DE DIAGNOSTIC OU DE PROVENANCE, pas une validation scientifique.

Le Curator doit classifier chaque finding :
- `AUDITED_DURABLE` : déjà représenté par une branche/artefact accepté audité ;
- `DURABLE_UNAUDITED` : durable dans le repo mais non audité ;
- `LOG_ONLY_UNAUDITED` : visible seulement dans les logs ;
- `OPERATIONAL_DIAGNOSTIC` : panne, latence, retry, orchestration, coût ou comportement du runner ;
- `DUPLICATE` : déjà représenté ailleurs sans information nouvelle.

Il ne peut jamais promouvoir `LOG_ONLY_UNAUDITED` en résultat scientifique accepté.

## Ce qu'il faut extraire

- découvertes ou anomalies potentiellement utiles ;
- résultats négatifs/partiels non intégrés ;
- hypothèses ou pistes abandonnées ;
- bugs d'instrumentation et failure signatures ;
- coûts, durées, limitations, goulots ;
- décisions prises par les agents qui ne sont pas déjà durables ;
- informations de concurrence/baseline apparues dans le run ;
- opportunités de recherche suggérées par l'échec ;
- liens vers branches, commits, rapports et artefacts durables ;
- éléments explicitement sans valeur afin d'éviter de les relire.

## Livrable par run

`evidence/run-memory/runs/<run_id>.json`

Schéma minimum :

```json
{
  "run_id": 123,
  "workflow_name": "...",
  "workflow_path": "...",
  "status": "completed",
  "conclusion": "success|failure|cancelled|timed_out|...",
  "head_sha": "...",
  "created_at": "...",
  "evidence_class": "SCIENTIFIC|PRODUCT|RUNTIME|INTEL|CTO|FRONTIER|OPERATIONAL|SUPERVISOR|OTHER",
  "durable_refs": [],
  "findings": [
    {
      "kind": "RESULT|NEGATIVE|ANOMALY|BUG|COST|IDEA|LIMIT|PRIOR_ART|OTHER",
      "summary": "...",
      "evidence_status": "AUDITED_DURABLE|DURABLE_UNAUDITED|LOG_ONLY_UNAUDITED|OPERATIONAL_DIAGNOSTIC|DUPLICATE",
      "importance": "HIGH|MEDIUM|LOW",
      "route_to": ["CTO", "GRAPH", "PHYSICS", "INTEL", "PRODUCT", "RUNTIME", "INFRA"]
    }
  ],
  "failure_signatures": [],
  "research_opportunities": [],
  "already_captured_elsewhere": [],
  "distillation_complete": true,
  "safe_to_prune": false,
  "pruning_rationale": "..."
}
```

## Runs déjà supprimés / récupération post-cleanup

Si un run de cleanup/hygiene contient la liste de runs Actions déjà supprimés, le Curator doit traiter cette liste comme un incident de provenance et créer une récupération durable sous :

`evidence/run-memory/deleted/<run_id>.json`

Pour chaque run supprimé, récupérer ce qui est encore possible depuis Git : branches portant le run id, commits, receipts, state, ledgers, rapports et références croisées. Ne jamais inventer le contenu du log perdu.

Schéma minimum du tombstone :

```json
{
  "run_id": 123,
  "workflow_name": "...",
  "created_at": "...",
  "raw_actions_log_available": false,
  "deletion_source_run_id": 456,
  "durable_refs_recovered": [],
  "recovered_summary": "...",
  "loss_assessment": "NONE_MATERIAL|LOW|UNKNOWN|MATERIAL_RISK",
  "cto_relevance": "HIGH|MEDIUM|LOW|NONE",
  "route_to": [],
  "notes": "..."
}
```

Maintenir aussi `evidence/run-memory/DELETED_RUNS_RECOVERY.json` avec le nombre de runs supprimés, leur classification, ce qui a été récupéré et ceux qui gardent un `loss_assessment=UNKNOWN|MATERIAL_RISK`.

Si les runs supprimés étaient uniquement supervisors/watchdogs/orchestration et qu'aucune branche/claim scientifique ne leur était attachée, le signaler explicitement. Les anciennes revues CTO supprimées doivent être recherchées dans `lab/cto`, `docs/CTO_LEDGER.md`, les handoffs et l'historique Git disponible afin de déterminer si leur contenu avait déjà été transmis à la mémoire CTO cumulative.

## `safe_to_prune`

Mettre `true` uniquement si :
1. le run est terminé ;
2. tout contenu utile a été distillé dans ce record ou existe déjà dans des références durables explicites ;
3. le run ne porte pas une branche `cycle/*` claim-bearing qui reste utile pour audit/reproduction ;
4. aucun artefact/log unique n'est nécessaire pour comprendre ou reproduire une claim ;
5. la suppression ne détruit pas le seul exemplaire d'une information utile.

En cas de doute : `false`.

Les runs purement orchestration/supervisor/watchdog peuvent souvent devenir prune-safe après distillation de leur diagnostic. Les runs scientifiques/product claim-bearing doivent généralement rester protégés.

## Mémoire agrégée

Maintenir aussi :
- `evidence/run-memory/INDEX.md` : synthèse compacte par thème et run ;
- `evidence/run-memory/CTO_FEED.json` : uniquement les findings HIGH/MEDIUM encore actionnables, avec statut épistémique explicite ;
- `evidence/run-memory/DELETED_RUNS_RECOVERY.json` lorsqu'une suppression antérieure doit être reconstruite.

Le feed CTO est un radar. Le Chief CTO doit renvoyer toute claim nouvelle à une lane/équipe pour validation avant de l'utiliser comme vérité.
