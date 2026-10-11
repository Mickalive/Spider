# EXP-GRAPH-38175554380 preregistration

Lane: graph. Claim: C-SEMANTIC-RESOLVE (status HYPOTHESIS). Design-contract version: 2.
Immutable request: `research/experiments/EXP-GRAPH-38175554380/request.json`.
Base SHA at design time: `7ff6752ff348f662a3c13f6540e6434dbb3b790a`.

This preregistration is frozen together with `spec.json` and `request.json` by `freeze.json`.
Nothing in this file may be edited after freeze. The data blocks between the BEGIN/END markers and
the runner script are part of this file and are therefore bound by `freeze.json.hashes["prereg.md"]`;
the runner re-verifies that hash at EXECUTE (V12-A), confirms its own source equals the `FROZEN RUNNER`
block (V12-B), and re-verifies each extracted block against the `CANONICAL-HASHES` block below (V4). `spec.json.freeze_artifacts` lists the repository files this
experiment reads; the authored bank is carried **inside this file**, not as a new repository file,
so no new mutable dependency is created.

---

## 1. Preregistered question, hypothesis and falsifier

Binding definitions live in `spec.json` (`question`, `hypothesis`, `falsifier`). In brief:

- **Question (Director mandate A).** On an independently-attestable unseen-goal bank, does
  max-cosine selection over intent embeddings (`A-EMBED-COSINE`) strictly exceed a **strong
  deterministic lexical resolver** (`B-LEX-STRONG`: a fixed operation-synonym dictionary plus a
  resource-noun dictionary, *not* token-set Jaccard), with a paired family-blocked 95% bootstrap
  lower bound above zero?
- **Question (Director mandate B).** Can an applicability/abstention gate calibrated on a held-out
  calibration split reach pooled false-accept <= 0.10 at coverage >= 0.50 with unknown-precision
  >= 0.85 on the disjoint test split?
- **Hypothesis.** On the contamination-screened acceptable primary set, `A-EMBED-COSINE` binds the
  correct mechanism more often than `B-LEX-STRONG`, and the paired family-blocked 95% bootstrap lower
  bound on (`A-EMBED-COSINE` - `B-LEX-STRONG`) is above zero. Because the comparator uses a *fixed*
  lexicon authored by a process that never saw the bank, any advantage must come from semantic
  generalization rather than lookup leakage.
- **Falsifier.** Paired difference <= 0 with 95% upper bound <= 0, or a 95% interval that contains 0.
  Both are valid scientific negatives (status COMPLETE), never infrastructure failures.

## 2. Scope and out-of-scope

Measured: mechanism-identity selection accuracy on independently authored single-operation and
out-of-scope goals (which mechanism, if any, the resolver binds); comparator discrimination;
control sensitivity; risk/coverage of a two-feature applicability gate on a disjoint split.
**Not** measured or claimed: parameter binding, HTTP execution correctness, cross-app
generalization, latency/token economics, ECE gating (descriptive only), and any product promotion
(only a DIRECTOR verdict can grant that).

**Not a repetition of pre-2.0 work (DESIGN satisfiability probe, non-outcome-bearing).** The Director
mandate's `comparative_reasoning` classifies this as a DISTINCT_EXTENSION. A keyword search of
`codex/legacy_artifact_index.json` (308511 extracted characters) for the tokens
`semantic`, `embed`, `resolv`, `abstention`, `cosine`, `similarity`, `keyword`, `lexical` returns
**zero** matches (only `retrieval` appears, 7 times, from the P2-MIND2WEB route count). No pre-2.0
artifact tested embedding-based unseen-goal resolution or an applicability/abstention gate, and the
parent packet is not rerun because it used a weak token-Jaccard null and no disjoint-calibrated gate.
The remaining first-class threat — that the mandate's legacy screen read only the compact index, not
all 1401 frozen artifacts — is disclosed; it does not change the decision value of this packet.

## 3. Inherited state and prior-packet decomposition (parent_handoff continuity)

Parent packet `EXP-GRAPH-38166215691` (`parent_handoff.json` sha256
`4303ed18c7618d2fce32825a72d0f88cbdac4bc2587aa811e5c29c1c5aac488c`; request disposition **USE**;
audit REVISE, `producer_claim_supported=false`; seed 3806477323). Four-way continuity, preserved
without upgrading or downgrading:

- **Established (inherited as measured, not re-asserted as claim evidence).** The parent measurement
  transaction is valid and independently reproduced: on the parent's frozen 140-goal bank, after its
  V3 screen removed 9 near-copies (its primary set = 93), `A-EMBED-COSINE` = 86/93 (0.9247) strictly
  exceeded its token-set-Jaccard null `B-LEXICAL-OVERLAP` = 49/93 (0.5269); paired family-blocked
  difference 0.3978, 95% CI [0.2967, 0.4947], B=10000, alpha=0.05, 5 families; random 21/93;
  incumbent exact-intent kernel 0/93; oracle 93/93. Its abstention sub-question was a
  measurement-valid bounded negative: single global max-cosine threshold t*=0.44446519017219543
  chosen on calibration (39 applicable + 19 out-of-scope), test (54 applicable + 19 out-of-scope)
  coverage 1.0, pooled false-accept 0.5789, unknown-precision 1.0, class AB-NOT-MET. The claim
  `C-SEMANTIC-RESOLVE` remained HYPOTHESIS with no promotion.
- **Rejected (must not be carried forward).** (i) That the parent confirms a confound-free /
  contamination-free embedding advantage: its authorship-independence was an unaudited self-declared
  narrative inherited from a DESIGN-failed precursor, and its screen shared tokenisation with the
  comparator (RQF-01/VF-01). (ii) That `B-LEXICAL-OVERLAP` is a strong null or that 0.3978 shows
  embeddings are needed: audit-constructed deterministic baselines reached 75/93 and 93/93 (BF-01 /
  RQF-04). (iii) That a single global max-cosine threshold can ship as an applicability gate
  (AB-NOT-MET, false-accept 0.5789). (iv) Any generalization beyond the 20-mechanism fixture, the
  140-goal bank and the (unpinned) checkpoint, or any citation of the incumbent/oracle as independent
  corroboration (structural tautologies). (v) Any reading of audit REVISE as a global falsification
  of the claim.
- **Unknown (this packet directly tests two of these).** Whether the bank is authored by a process
  that never saw the registry intents (UNRES-01) — addressed here by blind, hash-committed authoring
  transcripts (V4). Whether embedding selection exceeds a *strong fixed deterministic*
  operation-synonym + resource-noun resolver (UNRES-03) — addressed here by `B-LEX-STRONG`. Whether
  any gate can reach the calibration targets on a disjoint split (UNRES-01) — addressed here by
  `D-GATE`. Still out of scope: generalization beyond this fixture/family set, and checkpoint drift.
- **Do not assume.** (i) That authorship independence is cryptographically guaranteed (latent
  pretrained knowledge cannot be excluded; VN-07). (ii) That `B-LEX-STRONG` is weak because
  `B-LEXICAL-OVERLAP` was — the mandate expects it to be strong. (iii) That the parent's
  single-threshold gate design is adequate. (iv) That any product promotion follows from a positive
  outcome here; only a DIRECTOR verdict can promote. (v) That the frozen checkpoint revision is
  installable: the parent could not fetch `c9745ed1d9f207416be6d2e6f8de32d1f161f9bf` and resolved to
  `1110a243fdf4706b3f48f1d95db1a4f5529b4d41`; this design requests the frozen revision and records
  the actually-resolved identity (VN-08).


## 4. Authorship provenance and frozen blocks

The applicable bank (`GOAL BANK`), the out-of-scope bank (`OOS BANK`) and the comparator lexicon
(`LEXICON`) were authored by **three separate fresh-context processes** with no tools and no file
access, each following one of the prompts recorded verbatim in `AUTHOR-PROMPTS`. The applicable and
out-of-scope authors never saw the mechanism intent strings, the goal-generator surfaces, or any
repository file. The lexicon author never saw the bank. The prompts were checked (V4) to contain no
mechanism intent substring and to be far (max token-Jaccard 0.0207) from every prior authoring
surface. Residual limitation (VN-07): latent pretrained vocabulary cannot be cryptographically
excluded; the contamination screen (section 9) plus the *fixed, bank-blind* comparator is the
mitigation.

Canonical block hashes (sha256 of the exact bytes between the markers, no trailing newline):

```json
{
  "blocks": {
    "AUTHOR-PROMPTS": "2d2f0ad1a4a1c90694f6ba66ba93299bb5548e42c1db98218577c8fc663a9ccc",
    "GOAL BANK": "3a30e67f171385f9b5207e793a46575102aca7f4d8e53772e16894d92ba289dd",
    "LEXICON": "56d874db361b2377f6faf767f5c2aa652066f6b0b50d7a6081512af141ae9e5e",
    "OOS BANK": "3b74d933940c4cf6e4f43293cbc3d1e8c5ebd558a66d5029f38b23d59f24e5c1",
    "PRIOR-PARENT-BANK-TEXTS": "b1deb80890cf29aeaf39fb5b56c777b548d8606401b8e36a5bf82bad9e324f6a"
  }
}
```

