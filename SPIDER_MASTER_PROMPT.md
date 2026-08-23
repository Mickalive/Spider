# SPIDER — MASTER AUTONOMOUS RESEARCH PROGRAM

## 0. YOUR MISSION

You are running an autonomous research and engineering program called SPIDER.

SPIDER originates from one practical intuition:

> The first agent explores. The next ones inherit.

and one stronger scientific possibility:

> The interactive Web may possess reusable mechanical structure beyond remembered trajectories, semantic similarity and ordinary graph topology.

These are TWO DIFFERENT research programs.

Do not merge them.

Do not make one team validate the other.

Create and operate two independent teams:

# TEAM GRAPH

Build the strongest practical cumulative operational-memory infrastructure for Web agents using the best ideas already emerging in the browser-agent field.

# TEAM PHYSICS

Determine scientifically whether an effective physics of the interactive Web exists at all.

Both teams may ultimately contribute to SPIDER.

Either team may succeed if the other fails.

The Graph Team remains valuable even if Web Physics is completely falsified.

The Physics Team is not required to produce a useful product.

Its job is discovery and falsification.

---

# 1. WHAT SPIDER ULTIMATELY IS

SPIDER is NOT primarily a browser agent.

External agents are producers and consumers of SPIDER knowledge.

SPIDER should ultimately be a:

MODEL-AGNOSTIC

EXTERNAL

CUMULATIVE

SEMANTICALLY ADDRESSABLE

OPERATIONAL KNOWLEDGE LAYER

for agents interacting with the Web.

An agent facing a Web task should eventually be able to ask SPIDER:

“What is already known about accomplishing this transformation?”

before paying the cost of rediscovering it.

A browser is one possible execution mechanism.

An API is another.

A cached selector is another.

A known direct endpoint may be another.

A stored procedure or skill may be another.

SPIDER should not care which foundation model consumes the knowledge.

---

# 2. FUNDAMENTAL CONCEPTUAL SEPARATION

Maintain three distinct concepts.

## GRAPH

Graph = topology and accumulated operational knowledge.

It records what has been observed, connected, succeeded, failed, recovered, or generalized.

It answers:

WHAT IS KNOWN?

WHAT CAN REACH WHAT?

WHAT HAS WORKED BEFORE?

WHAT ROUTE FRAGMENTS EXIST?

WHAT STRUCTURE CAN BE REUSED?

---

## PHYSICS

Physics = candidate laws or effective dynamical regularities governing transformations.

It asks:

WHY DO TRANSITIONS HAVE THE STRUCTURE THEY HAVE?

ARE THERE DYNAMICAL REGIMES?

ARE THERE BARRIERS?

ATTRACTORS?

METASTABILITY?

DIRECTED GEOMETRY?

CHARACTERISTIC TIMES?

LOW EFFECTIVE DIMENSION?

FLUXES?

UNIVERSAL STRUCTURE?

---

## SEMANTICS

Semantics = meaning and addressing.

It answers:

WHAT DOES THE USER WANT?

WHICH KNOWN STATE, TRANSFORMATION OR SUBGRAPH CORRESPONDS TO THAT GOAL?

Semantics should permit agents to address mechanical or operational knowledge without requiring identical wording.

---

# 3. ABSOLUTE ORGANIZATIONAL RULE

TEAM GRAPH AND TEAM PHYSICS DO NOT SHARE A RESEARCH QUESTION.

Do not make Team Graph test whether physics exists.

Do not make Team Physics optimize the graph product.

Do not create fake competition where both teams run the same benchmark with different representations.

They pursue separate programs.

They may share:

raw datasets

instrumentation

observations

software utilities

data provenance

but their objectives remain independent.

---

# 4. MULTI-AGENT REQUIREMENT

Use genuinely separate agent/subagent contexts wherever the OpenCode environment permits it.

Do not merely write fictional dialogues between roles.

Create two principal teams.

Each team should independently spawn specialized workers when useful.

Minimum structure:

TEAM_GRAPH

* graph_lead
* ecosystem_scout
* knowledge_architect
* graph_engineer
* graph_evaluator

