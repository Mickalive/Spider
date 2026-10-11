# EXP-GRAPH-38112374668 preregistration

Lane: `graph`. Claim: `C-SEMANTIC-RESOLVE` (target, from `request.json.director_mandate.allocation`). Design contract: v2. Parent handoff: `EXP-GRAPH-37992949248` (disposition SUPERSEDE; its C-FRESHNESS D1V next-question is NOT this experiment's agenda and is not reopened here). This document is frozen by the deterministic freezer via `freeze.json.hashes["prereg.md"]`; it is immutable during EXECUTE.

Status at design time: DESIGN COMPLETE, awaiting independent `design_review.json` and freeze. No confirmatory outcome-bearing measurement has been taken. The only DESIGN probe was a non-outcome-bearing check of the contamination instrument (token overlap of each bank goal against every registry intent) on the frozen bank; neither outcome arm (`A-EMBED-COSINE`, `B-LEXICAL-OVERLAP`) was scored and the paired difference was not computed.

## 1. What this experiment decides (and what it does not)

The Global Research Director's binding question: on a stdlib-only locally served multi-endpoint multi-verb HTTP application whose goal texts are authored by a process that never sees the mechanism intent strings, does max-cosine-similarity selection over intent embeddings still bind the correct mechanism on goals never seen at authoring time, and by how much does it exceed a token-overlap null - i.e. does the bounded 45/52 vs 33/52 Research 2.0 advantage (paired family-blocked difference 0.2308, 95% CI [0.1136, 0.3509], from EXP-GRAPH-36287167610) survive removal of the joint-authorship confound, or was it an artifact of intents and goal templates being authored in the same file by the same agent?

This experiment measures ONE quantity: the paired difference in mechanism-identity binding accuracy between max-cosine embedding selection (A-EMBED-COSINE) and a token-overlap null (B-LEXICAL-OVERLAP) on independently authored goals.

Explicitly OUT of scope (do not over-read a result): parameter binding correctness, action execution correctness, abstention/UNKNOWN calibration (ECE, false-accept), cross-application generalization, and the shipped kernel's behavior beyond a product baseline. A positive result licenses EXPERIMENTAL for the embedding-selection sub-mechanism only.

## 2. Why the prior number was uninterpretable

`research/harness/goal_generator.py` defines both `INTENTS` (the 20 mechanism intent strings that `candidate_resolver.create_fixture` turns into the registry) and `PARAPHRASES` / `NO_APPLICABLE_TEMPLATES` (the goal texts) in the same file, authored by the same agent in the same execute-time edit. The paraphrase wordings therefore systematically reuse the intent vocabulary (e.g. intent `create a new user` -> goal `add a new user to the system`; intent `retrieve a user by id` -> goal `get a user by their id`). The 0.2308 advantage cannot be separated from that joint authorship. This experiment removes it by construction.

## 3. Frozen mechanism registry (intents)

The registry is the 20 mechanisms produced by `research/harness/candidate_resolver.py::create_fixture()` from `research/harness/goal_generator.py::INTENTS`: five resources `users, posts, comments, albums, photos` x four operations `create, read, update, delete`. Mechanism ids are `mech_<resource>_<operation>`. The intent strings are the registry's public vocabulary and are the strings the independent author never saw.

Registry intents (verbatim, from the bound generator):

| mechanism_id | intent |
|---|---|
| mech_users_create | create a new user |
| mech_users_read | retrieve a user by id |
| mech_users_update | update a user |
| mech_users_delete | delete a user |
| mech_posts_create | create a new post |
| mech_posts_read | retrieve a post by id |
| mech_posts_update | update a post |
| mech_posts_delete | delete a post |
| mech_comments_create | create a new comment |
| mech_comments_read | retrieve a comment by id |
| mech_comments_update | update a comment |
| mech_comments_delete | delete a comment |
| mech_albums_create | create a new album |
| mech_albums_read | retrieve an album by id |
| mech_albums_update | update an album |
| mech_albums_delete | delete an album |
| mech_photos_create | create a new photo |
| mech_photos_read | retrieve a photo by id |
| mech_photos_update | update a photo |
| mech_photos_delete | delete a photo |

## 4. Frozen goal bank and authoring provenance

### 4.1 Authoring provenance record

- Author: a fresh-context agent process invoked during DESIGN (no prior conversation, no repository reads).
- Input given to the author: ONLY the schema `{users, posts, comments, albums, photos} x {create = make a brand-new record, read = look up exactly one existing record, update = change fields of exactly one existing record, delete = remove exactly one existing record}`, plus the instruction to write 5 distinct natural goals per cell and 20 out-of-scope goals.
- Input explicitly withheld: the 20 registry intent strings in section 3 (the author was instructed not to read any repository file and had no access to the intent vocabulary). This is the operational meaning of "a process that never sees the mechanism intent strings".
- Labels: the author assigned each applicable goal its `(resource, operation)` cell; DESIGN mapped the cell to `mech_<resource>_<operation>`. The label mapping is structural (resource+operation), not derived from intent text.
- Authoring timestamp: 2026-10-11 (DESIGN session for EXP-GRAPH-38112374668).
- Bank canonical sha256 (over `json.dumps(bank, sort_keys=True, separators=(",",":"))`): `1fc5fca59d96b678ee2220c91ba8c27182775a59d4d3f1dbbe51d285f55e4f70`.

### 4.2 Frozen bank (verbatim, 100 applicable + 20 out-of-scope)

The bank below is frozen by this preregistration. EXECUTE must extract it byte-for-byte into `derived_goal_bank.json`, verify the canonical sha256 above, and never edit a goal text. The 20 out-of-scope goals are the `NC-NO-APPLICABLE` population and are NOT part of the primary metric; they are reported as the substrate's unsupported-request population. The 20 verbatim registry intents from section 3 form the `PC-VERBATIM-INTENT` control and are NOT part of the bank.

```json
{
  "applicable": [
    {
      "id": "app_001",
      "operation": "create",
      "resource": "users",
      "text": "add a new user to the system"
    },
    {
      "id": "app_002",
      "operation": "create",
      "resource": "users",
      "text": "register a user account please"
    },
    {
      "id": "app_003",
      "operation": "create",
      "resource": "users",
      "text": "create a fresh user record"
    },
    {
      "id": "app_004",
      "operation": "create",
      "resource": "users",
      "text": "kindly add a brand new user"
    },
    {
      "id": "app_005",
      "operation": "create",
      "resource": "users",
      "text": "make a new user entry"
    },
    {
      "id": "app_006",
      "operation": "read",
      "resource": "users",
      "text": "fetch the user with id five"
    },
    {
      "id": "app_007",
      "operation": "read",
      "resource": "users",
      "text": "show me user number seven"
    },
    {
      "id": "app_008",
      "operation": "read",
      "resource": "users",
      "text": "look up a single user profile"
    },
    {
      "id": "app_009",
      "operation": "read",
      "resource": "users",
      "text": "retrieve that specific user's details"
    },
    {
      "id": "app_010",
      "operation": "read",
      "resource": "users",
      "text": "give me one user's information"
    },
    {
      "id": "app_011",
      "operation": "update",
      "resource": "users",
      "text": "modify the email of user three"
    },
    {
      "id": "app_012",
      "operation": "update",
      "resource": "users",
      "text": "change user five's display name"
    },
    {
      "id": "app_013",
      "operation": "update",
      "resource": "users",
      "text": "update a single user's phone number"
    },
    {
      "id": "app_014",
      "operation": "update",
      "resource": "users",
      "text": "edit the existing user record"
    },
    {
      "id": "app_015",
      "operation": "update",
      "resource": "users",
      "text": "revise user eight's profile fields"
    },
    {
      "id": "app_016",
      "operation": "delete",
      "resource": "users",
      "text": "remove user number twelve permanently"
    },
    {
      "id": "app_017",
      "operation": "delete",
      "resource": "users",
      "text": "delete the user with id four"
    },
    {
      "id": "app_018",
      "operation": "delete",
      "resource": "users",
      "text": "get rid of that single user"
    },
    {
      "id": "app_019",
      "operation": "delete",
      "resource": "users",
      "text": "erase an existing user record"
    },
    {
      "id": "app_020",
      "operation": "delete",
      "resource": "users",
      "text": "drop user seven from the database"
    },
    {
      "id": "app_021",
      "operation": "create",
      "resource": "posts",
      "text": "publish a brand new post"
    },
    {
      "id": "app_022",
      "operation": "create",
      "resource": "posts",
      "text": "add a new blog post"
    },
    {
      "id": "app_023",
      "operation": "create",
      "resource": "posts",
      "text": "create one fresh post entry"
    },
    {
      "id": "app_024",
      "operation": "create",
      "resource": "posts",
      "text": "write and add a post"
    },
    {
      "id": "app_025",
      "operation": "create",
      "resource": "posts",
      "text": "kindly create a single post"
    },
    {
      "id": "app_026",
      "operation": "read",
      "resource": "posts",
      "text": "fetch the post with id nine"
    },
    {
      "id": "app_027",
      "operation": "read",
      "resource": "posts",
      "text": "show me post number three"
    },
    {
      "id": "app_028",
      "operation": "read",
      "resource": "posts",
      "text": "retrieve a single post's content"
    },
    {
      "id": "app_029",
      "operation": "read",
      "resource": "posts",
      "text": "look up one specific post"
    },
    {
      "id": "app_030",
      "operation": "read",
      "resource": "posts",
      "text": "give me that post's details"
    },
    {
      "id": "app_031",
      "operation": "update",
      "resource": "posts",
      "text": "edit the title of post six"
    },
    {
      "id": "app_032",
      "operation": "update",
      "resource": "posts",
      "text": "change post two's body text"
    },
    {
      "id": "app_033",
      "operation": "update",
      "resource": "posts",
      "text": "update a single post's content"
    },
    {
      "id": "app_034",
      "operation": "update",
      "resource": "posts",
      "text": "modify the existing post record"
    },
    {
      "id": "app_035",
      "operation": "update",
      "resource": "posts",
      "text": "revise post eleven's title field"
    },
    {
      "id": "app_036",
      "operation": "delete",
      "resource": "posts",
      "text": "delete the post with id eight"
    },
    {
      "id": "app_037",
      "operation": "delete",
      "resource": "posts",
      "text": "remove post number fifteen"
    },
    {
      "id": "app_038",
      "operation": "delete",
      "resource": "posts",
      "text": "erase that single post entry"
    },
    {
      "id": "app_039",
      "operation": "delete",
      "resource": "posts",
      "text": "drop an existing post record"
    },
    {
      "id": "app_040",
      "operation": "delete",
      "resource": "posts",
      "text": "get rid of post three"
    },
    {
      "id": "app_041",
      "operation": "create",
      "resource": "comments",
      "text": "add a new comment now"
    },
    {
      "id": "app_042",
      "operation": "create",
      "resource": "comments",
      "text": "post one fresh comment"
    },
    {
      "id": "app_043",
      "operation": "create",
      "resource": "comments",
      "text": "create a single comment record"
    },
    {
      "id": "app_044",
      "operation": "create",
      "resource": "comments",
      "text": "write a brand new comment"
    },
    {
      "id": "app_045",
      "operation": "create",
      "resource": "comments",
      "text": "kindly add one comment entry"
    },
    {
      "id": "app_046",
      "operation": "read",
      "resource": "comments",
      "text": "fetch the comment with id two"
    },
    {
      "id": "app_047",
      "operation": "read",
      "resource": "comments",
      "text": "show me comment number five"
    },
    {
      "id": "app_048",
      "operation": "read",
      "resource": "comments",
      "text": "retrieve a single comment's text"
    },
    {
      "id": "app_049",
      "operation": "read",
      "resource": "comments",
      "text": "look up one specific comment"
    },
    {
      "id": "app_050",
      "operation": "read",
      "resource": "comments",
      "text": "give me that comment's content"
    },
    {
      "id": "app_051",
      "operation": "update",
      "resource": "comments",
      "text": "edit the body of comment four"
    },
    {
      "id": "app_052",
      "operation": "update",
      "resource": "comments",
      "text": "change comment seven's text"
    },
    {
      "id": "app_053",
      "operation": "update",
      "resource": "comments",
      "text": "update a single comment's content"
    },
    {
      "id": "app_054",
      "operation": "update",
      "resource": "comments",
      "text": "modify the existing comment record"
    },
    {
      "id": "app_055",
      "operation": "update",
      "resource": "comments",
      "text": "revise comment nine's message"
    },
    {
      "id": "app_056",
      "operation": "delete",
      "resource": "comments",
      "text": "delete the comment with id six"
    },
    {
      "id": "app_057",
      "operation": "delete",
      "resource": "comments",
      "text": "remove comment number ten"
    },
    {
      "id": "app_058",
      "operation": "delete",
      "resource": "comments",
      "text": "erase that single comment entry"
    },
    {
      "id": "app_059",
      "operation": "delete",
      "resource": "comments",
      "text": "drop an existing comment record"
    },
    {
      "id": "app_060",
      "operation": "delete",
      "resource": "comments",
      "text": "get rid of comment two"
    },
    {
      "id": "app_061",
      "operation": "create",
      "resource": "albums",
      "text": "add a new photo album"
    },
    {
      "id": "app_062",
      "operation": "create",
      "resource": "albums",
      "text": "create one fresh album"
    },
    {
      "id": "app_063",
      "operation": "create",
      "resource": "albums",
      "text": "make a brand new album record"
    },
    {
      "id": "app_064",
      "operation": "create",
      "resource": "albums",
      "text": "start a single new album"
    },
    {
      "id": "app_065",
      "operation": "create",
      "resource": "albums",
      "text": "kindly add one album entry"
    },
    {
      "id": "app_066",
      "operation": "read",
      "resource": "albums",
      "text": "fetch the album with id three"
    },
    {
      "id": "app_067",
      "operation": "read",
      "resource": "albums",
      "text": "show me album number eight"
    },
    {
      "id": "app_068",
      "operation": "read",
      "resource": "albums",
      "text": "retrieve a single album's details"
    },
    {
      "id": "app_069",
      "operation": "read",
      "resource": "albums",
      "text": "look up one specific album"
    },
    {
      "id": "app_070",
      "operation": "read",
      "resource": "albums",
      "text": "give me that album's information"
    },
    {
      "id": "app_071",
      "operation": "update",
      "resource": "albums",
      "text": "edit the title of album five"
    },
    {
      "id": "app_072",
      "operation": "update",
      "resource": "albums",
      "text": "change album four's name"
    },
    {
      "id": "app_073",
      "operation": "update",
      "resource": "albums",
      "text": "update a single album's details"
    },
    {
      "id": "app_074",
      "operation": "update",
      "resource": "albums",
      "text": "modify the existing album record"
    },
    {
      "id": "app_075",
      "operation": "update",
      "resource": "albums",
      "text": "revise album six's title field"
    },
    {
      "id": "app_076",
      "operation": "delete",
      "resource": "albums",
      "text": "delete the album with id seven"
    },
    {
      "id": "app_077",
      "operation": "delete",
      "resource": "albums",
      "text": "remove album number nine"
    },
    {
      "id": "app_078",
      "operation": "delete",
      "resource": "albums",
      "text": "erase that single album entry"
    },
    {
      "id": "app_079",
      "operation": "delete",
      "resource": "albums",
      "text": "drop an existing album record"
    },
    {
      "id": "app_080",
      "operation": "delete",
      "resource": "albums",
      "text": "get rid of album two"
    },
    {
      "id": "app_081",
      "operation": "create",
      "resource": "photos",
      "text": "add a new photo record"
    },
    {
      "id": "app_082",
      "operation": "create",
      "resource": "photos",
      "text": "create one fresh photo entry"
    },
    {
      "id": "app_083",
      "operation": "create",
      "resource": "photos",
      "text": "make a brand new photo"
    },
    {
      "id": "app_084",
      "operation": "create",
      "resource": "photos",
      "text": "insert a single new photo"
    },
    {
      "id": "app_085",
      "operation": "create",
      "resource": "photos",
      "text": "kindly add one photo record"
    },
    {
      "id": "app_086",
      "operation": "read",
      "resource": "photos",
      "text": "fetch the photo with id ten"
    },
    {
      "id": "app_087",
      "operation": "read",
      "resource": "photos",
      "text": "show me photo number four"
    },
    {
      "id": "app_088",
      "operation": "read",
      "resource": "photos",
      "text": "retrieve a single photo's details"
    },
    {
      "id": "app_089",
      "operation": "read",
      "resource": "photos",
      "text": "look up one specific photo"
    },
    {
      "id": "app_090",
      "operation": "read",
      "resource": "photos",
      "text": "give me that photo's information"
    },
    {
      "id": "app_091",
      "operation": "update",
      "resource": "photos",
      "text": "edit the url of photo three"
    },
    {
      "id": "app_092",
      "operation": "update",
      "resource": "photos",
      "text": "change photo six's title"
    },
    {
      "id": "app_093",
      "operation": "update",
      "resource": "photos",
      "text": "update a single photo's details"
    },
    {
      "id": "app_094",
      "operation": "update",
      "resource": "photos",
      "text": "modify the existing photo record"
    },
    {
      "id": "app_095",
      "operation": "update",
      "resource": "photos",
      "text": "revise photo eight's caption field"
    },
    {
      "id": "app_096",
      "operation": "delete",
      "resource": "photos",
      "text": "delete the photo with id twelve"
    },
    {
      "id": "app_097",
      "operation": "delete",
      "resource": "photos",
      "text": "remove photo number five"
    },
    {
      "id": "app_098",
      "operation": "delete",
      "resource": "photos",
      "text": "erase that single photo entry"
    },
    {
      "id": "app_099",
      "operation": "delete",
      "resource": "photos",
      "text": "drop an existing photo record"
    },
    {
      "id": "app_100",
      "operation": "delete",
      "resource": "photos",
      "text": "get rid of photo nine"
    }
  ],
  "out_of_scope": [
    {
      "id": "oos_001",
      "text": "list all the users",
      "why_unsupported": "lists many records; not a single-record read"
    },
    {
      "id": "oos_002",
      "text": "search posts by the keyword tiger",
      "why_unsupported": "search over many records; no search operation exists"
    },
    {
      "id": "oos_003",
      "text": "show every comment on an entry",
      "why_unsupported": "lists many records; not a single-record read"
    },
    {
      "id": "oos_004",
      "text": "count the total number of photos",
      "why_unsupported": "aggregate count; not one of the four single-record operations"
    },
    {
      "id": "oos_005",
      "text": "filter albums by creation year",
      "why_unsupported": "filtering across records; no filter operation exists"
    },
    {
      "id": "oos_006",
      "text": "log in with my credentials",
      "why_unsupported": "authentication; not a CRUD operation on a collection"
    },
    {
      "id": "oos_007",
      "text": "upload a new image file",
      "why_unsupported": "media upload; not a record create"
    },
    {
      "id": "oos_008",
      "text": "tag a post with technology",
      "why_unsupported": "tagging; no tag operation exists"
    },
    {
      "id": "oos_009",
      "text": "like the third post",
      "why_unsupported": "liking; no like operation exists"
    },
    {
      "id": "oos_010",
      "text": "follow user number seven",
      "why_unsupported": "follow relationship; not a supported single-record operation"
    },
    {
      "id": "oos_011",
      "text": "export all comments to csv",
      "why_unsupported": "bulk export; not a single-record operation"
    },
    {
      "id": "oos_012",
      "text": "delete all posts at once",
      "why_unsupported": "bulk delete of many records; not a single-record delete"
    },
    {
      "id": "oos_013",
      "text": "find users whose name starts with a",
      "why_unsupported": "search/filter; no search operation exists"
    },
    {
      "id": "oos_014",
      "text": "get the newest five posts",
      "why_unsupported": "sorted list of many records; not a single-record read"
    },
    {
      "id": "oos_015",
      "text": "reset my forgotten account password",
      "why_unsupported": "authentication and account recovery; not CRUD"
    },
    {
      "id": "oos_016",
      "text": "sort albums alphabetically by title",
      "why_unsupported": "sorting across records; no sort operation exists"
    },
    {
      "id": "oos_017",
      "text": "import a batch of new posts",
      "why_unsupported": "bulk create of many records; not a single-record create"
    },
    {
      "id": "oos_018",
      "text": "download the photo image binary",
      "why_unsupported": "media download; not one of the four CRUD operations"
    },
    {
      "id": "oos_019",
      "text": "render the album gallery view",
      "why_unsupported": "custom view rendering; not a supported operation"
    },
    {
      "id": "oos_020",
      "text": "update every user's email address",
      "why_unsupported": "bulk update of many records; not a single-record update"
    }
  ]
}
```

## 5. Arms (stable identities)

- `A-EMBED-COSINE` (treatment): `research/harness/candidate_resolver.py::EmbeddingArgmaxResolver` over a `SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2", revision=c9745ed1d9f207416be6d2e6f8de32d1f161f9bf)` model. Selects `argmax` cosine between the goal embedding and the 20 normalized intent embeddings. Never abstains.
- `B-LEXICAL-OVERLAP` (strong null / comparator): `::LexicalOverlapResolver`. Selects `argmax` token set-Jaccard between goal tokens and each intent's tokens (lowercase whitespace split). Never abstains.
- `B-RANDOM-ROLE` (null floor): `::RandomRoleResolver` with seed 4242. Selects uniformly among mechanisms whose declared role matches the goal-inferred role. Never abstains. Role lists hold 5 mechanisms each, so its per-goal correctness is at most 1/5 by construction (lower when role inference errs).
- `B-INCUMBENT-KERNEL` (product baseline, measured not assumed): shipped `src/spider/kernel.py::SpiderKernel(registry, min_confidence=0.8).resolve(intent=goal_text, context={}, params=all_slots)`. Its `resolve` requires exact intent-string equality, so it can only bind the verbatim intents. `selected_mechanism_id` is scored whether the kernel returns `EXECUTABLE` or `EXPLORE`; `UNKNOWN` scores incorrect.
- `B-INTERNAL-ID-ORACLE` (ceiling): `::InternalIdOracle`. Receives the true target mechanism id via the goal's `target_mechanism_id` field; returns it, so the ceiling is 1.0 by construction unless the fixture is broken.
- `A-EMBED-COSINE-SHUFFLED` (instrument null, `NC-SHUFFLED-LABEL`): same intent embeddings as `A-EMBED-COSINE`, but the argmax index is mapped through a fixed permutation of the 20 mechanism labels (seed `38112374668`). Accuracy must collapse to chance.

A-EMBED-COSINE and B-LEXICAL-OVERLAP are structurally distinct functions (dense cosine over 384-d sentence embeddings vs set-Jaccard over whitespace tokens). `V9-NON-TAUTOLOGY` additionally requires their primary-set decision vectors to differ on at least one goal and the comparator to stay below 0.99.

All three `resolve`-based arms consume a goal object exposing `text` and `goal_id` (and `target_mechanism_id` for the oracle), exactly as the bound classes require; the frozen runner builds that object and never re-implements an arm.

## 6. Metrics and decision rule

Primary metric `M-PAIRED-DIFF-EMBED-MINUS-LEXICAL`: for the contamination-screened independently authored applicable set (primary set), per-goal `correct_A_EMBED - correct_B_LEXICAL` where `correct_arm = 1 if selected_mechanism_id == target_mechanism_id else 0`; report the mean difference and its paired family-blocked 95% bootstrap CI (`paired_bootstrap` from `research/harness/experiment_runner.py`, blocking unit = resource family, B=10000, alpha=0.05, with `numpy.random.seed(38112374668 % 2**32)` = `numpy.random.seed(3752636300)` called immediately before the call because that function draws from the global numpy RNG; the raw experiment id seed `38112374668` exceeds 2**32 and numpy would reject it, so the modulo is part of the frozen recipe).

Also reported: `M-MECH-ACC-EMBED`, `M-MECH-ACC-LEXICAL`, `M-MECH-ACC-RANDOM`, `M-MECH-ACC-INCUMBENT`, `M-MECH-ACC-ORACLE`, `M-MECH-ACC-EMBED-SHUFFLED`, `M-CONTAM-MAX-JACCARD` (max/mean over the applicable bank), `M-N-CONTAM-FLAGGED`, `M-N-PRIMARY`.

Contamination screen (`V-CONTAM-SCREEN`): for every goal compute `max` set-Jaccard against EVERY one of the 20 intents (same tokenisation as B-LEXICAL-OVERLAP). Flag as contaminated iff `max >= 0.60`; flagged goals are excluded from the primary set and reported. DESIGN instrument probe (non-outcome-bearing; it uses only the tokenisation over bank texts and intents and does not score any arm's decision): on the 100 applicable goals the maximum Jaccard to any intent is 0.50 and 0 goals are flagged at 0.60, so the screen is non-vacuous (a near-verbatim goal would be flagged) and non-degenerate. Neither `A-EMBED-COSINE` nor `B-LEXICAL-OVERLAP` accuracy, and not the paired difference, was computed during DESIGN.

Decision rule (precedence `MEASUREMENT_INVALID > FALSIFIES > MIXED > SUPPORTS`):

- `SUPPORTS`: V1-V11 all PASS AND PC PASS AND NC-SHUFFLE PASS AND V9-NON-TAUTOLOGY PASS AND `|primary_set| >= 80` AND `M-PAIRED-DIFF-EMBED-MINUS-LEXICAL.obs_diff > 0` AND `.ci_lower > 0`.
- `FALSIFIES`: V1-V11 all PASS AND `.obs_diff <= 0` (embedding selection does not exceed the token-overlap null on independently authored goals).
- `MIXED`: V1-V11 all PASS AND `.obs_diff > 0` but `.ci_lower <= 0` (positive point estimate, not decisive).
- `MEASUREMENT_INVALID` / `BLOCKED`: any V-gate fails or a hard prerequisite (model load, server start, fixture load) is unavailable; the exact failure is reported and the claim status is unchanged.

Reachability: the comparator is a genuinely different function over texts that are not the registry intents, and it is not pinned by a ceiling or floor (the instrument probe shows the maximum goal-to-intent token overlap is 0.50 < 1.0, while the shared resource nouns keep it off 0.0); the oracle is 1.0 by construction and B-RANDOM-ROLE is bounded by 1/5 per goal by construction. The primary quantity is therefore free to land `> 0` (SUPPORTS), `<= 0` (FALSIFIES) or positive-with-CI-including-0 (MIXED); no ceiling or floor baseline excludes either region, and no branch of the rule is empty. A weak treatment is a valid FALSIFIES, not a measurement failure: V7 gates only on treatment liveness (non-constant, valid selections), not on the treatment beating the floor.

## 7. Controls (stable identities, each able to fail)

- `PC-VERBATIM-INTENT` (positive control): the 20 intents of section 3 as goals. `A-EMBED-COSINE`, `B-LEXICAL-OVERLAP` and `B-INCUMBENT-KERNEL` must all score 1.0 (denominator 20); else `MEASUREMENT_INVALID`. Fails if the model, loader or registry is broken.
- `NC-SHUFFLED-LABEL` (instrument null): `A-EMBED-COSINE-SHUFFLED` accuracy must be `<= 0.20`; else `MEASUREMENT_INVALID`. Fails high on fixture/metric leakage.
- `NC-NO-APPLICABLE` (substrate null): the 20 out-of-scope goals. `B-INCUMBENT-KERNEL` must abstain (`UNKNOWN`) on all 20 (no exact intent); the treatment's non-abstention rate on this population is reported as the raw false-accept cost and is NOT a primary gate in this packet.
- `B-INTERNAL-ID-ORACLE` (ceiling): must be 1.0 on the primary set; else `MEASUREMENT_INVALID`.
- `V9-NON-TAUTOLOGY` (dynamic range): decision vectors of A-EMBED-COSINE and B-LEXICAL-OVERLAP differ on >= 1 primary goal AND the comparator accuracy `< 0.99`; else `MEASUREMENT_INVALID`. A treatment at the 1.0 ceiling is not a violation.
- `V-CONTAM-SCREEN` (contamination): as defined in section 6; non-vacuous and non-degenerate at the design instrument probe.

## 8. Measurement validity gates (V1-V11)

V1 primary metric definition (binding correctness of `selected_mechanism_id`, status-agnostic). V2 primary set definition and `|primary_set| >= 80`. V3 contamination screen. V4 authorship provenance. V5 PC. V6 oracle ceiling. V7 treatment liveness (A-EMBED-COSINE emits >= 2 distinct valid mechanism selections on the primary set; B-RANDOM-ROLE <= 0.30 floor sanity; the head-to-head is reported, not gated). V8 NC-SHUFFLED. V9 non-tautology (decision vectors differ; comparator below 0.99). V10 family-blocked bootstrap with explicit seed. V11 code bound via `freeze.json.artifact_hashes` plus the frozen reference runner.

This packet measures binding, not execution: the bound stdlib HTTP server module (`http_server.py`) is imported transitively by the metric module but is NOT started, and there is no per-goal state to reset because no action is executed. Execution correctness remains explicitly out of scope (section 1); an execution-substrate experiment is a separate packet.

## 9. Frozen reference runner (verbatim; EXECUTE transcribes unmodified)

EXECUTE must write this script unmodified at exactly `research/experiments/EXP-GRAPH-38112374668/runner.py` (the `parents[3]` repo-root resolution depends on that depth), run it, record its sha256 in `provenance.json`, and include its source as a raw artifact. It imports the bound modules; it does not re-implement any arm.

```python
#!/usr/bin/env python3
"""Frozen runner for EXP-GRAPH-38112374668. Verbatim from prereg.md. Do not modify."""
import argparse, hashlib, json, os, random, sys
from pathlib import Path

SEED = 38112374668
SEED32 = SEED % (2 ** 32)   # 3752636300; numpy.random.seed rejects seeds >= 2**32
BOOT = 10000


def canon_sha(obj):
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def toks(s):
    return set(s.lower().split())


def jaccard(a, b):
    A, B = toks(a), toks(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bank", required=True)
    ap.add_argument("--out", required=True)
    args = ap.parse_args()

    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    root = Path(__file__).resolve().parents[3]   # .../research/experiments/<id>/runner.py
    harness = root / "research" / "harness"
    cwd = os.getcwd()
    sys.path.insert(0, str(harness))
    import experiment_runner as ER          # module-level os.chdir happens here
    os.chdir(cwd)                            # restore
    import candidate_resolver as CR
    from goal_generator import INTENTS, PARAM_SLOTS
    sys.path.insert(0, str(root / "src"))
    from spider.registry import MechanismRegistry
    from spider.kernel import SpiderKernel
    from spider.models import Mechanism as KernelMechanism
    import numpy as np
    from sentence_transformers import SentenceTransformer

    bank = json.loads(Path(args.bank).read_text())
    bank_sha = canon_sha(bank)

    fixtures = CR.create_fixture()
    mech_ids = [m.mechanism_id for m in fixtures]

    model = SentenceTransformer(
        "sentence-transformers/all-MiniLM-L6-v2",
        revision="c9745ed1d9f207416be6d2e6f8de32d1f161f9bf",
    )
    embed = CR.EmbeddingArgmaxResolver(fixtures, model)
    lexical = CR.LexicalOverlapResolver(fixtures)
    role = CR.RandomRoleResolver(fixtures, seed=4242)
    oracle = CR.InternalIdOracle(fixtures)

    reg_path = out_dir / "_incumbent_registry.jsonl"
    reg = MechanismRegistry(reg_path)
    reg.replace([
        KernelMechanism(
            mechanism_id=m.mechanism_id, intent=m.intent,
            preconditions={}, action_template={"verb": m.role, "resource": m.family},
            postconditions={}, parameter_slots=list(m.parameter_slots),
        )
        for m in fixtures
    ])
    kernel = SpiderKernel(reg, min_confidence=0.8)

    def incumbent_select(text, target):
        params = {s: "<%s>" % s for s in PARAM_SLOTS.get(target, [])}
        return kernel.resolve(text, {}, params).mechanism_id or ""

    def goal(text, goal_id, target):
        # the bound arm classes read these exact keys
        return {"text": text, "goal_id": goal_id, "target_mechanism_id": target}

    def embed_index(text):
        e = model.encode([text], convert_to_numpy=True, normalize_embeddings=True)[0]
        return int(np.argmax(embed.mechanism_embeddings.dot(e)))

    perm = list(range(len(fixtures)))
    random.Random(SEED).shuffle(perm)
    shuffled_ids = [mech_ids[perm[i]] for i in range(len(mech_ids))]

    def target_of(g):
        return "mech_%s_%s" % (g["resource"], g["operation"])

    # contamination screen over the full bank
    contam = {}
    for g in bank["applicable"] + bank["out_of_scope"]:
        vals = [(jaccard(g["text"], m.intent), m.mechanism_id) for m in fixtures]
        contam[g["id"]] = {"max": max(v for v, _ in vals), "argmax": max(vals)[1]}

    primary = [g for g in bank["applicable"] if contam[g["id"]]["max"] < 0.60]

    arms = {
        "A-EMBED-COSINE": lambda gg: embed.resolve(gg).mechanism_id,
        "B-LEXICAL-OVERLAP": lambda gg: lexical.resolve(gg).mechanism_id,
        "B-RANDOM-ROLE": lambda gg: role.resolve(gg).mechanism_id,
        "B-EMBED-COSINE-SHUFFLED": lambda gg: shuffled_ids[embed_index(gg["text"])],
    }

    rows = []
    for g in primary:
        t = target_of(g)
        gd = goal(g["text"], g["id"], t)
        row = {"goal_id": g["id"], "text": g["text"], "target": t,
               "family": g["resource"], "contam_max": round(contam[g["id"]]["max"], 4)}
        for name, fn in arms.items():
            sel = fn(gd)
            row[name] = sel
            row[name + "_correct"] = int(sel == t)
        sel = incumbent_select(g["text"], t)
        row["B-INCUMBENT-KERNEL"] = sel
        row["B-INCUMBENT-KERNEL_correct"] = int(sel == t)
        sel = oracle.resolve(gd).mechanism_id
        row["B-INTERNAL-ID-ORACLE"] = sel
        row["B-INTERNAL-ID-ORACLE_correct"] = int(sel == t)
        rows.append(row)

    def acc(name):
        vals = [r[name + "_correct"] for r in rows]
        return {"numerator": int(sum(vals)), "denominator": len(vals),
                "accuracy": (sum(vals) / len(vals)) if vals else None}

    accs = {name: acc(name) for name in list(arms) + ["B-INCUMBENT-KERNEL", "B-INTERNAL-ID-ORACLE"]}

    cand = np.array([r["A-EMBED-COSINE_correct"] for r in rows], dtype=float)
    base = np.array([r["B-LEXICAL-OVERLAP_correct"] for r in rows], dtype=float)
    fams = np.array([r["family"] for r in rows])
    np.random.seed(SEED32)
    obs, lo, hi = ER.paired_bootstrap(cand, base, fams, n_resamples=BOOT, alpha=0.05)

    # PC-VERBATIM-INTENT
    pc = {}
    for mid in mech_ids:
        gd = goal(INTENTS[mid], "pc_" + mid, mid)
        pc[mid] = {
            "A-EMBED-COSINE": int(embed.resolve(gd).mechanism_id == mid),
            "B-LEXICAL-OVERLAP": int(lexical.resolve(gd).mechanism_id == mid),
            "B-INCUMBENT-KERNEL": int(incumbent_select(INTENTS[mid], mid) == mid),
        }
    pc_acc = {a: {"numerator": sum(v[a] for v in pc.values()), "denominator": len(pc),
                  "accuracy": sum(v[a] for v in pc.values()) / len(pc)}
              for a in ("A-EMBED-COSINE", "B-LEXICAL-OVERLAP", "B-INCUMBENT-KERNEL")}

    # NC-NO-APPLICABLE: incumbent abstention + embed non-abstention
    oos = []
    for g in bank["out_of_scope"]:
        oos.append({
            "goal_id": g["id"], "text": g["text"],
            "B-INCUMBENT-KERNEL": incumbent_select(g["text"], "mech_users_read"),
            "A-EMBED-COSINE": embed.resolve(goal(g["text"], g["id"], "")).mechanism_id,
        })

    metrics = {
        "M-N-PRIMARY": len(rows),
        "M-N-CONTAM-FLAGGED": sum(1 for g in bank["applicable"] if contam[g["id"]]["max"] >= 0.60),
        "M-CONTAM-MAX-JACCARD": {
            "max": max(contam[g["id"]]["max"] for g in bank["applicable"]),
            "mean": sum(contam[g["id"]]["max"] for g in bank["applicable"]) / len(bank["applicable"]),
        },
        "arms": accs,
        "M-PAIRED-DIFF-EMBED-MINUS-LEXICAL": {"obs_diff": float(obs), "ci_lower": float(lo), "ci_upper": float(hi)},
        "PC-VERBATIM-INTENT": pc_acc,
        "BANK_SHA256": bank_sha,
    }

    (out_dir / "derived_metrics.json").write_text(json.dumps(metrics, indent=2, sort_keys=True) + "\n")
    with (out_dir / "task_results.jsonl").open("w") as fh:
        for r in rows:
            fh.write(json.dumps(r, sort_keys=True) + "\n")
    (out_dir / "no_applicable.json").write_text(json.dumps(oos, indent=2, sort_keys=True) + "\n")
    print(json.dumps(metrics, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
```

EXECUTE procedure: `pip install sentence-transformers==3.0.1 torch==2.4.0 numpy==1.26.4`; extract the bank to `derived_goal_bank.json` (canonical sha256 must equal `1fc5fca59d96b678ee2220c91ba8c27182775a59d4d3f1dbbe51d285f55e4f70`); run the frozen runner; then apply V1-V11 and the decision rule and write `result.json` / `report.md` / `provenance.json`. If `pip install`, the HF download, or model load fails, write `status=BLOCKED` with the exact failure; that is an operational outcome, not a scientific negative.

## 10. Consequences

- Positive (`SUPPORTS`): the embedding advantage survives removal of the joint-authorship confound; C-SEMANTIC-RESOLVE's embedding-selection sub-mechanism moves toward EXPERIMENTAL and stays on the shipped resolve path; follow-ups are parameter binding and abstention calibration. No product promotion.
- Negative (`FALSIFIES`/`MIXED`): the bounded 0.2308 advantage was (at least substantially) a joint-authorship artifact; embedding-argmax must not be relied on, the claim stays HYPOTHESIS, and the next attempt must change architecture rather than re-tune thresholds. The claim is not retired.

## 11. Relation to pre-2.0 and to prior Research 2.0 attempts

Pre-2.0 `P2-BLIND-COMPOSITION` (artifact 4.697, sha `017a80aeb9a6759c8f6913a37031ff1616ec1bda`) reported 3/3 unseen compositions vs 0/3 weak baselines but only with keyword/oracle guidance - the same authorship/oracle confound class removed here. Pre-2.0 `P2-MIND2WEB` found retrieval 47/176 vs literal human routes 6/176, consistent with retrieve-and-bind over route replay. Prior Research 2.0 packets died on control-plane/design defects, not science: `EXP-GRAPH-36287167610` was MEASUREMENT_INVALID (inert gate, null control 0.5, and comparator identical to candidate); `EXP-GRAPH-36279237023` was MEASUREMENT_INVALID (V9 code not hashed into freeze, ambiguous false-accept denominator, inert gate); `EXP-GRAPH-36272373909` was MEASUREMENT_INVALID (positive control had zero trials). This packet fixes V9 by binding outcome-bearing code via `freeze_artifacts`, forbids a tautological comparator via V9-NON-TAUTOLOGY, makes the contamination screen explicit, and authors goals independently.

## 12. Validity threats (disclosed)

1. The independent author is an LLM; its word distribution may still correlate with the intent author's distribution through shared language. The contamination screen measures the resulting lexical overlap and the primary set is defined only after screening; the residual semantic-similarity correlation cannot be fully randomized away.
2. `paired_bootstrap` draws from the global numpy RNG; the seed is set immediately before the call, but any other numpy use between seeding and calling would change resamples. The frozen runner performs the call directly after seeding.
3. `experiment_runner` executes `os.chdir(harness_dir)` at import time; the frozen runner saves and restores cwd, and EXECUTE must confirm.
4. Family blocking uses 5 resource families; with only 5 blocks the bootstrap is coarse and can yield a wide CI. This is intentional and reported; MIXED is a legitimate outcome.
5. The bank exercises one application (5 resources x 4 operations). No cross-application generalization is claimed.
6. The DESIGN instrument probe observed only the bank's token overlap against the registry intents (a fixture property, independent of any arm). Neither outcome arm nor the paired difference was scored during DESIGN. The probe is disclosed in section 6.