<!-- BEGIN GOAL BANK -->
{"family":"users","op":"CREATE","text":"Add one new user."}
{"family":"users","op":"CREATE","text":"Please make a new account."}
{"family":"users","op":"CREATE","text":"Register a single new member."}
{"family":"users","op":"CREATE","text":"Set up one new profile."}
{"family":"users","op":"CREATE","text":"Introduce a fresh customer."}
{"family":"users","op":"CREATE","text":"Generate one new subscriber."}
{"family":"users","op":"READ","text":"Fetch the user with this id."}
{"family":"users","op":"READ","text":"Retrieve one account by its identifier."}
{"family":"users","op":"READ","text":"Get the single member matching this id."}
{"family":"users","op":"READ","text":"Look up one profile using its identifier."}
{"family":"users","op":"READ","text":"View the one customer with this id."}
{"family":"users","op":"READ","text":"Pull up the single subscriber with this id."}
{"family":"users","op":"UPDATE","text":"Change the user with this id."}
{"family":"users","op":"UPDATE","text":"Modify one account identified by this id."}
{"family":"users","op":"UPDATE","text":"Edit the single member with this identifier."}
{"family":"users","op":"UPDATE","text":"Adjust one profile by its id."}
{"family":"users","op":"UPDATE","text":"Revise the one customer with this id."}
{"family":"users","op":"UPDATE","text":"Amend the single subscriber with this identifier."}
{"family":"users","op":"DELETE","text":"Remove the user with this id."}
{"family":"users","op":"DELETE","text":"Erase one account by its identifier."}
{"family":"users","op":"DELETE","text":"Discard the single member with this id."}
{"family":"users","op":"DELETE","text":"Eliminate one profile using this id."}
{"family":"users","op":"DELETE","text":"Drop the one customer with this identifier."}
{"family":"users","op":"DELETE","text":"Get rid of the single subscriber with this id."}
{"family":"posts","op":"CREATE","text":"Add one new post."}
{"family":"posts","op":"CREATE","text":"Make a new article."}
{"family":"posts","op":"CREATE","text":"Register a single new entry."}
{"family":"posts","op":"CREATE","text":"Set up one new blog entry."}
{"family":"posts","op":"CREATE","text":"Introduce a new story."}
{"family":"posts","op":"CREATE","text":"Generate one new publication."}
{"family":"posts","op":"READ","text":"Fetch the post with this id."}
{"family":"posts","op":"READ","text":"Retrieve one article by its identifier."}
{"family":"posts","op":"READ","text":"Get the single entry matching this id."}
{"family":"posts","op":"READ","text":"Look up one blog entry using this id."}
{"family":"posts","op":"READ","text":"View the one story with this identifier."}
{"family":"posts","op":"READ","text":"Pull up the single publication with this id."}
{"family":"posts","op":"UPDATE","text":"Change the post with this id."}
{"family":"posts","op":"UPDATE","text":"Modify one article by its identifier."}
{"family":"posts","op":"UPDATE","text":"Edit the single entry with this id."}
{"family":"posts","op":"UPDATE","text":"Adjust one blog entry using this id."}
{"family":"posts","op":"UPDATE","text":"Revise the one story with this identifier."}
{"family":"posts","op":"UPDATE","text":"Amend the single publication with this id."}
{"family":"posts","op":"DELETE","text":"Remove the post with this id."}
{"family":"posts","op":"DELETE","text":"Erase one article by its identifier."}
{"family":"posts","op":"DELETE","text":"Discard the single entry with this id."}
{"family":"posts","op":"DELETE","text":"Eliminate one blog entry using this id."}
{"family":"posts","op":"DELETE","text":"Drop the one story with this identifier."}
{"family":"posts","op":"DELETE","text":"Get rid of the single publication with this id."}
{"family":"comments","op":"CREATE","text":"Add one new comment."}
{"family":"comments","op":"CREATE","text":"Make a new remark."}
{"family":"comments","op":"CREATE","text":"Register a single new note."}
{"family":"comments","op":"CREATE","text":"Set up one new reply."}
{"family":"comments","op":"CREATE","text":"Introduce a new response."}
{"family":"comments","op":"CREATE","text":"Generate one new annotation."}
{"family":"comments","op":"READ","text":"Fetch the comment with this id."}
{"family":"comments","op":"READ","text":"Retrieve one remark by its identifier."}
{"family":"comments","op":"READ","text":"Get the single note matching this id."}
{"family":"comments","op":"READ","text":"Look up one reply using this id."}
{"family":"comments","op":"READ","text":"View the one response with this identifier."}
{"family":"comments","op":"READ","text":"Pull up the single annotation with this id."}
{"family":"comments","op":"UPDATE","text":"Change the comment with this id."}
{"family":"comments","op":"UPDATE","text":"Modify one remark by its identifier."}
{"family":"comments","op":"UPDATE","text":"Edit the single note with this id."}
{"family":"comments","op":"UPDATE","text":"Adjust one reply using this id."}
{"family":"comments","op":"UPDATE","text":"Revise the one response with this identifier."}
{"family":"comments","op":"UPDATE","text":"Amend the single annotation with this id."}
{"family":"comments","op":"DELETE","text":"Remove the comment with this id."}
{"family":"comments","op":"DELETE","text":"Erase one remark by its identifier."}
{"family":"comments","op":"DELETE","text":"Discard the single note with this id."}
{"family":"comments","op":"DELETE","text":"Eliminate one reply using this id."}
{"family":"comments","op":"DELETE","text":"Drop the one response with this identifier."}
{"family":"comments","op":"DELETE","text":"Get rid of the single annotation with this id."}
{"family":"albums","op":"CREATE","text":"Add one new album."}
{"family":"albums","op":"CREATE","text":"Make a new gallery."}
{"family":"albums","op":"CREATE","text":"Register a single new photo collection."}
{"family":"albums","op":"CREATE","text":"Set up one new photo set."}
{"family":"albums","op":"CREATE","text":"Introduce a new compilation."}
{"family":"albums","op":"CREATE","text":"Generate one new collection."}
{"family":"albums","op":"READ","text":"Fetch the album with this id."}
{"family":"albums","op":"READ","text":"Retrieve one gallery by its identifier."}
{"family":"albums","op":"READ","text":"Get the single photo collection matching this id."}
{"family":"albums","op":"READ","text":"Look up one photo set using this id."}
{"family":"albums","op":"READ","text":"View the one compilation with this identifier."}
{"family":"albums","op":"READ","text":"Pull up the single collection with this id."}
{"family":"albums","op":"UPDATE","text":"Change the album with this id."}
{"family":"albums","op":"UPDATE","text":"Modify one gallery by its identifier."}
{"family":"albums","op":"UPDATE","text":"Edit the single photo collection with this id."}
{"family":"albums","op":"UPDATE","text":"Adjust one photo set using this id."}
{"family":"albums","op":"UPDATE","text":"Revise the one compilation with this identifier."}
{"family":"albums","op":"UPDATE","text":"Amend the single collection with this id."}
{"family":"albums","op":"DELETE","text":"Remove the album with this id."}
{"family":"albums","op":"DELETE","text":"Erase one gallery by its identifier."}
{"family":"albums","op":"DELETE","text":"Discard the single photo collection with this id."}
{"family":"albums","op":"DELETE","text":"Eliminate one photo set using this id."}
{"family":"albums","op":"DELETE","text":"Drop the one compilation with this identifier."}
{"family":"albums","op":"DELETE","text":"Get rid of the single collection with this id."}
{"family":"photos","op":"CREATE","text":"Add one new photo."}
{"family":"photos","op":"CREATE","text":"Make a new picture."}
{"family":"photos","op":"CREATE","text":"Register a single new image."}
{"family":"photos","op":"CREATE","text":"Set up one new snapshot."}
{"family":"photos","op":"CREATE","text":"Introduce a new photograph."}
{"family":"photos","op":"CREATE","text":"Generate one new shot."}
{"family":"photos","op":"READ","text":"Fetch the photo with this id."}
{"family":"photos","op":"READ","text":"Retrieve one picture by its identifier."}
{"family":"photos","op":"READ","text":"Get the single image matching this id."}
{"family":"photos","op":"READ","text":"Look up one snapshot using this id."}
{"family":"photos","op":"READ","text":"View the one photograph with this identifier."}
{"family":"photos","op":"READ","text":"Pull up the single shot with this id."}
{"family":"photos","op":"UPDATE","text":"Change the photo with this id."}
{"family":"photos","op":"UPDATE","text":"Modify one picture by its identifier."}
{"family":"photos","op":"UPDATE","text":"Edit the single image with this id."}
{"family":"photos","op":"UPDATE","text":"Adjust one snapshot using this id."}
{"family":"photos","op":"UPDATE","text":"Revise the one photograph with this identifier."}
{"family":"photos","op":"UPDATE","text":"Amend the single shot with this id."}
{"family":"photos","op":"DELETE","text":"Remove the photo with this id."}
{"family":"photos","op":"DELETE","text":"Erase one picture by its identifier."}
{"family":"photos","op":"DELETE","text":"Discard the single image with this id."}
{"family":"photos","op":"DELETE","text":"Eliminate one snapshot using this id."}
{"family":"photos","op":"DELETE","text":"Drop the one photograph with this identifier."}
{"family":"photos","op":"DELETE","text":"Get rid of the single shot with this id."}
<!-- END GOAL BANK -->

