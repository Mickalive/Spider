# Spider public-site pilot — executable protocol (2026-10-11)

**Status: gated engineering benchmark, not validated product economics.**
Runs on real, public, read-only sites without authentication:
* `pypi`: latest released version for packages on pypi.org;
* `github`: latest GitHub Releases tag (not branches or prereleases).

Only curated identifiers are allowed. Each family has two TRAIN ids and two
separate HOLDOUT ids. The first agent starts at the public home page, must
navigate to a release page and return the exact answer. A *separate official
API* checks the answer: PyPI JSON and GitHub Releases/latest JSON.

## Zero-cost/default

```bash
PYTHONPATH=src python scripts/run_public_benchmark.py --mode plan --output /tmp/spider-public-plan.json
PYTHONPATH=src python scripts/run_public_benchmark.py --mode probe --output /tmp/spider-public-probe.json
```

`plan` produces 24 paired task slots, including `DIRECT_API` as the strongest
simple comparator. Adding `--include-stagehand` produces 28 slots. These are
**plans, not results**. `probe` fetches exactly eight public pages (TRAIN + HOLDOUT) and official
public read-only APIs without an LLM. Any disagreement results in `all_match:
false`; do not start a paid benchmark on an unverified site/task.

GitHub Actions `public-sites-probe.yml` actually executes `probe` on PRs.
Its report includes a per-family `family_ready` result and an explicit
`training_and_holdout_probed` flag. **Github is currently the verified
family. PyPI is quarantined because some public pages deliver a ~3 KB
anti-bot/verification interstitial to CI instead of package content.**
The workflow reports this quarantine, but does not block the functioning
GitHub family. Model-backed trials **require** a fresh (under 24 hours)
readiness receipt with a PASS for that family. No paid PyPI calls should
run until actual public HTML can be read without circumventing access
controls. Network errors, protection challenges and site redesigns are
**invalid substrate**, not evidence against Spider.

`--mode plan` may still include quarantined families, but **plan does
not execute**, and the paid runner refuses them.

## Explicitly authorized provider calls only

Run a single real-agent task (one paid model run maximum per invocation):

```bash
export GOOGLE_API_KEY="<your-own-key>"
PYTHONPATH=src python scripts/run_public_benchmark.py \
  --mode trial --family pypi --id httpx --arm COLD \
  --readiness-file /tmp/spider-public-probe.json \
  --allow-model-charges --output /tmp/spider-public-trials.jsonl
```

Train Spider **only from a real Browser Use agent that succeeds** on two
independent training records:

```bash
PYTHONPATH=src python scripts/run_public_benchmark.py \
  --mode learn --family pypi --memory-path /tmp/spider-public-memory.jsonl \
  --readiness-file /tmp/spider-public-probe.json --allow-model-charges --output /tmp/spider-public-train-pypi.json
PYTHONPATH=src python scripts/run_public_benchmark.py \
  --mode learn --family github --memory-path /tmp/spider-public-memory.jsonl \
  --readiness-file /tmp/spider-public-probe.json --allow-model-charges --output /tmp/spider-public-train-github.json
PYTHONPATH=src python scripts/run_public_benchmark.py \
  --mode trial --family pypi --id urllib3 --arm SPIDER \
  --memory-path /tmp/spider-public-memory.jsonl --readiness-file /tmp/spider-public-probe.json --allow-model-charges \
  --output /tmp/spider-public-trials.jsonl
```

The public trace compiler requires actual observed matching website URLs from
two distinct successful agent runs, independently API-verified answers,
an exact curated read-only site template, and bounded authorization. It is
**not** a universal Web learner, and the compiler incorporates explicit
site-specific knowledge. A failed or invalidated mechanism falls back to the
same agent when permitted; after uncertain execution it will not blindly retry.

## Strong baseline: real Stagehand v4 remote cache

Stagehand v4 server caching needs a **Browserbase remote browser**.
Its LOCAL caching is *not* equivalent: local v4 does not use Browserbase
server-side cache. We implement Stagehand's real `browserbase.launch` and
`Stagehand.create(cache={"threshold":1})`, and record returned
`metadata.cache`; a MISS must not be counted as a HIT.

```bash
python -m pip install stagehand pydantic
export BROWSERBASE_API_KEY="<your-own-key>"
PYTHONPATH=src python scripts/run_public_benchmark.py \
  --mode trial --family pypi --id httpx \
  --arm STAGEHAND_V4_SERVER_CACHE \
  --allow-model-charges --allow-browserbase-charges \
  --output /tmp/spider-public-trials.jsonl
```

Stagehand browser cloud and model gateway may charge. Neither is invoked in
GitHub CI and no cloud cost is approved by the existence of this script.
Use **account-side spending caps**. Python CLI permissions are opt-in but
cannot hard-cap provider-side costs after a request is accepted.

## Measurement and go/no-go

Comparable variants on the same task / replicate:
`COLD`, `INSTRUCTIONS`, `RETRIEVAL`, `SPIDER`,
`COMPILED`, `DIRECT_API`, and
`STAGEHAND_V4_SERVER_CACHE`.

Do NOT compare raw tokens alone. For total cost per verified safe success:
model inference, browser/cloud time, retrieval, independent verification,
memory writes/reads, *amortized training*, repairs, all other expenses.
Compare safety and success at the same task/model/tool budget. When Stagehand
uses a different model/tool budget from Browser Use, label it as an unmatched
competitor scenario; do not infer a causal Spider effect.

The scorer rejects incomplete or hand-seeded costs. After external accounting
and evidence audits it can run with:

```bash
PYTHONPATH=src python scripts/score_product_benchmark.py \
  --input /tmp/independently-priced-matched-trials.jsonl \
  --public --require-native-stagehand --output /tmp/descriptive-scores.json
PYTHONPATH=src python scripts/decide_product_gate.py \
  --input /tmp/independently-priced-matched-trials.jsonl \
  --output /tmp/spider-gate.json
```

The advisory gate needs at least **10 paired trials per family**, no
cold/retrieval success ceiling, at least **20% lower fully loaded USD per safe
success than the cheapest comparator**, no recorded unsafe actions, and
at most a **2 percentage point** success-rate deficit. `DIRECT_API` can be
the cheapest comparator, in which case the correct business response may be
to drop the Spider approach on that task family.

`CANDIDATE_GO_PENDING_INDEPENDENT_AUDIT` is *not* scientific validation,
product readiness, a merge approval or shipment. The Product research lane's
separate audit and promotion gate still controls merging source changes.

## Critical scope limits

- No live credentialed Browser Use or real Browserbase Stagehand run has been
  completed in CI, and **no verified cost saving exists yet**.
- Sites change; external probe failures must be investigated and frozen, not
  scored as a Spider defeat.
- These first read-only sites are deliberately easy: direct APIs may dominate.
  Next task bank must add meaningful multi-action, changing sites before
  general claims.
- Fractal graph decomposition and delta repair remain unvalidated research
  hypotheses; they are NOT prerequisites to shipping a useful memory feature.