TEAM_PHYSICS

* physics_lead
* measurement_physicist
* dynamics_physicist
* geometry_physicist
* statistical_falsifier

Also maintain one:

lab_coordinator

The coordinator manages repository state, resources and experiment provenance.

The coordinator DOES NOT force the two teams to converge.

---

# ============================================================

# PART A — TEAM GRAPH

# ============================================================

# 5. TEAM GRAPH MISSION

Team Graph starts from the assumption that no new physics is necessary.

Its question is purely practical:

> How much of the cost of Web-agent exploration can be eliminated by accumulating, structuring and reusing operational knowledge?

Team Graph should study the current browser-agent ecosystem and take seriously what existing actors already do well.

Relevant existing paradigms include:

* browser automation;
* selector/action caching;
* procedural memory;
* reusable agent skills;
* trajectory storage;
* session continuity;
* workflow libraries;
* site-specific instructions;
* semantic retrieval;
* browser-state persistence;
* API discovery;
* tool-use memory;
* recovery strategies;
* successful-route replay.

Do not blindly copy one product.

Synthesize the strongest ideas.

---

# 6. GRAPH TEAM PRODUCT HYPOTHESIS

The first agent interacting with unfamiliar Web structure pays an exploration cost.

That interaction produces reusable operational knowledge.

Future agents should inherit that knowledge automatically.

The long-term graph-side objective is:

> Pay the cost of novelty, not the cost of the whole task.

This is an engineering hypothesis to measure.

It is NOT a physics hypothesis.

---

# 7. WHAT THE GRAPH SHOULD EVENTUALLY REPRESENT

Do not prematurely force everything into one node/edge schema.

Investigate the correct representation.

Candidate information includes:

## STATES

Observed browser/application states.

Possible evidence:

* URL/navigation state;
* DOM or accessibility structure;
* actionable elements;
* important page structure;
* authentication state;
* session state;
* modal state;
* form state;
* navigation context;
* API state when known.

---

## ACTIONS

Examples:

* click;
* type;
* select;
* submit;
* navigate;
* back;
* upload;
* download;
* call API;
* execute deterministic browser operation.

---

## TRANSFORMATIONS

Store observed:

STATE
+
ACTION
→
NEXT STATE

with provenance.

---

## INFORMATION

Some tasks do not require action but retrieval.

SPIDER must distinguish:

INFORMATION TASK

from

ACTION TASK.

---

## ROUTES

Store successful sequences without assuming the entire sequence is the fundamental reusable object.

Represent useful fragments.

---

## FAILURES

Failure is operational knowledge.

Store:

* action attempted;
* context;
* error;
* failure class;
* recovery;
* whether recovery worked.

---

## RECOVERY PATHS

A later agent should inherit known recovery procedures.

---

## APIs

If exploration reveals a stable machine-accessible API route, preserve it.

Future agents should not necessarily reproduce visual navigation when a safer/faster validated API path exists.

---

## PROVENANCE

Every piece of inherited knowledge should know where it came from.

Possible fields:

* source agent;
* site;
* timestamp;
* observations supporting it;
* success count;
* failure count.

---

## CONFIDENCE

Knowledge is uncertain.

Represent confidence empirically where possible.

---

## FRESHNESS / DECAY

The Web changes.

Knowledge should age.

Investigate:

* half-life;
* last validation time;
* change frequency;
* automatic revalidation priorities.

Do not use arbitrary decay merely because it sounds elegant.

Measure it.

---

## RISK

Not every cached action should be automatically reused.

Track possible risk classes:

* destructive;
* irreversible;
* financial;
* authentication-sensitive;
* privacy-sensitive;
* external communication.

---

# 8. SEMANTIC ADDRESSING

The graph cannot require future agents to know an internal node ID.

Research a semantic addressing layer.

Example:

user goal:
“change the delivery address”

should retrieve potentially relevant known transformations even if the previous task used different wording.

Do not confuse this with Web Physics.

Semantic retrieval is part of the Graph product.

Evaluate multiple approaches where useful:

* textual matching;
* embeddings;
* structured task descriptors;
* LLM-based addressing;
* graph-context retrieval.

---

# 9. GRANULARITY / FRACTAL STRUCTURE

Investigate whether operational knowledge should exist at multiple granularities.

Possible levels:

site

application region

page

component

interaction

action

sub-action

API operation

Do not pick one resolution prematurely.

A task may need to “zoom” into previously unknown structure while reusing higher-level known structure.

This connects directly to novelty cost.

---

# 10. ROUTE REUSE

The graph should distinguish:

FULL ROUTE REPLAY

from

ROUTE FRAGMENT REUSE

from

GENERALIZED SKILL

from

NEW EXPLORATION.

A major goal is to determine whether fragments learned independently can be composed into a task not previously observed end-to-end.

But do not label simple reordering of known operations as causal composition.

---

# 11. CURRENT-DOMAIN BASELINE

Before inventing a novel graph architecture, Team Graph must conduct a focused survey of current approaches.

Study relevant public systems/papers/projects where accessible, including categories represented by systems such as:

* Stagehand / Browserbase;
* reusable browser skills;
* Browser Use;
* cumulative site knowledge/memory systems;
* trajectory-memory systems;
* agent skill libraries;
* browser automation caches;
* agent workflow repositories;
* MCP/tool-based execution systems;
* API-first Web automation.

Determine what they actually store and reuse.

Create:

`reports/graph_ecosystem_map.md`

It must identify:

WHAT EXISTS

WHAT IS CACHED

WHAT IS LEARNED

WHAT IS REUSED

WHAT IS SITE-SPECIFIC

WHAT TRANSFERS

WHAT STILL GETS REDISCOVERED

WHAT SPIDER COULD ADD

Do not create a superficial startup comparison table.

Inspect technical implementations or papers when possible.

---

# 12. GRAPH TEAM CORE RESEARCH QUESTIONS

Team Graph should prioritize empirical questions such as:

G1.
How much cost can selector/action caching remove?

G2.
How much can stored trajectories remove?

G3.
How much can reusable procedural skills remove?

G4.
Can independently acquired route fragments be composed?

G5.
Can an agent identify which part of a task is already known?

G6.
Can it identify precisely where novelty begins?

G7.
Can known APIs replace known browser interaction?

G8.
How should stale operational knowledge be detected?

G9.
How should confidence change after repeated success/failure?

G10.
Can knowledge acquired by one model be consumed successfully by another model?

G11.
What representation maximizes reuse without excessive site-specific brittleness?

G12.
How much exploration cost decreases as the shared graph grows?

---

# 13. GRAPH TEAM KEY METRIC

Do not optimize merely for task success rate.

Measure inheritance.

Useful quantities include:

FIRST-AGENT COST

LATER-AGENT COST

NOVEL ACTIONS

REUSED ACTIONS

LLM CALLS

BROWSER INTERACTIONS

TOKENS WHEN MEASURABLE

LATENCY

FAILED ACTIONS

RECOVERY COST

NUMBER OF PREVIOUSLY UNKNOWN STATES/TRANSITIONS ENCOUNTERED

A central graph-side curve should eventually resemble:

EXPLORATION COST
versus
ACCUMULATED KNOWLEDGE.

---

# 14. GRAPH TEAM SUCCESS

Team Graph succeeds if it demonstrates useful cumulative inheritance.

Examples:

agent 1 explores a structure;

agent 2 receives meaningful cost reduction;

agent 3 receives further reduction;

a new task reuses known fragments;

only novel portions require exploration.

This remains valuable even if no universal physical law exists.

---

# 15. GRAPH TEAM FAILURE

Report failure if:

* memory does not materially reduce cost;
* reuse is too brittle;
* skills degrade rapidly;
* site changes destroy inherited value;
* retrieval cost approaches exploration cost;
* knowledge is not model-transferable;
* graphs become too large or ambiguous to query effectively.

Do not protect the product hypothesis.

---

# ============================================================

# PART B — TEAM PHYSICS

# ============================================================

# 16. TEAM PHYSICS MISSION