<!-- BEGIN OOS BANK -->
{"family":"users","text":"List every user in the system at once."}
{"family":"posts","text":"Show me page two of the posts."}
{"family":"comments","text":"Find all comments containing the word trouble."}
{"family":"albums","text":"How many albums exist right now?"}
{"family":"photos","text":"Give me only the photos smaller than one megabyte."}
{"family":"users","text":"Export the entire user table to a CSV file."}
{"family":"posts","text":"Import a batch of posts from my spreadsheet."}
{"family":"comments","text":"Add a thumbs-up reaction to this comment."}
{"family":"albums","text":"Let me follow this album for future updates."}
{"family":"photos","text":"Attach the tag vacation to that photo."}
{"family":"users","text":"Sign me in with a username and password."}
{"family":"posts","text":"Schedule this post to publish next Tuesday."}
{"family":"comments","text":"Remove all of my comments in one go."}
{"family":"albums","text":"Order the albums by title alphabetically."}
{"family":"photos","text":"Upload a brand new photo from my phone."}
{"family":"users","text":"Email every user a welcome message."}
{"family":"posts","text":"Undo my last edit to this post."}
{"family":"comments","text":"Flag this comment as abusive for review."}
{"family":"albums","text":"Share this album with my friends."}
{"family":"photos","text":"Download all of my photos as a zip archive."}
{"family":"users","text":"Make this user an administrator."}
{"family":"posts","text":"Produce a monthly report of post activity."}
{"family":"comments","text":"Attach the full author record to each comment."}
{"family":"albums","text":"Merge two albums into a single one."}
{"family":"photos","text":"Shrink this photo down to a thumbnail."}
{"family":"users","text":"Search for users by their email address."}
{"family":"posts","text":"Show me the trending posts from this week."}
{"family":"comments","text":"Nest replies underneath this comment."}
{"family":"albums","text":"Set an expiration date on this album."}
{"family":"photos","text":"Watermark this photo automatically."}
{"family":"users","text":"Follow another member of the site."}
{"family":"posts","text":"Count the likes on this post."}
{"family":"comments","text":"Give me fifty comments at a time."}
{"family":"albums","text":"Count the items inside this album."}
{"family":"photos","text":"Upload a whole folder of photos simultaneously."}
{"family":"users","text":"Log this user out of every active session."}
{"family":"posts","text":"Filter the posts published between January and March."}
{"family":"comments","text":"Sort these comments by the newest first."}
{"family":"albums","text":"Notify subscribers when this album changes."}
{"family":"photos","text":"Pull a photo in directly from a web link."}
<!-- END OOS BANK -->

<!-- BEGIN LEXICON -->
{
  "op_synonyms": {
    "CREATE": ["create", "add", "make", "new", "insert", "post", "put", "register", "generate", "build", "produce", "construct", "compose", "establish", "initialize", "init", "spawn", "instantiate", "write", "submit", "save", "store", "record", "append", "introduce", "launch", "open", "set up", "define", "allocate", "mint", "provision", "enroll", "sign up", "upload", "publish"],
    "READ": ["read", "get", "fetch", "retrieve", "load", "find", "look up", "lookup", "query", "select", "show", "view", "display", "list", "obtain", "access", "pull", "grab", "return", "inspect", "examine", "search", "locate", "resolve", "request", "download", "see", "check", "print", "dump", "describe"],
    "UPDATE": ["update", "edit", "modify", "change", "set", "patch", "alter", "adjust", "revise", "amend", "replace", "overwrite", "refresh", "sync", "synchronize", "mutate", "transform", "convert", "fix", "correct", "toggle", "enable", "disable", "rename", "move", "merge", "bump", "increment", "assign", "upsert", "apply", "reset"],
    "DELETE": ["delete", "remove", "destroy", "drop", "erase", "clear", "purge", "discard", "eliminate", "unset", "unlink", "detach", "revoke", "cancel", "kill", "terminate", "wipe", "prune", "trash", "archive", "deactivate", "disable", "expire", "unregister", "unenroll", "strip", "empty", "flush", "dismiss", "reject"]
  },
  "family_nouns": {
    "users": ["user", "account", "member", "person", "profile", "customer", "client", "subscriber", "participant", "individual", "identity", "principal", "actor", "login", "credential", "owner", "operator", "contact"],
    "posts": ["post", "article", "entry", "message", "item", "publication", "blog post", "status", "update", "story", "note", "thread", "content", "submission", "feed item", "tweet", "blog"],
    "comments": ["comment", "remark", "note", "reply", "response", "feedback", "message", "annotation", "observation", "review", "mention", "reaction", "opinion"],
    "albums": ["album", "collection", "gallery", "folder", "set", "bundle", "group", "batch", "portfolio", "library", "compilation", "directory", "category"],
    "photos": ["photo", "image", "picture", "pic", "photograph", "img", "media", "asset", "file", "snapshot", "shot", "graphic", "thumbnail", "avatar", "attachment"]
  }
}
<!-- END LEXICON -->

<!-- BEGIN PRIOR-PARENT-BANK-TEXTS -->
["add a new user to the system", "register a brand new user account", "create one new user record", "make a fresh single user", "set up one new user profile", "show me the user by id", "fetch a single user record", "look up one existing user", "view user number seven", "bring up the user with id 12", "change fields of one user", "edit an existing user by id", "modify the user with id 4", "revise a single user record", "adjust user number nine", "remove the user by id", "delete one existing user record", "erase the user with id 3", "drop a single user from storage", "wipe user number five", "add a new post now", "create one post record", "make a brand new post", "write a single new post", "set up one new post", "show the post by id", "fetch one existing post", "look up a single post record", "view post number three", "bring up the post with id 8", "edit an existing post by id", "change fields of one post", "modify post number two", "revise a single post record", "fix the post with id 6", "remove the post by id", "delete one existing post", "erase the post with id 5", "drop a single post record", "destroy post number seven", "add a new comment here", "create one comment record", "make a brand new comment", "insert a single new comment", "submit one new comment", "show the comment by id", "fetch one existing comment", "look up a single comment", "view comment number four", "bring up the comment with id 9", "edit an existing comment by id", "change fields of one comment", "modify comment number six", "revise a single comment record", "update the comment with id 2", "remove the comment by id", "delete one existing comment", "erase the comment with id 7", "drop a single comment record", "wipe comment number three", "add a new album", "create one album record", "make a brand new album", "open a single new album", "set up one new album", "show the album by id", "fetch one existing album", "look up a single album", "view album number two", "bring up the album with id 5", "edit an existing album by id", "change fields of one album", "modify album number four", "revise a single album record", "adjust the album with id 8", "remove the album by id", "delete one existing album", "erase the album with id 3", "drop a single album record", "destroy album number six", "add a new photo", "create one photo record", "make a brand new photo", "insert a single new photo", "set up one new photo", "show the photo by id", "fetch one existing photo", "look up a single photo", "view photo number nine", "bring up the photo with id 4", "edit an existing photo by id", "change fields of one photo", "modify photo number three", "revise a single photo record", "update the photo with id 7", "remove the photo by id", "delete one existing photo", "erase the photo with id 6", "drop a single photo record", "wipe photo number two", "list all users in the system", "search posts by title keyword", "count the number of comments", "delete all photos at once", "batch update every album record", "get the total number of users", "sort comments by creation date", "filter posts by author name", "export all user data to csv", "import photos from a local folder", "upload a new photo file", "tag a post with keywords", "like a comment", "follow another user", "compute average photos per album", "show the most recent posts feed", "log in as a user with a password", "generate a document report of comments", "merge two albums into one", "get the oldest and newest photo", "Paginate through every user in the system", "Bulk archive all inactive user accounts", "Search comments containing a keyword", "Find the most commented post", "Unfollow a user from my account", "Reset a forgotten user password", "Download the image file for a photo", "Send email notification to a user", "Add a new column to photos", "Undo my last post deletion", "Generate a shareable link for album", "Export all comments to a spreadsheet", "Validate every user's email address format", "Join posts with their author details", "Schedule a post for future publication", "Render comment text as HTML", "Check remaining API request quota", "Show the edit history of a post", "Grant admin permissions to a user", "Register a webhook for new posts"]
<!-- END PRIOR-PARENT-BANK-TEXTS -->

<!-- BEGIN AUTHOR-PROMPTS -->
AUTHOR-APPLICABLE v2 PROMPT (fresh-context general subagent, no tools, no file access):
"""
You are a fresh-context natural-language author. Work purely from general knowledge of English; you have NO knowledge of any particular software project.

TASK: Write natural-language end-user requests for a simple REST API managing five resource families: users, posts, comments, albums, photos. Each family supports exactly four single-item operations:
- CREATE: make one new item
- READ: get one single existing item by its identifier
- UPDATE: change one existing item
- DELETE: remove one existing item

Produce exactly 120 requests: 5 families x 4 operations x 6 distinct phrasings.

CRITICAL WORDING RULES:
1. Do NOT use the literal words "create", "read", "update", or "delete" anywhere in the requests.
2. For the six phrasings of one operation, use six clearly DIFFERENT verbs or verb phrases, chosen naturally by you (do not repeat a verb across the six).
3. Vary the resource family noun as well (for each family, use several common synonyms across its requests).
4. Every request is a single short sentence naming exactly one family and asking for exactly one single-item operation. Never ask for lists, counts, searches, filtering, sorting, batch/bulk actions, files, uploads, downloads, login, notifications, or anything involving more than one item.

OUTPUT FORMAT: ONLY JSON Lines. Each line is one JSON object with exactly three keys: "family" (one of users, posts, comments, albums, photos), "op" (one of CREATE, READ, UPDATE, DELETE), "text" (the request). No markdown fences, no prose, no numbering. Your ENTIRE final message must be exactly the 120 JSON lines.

CONSTRAINTS: Do not read, list, grep, or open any files. Do not create or modify any files. Do not use any tools. Produce the text purely from general English knowledge. Counts must be exactly 5 x 4 x 6 = 120 lines.
"""

