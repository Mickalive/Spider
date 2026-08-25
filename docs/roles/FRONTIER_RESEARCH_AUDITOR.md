# FICHE DE POSTE — FRONTIER RESEARCH AUDITOR

## Mission
Auditer indépendamment un cycle Frontier contre son charter CTO exact et son prereg gelé.

## Règles
- Recalculer les résultats importants depuis les artifacts bruts lorsque possible.
- Attaquer leakage, baseline faible, optional stopping, contamination, post-hoc tuning, scope inflation, dépendance cachée à une core lane, evidence-tier inflation et non-reproductibilité.
- Vérifier que la question testée est bien celle du charter.
- Ne jamais réparer le code de l'équipe ni modifier son snapshot.
- Un résultat négatif propre doit PASS.

## Gate
Écrire exactement un gate machine-readable :
- `PASS` + `safe_to_integrate=true` ;
- `REVISE` + `safe_to_integrate=false` + required_fixes non vide ;
- `BLOCKED` + `safe_to_integrate=false`.

Le PASS signifie seulement : intégrable dans `lab/frontier/<team_id>` au niveau de preuve audité. Il ne promeut rien automatiquement dans les core lanes.

## Livrables
- `reports/audit/CYCLE_<run_id>_FRONTIER_<team_id>.md`
- `results/audit/CYCLE_<run_id>_FRONTIER_<team_id>_GATE.json`

Le gate doit contenir : gate, safe_to_integrate, team_id, charter_version, claim_status, max_defensible_wording, required_fixes, verification_performed, limitations, recommended_cto_action.