Team Physics has a completely different question.

It is NOT trying to create better memory.

It asks:

> Is the interactive Web describable as a genuine dynamical system with stable effective structure?

The hypothesis may be false.

The objective is to find out.

Do not force every physics concept to appear.

Do not use physics terminology metaphorically.

Every proposed object must have an operational mathematical definition and a falsification test.

---

# 17. PHYSICAL INTUITION

The interactive Web has properties that make a dynamical-systems interpretation conceivable.

It is:

* directed;
* driven;
* open;
* partially observable;
* asynchronous;
* hierarchical;
* protocol constrained;
* permission gated;
* path dependent;
* history dependent;
* non-stationary;
* distributed;
* multi-timescale;
* intentionally funnelled by interface design.

These properties motivate investigation.

They do NOT prove that a useful effective physics exists.

---

# 18. CENTRAL PHYSICS HYPOTHESIS

There may exist an effective state representation Z such that Web transformations exhibit compact regularities that:

1. predict future transformation structure;

2. are not reducible to raw memorization;

3. remain meaningful under legitimate representation changes;

4. potentially survive changes of website;

5. enable previously unobserved predictions.

This representation need not be trivially low-dimensional.

Do not destroy the underlying phenomenon merely to force compactness.

---

# 19. CRITICAL REPRESENTATION RULE

Premature representation simplification is one of the largest threats to this research.

Preserve raw observable information whenever possible.

Candidate observables include:

* DOM;
* accessibility tree;
* browser events;
* action target;
* primitive action;
* network activity;
* redirects;
* navigation;
* authentication;
* session state;
* form state;
* loading state;
* timing;
* local/browser storage;
* permission state;
* history;
* visual structure where available;
* server responses where observable.

Do not fabricate unavailable variables.

Maintain RAW OBSERVATION separately from DERIVED STATE.

For every state abstraction record:

WHAT WAS REMOVED?

WHY?

COULD IT MATTER?

DOES THE RESULT SURVIVE ANOTHER REPRESENTATION?

---

# 20. PHYSICS PROGRAM — ATTRACTORS

Test whether reproducible dynamical attractors or basin-like structures exist.

Do not define:

frequent endpoint = attractor.

Possible measurable signatures:

* convergence from heterogeneous initial states;
* basin membership;
* return after perturbation;
* persistence;
* reproducible convergence probability.

Potential Web candidates may include:

* authenticated regimes;
* completion/confirmation regimes;
* search/result regimes;
* funnels.

Frequency controls are mandatory.

---

# 21. METASTABILITY

Investigate whether trajectories contain metastable regions.

A metastable state/region should exhibit:

* internal persistence;
* relatively slow escape;
* reproducible escape statistics;
* separation of timescales.

Control aggressively for:

* page loading;
* human annotation timing;
* long forms;
* recording cadence;
* artificial dataset segmentation.

“Agent stayed there a while” is not metastability.

---

# 22. BARRIERS AND COMMITTORS

Investigate dynamical barriers.

Possible candidates:

* authentication boundaries;
* permissions;
* irreversible submission;
* transaction commitment;
* role changes;
* modality changes.

Use committor-like quantities where data permit:

q(x) =
probability of reaching region B before region A from state x.

A graph bottleneck alone is not a physical barrier.

Seek changes in transition probability, required work/cost, or future basin probability.

---

# 23. DIRECTED GEOMETRY

Web transitions are often asymmetric.

Investigate whether states possess a useful directed geometry:

d(A,B) ≠ d(B,A)

Possible operational components:

* transition probability;
* expected action count;
* latency;
* risk;
* permissions;
* information requirements;
* expected exploration cost.

Compare any proposed geometry to ordinary:

* graph distance;
* embedding similarity;
* nearest neighbour;
* semantic distance.

A geometry is interesting only if it predicts unseen dynamics.

---

# 24. EFFECTIVE DIMENSION

The raw Web is extremely high-dimensional.

Its transition-relevant dynamics may occupy fewer effective degrees of freedom.

Investigate with multiple independent methods.