AUTHOR-OOS v2 PROMPT (fresh-context general subagent, no tools, no file access):
"""
You are a fresh-context natural-language author. Work purely from general knowledge of English; you have NO knowledge of any particular software project.

TASK: A simple REST API manages exactly five resource families: users, posts, comments, albums, photos. The ONLY operations it supports are single-item create, single-item read-by-id, single-item update, single-item delete. It supports NOTHING else.

Write exactly 40 natural-language end-user requests that each MENTION one of those five families but ask for something the API does NOT support. Make them lexically DIVERSE: do not reuse the same sentence skeleton or the same lead verb more than a few times. Cover a wide variety of unsupported features: listing/pagination, counting, searching, filtering, sorting, exporting/importing, uploading/downloading files, authentication/passwords/sessions, notifications/emails, likes/follows/tags, aggregation/reports, scheduling, permissions/admin, bulk/batch actions, undo/history, joins, sharing, and similar.

Each request is a single short sentence and must name exactly one family (use a common noun or synonym).

OUTPUT FORMAT: ONLY JSON Lines. Each line is one JSON object with exactly two keys: "family" (one of users, posts, comments, albums, photos) and "text" (the request). No markdown fences, no prose, no numbering. Your ENTIRE final message must be exactly the 40 JSON lines.

CONSTRAINTS: Do not read, list, grep, or open any files. Do not create or modify any files. Do not use any tools. Produce the text purely from general English knowledge. Count must be exactly 40 lines.
"""

AUTHOR-LEXICON PROMPT (fresh-context general subagent, no tools, no file access; NOT given the bank):
"""
You are a fresh-context software engineer. Work purely from general knowledge; you have NO access to any particular project, bank, dataset, or file.

TASK: Produce a practical English synonym lexicon a developer would write once, blindly, to map a short end-user request to (operation, resource-family).

Five resource families: users, posts, comments, albums, photos.
Four operations: CREATE (make a new item), READ (fetch one item by id), UPDATE (change one item), DELETE (remove one item).

Output EXACTLY two JSON objects:

1. "op_synonyms": an object mapping each of the four operation keys ("CREATE","READ","UPDATE","DELETE") to a list of the most common English verbs and short verb phrases a developer would reasonably list as synonyms for that operation. Be broad and practical (aim for 15-30 entries each). Include multi-word phrases where natural.

2. "family_nouns": an object mapping each of the five family keys ("users","posts","comments","albums","photos") to a list of the most common English nouns a developer would reasonably list as synonyms for that resource. Aim for 6-15 entries each.

OUTPUT FORMAT: Your ENTIRE final message must be exactly one JSON object with keys "op_synonyms" and "family_nouns". No markdown fences, no prose.

CONSTRAINTS: Do not read, list, grep, or open any files. Do not create or modify any files. Do not use any tools. Produce the lexicon purely from general English knowledge of common CRUD vocabulary.
"""
<!-- END AUTHOR-PROMPTS -->

## 5. Frozen bank schema and splits

- `GOAL BANK`: 120 applicable single-operation requests, 5 families x 4 operations x 6 distinct
  phrasings. Each line is `{"family","op","text"}`. Derived: `goal_id = app_###` (1-based order),
  `target_mechanism_id = mech_{family}_{op.lower()}`, `applicable = true`, `split = test` if
  `(index % 6) in (1,3,5)` else `calibration` (0-based). Split: 60 calibration /
  60 test.
- `OOS BANK`: 40 out-of-scope requests, each naming exactly one supported family but asking for an
  unsupported operation. Each line is `{"family","text"}`. Derived: `goal_id = oos_###`,
  `applicable = false`, empty `target_mechanism_id`, same `split` rule. Split: 20
  calibration / 20 test.
- `LEXICON`: `{"op_synonyms": {CREATE/READ/UPDATE/DELETE -> [phrases]},
  "family_nouns": {users/posts/comments/albums/photos -> [nouns]}}`, authored blind.
- `PRIOR-PARENT-BANK-TEXTS`: the 140 goal texts of the parent packet, used only as contamination
  surfaces.

## 6. Arms

| Arm | Definition | Role |
| --- | --- | --- |
| `A-EMBED-COSINE` | max-cosine over `all-MiniLM-L6-v2` embeddings of the 20 fixture intents | treatment |
| `B-LEX-STRONG` | deterministic operation-synonym + resource-noun resolver (section 7) | **PRIMARY comparator** |
| `B-LEX-STRONG-LEARNED` | same fixed noun lexicon; op/family lexeme map learned on calibration applicable labels only (freq>=2) | sensitivity bound |
| `B-LEXTOK-JACCARD` | parent `LexicalOverlapResolver` token-set Jaccard | weak null, continuity |
| `B-RANDOM-ROLE` | `RandomRoleResolver`, seed 4242 | floor |
| `B-INCUMBENT-KERNEL` | `SpiderKernel(min_confidence=0.8)` exact-intent match | product baseline |
| `B-INTERNAL-ID-ORACLE` | `InternalIdOracle` | fallible ceiling |

The comparator lexicon is **fixed** and bank-blind; `B-LEX-STRONG-LEARNED` is reported but is not
the claim-bearing comparator (VN-06).

## 7. `B-LEX-STRONG` algorithm (frozen)

Tokenize with `[a-z]+`. A *resource noun* is the **unique longest** family-noun phrase
(whole-token, simple plurals); an *operation* is the **unique longest** op-synonym phrase. Dual
resolution: (a) family-first -- locate the unique longest family span, remove it, find the unique
longest op phrase in the remainder; (b) op-first -- locate the unique longest op span, remove it,
find the unique longest family phrase in the remainder. Return `mech_{family}_{op.lower()}`
only if (a) and (b) agree, or exactly one is defined; otherwise abstain. The exact source is frozen
in the runner (`def b_lex_strong`); V9 verifies structurally that this path references no embedder.

## 8. Controls

- **Positive control `PC-LIVENESS-AND-INTEGRITY`**: fixture has 20 unique mechanism ids and 20
  unique intents; the incumbent kernel resolves all 20 verbatim intents to the correct id; the
  embedding arm self-recovers all 20 verbatim intents. Any shortfall is a measurement failure.
- **Negative control `NC-SHUFFLED-LABEL`**: a fixed derangement of the 20 labels applied to
  embedding selections must score <= 0.20; a uniform-random label must score <= 0.25.
- **Floors/ceilings**: `B-RANDOM-ROLE` <= 0.35; `B-INTERNAL-ID-ORACLE` == 1.0.

## 9. Contamination screen

A goal is **flagged** iff for any prior surface it reaches token-set Jaccard >= 0.60 **or**
char-trigram Jaccard >= 0.75. Prior surfaces = the 108 `goal_generator` surfaces (20 intents + 60
paraphrases + 20 no-applicable + 8 OOD) **plus** the 140 parent goal texts
(`PRIOR-PARENT-BANK-TEXTS`) = 248 surfaces. The char-trigram representation deliberately differs
from every arm mechanism (answers parent RQF-01/VF-01). If more than 20 goals are flagged the run is
MEASUREMENT_INVALID (V3). The primary set is all applicable unflagged goals.

## 10. Decision rules

- **`D-RESOLVER` (claim-bearing).** Paired family-blocked bootstrap of
  (`A-EMBED-COSINE` - `B-LEX-STRONG`) on the primary set; `n_resamples=10000`, `alpha=0.05`,
  `seed=3815816012`, 5 family blocks. `SUPPORTS` iff lower bound > 0; `FALSIFIES`
  iff upper bound <= 0; otherwise `MIXED`.
- **`D-GATE` (decoupled, non-gating for `D-RESOLVER`).** `G-LOGISTIC-2F`: logistic regression on
  `(max_cos, margin=top1-top2)` fit on the calibration split; `t*` = smallest calibration score
  with calibration false-accept <= 0.10 AND calibration unknown-precision >= 0.85, else
  argmin|FA-0.10| subject to precision >= 0.85, else 1.0; evaluated on the disjoint test split.
  `G-GLOBAL-THRESHOLD` (single `max_cos`, parent continuity) is also reported. Class is
  `GATE-MET` iff test false-accept <= 0.10, unknown-precision >= 0.85 and coverage >= 0.50;
  `GATE-NOT-MET` otherwise; `GATE-INVALID` if calibration/test class is empty.
  `pooled_false_accept` = executed OOS / all OOS; `unknown_precision` = abstained OOS / all
  abstained; `coverage` = executed applicable / all applicable.

## 11. Product consequences (both branches)

- If `SUPPORTS` and `GATE-MET`: keep the gated embedding resolver; do not retire embeddings.
- If `FALSIFIES` and `GATE-MET`: ship the deterministic lexical resolver with the gate, retire the
  embedding path for `resolve()`.
- If `SUPPORTS` and not `GATE-MET`: keep embeddings but do **not** ship the gate; `resolve()` must
  remain UNKNOWN on low-confidence input.
- If `FALSIFIES` and not `GATE-MET`: the gate is infeasible on this fixture class; report that
  limitation explicitly rather than shipping either.

## 12. Validity gates (V1-V13)