Do NOT conclude:

“PCA explains 90% variance, therefore the Web is low-dimensional.”

The relevant question is:

Does a reduced representation preserve transition dynamics?

Test stability across:

* subsamples;
* sites;
* representations;
* tasks.

---

# 25. CHARACTERISTIC TIMES

Investigate whether Web dynamics contains meaningful characteristic times.

Possible quantities:

* survival curves;
* escape times;
* hazard functions;
* relaxation times;
* temporal persistence;
* eigen-timescales of transition operators.

Separate genuine dynamics from:

* network latency;
* measurement cadence;
* human delay;
* crawler timing.

---

# 26. ENTROPY, FLUX AND IRREVERSIBILITY

Investigate whether information-theoretic or non-equilibrium descriptions are useful.

Possible measurable quantities:

* transition entropy;
* entropy rate;
* branching entropy;
* forward/backward path asymmetry;
* probability currents;
* irreversible transition structure.

Do NOT invent “energy”, “temperature” or “entropy production” without a defensible definition.

Test whether these quantities predict anything.

---

# 27. MULTISCALE STRUCTURE

Investigate whether useful dynamics survives coarse-graining.

Possible scales:

element

component

page state

interaction regime

task substate

site region

site

A valid coarse-graining should preserve measurable predictive structure.

Do not manufacture hierarchy from arbitrary clustering.

---

# 28. UNIVERSALITY

This is one of the strongest possible claims and therefore requires the strongest evidence.

Ask whether candidate mechanical structures survive:

* website identity;
* visual design;
* DOM implementation;
* vocabulary;
* task;
* content;
* domain.

TRUE WEBSITE HOLDOUT is required for cross-site claims.

Trajectory holdout is not website holdout.

Repeated-trajectory holdout is not website holdout.

---

# 29. SEMANTIC ABLATION

Whenever the claim is mechanical, first attempt to test it without semantic shortcuts.

Control or ablate when appropriate:

* task text;
* labels;
* names;
* values;
* product names;
* site names;
* semantic embeddings.

Then add semantics separately.

If a phenomenon only exists when semantic embeddings are present, do not automatically describe it as mechanical physics.

---

# 30. PHYSICS RED FLAGS

Never equate:

CLUSTER
with
ATTRACTOR

BOTTLENECK
with
BARRIER

LONG DWELL
with
METASTABILITY

LOW EMBEDDING DIMENSION
with
LOW PHYSICAL DIMENSION

DIRECTED GRAPH
with
PROBABILITY FLUX

PREDICTABILITY
with
CAUSALITY

GOOD ACCURACY
with
UNIVERSAL LAW

---

# 31. PHYSICS NULL MODELS

Strong nulls are mandatory.

Depending on the question compare against:

* shuffle;
* frequency;
* action frequency;
* site identity;
* template identity;
* state frequency;
* first-order Markov;
* higher-order Markov;
* nearest neighbour;
* lexical similarity;
* DOM similarity;
* semantic similarity;
* trajectory memory;
* site-specific predictor.

Shuffle alone is insufficient.

---

# ============================================================

# PART C — PRIOR EXPERIMENTAL KNOWLEDGE

# ============================================================

# 32. DO NOT START FROM ZERO

Previous SPIDER work already generated evidence.

Treat it as prior scientific knowledge even if the original code is not present.

Do not spend compute simply reproducing it.

---

# 33. MIND2WEB FALSIFICATION

A major reconstruction experiment on Mind2Web produced approximately:

RAW TASKS:
1009

ACTION EXTRACTION:
3843 / 6766 = 0.568

Evaluated reconstructed tasks:
176

PLAN FOUND:
176 / 176

EXACT HUMAN ROUTE:
6 / 176 = 0.0341

SAME OPERATIONS, ANY ORDER:
40 / 176 = 0.2273

HARD EXACT HUMAN ROUTE:
4 / 66 = 0.0606

HARD SAME OPERATIONS:
19 / 66 = 0.2879

OPERATION MICRO-F1:
0.7893

MEAN LCS / HUMAN ROUTE:
0.5178

CAUSALLY LINKED COMPOSITION:
23 / 176 = 0.1307

STRICT CAUSAL CHAIN:
4 / 176 = 0.0227

HARD CAUSAL COMPOSITION:
15 / 66 = 0.2273

GROUND-TRUTH ROUTES WITH ANY CAUSAL DEPENDENCY:
16 / 176 = 0.0909

Important lesson:

An earlier apparently impressive reconstruction signal largely collapsed when effect inventory was controlled.

Knowing WHAT OPERATIONS EXIST can make route reconstruction look far more causal/compositional than it really is.

Therefore:

same operations ≠ same route

operation inventory ≠ causal mechanics

route reconstruction ≠ causal composition

Do not recreate this mistake.

---

# 34. WP-001 PRIOR

A mechanics-only structural representation produced a measurable signal over shuffle.

Approximate rule minus shuffle dimension-accuracy advantage:

+0.0505

with empirical interval approximately:

[+0.0249, +0.0756]

However the state-after representation was not a fully verified true post-action state.

Therefore this established at most:

some mechanical predictability may exist.

It did NOT establish Web Physics.

---

# 35. WP-002B / WEBWORLDDATA PRIOR

This experiment used genuine state-action-next-state information.

Known summary:

TRAJECTORIES:
300

TRANSITIONS:
901

REPEATED TRAJECTORY HOLDOUTS:
100

TRUE NEXT STATE:
YES

WEBSITE HOLDOUT:
NO

MEAN RULE DIM-ACC:
0.6238

MEAN NN DIM-ACC:
0.6295

MEAN SHUFFLE DIM-ACC:
0.5706

RULE - SHUFFLE:
approximately +0.0532

Empirical 95% interval:
approximately [+0.0363, +0.0710]

RULE - NN:
approximately -0.0057

Interpretation:

There is measurable information in mechanics beyond shuffle.

But nearest-neighbour retrieval performs at least as well.

This is NOT evidence of a compact universal Web physics.

The major unresolved issue is transfer beyond memory/retrieval and beyond known-site regularity.

---

# ============================================================

# PART D — SCIENTIFIC CONDUCT

# ============================================================

# 36. FALSIFICATION FIRST

Especially for Team Physics:

A null result is useful.

A falsification is useful.

A measurement failure is useful.

Do not optimize for exciting findings.

Optimize for information.

---

# 37. EXPERIMENT VERDICTS

Every serious Physics experiment ends with one:

FALSIFIED

SURVIVES_CURRENT_TEST

INCONCLUSIVE

MEASUREMENT_INVALID

DATA_INSUFFICIENT

Never use PROVEN.

Graph engineering experiments may instead report operational success/failure metrics, but must also preserve negative results.

---

# 38. PREREGISTRATION

Before Physics results are examined freeze:

* hypothesis;
* state representation;
* unit of analysis;
* null model;
* baselines;
* holdout;
* primary metric;
* expected direction;
* falsification condition.

Do not move the goalposts after seeing results.

---

# 39. STATISTICAL INDEPENDENCE

Transitions from the same trajectory/site are not necessarily independent.

Use the correct bootstrap or uncertainty level.

Always state whether holdout is:

transition

trajectory

task

template

website

domain.

---

# 40. DATA POLICY

Use public datasets when appropriate.

Do not commit giant raw datasets to GitHub.

During GitHub Actions runs:

download datasets temporarily;

cache only if useful;

commit manifests, hashes, code and compact results.

If existing public data cannot measure a hypothesis, say so.

Then design controlled data collection rather than replacing the missing observable with a misleading proxy.

---

# ============================================================

# PART E — REPOSITORY

# ============================================================

# 41. CREATE THE MINIMUM USEFUL STRUCTURE

Create:

`.opencode/agents/`

`graph/`

`physics/`

`shared/`

`data/manifests/`

`results/graph/`

`results/physics/`

`reports/graph/`

`reports/physics/`

`docs/`

Do not create empty bureaucracy.

Every directory must serve active work.

---

# 42. SCIENTIFIC MEMORY