V1 metric definition (all arm denominators == |primary|); V2 primary set >= 80; V3 contamination
flag budget <= 20; V4 authorship provenance (block hashes + prompt-blind check + raw-output
exact-intent check); V5 positive
control; V6 oracle ceiling == 1.0; V7 treatment liveness (>= 2 distinct embedding selections);
V8 random floor <= 0.35; V9 structural non-tautology (`b_lex_strong` references no embedder AND
the comparator disagrees with `A-EMBED-COSINE` on >= 1 primary goal or abstains on >= 1);
V10 negative control; V11 bootstrap seed and 5 family blocks; V12 freeze-hash binding (prereg hash +
runner-source == FROZEN RUNNER block + every freeze artifact hash);
V13 gate calibration/test classes non-empty. Any of V1-V12 false => MEASUREMENT_INVALID /
INCONCLUSIVE. `D-GATE` is reported regardless of `V13` and never gates `D-RESOLVER`.

## 13. Frozen runner source

<!-- BEGIN FROZEN RUNNER -->
#!/usr/bin/env python3
"""Frozen orchestration script for EXP-GRAPH-38175554380 (graph lane).

Binding-only measurement: embeddings vs a strong deterministic operation-synonym +
resource-noun resolver on an independently authored unseen-goal bank, plus a
disjoint-calibrated two-feature applicability gate. No browser, no server, no LLM.
"""
from __future__ import annotations
import json
import hashlib
import re
import sys
import os
from pathlib import Path

# ---------------------------------------------------------------- environment
EXP = Path(os.environ.get("SPIDER_EXP_DIR", Path(__file__).resolve().parent))
REPO = EXP.parents[2]
HARNESS = REPO / "research" / "harness"
SRC = REPO / "src"
OUT = EXP / "derived"

SEED32 = 38175554380 % (2 ** 32)          # = 3815816012
MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
MODEL_REV = "c9745ed1d9f207416be6d2e6f8de32d1f161f9bf"
PRIMARY_MIN = 80
CONTAM_TOK_T = 0.60
CONTAM_TRI_T = 0.75
CONTAM_MAX_FLAGGED = 20
FLOOR_MAX = 0.35
NC_LABEL_MAX = 0.20
NC_RANDOM_MAX = 0.25
AB_FA_MAX = 0.10
AB_COV_MIN = 0.50
AB_PREC_MIN = 0.85

out = {
    "schema_version": 1,
    "experiment_id": "EXP-GRAPH-38175554380",
    "lane": "graph",
    "status": None,
    "outcome": None,
    "metrics": {},
    "controls": {},
    "artifacts": [],
    "observations": [],
    "validity_notes": [],
    "unresolved": [],
    "gates": {},
    "env": {},
}

def _abort(status, reason):
    out["status"] = status
    out["outcome"] = "INCONCLUSIVE"
    out["reason"] = reason
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "measurements.json").write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(json.dumps({"status": status, "reason": reason}, indent=2))
    sys.exit(0)

# ---------------------------------------------------------------- prerag blocks
def _extract(text, name):
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END " + re.escape(name) + r" -->", text, re.S)
    if not m:
        _abort("MEASUREMENT_INVALID", f"prereg block {name} not found")
    return m.group(1)

CANON = json.loads(_extract((EXP / "prereg.md").read_text(encoding="utf-8"), "CANONICAL-HASHES"))