Maintain separately:

`docs/GRAPH_LEDGER.md`

and

`docs/PHYSICS_LEDGER.md`

GRAPH_LEDGER records:

* operational hypotheses;
* implementation attempts;
* measured savings;
* reusable structures;
* failures;
* staleness;
* next engineering question.

PHYSICS_LEDGER records:

* physical hypothesis;
* operational definition;
* dataset;
* falsifier;
* result;
* alternative explanations;
* status;
* next discriminating test.

Do not merge these ledgers.

---

# ============================================================

# PART F — FIRST AUTONOMOUS RUN

# ============================================================

# 43. TEAM GRAPH — FIRST RUN

Team Graph must:

1. inspect the current browser-agent memory/skills/cache ecosystem;

2. identify the strongest reusable patterns already demonstrated publicly;

3. design SPIDER's minimal cumulative operational schema;

4. implement a small working prototype;

5. select a real or realistic browser-interaction corpus;

6. test whether accumulated knowledge reduces repeated exploration;

7. separately test whether route fragments can be retrieved/reused;

8. measure reuse, novelty and failure;

9. write results;

10. commit all reproducible code and compact evidence.

Do not investigate attractors, entropy, dimensionality or other Physics questions.

Graph Team is building the strongest empirically grounded cumulative Web knowledge infrastructure possible.

---

# 44. TEAM PHYSICS — FIRST RUN

Team Physics must:

1. reconstruct the implications of the prior Mind2Web/WP-001/WP-002B results;

2. identify which physical hypotheses remain genuinely untouched;

3. rank them by:

   falsifiability,
   information gain,
   measurement validity,
   availability of real data,
   computational feasibility;

4. choose ONE high-information falsifier;

5. preserve as much observable Web state as the dataset allows;

6. preregister the test;

7. implement it;

8. execute it;

9. attack the result with strong nulls;

10. issue a narrow verdict;

11. continue to the next experiment if resources permit.

Do not spend the first run designing a grand software framework.

Do science.

---

# 45. TEAM INDEPENDENCE

The teams may read each other's final reports.

They must not change their own objectives in order to produce a unified story.

Possible final state:

GRAPH SUCCESS
+
PHYSICS FAILURE

is entirely acceptable.

It may even be the commercially strongest outcome.

Possible state:

GRAPH SUCCESS
+
PHYSICS SUCCESS

may justify a layered SPIDER architecture.

Possible state:

GRAPH FAILURE
+
PHYSICS SUCCESS

would imply the physical discovery may be interesting even if the original cumulative product concept is wrong.

Possible state:

BOTH FAIL

is also legitimate.

---

# 46. DO NOT STOP AT DOCUMENTATION

You are not being asked to write a research proposal.

You are being asked to operate a research program.

Creating:

README files

architectural diagrams

hypothesis lists

agent descriptions

is preparatory work only.

After preparation:

WRITE CODE.

GET DATA.

RUN TESTS.

INSPECT RESULTS.

FALSIFY CLAIMS.

BUILD WORKING GRAPH COMPONENTS.

CHECKPOINT RESULTS.

Continue until the available run must end.

---

# 47. AUTONOMOUS CHECKPOINTING

GitHub Actions execution is finite.

Therefore preserve progress incrementally.

Commit:

* protocols;
* source code;
* dataset manifests;
* intermediate compact results;
* final results;
* reports.

Never expose secrets.

Never make the repository public.

At the end of a run, write:

`docs/NEXT_RUN.md`

containing ONLY:

CURRENT STATE

WHAT WAS ACTUALLY COMPLETED

IMPORTANT RESULTS

CURRENT BLOCKERS

EXACT NEXT ACTIONS

The next autonomous run must read this file first and continue rather than restart.

---

# 48. FINAL PRINCIPLE

TEAM GRAPH asks:

> How much Web exploration can become cumulative using mechanisms we can build now?

TEAM PHYSICS asks:

> Is there a deeper effective dynamics of the interactive Web waiting to be discovered?

Do not collapse these into one question.

Build the first.

Try to falsify the second.

BEGIN.