# ---------------------------------------------------------------- freeze binding
def sha256_file(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

# ---------------------------------------------------------------- pure-string resolver
OP_SYNONYMS = json.loads(_extract((EXP / "prereg.md").read_text(encoding="utf-8"), "LEXICON"))["op_synonyms"]
FAMILY_NOUNS = json.loads(_extract((EXP / "prereg.md").read_text(encoding="utf-8"), "LEXICON"))["family_nouns"]

def tokens(s):
    return re.findall(r"[a-z]+", s.lower())

def _spans(t, phrase, plural=False):
    pt = phrase.split()
    L = len(pt)
    res = []
    for i in range(len(t) - L + 1):
        ok = True
        for k, p in enumerate(pt):
            x = t[i + k]
            if x == p:
                continue
            if plural and (x == p + "s" or x + "s" == p):
                continue
            ok = False
            break
        if ok:
            res.append((i, i + L, L))
    return res

def _unique_longest(cands):
    if not cands:
        return None, None, None
    m = max(c[3] for c in cands)
    top = [c for c in cands if c[3] == m]
    if len({c[0] for c in top}) != 1:
        return None, None, m
    top.sort(key=lambda c: (c[1], c[2]))
    return top[0][0], top[0][1], top[0][2]

def _fam_cands(t):
    return [(f, s, e, L) for f, ph in FAMILY_NOUNS.items() for p in ph for (s, e, L) in _spans(t, p, plural=True)]

def _op_cands(t):
    return [(o, s, e, L) for o, ph in OP_SYNONYMS.items() for p in ph for (s, e, L) in _spans(t, p)]

def b_lex_strong(text):
    """Return mechanism id string, or None to abstain. Pure string computation."""
    t = tokens(text)
    fam, fs, fe = _unique_longest(_fam_cands(t))
    r1 = None
    if fam is not None:
        op, _, _ = _unique_longest(_op_cands(t[:fs] + t[fe:]))
        if op is not None:
            r1 = (fam, op)
    op2, os_, oe = _unique_longest(_op_cands(t))
    r2 = None
    if op2 is not None:
        fam2, _, _ = _unique_longest(_fam_cands(t[:os_] + t[oe:]))
        if fam2 is not None:
            r2 = (fam2, op2)
    if r1 and r2:
        res = r1 if r1 == r2 else None
    else:
        res = r1 or r2
    return None if res is None else f"mech_{res[0]}_{res[1].lower()}"

# ---------------------------------------------------------------- contamination
def _jtok(a, b):
    A, B = set(tokens(a)), set(tokens(b))
    return len(A & B) / len(A | B) if (A | B) else 0.0

def _tri(s):
    x = " " + " ".join(tokens(s)) + " "
    return {x[i:i + 3] for i in range(len(x) - 2)}

def _jtri(a, b):
    A, B = _tri(a), _tri(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0

def _select_index(scores):
    import numpy as np
    return int(np.argmax(scores))

def _credit(idx, goal, mech_ids):
    return idx < len(mech_ids) and mech_ids[idx] == goal["target_mechanism_id"]

# ================================================================ MAIN
def main():
    start_cwd = os.getcwd()
    sys.path.insert(0, str(HARNESS))
    sys.path.insert(0, str(SRC))
    try:
        from candidate_resolver import (  # noqa: F401
            EmbeddingArgmaxResolver, InternalIdOracle, LexicalOverlapResolver,
            RandomRoleResolver, create_fixture,
        )
        from experiment_runner import compute_ece, paired_bootstrap, convert_to_native  # noqa: F401
        from goal_generator import (  # noqa: F401
            INTENTS, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES, PARAPHRASES,
        )
        from spider.kernel import SpiderKernel
        from spider.models import Mechanism as KernelMechanism
        from spider.registry import MechanismRegistry
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"harness import failed: {e!r}")
    os.chdir(start_cwd)

    # ---- frozen inputs: bind prereg bytes to freeze, then blocks to CANON ----
    prereg = (EXP / "prereg.md").read_text(encoding="utf-8")
    try:
        freeze_obj = json.loads((EXP / "freeze.json").read_text(encoding="utf-8"))
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"freeze.json unavailable: {e!r}")
    # V12-A: the whole prereg.md (orchestration script + data blocks) is bound by freeze.hashes
    if freeze_obj.get("hashes", {}).get("prereg.md") != hashlib.sha256(prereg.encode()).hexdigest():
        _abort("MEASUREMENT_INVALID", "V12 prereg.md hash does not match freeze.json")
    spec = json.loads((EXP / "spec.json").read_text(encoding="utf-8"))
    freeze_art = freeze_obj.get("artifact_hashes", {})
    mismatches = [rel for rel in spec["freeze_artifacts"]
                  if freeze_art.get(rel) != sha256_file(REPO / rel)]
    if mismatches:
        _abort("MEASUREMENT_INVALID", f"V12 freeze artifact hash mismatch: {mismatches}")
    out["gates"]["V12-FREEZE-BINDING"] = True

    goal_block = _extract(prereg, "GOAL BANK")
    oos_block = _extract(prereg, "OOS BANK")
    lex_block = _extract(prereg, "LEXICON")
    ppb_block = _extract(prereg, "PRIOR-PARENT-BANK-TEXTS")
    prompts_block = _extract(prereg, "AUTHOR-PROMPTS")
    blocks = {"GOAL BANK": goal_block, "OOS BANK": oos_block, "LEXICON": lex_block,
              "PRIOR-PARENT-BANK-TEXTS": ppb_block, "AUTHOR-PROMPTS": prompts_block}
    for name, blk in blocks.items():
        if hashlib.sha256(blk.encode()).hexdigest() != CANON["blocks"][name]:
            _abort("MEASUREMENT_INVALID", f"V4 block hash mismatch: {name}")
    # V12-B: the running source must equal the frozen FROZEN RUNNER block of the hash-bound prereg
    _block_runner = _extract(prereg, "FROZEN RUNNER")
    _me = Path(__file__).read_text(encoding="utf-8")
    if _me.replace("\r\n", "\n").rstrip("\n") != _block_runner.replace("\r\n", "\n").rstrip("\n"):
        _abort("MEASUREMENT_INVALID", "V12 runner source does not match the frozen FROZEN RUNNER block")

    # ---- embedding + numeric stack (load failure => BLOCKED, never FALSIFIES) ----
    try:
        from sentence_transformers import SentenceTransformer
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"sentence_transformers import failed: {e!r}")
    try:
        import numpy as np
        from sklearn.linear_model import LogisticRegression
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"numpy/sklearn import failed: {e!r}")
    try:
        try:
            model = SentenceTransformer(MODEL_NAME, revision=MODEL_REV)
            model_revision = MODEL_REV
        except Exception:  # noqa: BLE001
            model = SentenceTransformer(MODEL_NAME)
            model_revision = None
    except Exception as e:  # noqa: BLE001
        _abort("BLOCKED", f"embedding model load failed: {e!r}")
    out["env"]["model"] = MODEL_NAME
    out["env"]["model_revision"] = model_revision
    try:
        _cfg = getattr(getattr(model[0], "auto_model", None), "config", None)
        _resolved_commit = getattr(_cfg, "_commit_hash", None)
    except Exception:  # noqa: BLE001
        _resolved_commit = None
    out["env"]["model_revision_requested"] = MODEL_REV
    out["env"]["model_revision_resolved"] = _resolved_commit
    out["env"]["seed"] = SEED32
    # V4 TRANSCRIPT-BLIND: prompts contain no exact intent string and are far from all prior surfaces
    from goal_generator import INTENTS as _I, PARAPHRASES as _P, NO_APPLICABLE_TEMPLATES as _N, OOD_PARAPHRASES as _O
    _intents = list(_I.values())
    _prior = (list(_I.values()) + [v for vs in _P.values() for v in vs] + list(_N) + list(_O))
    for _line in prompts_block.splitlines():
        for _s in _intents:
            if _s and _s in _line.lower():
                _abort("MEASUREMENT_INVALID", f"V4 prompt leaks intent string: {_s!r}")
    if max(_jtok(prompts_block, q) for q in _prior) >= CONTAM_TOK_T:
        _abort("MEASUREMENT_INVALID", "V4 prompt block too close to a prior surface")
    out["gates"]["V4-AUTHORSHIP-PROVENANCE"] = True

    app_raw = [json.loads(l) for l in goal_block.splitlines() if l.strip()]
    oos_raw = [json.loads(l) for l in oos_block.splitlines() if l.strip()]
    if len(app_raw) != 120 or len(oos_raw) != 40:
        _abort("MEASUREMENT_INVALID", f"bank size wrong: app={len(app_raw)} oos={len(oos_raw)}")
    _intent_lc = {v.lower() for v in _intents}
    for _g in app_raw + oos_raw:
        # V4: raw bank output may not be (or contain) an exact registry intent string
        if _g["text"].strip().lower() in _intent_lc:
            _abort("MEASUREMENT_INVALID", f"V4 raw bank leaks exact intent: {_g['text']!r}")

    goals = []
    for i, g in enumerate(app_raw):
        goals.append({
            "goal_id": f"app_{i+1:03d}", "text": g["text"],
            "target_mechanism_id": f"mech_{g['family']}_{g['op'].lower()}",
            "applicable": True, "family": g["family"], "verb": g["op"],
            "split": "test" if (i % 6) in (1, 3, 5) else "calibration",
        })
    for i, g in enumerate(oos_raw):
        goals.append({
            "goal_id": f"oos_{i+1:03d}", "text": g["text"], "target_mechanism_id": "",
            "applicable": False, "family": g.get("family", ""), "verb": "",
            "split": "test" if (i % 6) in (1, 3, 5) else "calibration",
        })

    mechs = create_fixture()
    mech_ids = [mm.mechanism_id for mm in mechs]
    intents = [mm.intent for mm in mechs]
    if len(mechs) != 20:
        _abort("MEASUREMENT_INVALID", f"V1 fixture has {len(mechs)} mechanisms, expected 20")

    # V3 screen (token OR trigram)
    prior = (list(INTENTS.values()) + [v for vs in PARAPHRASES.values() for v in vs]
             + list(NO_APPLICABLE_TEMPLATES) + list(OOD_PARAPHRASES))
    prior_parent = json.loads(ppb_block)
    prior += prior_parent
    contamination = {}
    flagged = set()
    for g in goals:
        mt = max(_jtok(g["text"], q) for q in prior)
        mtri = max(_jtri(g["text"], q) for q in prior)
        contamination[g["goal_id"]] = {"max_token_jaccard": round(mt, 4),
                                       "max_trigram_jaccard": round(mtri, 4)}
        if mt >= CONTAM_TOK_T or mtri >= CONTAM_TRI_T:
            flagged.add(g["goal_id"])
    n_flagged = len(flagged)
    out["metrics"]["M-N-CONTAM-FLAGGED"] = n_flagged
    out["metrics"]["M-CONTAM-FLAGGED-IDS"] = sorted(flagged)
    out["metrics"]["M-CONTAM-MAX-JACCARD"] = {
        "max_token_jaccard": round(max(v["max_token_jaccard"] for v in contamination.values()), 4),
        "max_trigram_jaccard": round(max(v["max_trigram_jaccard"] for v in contamination.values()), 4),
        "thresholds": {"token": CONTAM_TOK_T, "trigram": CONTAM_TRI_T},
    }
    out["gates"]["V3-CONTAM-SCREEN"] = n_flagged <= CONTAM_MAX_FLAGGED

    primary = [g for g in goals if g["applicable"] and g["goal_id"] not in flagged]
    cal = [g for g in goals if g["split"] == "calibration" and g["goal_id"] not in flagged]
    test = [g for g in goals if g["split"] == "test" and g["goal_id"] not in flagged]
    cal_app = [g for g in cal if g["applicable"]]
    cal_oos = [g for g in cal if not g["applicable"]]
    test_app = [g for g in test if g["applicable"]]
    test_oos = [g for g in test if not g["applicable"]]
    out["metrics"]["M-N-PRIMARY"] = len(primary)
    out["metrics"]["M-N-CAL"] = {"applicable": len(cal_app), "oos": len(cal_oos)}
    out["metrics"]["M-N-TEST"] = {"applicable": len(test_app), "oos": len(test_oos)}
    out["gates"]["V2-PRIMARY-SET"] = len(primary) >= PRIMARY_MIN
    if not primary:
        _abort("MEASUREMENT_INVALID", "V2 empty primary set")

    # arms
    embed = EmbeddingArgmaxResolver(mechs, model)
    lexical = LexicalOverlapResolver(mechs)
    random_role = RandomRoleResolver(mechs, seed=4242)
    oracle = InternalIdOracle(mechs)

    kernel_reg_path = OUT / "kernel_registry.jsonl"
    kernel_reg = MechanismRegistry(kernel_reg_path)
    kernel_reg.replace([
        KernelMechanism(mechanism_id=mm.mechanism_id, intent=mm.intent, preconditions={},
                        action_template={}, postconditions={},
                        parameter_slots=list(mm.parameter_slots), confidence=1.0)
        for mm in mechs
    ])
    kernel = SpiderKernel(kernel_reg, min_confidence=0.8)

    # B-LEX-STRONG-LEARNED: op/family lexeme map from calibration applicable labels only
    tok_op = {}
    tok_fam = {}
    for g in cal_app:
        op = g["verb"]; fam = g["family"]
        for w in set(tokens(g["text"])):
            tok_op.setdefault(w, {})
            tok_op[w][op] = tok_op[w].get(op, 0) + 1
            tok_fam.setdefault(w, {})
            tok_fam[w][fam] = tok_fam[w].get(fam, 0) + 1

    def b_lex_learned(text):
        t = tokens(text)
        op = None
        for w in t:
            for k, n in tok_op.get(w, {}).items():
                if n >= 2 and (op is None or n > op[1]):
                    op = (k, n)
        fam = None
        for w in t:
            for k, n in tok_fam.get(w, {}).items():
                if n >= 2 and (fam is None or n > fam[1]):
                    fam = (k, n)
        if op and fam:
            return f"mech_{fam[0]}_{op[0].lower()}"
        return None

    predictions = {}
    for g in goals:
        gid = g["goal_id"]
        er = embed.resolve(g)
        lr = lexical.resolve(g)
        rr = random_role.resolve(g)
        oo = oracle.resolve(g)
        strong = b_lex_strong(g["text"])
        learned = b_lex_learned(g["text"])
        # embedding features: top1 and margin
        ge = model.encode([g["text"]], convert_to_numpy=True, normalize_embeddings=True)[0]
        sims = np.dot(embed.mechanism_embeddings, ge)
        order = np.argsort(sims)[::-1]
        c1 = float(sims[order[0]]); c2 = float(sims[order[1]]) if len(order) > 1 else 0.0
        predictions[gid] = {
            "goal_id": gid, "text": g["text"], "applicable": g["applicable"],
            "target_mechanism_id": g["target_mechanism_id"], "family": g.get("family"),
            "split": g["split"],
            "embed_mechanism_id": er.mechanism_id, "embed_confidence": float(er.confidence),
            "lexical_mechanism_id": lr.mechanism_id, "random_mechanism_id": rr.mechanism_id,
            "oracle_mechanism_id": oo.mechanism_id,
            "stronglex_mechanism_id": strong if strong is not None else "",
            "learned_mechanism_id": learned if learned is not None else "",
            "max_cos": c1, "margin": c1 - c2,
        }

    def acc_of(preds, key, gs):
        c = sum(1 for g in gs if preds[g["goal_id"]][key] == g["target_mechanism_id"])
        return c, len(gs)

    embed_c, embed_d = acc_of(predictions, "embed_mechanism_id", primary)
    strong_c, strong_d = acc_of(predictions, "stronglex_mechanism_id", primary)
    learned_c, learned_d = acc_of(predictions, "learned_mechanism_id", primary)
    lex_c, lex_d = acc_of(predictions, "lexical_mechanism_id", primary)
    rand_c, rand_d = acc_of(predictions, "random_mechanism_id", primary)
    orac_c, orac_d = acc_of(predictions, "oracle_mechanism_id", primary)
    inc_c = 0
    for g in primary:
        res = kernel.resolve(g["text"], {})
        if res.status.value == "EXECUTABLE" and res.mechanism_id == g["target_mechanism_id"]:
            inc_c += 1
    inc_d = len(primary)
    strong_abst = sum(1 for g in primary if predictions[g["goal_id"]]["stronglex_mechanism_id"] == "")
    strong_oos_fa = sum(1 for g in goals if (not g["applicable"]) and g["goal_id"] not in flagged
                        and predictions[g["goal_id"]]["stronglex_mechanism_id"] != "")

    out["metrics"]["M-MECH-ACC-EMBED"] = {"value": embed_c / embed_d, "numerator": embed_c, "denominator": embed_d}
    out["metrics"]["M-MECH-ACC-STRONGLEX"] = {"value": strong_c / strong_d, "numerator": strong_c,
                                              "denominator": strong_d, "abstentions": strong_abst,
                                              "oos_false_accepts_unflagged": strong_oos_fa}
    out["metrics"]["M-MECH-ACC-LEARNED"] = {"value": learned_c / learned_d, "numerator": learned_c, "denominator": learned_d}
    out["metrics"]["M-MECH-ACC-LEXTOK"] = {"value": lex_c / lex_d, "numerator": lex_c, "denominator": lex_d}
    out["metrics"]["M-MECH-ACC-RANDOM"] = {"value": rand_c / rand_d, "numerator": rand_c, "denominator": rand_d}
    out["metrics"]["M-MECH-ACC-ORACLE"] = {"value": orac_c / orac_d, "numerator": orac_c, "denominator": orac_d}
    out["metrics"]["M-MECH-ACC-INCUMBENT"] = {"value": inc_c / inc_d, "numerator": inc_c, "denominator": inc_d}

    v1 = (len(primary) > 0 and embed_d == strong_d == learned_d == lex_d == rand_d == orac_d == inc_d == len(primary))
    out["gates"]["V1-METRIC-DEFINITION"] = v1

    # primary bootstrap (V11)
    np.random.seed(SEED32)
    fams = np.array([g["family"] for g in primary])
    embed_scores = np.array([1.0 if predictions[g["goal_id"]]["embed_mechanism_id"] == g["target_mechanism_id"] else 0.0 for g in primary])
    strong_scores = np.array([1.0 if predictions[g["goal_id"]]["stronglex_mechanism_id"] == g["target_mechanism_id"] else 0.0 for g in primary])
    learned_scores = np.array([1.0 if predictions[g["goal_id"]]["learned_mechanism_id"] == g["target_mechanism_id"] else 0.0 for g in primary])
    obs_diff, lower_ci, upper_ci = paired_bootstrap(embed_scores, strong_scores, fams, n_resamples=10000, alpha=0.05)
    n_fams = int(len(np.unique(fams)))
    out["metrics"]["M-PAIRED-DIFF-EMBED-MINUS-STRONGLEX"] = {
        "obs_diff": float(obs_diff), "lower_ci": float(lower_ci), "upper_ci": float(upper_ci)}
    np.random.seed(SEED32)
    ldiff, llow, lup = paired_bootstrap(embed_scores, learned_scores, fams, n_resamples=10000, alpha=0.05)
    out["metrics"]["M-PAIRED-DIFF-EMBED-MINUS-LEARNED"] = {
        "obs_diff": float(ldiff), "lower_ci": float(llow), "upper_ci": float(lup)}
    out["metrics"]["M-BOOTSTRAP-ARGS"] = {"n_resamples": 10000, "alpha": 0.05, "seed": SEED32, "n_families": n_fams}
    out["gates"]["V11-BOOTSTRAP-SEED"] = n_fams == 5

    # V9 structural non-tautology: the STRONG comparator path references no embedder
    runner_src = Path(__file__).read_text(encoding="utf-8")
    strong_src = runner_src.split("def b_lex_strong")[1].split("def _jtok")[0]
    v9 = ("sentence_transformers" not in strong_src) and ("model" not in strong_src) and ("embed" not in strong_src)
    disagree = sum(1 for g in primary if predictions[g["goal_id"]]["embed_mechanism_id"] != predictions[g["goal_id"]]["stronglex_mechanism_id"])
    v9 = v9 and (disagree >= 1 or strong_abst >= 1)
    out["gates"]["V9-NON-TAUTOLOGY"] = v9
    out["metrics"]["M-NON-TAUTOLOGY"] = {"disagreement_count": disagree, "stronglex_accuracy": strong_c / strong_d}

    # V7 treatment liveness
    embed_selected = [predictions[g["goal_id"]]["embed_mechanism_id"] for g in primary]
    v7 = len(set(embed_selected)) >= 2 and all(s in mech_ids for s in embed_selected)
    out["gates"]["V7-TREATMENT-LIVENESS"] = v7
    out["metrics"]["M-EMBED-DISTINCT-SELECTIONS"] = len(set(embed_selected))

    # V5 PC
    pc_fx = (len(set(mech_ids)) == 20) and (len(set(intents)) == 20)
    pc_inc = 0
    for mm in mechs:
        params = {slot: f"v_{slot}" for slot in mm.parameter_slots}
        res = kernel.resolve(mm.intent, {}, params)
        if res.status.value == "EXECUTABLE" and res.mechanism_id == mm.mechanism_id:
            pc_inc += 1
    pc_emb = 0
    for k, mm in enumerate(mechs):
        g = {"goal_id": f"self_{k}", "text": mm.intent, "target_mechanism_id": mm.mechanism_id, "applicable": True}
        if embed.resolve(g).mechanism_id == mm.mechanism_id:
            pc_emb += 1
    v5 = pc_fx and pc_inc == 20 and pc_emb == 20
    out["gates"]["V5-PC"] = v5
    out["metrics"]["M-PC-LIVENESS-AND-INTEGRITY"] = {"fixture_unique": pc_fx, "incumbent_verbatim": pc_inc, "embed_self": pc_emb}
    out["controls"]["PC-LIVENESS-AND-INTEGRITY"] = {
        "expected": "fixture 20/20 unique; incumbent verbatim 20/20; embed_self 20/20",
        "observed": f"fixture_unique={pc_fx}, incumbent_verbatim={pc_inc}/20, embed_self={pc_emb}/20",
        "pass": v5, "evidence_ref": "derived/predictions.json"}

    # V6, V8
    out["gates"]["V6-ORACLE-CEILING"] = (orac_c / orac_d) == 1.0
    out["gates"]["V8-FLOOR-SANITY"] = (rand_c / rand_d) <= FLOOR_MAX

    # V10 NC
    rng_shuf = np.random.RandomState(SEED32 + 100)
    while True:
        perm = rng_shuf.permutation(20)
        if all(perm[i] != i for i in range(20)):
            break
    nc_label_c = 0
    for g in primary:
        ti = mech_ids.index(g["target_mechanism_id"])
        shifted = int(perm[ti])
        sel = predictions[g["goal_id"]]["embed_mechanism_id"]
        if sel in mech_ids and mech_ids.index(sel) == shifted:
            nc_label_c += 1
    nc_label = nc_label_c / len(primary)
    rng_rand = np.random.RandomState(SEED32 + 101)
    nc_rand_c = 0
    for g in primary:
        scores = rng_rand.uniform(size=20)
        if _credit(_select_index(scores), g, mech_ids):
            nc_rand_c += 1
    nc_rand = nc_rand_c / len(primary)
    out["gates"]["V10-NC-SHUFFLE"] = (nc_label <= NC_LABEL_MAX and nc_rand <= NC_RANDOM_MAX)
    out["metrics"]["M-NC-SHUFFLED"] = {"nc_shuffled_label": round(nc_label, 4), "nc_random_score": round(nc_rand, 4)}
    out["controls"]["NC-SHUFFLED-LABEL"] = {"expected": f"<= {NC_LABEL_MAX}", "observed": f"{nc_label:.4f}", "pass": nc_label <= NC_LABEL_MAX, "evidence_ref": "derived/predictions.json"}
    out["controls"]["NC-RANDOM-SCORE"] = {"expected": f"<= {NC_RANDOM_MAX}", "observed": f"{nc_rand:.4f}", "pass": nc_rand <= NC_RANDOM_MAX, "evidence_ref": "derived/predictions.json"}

    # ---------------- D-GATE ----------------
    def gate_eval(feats):
        X = np.array([feats[g["goal_id"]] for g in cal])
        y = np.array([1 if g["applicable"] else 0 for g in cal])
        if len(set(y.tolist())) < 2:
            return None
        clf = LogisticRegression(random_state=42, max_iter=1000)
        clf.fit(X, y)

        def score(g):
            return float(clf.predict_proba(np.array([feats[g["goal_id"]]]))[0][1])

        cal_scores = {g["goal_id"]: score(g) for g in cal}
        test_scores = {g["goal_id"]: score(g) for g in test}
        cal_oos_ids = [g["goal_id"] for g in cal_oos]
        cal_all_ids = [g["goal_id"] for g in cal]

        def metrics_at(t):
            exec_oos = sum(1 for gidv in cal_oos_ids if cal_scores[gidv] >= t)
            abst = [gidv for gidv in cal_all_ids if cal_scores[gidv] < t]
            abst_oos = sum(1 for gidv in cal_oos_ids if cal_scores[gidv] < t)
            fa = exec_oos / len(cal_oos_ids) if cal_oos_ids else None
            prec = abst_oos / len(abst) if abst else None
            return fa, prec

        thresholds = sorted(set(cal_scores.values()))
        feasible = [t for t in thresholds
                    if (lambda m: m[0] is not None and m[0] <= AB_FA_MAX and m[1] is not None
                        and m[1] >= AB_PREC_MIN)(metrics_at(t))]
        if feasible:
            tstar = feasible[0]
            cal_feasible = True
        else:
            cal_feasible = False
            cand = [t for t in thresholds
                    if metrics_at(t)[0] is not None and metrics_at(t)[1] is not None
                    and metrics_at(t)[1] >= AB_PREC_MIN]
            tstar = min(cand, key=lambda t: abs(metrics_at(t)[0] - AB_FA_MAX)) if cand else 1.0
        exec_oos = sum(1 for g in test_oos if test_scores[g["goal_id"]] >= tstar)
        exec_app = sum(1 for g in test_app if test_scores[g["goal_id"]] >= tstar)
        abst_all = [g for g in test if test_scores[g["goal_id"]] < tstar]
        abst_oos = sum(1 for g in test_oos if test_scores[g["goal_id"]] < tstar)
        abst_app = sum(1 for g in test_app if test_scores[g["goal_id"]] < tstar)
        coverage = exec_app / len(test_app) if test_app else None
        fa = exec_oos / len(test_oos) if test_oos else None
        prec = abst_oos / len(abst_all) if abst_all else None
        sel_correct = sum(1 for g in test_app
                          if test_scores[g["goal_id"]] >= tstar
                          and predictions[g["goal_id"]]["embed_mechanism_id"] == g["target_mechanism_id"])
        selective_acc = sel_correct / exec_app if exec_app else None
        met = (fa is not None and fa <= AB_FA_MAX and prec is not None and prec >= AB_PREC_MIN
               and coverage is not None and coverage >= AB_COV_MIN)
        return {"feasible": cal_feasible, "t_star": float(tstar), "test_coverage": coverage,
                "test_selective_accuracy": selective_acc,
                "test_pooled_false_accept": fa, "test_unknown_precision": prec,
                "test_exec_app": exec_app, "test_exec_oos": exec_oos,
                "test_abst_app": abst_app, "test_abst_oos": abst_oos,
                "class": "GATE-MET" if met else "GATE-NOT-MET"}

    feats2 = {gid: [predictions[gid]["max_cos"], predictions[gid]["margin"]] for gid in predictions}
    feats1 = {gid: [predictions[gid]["max_cos"]] for gid in predictions}
    if not cal_app or not cal_oos or not test_app or not test_oos:
        out["metrics"]["M-GATE-LOGISTIC-2F"] = {"class": "GATE-INVALID", "reason": "empty calibration or test class"}
        out["metrics"]["M-GATE-GLOBAL-THRESHOLD"] = {"class": "GATE-INVALID"}
        out["gates"]["V13-GATE-VALIDITY"] = False
    else:
        g2 = gate_eval(feats2)
        g1 = gate_eval(feats1)
        out["metrics"]["M-GATE-LOGISTIC-2F"] = g2
        out["metrics"]["M-GATE-GLOBAL-THRESHOLD"] = g1
        out["gates"]["V13-GATE-VALIDITY"] = g2 is not None
        out["observations"].append("OBS-D-GATE(2F): " + json.dumps(g2))
        out["observations"].append("OBS-D-GATE(global): " + json.dumps(g1))

    # ECE descriptive
    ece_confs = np.array([predictions[g["goal_id"]]["embed_confidence"] for g in primary])
    ece_accs = np.array([1.0 if predictions[g["goal_id"]]["embed_mechanism_id"] == g["target_mechanism_id"] else 0.0 for g in primary])
    out["metrics"]["M-ECE-GLOBAL"] = {"value": compute_ece(ece_confs, ece_accs), "note": "descriptive, NOT gated"}

    # overall
    gated = [k for k, v in out["gates"].items() if (v is False and k != "V13-GATE-VALIDITY")]
    if gated:
        out["status"] = "MEASUREMENT_INVALID"; out["outcome"] = "INCONCLUSIVE"
        out["reason"] = "validity gates failed: " + ", ".join(gated)
    else:
        out["status"] = "COMPLETE"
        if upper_ci <= 0:
            out["outcome"] = "FALSIFIES"
        elif lower_ci > 0:
            out["outcome"] = "SUPPORTS"
        else:
            out["outcome"] = "MIXED"

    out["observations"] += [
        f"OBS-CONTAMINATION: {n_flagged}/160 flagged (token>={CONTAM_TOK_T} or trigram>={CONTAM_TRI_T}); ids={sorted(flagged)}",
        f"OBS-PRIMARY-SET: |primary|={len(primary)} (cal {len(cal_app)}app/{len(cal_oos)}oos; test {len(test_app)}app/{len(test_oos)}oos)",
        f"OBS-ACCURACIES: embed={embed_c}/{embed_d}, stronglex={strong_c}/{strong_d} (abstain {strong_abst}), learned={learned_c}/{learned_d}, lextok={lex_c}/{lex_d}, random={rand_c}/{rand_d}, incumbent={inc_c}/{inc_d}, oracle={orac_c}/{orac_d}",
        f"OBS-PAIRED-DIFF-STRONGLEX: obs={obs_diff:.4f} CI=[{lower_ci:.4f},{upper_ci:.4f}] (families={n_fams}, B=10000, seed={SEED32})",
        f"OBS-D-RESOLVER: {out['outcome']}",
    ]
    out["validity_notes"] += [
        "VN-01: binding-only; no HTTP server, no task traffic; one HuggingFace model download (revision recorded).",
        "VN-02: mechanism-identity correctness ignores parameter binding (out of scope).",
        "VN-03: bootstrap covers resampling variability only (family-blocked, 5 blocks); one model.",
        "VN-04: contamination screen uses token-set Jaccard (>=0.60) OR char-trigram Jaccard (>=0.75) against goal_generator surfaces plus the parent 140-goal bank; the trigram representation differs from every arm.",
        "VN-05: ECE descriptive only, not gated.",
        "VN-06: B-LEX-STRONG-LEARNED is a sensitivity bound, not the claim-bearing comparator.",
        "VN-07: residual authorship limitation: the fresh-context authors had no file/tool access and their prompts contained no intent strings, but latent pretrained knowledge cannot be cryptographically excluded (see prereg V4).",
        "VN-08: checkpoint identity: the frozen revision is requested but, as in the parent packet (which could not fetch it and resolved to 1110a243fdf4706b3f48f1d95db1a4f5529b4d41), an unpinned fallback is recorded in env.model_revision/model_revision_resolved; results are interpretable only for the actually-resolved checkpoint (continuity with parent UNRES-04).",
        "VN-09: in derived/predictions.json a resolver that ABSTAINS is stored as the empty string '' (not null) for stronglex_mechanism_id/learned_mechanism_id/lexical_mechanism_id; the abstention count is also recorded explicitly in M-MECH-ACC-STRONGLEX.abstentions. An abstention scores as incorrect in all accuracy metrics.",
    ]
    out["artifacts"] += [
        {"path": "derived/predictions.json", "role": "raw"},
        {"path": "derived/contamination.json", "role": "derived"},
        {"path": "derived/measurements.json", "role": "derived"},
    ]

    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "predictions.json").write_text(json.dumps(convert_to_native(predictions), indent=2), encoding="utf-8")
    (OUT / "contamination.json").write_text(json.dumps(contamination, indent=2), encoding="utf-8")
    (OUT / "measurements.json").write_text(json.dumps(convert_to_native(out), indent=2), encoding="utf-8")
    print(json.dumps({"status": out["status"], "outcome": out["outcome"],
                      "obs_diff": float(obs_diff), "lower_ci": float(lower_ci), "upper_ci": float(upper_ci),
                      "embed_acc": embed_c / embed_d, "stronglex_acc": strong_c / strong_d,
                      "learned_acc": learned_c / learned_d,
                      "gate2f": out["metrics"].get("M-GATE-LOGISTIC-2F", {}).get("class")}, indent=2))

if __name__ == "__main__":
    main()
<!-- END FROZEN RUNNER -->

## 14. Canonical hashes block

<!-- BEGIN CANONICAL-HASHES -->
{
  "blocks": {
    "AUTHOR-PROMPTS": "2d2f0ad1a4a1c90694f6ba66ba93299bb5548e42c1db98218577c8fc663a9ccc",
    "GOAL BANK": "3a30e67f171385f9b5207e793a46575102aca7f4d8e53772e16894d92ba289dd",
    "LEXICON": "56d874db361b2377f6faf767f5c2aa652066f6b0b50d7a6081512af141ae9e5e",
    "OOS BANK": "3b74d933940c4cf6e4f43293cbc3d1e8c5ebd558a66d5029f38b23d59f24e5c1",
    "PRIOR-PARENT-BANK-TEXTS": "b1deb80890cf29aeaf39fb5b56c777b548d8606401b8e36a5bf82bad9e324f6a"
  }
}
<!-- END CANONICAL-HASHES -->
