# EXP-GRAPH-38180711589 preregistration

STATUS: DESIGN FINAL — awaiting the deterministic freeze step (design_contract_version 2). This file becomes an immutable interpretation dependency once freeze.json exists.

## 1. Scope and claim

Lane: graph. Claim: C-SEMANTIC-RESOLVE (currently HYPOTHESIS; no promotion is licensed by this packet).
This packet tests ONE bounded sub-mechanism left unmeasured by the parent EXP-GRAPH-38175554380: whether a bank-blind,
model-free deterministic resolver's OWN ambiguity/coverage signal can supply an abstention gate that simultaneously reaches
`pooled_false_accept <= 0.10`, `coverage >= 0.50` and `unknown_precision >= 0.85` on a disjoint calibration/test split, and
whether the deterministic resolve()+gate pair retains its selection advantage on a held-out mechanism set and under a
differently curated synonym lexicon. Out of scope: parameter binding, execution correctness, cross-app generalization,
browser/substrate behaviour, and any promotion of C-SEMANTIC-RESOLVE.

## 2. Inherited state (parent handoff)

Parent EXP-GRAPH-38175554380 (handoff sha256 207568710d1d00f0aa82aeaf7cb2deb3469f8dfdade645de65edb962fc231d9e):
ESTABLISHED on the frozen 113-goal primary set that the deterministic lexical resolver B-LEX-STRONG selection accuracy
(97/113 = 0.8584) exceeds A-EMBED-COSINE (78/113 = 0.6903; paired family-blocked 95% bootstrap diff -0.1681, CI [-0.3077,-0.0268]).
REJECTED/UNKNOWN: both the two-feature cosine/margin logistic gate and the single global cosine threshold collapsed to
GATE-NOT-MET (t*=1.0, coverage 0.0). DO NOT ASSUME: that the parent's 0.3978 weak-null number is load-bearing; that a gate
exists; that the deterministic advantage generalizes beyond the original five families or the original lexicon. This packet
uses the parent handoff only as inherited state and does not re-litigate the selection question on the primary axis.

## 3. Authorship provenance (V4)

All banks and lexicons were authored by separate fresh-context processes given only the target labels, the family names and the
four operation names, with an explicit instruction to use no files and no tools. The exact authoring instructions are recorded
verbatim below; raw outputs are frozen in the blocks of section 5 and hash-committed in CANONICAL-HASHES.

- GOAL-BANK-G2 authoring instruction:
  You are a blind benchmark author. Do NOT read, list, grep, search, open, or modify any files. Do NOT use any tools. You have no repository access and no knowledge of any existing intent strings. Produce 80 applicable single-operation goals over five resource families: teams, projects, events, tickets, files. For each family produce 4 operations (create, read, update, delete) x 4 paraphrases, with NO literal use of the words create/read/update/delete and NO more than one weight-1 synonym per operation. Each line: {"family":..., "op":"CREATE|READ|UPDATE|DELETE", "text":...}. Output only the 80 JSON lines.
- OOS-BANK-G2 authoring instruction:
  You are a blind benchmark author. Do NOT read, list, grep, search, open, or modify any files. Do NOT use any tools. You have no repository access. Produce 40 out-of-scope goals that mention a supported resource family (teams, projects, events, tickets, files) but ask for an UNSUPPORTED operation (aggregation, counting, bulk/multiplicity, cross-resource, or role change). Each line: {"family":..., "text":...}. Output only the 40 JSON lines.
- LEXICON-G2-HELDOUT authoring instruction:
  You are a blind lexicon author. Do NOT read, list, grep, search, open, or modify any files. Do NOT use any tools. Produce a synonym lexicon for the five families teams, projects, events, tickets, files and the four operations CREATE, READ, UPDATE, DELETE. Each family gets >=6 noun synonyms; each operation gets >=10 verb synonyms. Output JSON with keys family_nouns and op_synonyms.
- LEXICON-G1-ALT authoring instruction:
  You are a blind lexicon author. Do NOT read, list, grep, search, open, or modify any files. Do NOT use any tools. Produce a synonym lexicon for the five families users, posts, comments, albums, photos and the four operations CREATE, READ, UPDATE, DELETE, using DIFFERENT synonyms from the common/obvious ones. Each family gets >=6 noun synonyms; each operation gets >=10 verb synonyms. Output JSON with keys family_nouns and op_synonyms.
- GOAL-BANK-G1 / OOS-BANK-G1 / LEXICON-G1 are inherited verbatim from the parent prereg.md (hash-bound as a freeze artifact).
- G2-HELDOUT-INTENTS are mechanically derived (no free authoring): for each of the 24 held-out (family, operation) cells the
  canonical intent is the first CREATE/READ/UPDATE/DELETE synonym in LEXICON-G2-HELDOUT followed by "a " and the first family noun.

RESIDUAL LIMITATION (disclosed, not fixable here): fresh-context authors with no file access cannot be cryptographically proven
not to hold common intent strings in pretrained latent knowledge. The blind instruction, the no-tool constraint and the
contamination screen bound but do not eliminate this.

## 4. Axes

- AXIS-PRIMARY = GOAL-BANK-G1 + OOS-BANK-G1 + LEXICON-G1, split rule i%6 in (1,3,5) -> test. Decision-bearing, model-free.
- AXIS-ALTLEX = GOAL-BANK-G1 + OOS-BANK-G1 + LEXICON-G1-ALT, same split. Retention/generalization.
- AXIS-HELDOUT = GOAL-BANK-G2 + OOS-BANK-G2 + LEXICON-G2-HELDOUT, split rule i%4 in (1,3) -> test. Retention/generalization.

Contamination screen (V3): for every goal, flag iff max token-set Jaccard >= 0.6 OR max char-trigram Jaccard >= 0.75
against every prior authoring surface (the 20 registry intents, all PARAPHRASES/NO_APPLICABLE/OOD templates in the bound
goal_generator.py, the parent's 140-goal PRIOR-PARENT-BANK-TEXTS extracted from the hash-bound parent prereg.md, and for
AXIS-HELDOUT also the 160 G1 goal texts). More than 20 flags -> MEASUREMENT_INVALID. DESIGN satisfiability probe:
AXIS-PRIMARY flags 9 (app_004, app_049, app_052, app_073, app_076, app_097, app_100, oos_024, oos_026) reproducing the
parent exactly; AXIS-HELDOUT flags 0.

## 5. Frozen blocks

### GOAL-BANK-G1 (120 applicable goals, inherited verbatim from parent)
<!-- BEGIN GOAL-BANK-G1 -->
{"family": "users", "op": "CREATE", "text": "Add one new user."}
{"family": "users", "op": "CREATE", "text": "Please make a new account."}
{"family": "users", "op": "CREATE", "text": "Register a single new member."}
{"family": "users", "op": "CREATE", "text": "Set up one new profile."}
{"family": "users", "op": "CREATE", "text": "Introduce a fresh customer."}
{"family": "users", "op": "CREATE", "text": "Generate one new subscriber."}
{"family": "users", "op": "READ", "text": "Fetch the user with this id."}
{"family": "users", "op": "READ", "text": "Retrieve one account by its identifier."}
{"family": "users", "op": "READ", "text": "Get the single member matching this id."}
{"family": "users", "op": "READ", "text": "Look up one profile using its identifier."}
{"family": "users", "op": "READ", "text": "View the one customer with this id."}
{"family": "users", "op": "READ", "text": "Pull up the single subscriber with this id."}
{"family": "users", "op": "UPDATE", "text": "Change the user with this id."}
{"family": "users", "op": "UPDATE", "text": "Modify one account identified by this id."}
{"family": "users", "op": "UPDATE", "text": "Edit the single member with this identifier."}
{"family": "users", "op": "UPDATE", "text": "Adjust one profile by its id."}
{"family": "users", "op": "UPDATE", "text": "Revise the one customer with this id."}
{"family": "users", "op": "UPDATE", "text": "Amend the single subscriber with this identifier."}
{"family": "users", "op": "DELETE", "text": "Remove the user with this id."}
{"family": "users", "op": "DELETE", "text": "Erase one account by its identifier."}
{"family": "users", "op": "DELETE", "text": "Discard the single member with this id."}
{"family": "users", "op": "DELETE", "text": "Eliminate one profile using this id."}
{"family": "users", "op": "DELETE", "text": "Drop the one customer with this identifier."}
{"family": "users", "op": "DELETE", "text": "Get rid of the single subscriber with this id."}
{"family": "posts", "op": "CREATE", "text": "Add one new post."}
{"family": "posts", "op": "CREATE", "text": "Make a new article."}
{"family": "posts", "op": "CREATE", "text": "Register a single new entry."}
{"family": "posts", "op": "CREATE", "text": "Set up one new blog entry."}
{"family": "posts", "op": "CREATE", "text": "Introduce a new story."}
{"family": "posts", "op": "CREATE", "text": "Generate one new publication."}
{"family": "posts", "op": "READ", "text": "Fetch the post with this id."}
{"family": "posts", "op": "READ", "text": "Retrieve one article by its identifier."}
{"family": "posts", "op": "READ", "text": "Get the single entry matching this id."}
{"family": "posts", "op": "READ", "text": "Look up one blog entry using this id."}
{"family": "posts", "op": "READ", "text": "View the one story with this identifier."}
{"family": "posts", "op": "READ", "text": "Pull up the single publication with this id."}
{"family": "posts", "op": "UPDATE", "text": "Change the post with this id."}
{"family": "posts", "op": "UPDATE", "text": "Modify one article by its identifier."}
{"family": "posts", "op": "UPDATE", "text": "Edit the single entry with this id."}
{"family": "posts", "op": "UPDATE", "text": "Adjust one blog entry using this id."}
{"family": "posts", "op": "UPDATE", "text": "Revise the one story with this identifier."}
{"family": "posts", "op": "UPDATE", "text": "Amend the single publication with this id."}
{"family": "posts", "op": "DELETE", "text": "Remove the post with this id."}
{"family": "posts", "op": "DELETE", "text": "Erase one article by its identifier."}
{"family": "posts", "op": "DELETE", "text": "Discard the single entry with this id."}
{"family": "posts", "op": "DELETE", "text": "Eliminate one blog entry using this id."}
{"family": "posts", "op": "DELETE", "text": "Drop the one story with this identifier."}
{"family": "posts", "op": "DELETE", "text": "Get rid of the single publication with this id."}
{"family": "comments", "op": "CREATE", "text": "Add one new comment."}
{"family": "comments", "op": "CREATE", "text": "Make a new remark."}
{"family": "comments", "op": "CREATE", "text": "Register a single new note."}
{"family": "comments", "op": "CREATE", "text": "Set up one new reply."}
{"family": "comments", "op": "CREATE", "text": "Introduce a new response."}
{"family": "comments", "op": "CREATE", "text": "Generate one new annotation."}
{"family": "comments", "op": "READ", "text": "Fetch the comment with this id."}
{"family": "comments", "op": "READ", "text": "Retrieve one remark by its identifier."}
{"family": "comments", "op": "READ", "text": "Get the single note matching this id."}
{"family": "comments", "op": "READ", "text": "Look up one reply using this id."}
{"family": "comments", "op": "READ", "text": "View the one response with this identifier."}
{"family": "comments", "op": "READ", "text": "Pull up the single annotation with this id."}
{"family": "comments", "op": "UPDATE", "text": "Change the comment with this id."}
{"family": "comments", "op": "UPDATE", "text": "Modify one remark by its identifier."}
{"family": "comments", "op": "UPDATE", "text": "Edit the single note with this id."}
{"family": "comments", "op": "UPDATE", "text": "Adjust one reply using this id."}
{"family": "comments", "op": "UPDATE", "text": "Revise the one response with this identifier."}
{"family": "comments", "op": "UPDATE", "text": "Amend the single annotation with this id."}
{"family": "comments", "op": "DELETE", "text": "Remove the comment with this id."}
{"family": "comments", "op": "DELETE", "text": "Erase one remark by its identifier."}
{"family": "comments", "op": "DELETE", "text": "Discard the single note with this id."}
{"family": "comments", "op": "DELETE", "text": "Eliminate one reply using this id."}
{"family": "comments", "op": "DELETE", "text": "Drop the one response with this identifier."}
{"family": "comments", "op": "DELETE", "text": "Get rid of the single annotation with this id."}
{"family": "albums", "op": "CREATE", "text": "Add one new album."}
{"family": "albums", "op": "CREATE", "text": "Make a new gallery."}
{"family": "albums", "op": "CREATE", "text": "Register a single new photo collection."}
{"family": "albums", "op": "CREATE", "text": "Set up one new photo set."}
{"family": "albums", "op": "CREATE", "text": "Introduce a new compilation."}
{"family": "albums", "op": "CREATE", "text": "Generate one new collection."}
{"family": "albums", "op": "READ", "text": "Fetch the album with this id."}
{"family": "albums", "op": "READ", "text": "Retrieve one gallery by its identifier."}
{"family": "albums", "op": "READ", "text": "Get the single photo collection matching this id."}
{"family": "albums", "op": "READ", "text": "Look up one photo set using this id."}
{"family": "albums", "op": "READ", "text": "View the one compilation with this identifier."}
{"family": "albums", "op": "READ", "text": "Pull up the single collection with this id."}
{"family": "albums", "op": "UPDATE", "text": "Change the album with this id."}
{"family": "albums", "op": "UPDATE", "text": "Modify one gallery by its identifier."}
{"family": "albums", "op": "UPDATE", "text": "Edit the single photo collection with this id."}
{"family": "albums", "op": "UPDATE", "text": "Adjust one photo set using this id."}
{"family": "albums", "op": "UPDATE", "text": "Revise the one compilation with this identifier."}
{"family": "albums", "op": "UPDATE", "text": "Amend the single collection with this id."}
{"family": "albums", "op": "DELETE", "text": "Remove the album with this id."}
{"family": "albums", "op": "DELETE", "text": "Erase one gallery by its identifier."}
{"family": "albums", "op": "DELETE", "text": "Discard the single photo collection with this id."}
{"family": "albums", "op": "DELETE", "text": "Eliminate one photo set using this id."}
{"family": "albums", "op": "DELETE", "text": "Drop the one compilation with this identifier."}
{"family": "albums", "op": "DELETE", "text": "Get rid of the single collection with this id."}
{"family": "photos", "op": "CREATE", "text": "Add one new photo."}
{"family": "photos", "op": "CREATE", "text": "Make a new picture."}
{"family": "photos", "op": "CREATE", "text": "Register a single new image."}
{"family": "photos", "op": "CREATE", "text": "Set up one new snapshot."}
{"family": "photos", "op": "CREATE", "text": "Introduce a new photograph."}
{"family": "photos", "op": "CREATE", "text": "Generate one new shot."}
{"family": "photos", "op": "READ", "text": "Fetch the photo with this id."}
{"family": "photos", "op": "READ", "text": "Retrieve one picture by its identifier."}
{"family": "photos", "op": "READ", "text": "Get the single image matching this id."}
{"family": "photos", "op": "READ", "text": "Look up one snapshot using this id."}
{"family": "photos", "op": "READ", "text": "View the one photograph with this identifier."}
{"family": "photos", "op": "READ", "text": "Pull up the single shot with this id."}
{"family": "photos", "op": "UPDATE", "text": "Change the photo with this id."}
{"family": "photos", "op": "UPDATE", "text": "Modify one picture by its identifier."}
{"family": "photos", "op": "UPDATE", "text": "Edit the single image with this id."}
{"family": "photos", "op": "UPDATE", "text": "Adjust one snapshot using this id."}
{"family": "photos", "op": "UPDATE", "text": "Revise the one photograph with this identifier."}
{"family": "photos", "op": "UPDATE", "text": "Amend the single shot with this id."}
{"family": "photos", "op": "DELETE", "text": "Remove the photo with this id."}
{"family": "photos", "op": "DELETE", "text": "Erase one picture by its identifier."}
{"family": "photos", "op": "DELETE", "text": "Discard the single image with this id."}
{"family": "photos", "op": "DELETE", "text": "Eliminate one snapshot using this id."}
{"family": "photos", "op": "DELETE", "text": "Drop the one photograph with this identifier."}
{"family": "photos", "op": "DELETE", "text": "Get rid of the single shot with this id."}
<!-- END GOAL-BANK-G1 -->

### OOS-BANK-G1 (40 out-of-scope goals, inherited verbatim from parent)
<!-- BEGIN OOS-BANK-G1 -->
{"family": "users", "text": "List every user in the system at once."}
{"family": "posts", "text": "Show me page two of the posts."}
{"family": "comments", "text": "Find all comments containing the word trouble."}
{"family": "albums", "text": "How many albums exist right now?"}
{"family": "photos", "text": "Give me only the photos smaller than one megabyte."}
{"family": "users", "text": "Export the entire user table to a CSV file."}
{"family": "posts", "text": "Import a batch of posts from my spreadsheet."}
{"family": "comments", "text": "Add a thumbs-up reaction to this comment."}
{"family": "albums", "text": "Let me follow this album for future updates."}
{"family": "photos", "text": "Attach the tag vacation to that photo."}
{"family": "users", "text": "Sign me in with a username and password."}
{"family": "posts", "text": "Schedule this post to publish next Tuesday."}
{"family": "comments", "text": "Remove all of my comments in one go."}
{"family": "albums", "text": "Order the albums by title alphabetically."}
{"family": "photos", "text": "Upload a brand new photo from my phone."}
{"family": "users", "text": "Email every user a welcome message."}
{"family": "posts", "text": "Undo my last edit to this post."}
{"family": "comments", "text": "Flag this comment as abusive for review."}
{"family": "albums", "text": "Share this album with my friends."}
{"family": "photos", "text": "Download all of my photos as a zip archive."}
{"family": "users", "text": "Make this user an administrator."}
{"family": "posts", "text": "Produce a monthly report of post activity."}
{"family": "comments", "text": "Attach the full author record to each comment."}
{"family": "albums", "text": "Merge two albums into a single one."}
{"family": "photos", "text": "Shrink this photo down to a thumbnail."}
{"family": "users", "text": "Search for users by their email address."}
{"family": "posts", "text": "Show me the trending posts from this week."}
{"family": "comments", "text": "Nest replies underneath this comment."}
{"family": "albums", "text": "Set an expiration date on this album."}
{"family": "photos", "text": "Watermark this photo automatically."}
{"family": "users", "text": "Follow another member of the site."}
{"family": "posts", "text": "Count the likes on this post."}
{"family": "comments", "text": "Give me fifty comments at a time."}
{"family": "albums", "text": "Count the items inside this album."}
{"family": "photos", "text": "Upload a whole folder of photos simultaneously."}
{"family": "users", "text": "Log this user out of every active session."}
{"family": "posts", "text": "Filter the posts published between January and March."}
{"family": "comments", "text": "Sort these comments by the newest first."}
{"family": "albums", "text": "Notify subscribers when this album changes."}
{"family": "photos", "text": "Pull a photo in directly from a web link."}
<!-- END OOS-BANK-G1 -->

### LEXICON-G1 (inherited verbatim from parent; LEXICON-G1-ORIG used for AXIS-PRIMARY)
<!-- BEGIN LEXICON-G1 -->
{
  "op_synonyms": {
    "CREATE": [
      "create",
      "add",
      "make",
      "new",
      "insert",
      "post",
      "put",
      "register",
      "generate",
      "build",
      "produce",
      "construct",
      "compose",
      "establish",
      "initialize",
      "init",
      "spawn",
      "instantiate",
      "write",
      "submit",
      "save",
      "store",
      "record",
      "append",
      "introduce",
      "launch",
      "open",
      "set up",
      "define",
      "allocate",
      "mint",
      "provision",
      "enroll",
      "sign up",
      "upload",
      "publish"
    ],
    "READ": [
      "read",
      "get",
      "fetch",
      "retrieve",
      "load",
      "find",
      "look up",
      "lookup",
      "query",
      "select",
      "show",
      "view",
      "display",
      "list",
      "obtain",
      "access",
      "pull",
      "grab",
      "return",
      "inspect",
      "examine",
      "search",
      "locate",
      "resolve",
      "request",
      "download",
      "see",
      "check",
      "print",
      "dump",
      "describe"
    ],
    "UPDATE": [
      "update",
      "edit",
      "modify",
      "change",
      "set",
      "patch",
      "alter",
      "adjust",
      "revise",
      "amend",
      "replace",
      "overwrite",
      "refresh",
      "sync",
      "synchronize",
      "mutate",
      "transform",
      "convert",
      "fix",
      "correct",
      "toggle",
      "enable",
      "disable",
      "rename",
      "move",
      "merge",
      "bump",
      "increment",
      "assign",
      "upsert",
      "apply",
      "reset"
    ],
    "DELETE": [
      "delete",
      "remove",
      "destroy",
      "drop",
      "erase",
      "clear",
      "purge",
      "discard",
      "eliminate",
      "unset",
      "unlink",
      "detach",
      "revoke",
      "cancel",
      "kill",
      "terminate",
      "wipe",
      "prune",
      "trash",
      "archive",
      "deactivate",
      "disable",
      "expire",
      "unregister",
      "unenroll",
      "strip",
      "empty",
      "flush",
      "dismiss",
      "reject"
    ]
  },
  "family_nouns": {
    "users": [
      "user",
      "account",
      "member",
      "person",
      "profile",
      "customer",
      "client",
      "subscriber",
      "participant",
      "individual",
      "identity",
      "principal",
      "actor",
      "login",
      "credential",
      "owner",
      "operator",
      "contact"
    ],
    "posts": [
      "post",
      "article",
      "entry",
      "message",
      "item",
      "publication",
      "blog post",
      "status",
      "update",
      "story",
      "note",
      "thread",
      "content",
      "submission",
      "feed item",
      "tweet",
      "blog"
    ],
    "comments": [
      "comment",
      "remark",
      "note",
      "reply",
      "response",
      "feedback",
      "message",
      "annotation",
      "observation",
      "review",
      "mention",
      "reaction",
      "opinion"
    ],
    "albums": [
      "album",
      "collection",
      "gallery",
      "folder",
      "set",
      "bundle",
      "group",
      "batch",
      "portfolio",
      "library",
      "compilation",
      "directory",
      "category"
    ],
    "photos": [
      "photo",
      "image",
      "picture",
      "pic",
      "photograph",
      "img",
      "media",
      "asset",
      "file",
      "snapshot",
      "shot",
      "graphic",
      "thumbnail",
      "avatar",
      "attachment"
    ]
  }
}
<!-- END LEXICON-G1 -->

### LEXICON-G1-ALT (independent alternate lexicon for the original five families)
<!-- BEGIN LEXICON-G1-ALT -->
{
  "op_synonyms": {
    "CREATE": [
      "create",
      "make",
      "add",
      "build",
      "generate",
      "produce",
      "construct",
      "insert",
      "register",
      "set up",
      "start",
      "open",
      "new",
      "post",
      "upload",
      "publish",
      "submit",
      "write",
      "draft",
      "compose",
      "form",
      "initiate"
    ],
    "READ": [
      "read",
      "get",
      "fetch",
      "retrieve",
      "load",
      "show",
      "view",
      "display",
      "see",
      "find",
      "look up",
      "lookup",
      "query",
      "access",
      "open",
      "inspect",
      "check",
      "pull",
      "grab",
      "obtain",
      "browse",
      "search",
      "list"
    ],
    "UPDATE": [
      "update",
      "edit",
      "modify",
      "change",
      "alter",
      "adjust",
      "revise",
      "amend",
      "patch",
      "set",
      "replace",
      "rename",
      "correct",
      "fix",
      "refresh",
      "rewrite",
      "tweak",
      "overwrite",
      "save",
      "update in place",
      "reconfigure"
    ],
    "DELETE": [
      "delete",
      "remove",
      "drop",
      "erase",
      "destroy",
      "clear",
      "discard",
      "eliminate",
      "purge",
      "cancel",
      "unlink",
      "trash",
      "wipe",
      "kill",
      "void",
      "scrap",
      "expunge",
      "withdraw",
      "take out",
      "get rid of",
      "dispose of"
    ]
  },
  "family_nouns": {
    "users": [
      "user",
      "account",
      "member",
      "person",
      "profile",
      "customer",
      "subscriber",
      "client",
      "login",
      "identity",
      "people",
      "participant"
    ],
    "posts": [
      "post",
      "article",
      "entry",
      "blog post",
      "message",
      "status update",
      "publication",
      "content item",
      "write-up",
      "story",
      "piece",
      "thread"
    ],
    "comments": [
      "comment",
      "remark",
      "reply",
      "response",
      "note",
      "feedback",
      "message",
      "annotation",
      "observation",
      "mention",
      "reaction"
    ],
    "albums": [
      "album",
      "gallery",
      "collection",
      "photo album",
      "set",
      "folder",
      "photobook",
      "portfolio",
      "compilation",
      "binder",
      "group"
    ],
    "photos": [
      "photo",
      "picture",
      "image",
      "pic",
      "photograph",
      "snapshot",
      "shot",
      "frame",
      "capture",
      "still",
      "print"
    ]
  }
}
<!-- END LEXICON-G1-ALT -->

### GOAL-BANK-G2 (80 applicable held-out-family goals, blind-authored)
<!-- BEGIN GOAL-BANK-G2 -->
{"family": "teams", "op": "CREATE", "text": "Add a new squad named Blue Falcons."}
{"family": "teams", "op": "CREATE", "text": "Start a fresh group called Night Owls."}
{"family": "teams", "op": "CREATE", "text": "Form a new team for the design guild."}
{"family": "teams", "op": "CREATE", "text": "Register a new crew named Iron Wolves."}
{"family": "teams", "op": "READ", "text": "Fetch the squad with identifier 42."}
{"family": "teams", "op": "READ", "text": "Show me the group whose id is 17."}
{"family": "teams", "op": "READ", "text": "Retrieve the team identified as 88."}
{"family": "teams", "op": "READ", "text": "Look up the crew with id 5."}
{"family": "teams", "op": "UPDATE", "text": "Rename the squad with id 42 to Red Hawks."}
{"family": "teams", "op": "UPDATE", "text": "Modify the group identified by id 17."}
{"family": "teams", "op": "UPDATE", "text": "Change the team named Blue Falcons."}
{"family": "teams", "op": "UPDATE", "text": "Revise the crew with identifier 5."}
{"family": "teams", "op": "DELETE", "text": "Remove the squad with id 42."}
{"family": "teams", "op": "DELETE", "text": "Discard the group identified by id 17."}
{"family": "teams", "op": "DELETE", "text": "Drop the team whose identifier is 88."}
{"family": "teams", "op": "DELETE", "text": "Erase the crew with id 5."}
{"family": "projects", "op": "CREATE", "text": "Launch a new initiative called Apollo."}
{"family": "projects", "op": "CREATE", "text": "Add a fresh undertaking named Borealis."}
{"family": "projects", "op": "CREATE", "text": "Initiate a new project for the mobile app."}
{"family": "projects", "op": "CREATE", "text": "Set up a new venture titled Comet."}
{"family": "projects", "op": "READ", "text": "Fetch the initiative with id 12."}
{"family": "projects", "op": "READ", "text": "Display the undertaking identified by 34."}
{"family": "projects", "op": "READ", "text": "Retrieve the project whose id is 7."}
{"family": "projects", "op": "READ", "text": "Look up the venture with identifier 91."}
{"family": "projects", "op": "UPDATE", "text": "Rename the initiative with id 12."}
{"family": "projects", "op": "UPDATE", "text": "Amend the undertaking identified by 34."}
{"family": "projects", "op": "UPDATE", "text": "Adjust the project with id 7."}
{"family": "projects", "op": "UPDATE", "text": "Revise the venture whose id is 91."}
{"family": "projects", "op": "DELETE", "text": "Remove the initiative with id 12."}
{"family": "projects", "op": "DELETE", "text": "Discard the undertaking identified by 34."}
{"family": "projects", "op": "DELETE", "text": "Scrap the project with id 7."}
{"family": "projects", "op": "DELETE", "text": "Erase the venture whose id is 91."}
{"family": "events", "op": "CREATE", "text": "Schedule a new event called Kickoff."}
{"family": "events", "op": "CREATE", "text": "Add a fresh meeting named Standup."}
{"family": "events", "op": "CREATE", "text": "Book a new happening titled Launch Day."}
{"family": "events", "op": "CREATE", "text": "Arrange a new gathering for the conference."}
{"family": "events", "op": "READ", "text": "Fetch the event with id 3."}
{"family": "events", "op": "READ", "text": "Show the meeting identified by 56."}
{"family": "events", "op": "READ", "text": "Retrieve the happening whose id is 22."}
{"family": "events", "op": "READ", "text": "Look up the gathering with identifier 8."}
{"family": "events", "op": "UPDATE", "text": "Reschedule the event with id 3."}
{"family": "events", "op": "UPDATE", "text": "Modify the meeting identified by 56."}
{"family": "events", "op": "UPDATE", "text": "Change the happening whose id is 22."}
{"family": "events", "op": "UPDATE", "text": "Revise the gathering with identifier 8."}
{"family": "events", "op": "DELETE", "text": "Cancel the event with id 3."}
{"family": "events", "op": "DELETE", "text": "Remove the meeting identified by 56."}
{"family": "events", "op": "DELETE", "text": "Drop the happening whose id is 22."}
{"family": "events", "op": "DELETE", "text": "Erase the gathering with identifier 8."}
{"family": "tickets", "op": "CREATE", "text": "Open a new ticket about the login bug."}
{"family": "tickets", "op": "CREATE", "text": "Add a fresh issue titled Slow query."}
{"family": "tickets", "op": "CREATE", "text": "File a new case for the billing glitch."}
{"family": "tickets", "op": "CREATE", "text": "Lodge a new request regarding the crash."}
{"family": "tickets", "op": "READ", "text": "Fetch the ticket with id 101."}
{"family": "tickets", "op": "READ", "text": "Show the issue identified by 202."}
{"family": "tickets", "op": "READ", "text": "Retrieve the case whose id is 303."}
{"family": "tickets", "op": "READ", "text": "Look up the request with identifier 404."}
{"family": "tickets", "op": "UPDATE", "text": "Modify the ticket with id 101."}
{"family": "tickets", "op": "UPDATE", "text": "Amend the issue identified by 202."}
{"family": "tickets", "op": "UPDATE", "text": "Change the case whose id is 303."}
{"family": "tickets", "op": "UPDATE", "text": "Revise the request with identifier 404."}
{"family": "tickets", "op": "DELETE", "text": "Close the ticket with id 101."}
{"family": "tickets", "op": "DELETE", "text": "Remove the issue identified by 202."}
{"family": "tickets", "op": "DELETE", "text": "Discard the case whose id is 303."}
{"family": "tickets", "op": "DELETE", "text": "Erase the request with identifier 404."}
{"family": "files", "op": "CREATE", "text": "Add a new document called report.pdf."}
{"family": "files", "op": "CREATE", "text": "Store a fresh file named notes.txt."}
{"family": "files", "op": "CREATE", "text": "Save a new asset titled logo.png."}
{"family": "files", "op": "CREATE", "text": "Register a new asset named banner.jpg."}
{"family": "files", "op": "READ", "text": "Fetch the document with id 9."}
{"family": "files", "op": "READ", "text": "Show the file identified by 18."}
{"family": "files", "op": "READ", "text": "Retrieve the asset whose id is 27."}
{"family": "files", "op": "READ", "text": "Look up the document with identifier 36."}
{"family": "files", "op": "UPDATE", "text": "Rename the document with id 9."}
{"family": "files", "op": "UPDATE", "text": "Modify the file identified by 18."}
{"family": "files", "op": "UPDATE", "text": "Change the asset whose id is 27."}
{"family": "files", "op": "UPDATE", "text": "Revise the document with identifier 36."}
{"family": "files", "op": "DELETE", "text": "Remove the document with id 9."}
{"family": "files", "op": "DELETE", "text": "Discard the file identified by 18."}
{"family": "files", "op": "DELETE", "text": "Drop the asset whose id is 27."}
{"family": "files", "op": "DELETE", "text": "Erase the document with identifier 36."}
<!-- END GOAL-BANK-G2 -->

### OOS-BANK-G2 (40 held-out-family out-of-scope goals, blind-authored)
<!-- BEGIN OOS-BANK-G2 -->
{"family": "teams", "text": "Show me every team that exists in the workspace."}
{"family": "projects", "text": "Which projects match the keyword launch?"}
{"family": "events", "text": "List all meetings happening next week."}
{"family": "tickets", "text": "How many issues are currently open?"}
{"family": "files", "text": "Download the contents of an asset to my machine."}
{"family": "teams", "text": "Invite a new member into the squad I belong to."}
{"family": "projects", "text": "Sort the initiatives by their due date."}
{"family": "events", "text": "Send a reminder about tomorrow's meeting."}
{"family": "tickets", "text": "Assign this case to the on-call engineer."}
{"family": "files", "text": "Upload a new attachment onto a document."}
{"family": "teams", "text": "Wipe out several teams in one batch."}
{"family": "projects", "text": "Export every initiative into a spreadsheet."}
{"family": "events", "text": "Comment on a meeting to suggest a later time."}
{"family": "tickets", "text": "Add a tag to the issue about login failures."}
{"family": "files", "text": "Share this asset with an external colleague."}
{"family": "teams", "text": "Page through the full group directory."}
{"family": "projects", "text": "Roll back the last edit made to an initiative."}
{"family": "events", "text": "Log in so I can see my meeting schedule."}
{"family": "tickets", "text": "Merge two duplicate cases together."}
{"family": "files", "text": "Move a document into a nested folder."}
{"family": "teams", "text": "Follow a squad to get its updates."}
{"family": "projects", "text": "Build a progress report across all initiatives."}
{"family": "events", "text": "Import my calendar into the meeting system."}
{"family": "tickets", "text": "Filter cases by their priority level."}
{"family": "files", "text": "Show the version history of an asset."}
{"family": "teams", "text": "Grant an admin role to everyone in the group."}
{"family": "projects", "text": "Join each initiative with its owning team."}
{"family": "events", "text": "Cancel the whole recurring meeting series."}
{"family": "tickets", "text": "Update the status of many issues at once."}
{"family": "files", "text": "Restore a document I deleted yesterday."}
{"family": "teams", "text": "Reset the password of a squad member."}
{"family": "projects", "text": "Watch an initiative so I get notified of changes."}
{"family": "events", "text": "Group meetings by their location."}
{"family": "tickets", "text": "Search for cases mentioning the billing bug."}
{"family": "files", "text": "Compress all assets into a single archive."}
{"family": "teams", "text": "Count how many people are in each team."}
{"family": "projects", "text": "Like or star an initiative I enjoy."}
{"family": "events", "text": "Undo my last change to a meeting."}
{"family": "tickets", "text": "Print a summary report of all tickets."}
{"family": "files", "text": "Lock a document so no one else can touch it."}
<!-- END OOS-BANK-G2 -->

### LEXICON-G2-HELDOUT (blind-authored lexicon for the held-out families)
<!-- BEGIN LEXICON-G2-HELDOUT -->
{
  "op_synonyms": {
    "CREATE": [
      "add",
      "create",
      "make",
      "new",
      "insert",
      "register",
      "generate",
      "build",
      "set up",
      "spin up",
      "open",
      "start",
      "initiate",
      "establish",
      "form",
      "compose",
      "draft",
      "submit",
      "post",
      "upload",
      "launch",
      "define",
      "instantiate",
      "provision",
      "record",
      "log",
      "publish",
      "schedule",
      "book",
      "enroll",
      "import",
      "append",
      "raise",
      "file",
      "spawn",
      "mint",
      "add new",
      "create new"
    ],
    "READ": [
      "get",
      "fetch",
      "read",
      "retrieve",
      "view",
      "show",
      "list",
      "find",
      "look up",
      "query",
      "search",
      "load",
      "open",
      "inspect",
      "display",
      "print",
      "check",
      "see",
      "access",
      "pull",
      "grab",
      "obtain",
      "get by id",
      "fetch one",
      "describe",
      "dump",
      "summarize",
      "count",
      "examine",
      "review",
      "report",
      "browse",
      "preview",
      "download"
    ],
    "UPDATE": [
      "update",
      "edit",
      "modify",
      "change",
      "set",
      "patch",
      "adjust",
      "amend",
      "revise",
      "fix",
      "correct",
      "rename",
      "replace",
      "overwrite",
      "save",
      "apply",
      "commit",
      "move",
      "reassign",
      "assign",
      "alter",
      "tweak",
      "refresh",
      "sync",
      "mark",
      "transition",
      "reopen",
      "upsert",
      "merge",
      "write back",
      "update field",
      "reword",
      "reschedule",
      "toggle",
      "enable",
      "disable"
    ],
    "DELETE": [
      "delete",
      "remove",
      "destroy",
      "drop",
      "erase",
      "discard",
      "clear",
      "purge",
      "trash",
      "archive",
      "deactivate",
      "cancel",
      "revoke",
      "withdraw",
      "unlink",
      "detach",
      "terminate",
      "kill",
      "wipe",
      "unset",
      "expunge",
      "retire",
      "soft delete",
      "hard delete",
      "delete permanently",
      "dismiss",
      "close out",
      "void",
      "strip",
      "eliminate",
      "scrub"
    ]
  },
  "family_nouns": {
    "teams": [
      "team",
      "group",
      "squad",
      "crew",
      "org",
      "organization",
      "department",
      "unit",
      "pod",
      "guild",
      "party",
      "cohort",
      "band",
      "circle",
      "division",
      "working group"
    ],
    "projects": [
      "project",
      "initiative",
      "program",
      "effort",
      "endeavor",
      "venture",
      "workstream",
      "epic",
      "campaign",
      "task force",
      "plan",
      "undertaking",
      "job",
      "engagement"
    ],
    "events": [
      "event",
      "meeting",
      "appointment",
      "occurrence",
      "happening",
      "session",
      "gathering",
      "occasion",
      "conference",
      "call",
      "booking",
      "activity",
      "ceremony",
      "function",
      "slot"
    ],
    "tickets": [
      "ticket",
      "issue",
      "task",
      "bug",
      "case",
      "request",
      "incident",
      "problem",
      "item",
      "work item",
      "trouble ticket",
      "support ticket",
      "backlog item",
      "report"
    ],
    "files": [
      "file",
      "document",
      "doc",
      "attachment",
      "asset",
      "record",
      "artifact",
      "upload",
      "blob",
      "resource",
      "folder",
      "image",
      "media",
      "spreadsheet",
      "pdf",
      "note"
    ]
  }
}
<!-- END LEXICON-G2-HELDOUT -->

### G2-HELDOUT-INTENTS (24 mechanically derived held-out embedding intents)
<!-- BEGIN G2-HELDOUT-INTENTS -->
{"family": "teams", "op": "CREATE", "intent": "add a team"}
{"family": "teams", "op": "READ", "intent": "get a team"}
{"family": "teams", "op": "UPDATE", "intent": "update a team"}
{"family": "teams", "op": "DELETE", "intent": "delete a team"}
{"family": "projects", "op": "CREATE", "intent": "add a project"}
{"family": "projects", "op": "READ", "intent": "get a project"}
{"family": "projects", "op": "UPDATE", "intent": "update a project"}
{"family": "projects", "op": "DELETE", "intent": "delete a project"}
{"family": "events", "op": "CREATE", "intent": "add a event"}
{"family": "events", "op": "READ", "intent": "get a event"}
{"family": "events", "op": "UPDATE", "intent": "update a event"}
{"family": "events", "op": "DELETE", "intent": "delete a event"}
{"family": "tickets", "op": "CREATE", "intent": "add a ticket"}
{"family": "tickets", "op": "READ", "intent": "get a ticket"}
{"family": "tickets", "op": "UPDATE", "intent": "update a ticket"}
{"family": "tickets", "op": "DELETE", "intent": "delete a ticket"}
{"family": "files", "op": "CREATE", "intent": "add a file"}
{"family": "files", "op": "READ", "intent": "get a file"}
{"family": "files", "op": "UPDATE", "intent": "update a file"}
{"family": "files", "op": "DELETE", "intent": "delete a file"}
<!-- END G2-HELDOUT-INTENTS -->

## 6. Resolver B-LEX-STRONG (key-set longest, noun-homograph disambiguation)

See `comp()` in the FROZEN RUNNER (section 10). Summary: find all whole-token (plural-tolerant) family-noun spans and operation
phrase spans; discard an operation candidate whose first token is also a family noun when preceded by a determiner (so the noun
"post"/"file" is not read as the verb); a tie among synonyms of the SAME category is not ambiguous, only cross-category ties are;
resolve family-first and operation-first, accept iff the two agree or exactly one is defined; else unresolved. Never loads a model.

## 7. Ambiguity signal and gate T-LEX-AMBIG

Per goal integer signal S = 1[famNONE] + 1[opNONE] + 1[opTIE] + 1[noslot] + 1[quant], where famNONE/opNONE means no supported
family noun / operation synonym was found, opTIE means two different operations share the longest-span tie, noslot means a
resolved READ/UPDATE/DELETE goal has no reference cue in REF, and quant means a multiplicity cue in QUANT is present.
EXECUTE iff the resolver produced a mechanism AND S <= t*. t* is calibrated on the calibration split by the objective-direct
rule: the smallest observed calibration S with cal pooled_false_accept <= 0.1 and cal unknown_precision >= 0.85;
if none, the predeclared fallback t* = argmin |cal pooled_false_accept - 0.1| subject to cal unknown_precision >= 0.85;
if none, t* = max(S)+1 (abstain-all).

REF = ['called', 'id', 'identified', 'identifier', 'labeled', 'labelled', 'named', 'number', 'numbered', 'referred', 'titled']. QUANT = ['all', 'any', 'batch', 'both', 'bulk', 'each', 'entire', 'every', 'many', 'multiple', 'several', 'some', 'whole'].

DESIGN satisfiability probe (calibration split only; the test split is NOT scored in DESIGN): AXIS-PRIMARY cal-feasible at t*=0
with coverage 0.860, pooled_false_accept 0.100, unknown_precision 1.000; AXIS-ALTLEX at t*=0 with 0.912/0.100/1.000;
AXIS-HELDOUT at t*=0 with 0.875/0.050/1.000. The accept branch is therefore reachable on every axis.

## 8. Metrics

- pooled_false_accept = executed out-of-scope / all out-of-scope.
- coverage = executed applicable / all applicable.
- unknown_precision (PRIMARY) = gate-abstained out-of-scope / all gate-abstained goals WITH a resolver mechanism. Goals the
  resolver cannot resolve carry no candidate mechanism and are a coverage failure, not a signal-driven abstention; they are
  reported via coverage and unresolved_applicable and excluded from unknown_precision. Justification: the mandate attributes the
  abstention decision to the resolver's OWN ambiguity signal, so precision must be measured on signal-driven abstentions.
- unknown_precision_inclusive (SECONDARY, parent-faithful) = abstained out-of-scope / all abstained.
- selective_acc = executed applicable with mechanism id == target / executed applicable.
- det_acc / emb_acc = per-applicable selection correctness (abstention counts incorrect) over the whole axis.

## 9. Decision rules

- D-PRIMARY (claim-bearing): GATE-MET iff test pooled_false_accept <= 0.1 AND unknown_precision >= 0.85 AND
  coverage >= 0.5; else GATE-NOT-MET; GATE-INVALID if the calibration split lacks a class. Primary metric
  M-GATE-TRIPLET-PRIMARY.
- D-ALTLEX / D-HELDOUT (retention; secondary): RETAINED iff the paired family-blocked 95% bootstrap (B=10000, seed 3820973221)
  of (det correct - emb correct) over test applicable goals has lower bound > 0; LOST iff upper bound <= 0; else MIXED;
  BLOCKED if the embedding stack cannot load.
- Overall: status COMPLETE with outcome = D-PRIMARY for the model-free axis; retention recorded independently and never
  collapsed into D-PRIMARY. Precedence: MEASUREMENT_INVALID > LOST > MIXED > GATE-INVALID > GATE-NOT-MET > GATE-MET.

Product consequence positive: if D-PRIMARY = GATE-MET and both retention checks are RETAINED, resolve() ships as a
deterministic resolver + ambiguity gate with the embedding path retired (cheaper, inspectable, zero model calls).
Product consequence negative: if D-PRIMARY = GATE-NOT-MET, no safe model-free gate exists at this operating point and
unseen-goal resolution must move to a structured slot/parameter or retrieval-model architecture; if retention is LOST, the
deterministic advantage does not generalize beyond the original bank/lexicon and must not be cited as general.

## 10. Frozen runner source

<!-- BEGIN FROZEN-RUNNER -->
#!/usr/bin/env python3
# FROZEN RUNNER for EXP-GRAPH-38180711589 (design_contract_version 2).
# Model-free primary; embedding arm optional (secondary retention checks).
# Usage: python runner_frozen.py [--mechanics-only]
from __future__ import annotations
import argparse, hashlib, json, math, re, sys, platform
from pathlib import Path

ROOT = Path("/home/runner/work/Spider/Spider")
EXP_ID = "EXP-GRAPH-38180711589"
EXP_DIR = ROOT / "research/experiments" / EXP_ID
PREREG = EXP_DIR / "prereg.md"
PARENT_PREREG = ROOT / "research/experiments" / "EXP-GRAPH-38175554380" / "prereg.md"
FREEZE_PATH = EXP_DIR / "freeze.json"
RESULT_PATH = EXP_DIR / "result.json"
REPORT_PATH = EXP_DIR / "report.md"
PROV_PATH = EXP_DIR / "provenance.json"

SEED = 38180711589 % (2 ** 32)
N_BOOT = 10000
ALPHA = 0.05
FA_TARGET = 0.10
COV_TARGET = 0.50
PREC_TARGET = 0.85
TOK_BAND = 0.60
TRI_BAND = 0.75
MAX_FLAGGED = 20

FAMILIES_G1 = ["users", "posts", "comments", "albums", "photos"]
FAMILIES_G2 = ["teams", "projects", "events", "tickets", "files"]
OPS = ["CREATE", "READ", "UPDATE", "DELETE"]
DET = {"a","an","the","this","that","these","those","one","two","my","your","his","her","its","our","their","each","every","any","some","all","no","another","other"}
REF = {"id","identifier","identified","number","numbered","named","called","titled","referred","labelled","labeled"}
QUANT = {"all","every","each","any","some","several","many","both","whole","entire","multiple","batch","bulk"}

# ------------------------------------------------------------------ helpers
def sha_file(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def canon_sha(obj) -> str:
    return hashlib.sha256(json.dumps(obj, sort_keys=True, separators=(",", ":")).encode()).hexdigest()

def extract_block(text: str, name: str) -> str:
    m = re.search(r"<!-- BEGIN " + re.escape(name) + r" -->\n(.*?)\n<!-- END " + re.escape(name) + r" -->", text, re.S)
    if not m:
        raise SystemExit(f"missing block {name}")
    return m.group(1)

def jlines(block: str):
    return [json.loads(l) for l in block.splitlines() if l.strip()]

def tokens(s: str):
    return re.findall(r"[a-z]+", s.lower())

def _spans(t, phrase, plural=False):
    pt = phrase.split(); L = len(pt); res = []
    for i in range(len(t) - L + 1):
        ok = True
        for k, p in enumerate(pt):
            x = t[i + k]
            if x == p:
                continue
            if plural and (x == p + "s" or x + "s" == p):
                continue
            ok = False; break
        if ok:
            res.append((i, i + L, L))
    return res

def jaccard(a, b):
    A, B = set(a), set(b)
    return len(A & B) / len(A | B) if (A | B) else 0.0

def trigrams(s):
    x = " " + " ".join(tokens(s)) + " "
    return {x[i:i+3] for i in range(len(x) - 2)}

# ------------------------------------------------------------------ resolver
def comp(text: str, lex: dict):
    """B-LEX-STRONG key-set longest resolver with noun-homograph disambiguation.
    Returns dict(mech, famNONE, famTIE, opNONE, opTIE, dis, noslot, quant)."""
    t = tokens(text)
    fam_tokens = {p.split()[0] for ph in lex["family_nouns"].values() for p in ph}
    fsp = [(f, s, e, L) for f, ph in lex["family_nouns"].items() for p in ph for (s, e, L) in _spans(t, p, plural=True)]
    osp = [(o, s, e, L) for o, ph in lex["op_synonyms"].items() for p in ph for (s, e, L) in _spans(t, p)
           if not (t[s] in fam_tokens and s > 0 and t[s - 1] in DET)]
    fmax = max([L for _, _, _, L in fsp], default=0)
    omax = max([L for _, _, _, L in osp], default=0)
    fkm = {f for f, _, _, L in fsp if L == fmax}
    okm = {o for o, _, _, L in osp if L == omax}
    fst = "NONE" if not fsp else ("UNIQUE" if len(fkm) == 1 else "TIE")
    ost = "NONE" if not osp else ("UNIQUE" if len(okm) == 1 else "TIE")
    fam = list(fkm)[0] if fst == "UNIQUE" else None
    op = list(okm)[0] if ost == "UNIQUE" else None
    r1 = None
    if fam:
        s0 = min(s for f, s, _, _ in fsp if f == fam); e0 = max(e for f, _, e, _ in fsp if f == fam)
        rem = t[:s0] + t[e0:]
        ors = [(o, s, e, L) for o, ph in lex["op_synonyms"].items() for p in ph for (s, e, L) in _spans(rem, p)
               if not (rem[s] in fam_tokens and s > 0 and rem[s - 1] in DET)]
        om = max([L for _, _, _, L in ors], default=0); okm2 = {o for o, _, _, L in ors if L == om}
        if len(okm2) == 1:
            r1 = (fam, list(okm2)[0])
    r2 = None
    if op:
        s0 = min(s for o, s, _, _ in osp if o == op); e0 = max(e for o, _, e, _ in osp if o == op)
        rem = t[:s0] + t[e0:]
        frs = [(f, s, e, L) for f, ph in lex["family_nouns"].items() for p in ph for (s, e, L) in _spans(rem, p, plural=True)]
        fm = max([L for _, _, _, L in frs], default=0); fkm2 = {f for f, _, _, L in frs if L == fm}
        if len(fkm2) == 1:
            r2 = (list(fkm2)[0], op)
    res = (r1 if r1 == r2 else None) if (r1 and r2) else (r1 or r2)
    dis = 1 if (r1 and r2 and r1 != r2) else 0
    hasref = any(w in REF for w in t)
    noslot = 1 if (res is not None and res[1] in ("READ", "UPDATE", "DELETE") and not hasref) else 0
    q = 1 if any(w in QUANT for w in t) else 0
    return dict(mech=None if res is None else f"mech_{res[0]}_{res[1].lower()}",
                famNONE=int(fst == "NONE"), famTIE=int(fst == "TIE"), opNONE=int(ost == "NONE"),
                opTIE=int(ost == "TIE"), dis=dis, noslot=noslot, quant=q)

W = {"famNONE": 1, "opNONE": 1, "opTIE": 1, "noslot": 1, "quant": 1}
def S(r): return sum(w * r[k] for k, w in W.items())

# ------------------------------------------------------------------ fingerprint / gate
def target_of(goal): return f"mech_{goal['family']}_{goal['op'].lower()}"

def build_axis(app, oos, lex, splitmod, prior_texts):
    rows = []
    for i, g in enumerate(app):
        rows.append(dict(gid=f"app_{i+1:03d}", text=g["text"], app=1, target=target_of(g),
                         split=(i % splitmod) in (1, 3, 5)))
    for i, g in enumerate(oos):
        rows.append(dict(gid=f"oos_{i+1:03d}", text=g["text"], app=0, target=None,
                         split=(i % splitmod) in (1, 3, 5)))
    flagged = []
    for r in rows:
        r.update(comp(r["text"], lex))
        if max(jaccard(tokens(r["text"]), tokens(p)) for p in prior_texts) >= TOK_BAND or \
           max(jaccard(trigrams(r["text"]), trigrams(p)) for p in prior_texts) >= TRI_BAND:
            flagged.append(r["gid"])
    bound = [r for r in rows if r["gid"] not in flagged]
    return bound, flagged

def metrics(rows, t):
    ex = [r for r in rows if r["mech"] is not None and S(r) <= t]
    exo = sum(1 for r in ex if not r["app"]); exa = sum(1 for r in ex if r["app"])
    co = sum(1 for r in rows if not r["app"]); ca = sum(1 for r in rows if r["app"])
    abR = [r for r in rows if r["mech"] is not None and S(r) > t]
    abRo = sum(1 for r in abR if not r["app"])
    unres_app = sum(1 for r in rows if r["app"] and r["mech"] is None)
    ab_all = [r for r in rows if not (r["mech"] is not None and S(r) <= t)]
    fa = exo / co if co else None
    cov = exa / ca if ca else None
    precR = abRo / len(abR) if abR else None
    precI = (sum(1 for r in ab_all if not r["app"]) / len(ab_all)) if ab_all else None
    sel_ex = sum(1 for r in ex if r["app"] and r["mech"] == r["target"])
    return dict(t=t, coverage=cov, pooled_false_accept=fa, unknown_precision=precR,
                unknown_precision_inclusive=precI, abstained_resolved=len(abR),
                executed=len(ex), executed_oos=exo, executed_app=exa,
                selective_acc=(sel_ex / exa) if exa else None,
                unresolved_applicable=unres_app)

def calibrate(cal):
    co = [r for r in cal if not r["app"]]; ca = [r for r in cal if r["app"]]
    if not co or not ca:
        return None, "GATE-INVALID"
    cands = sorted({S(r) for r in cal})
    feas = [t for t in cands if (lambda m: m["pooled_false_accept"] is not None and m["pooled_false_accept"] <= FA_TARGET
                                 and m["unknown_precision"] is not None and m["unknown_precision"] >= PREC_TARGET)(metrics(cal, t))]
    if feas:
        return min(feas), "CAL-FEASIBLE"
    # predeclared fallback: min |cal_fa-0.10| subject to cal_precR>=0.85, else abstain-all
    sub = [(abs(metrics(cal, t)["pooled_false_accept"] - FA_TARGET), t) for t in cands
           if metrics(cal, t)["pooled_false_accept"] is not None and metrics(cal, t)["unknown_precision"] is not None
           and metrics(cal, t)["unknown_precision"] >= PREC_TARGET]
    if sub:
        return min(sub)[1], "CAL-FALLBACK"
    return max(cands) + 1, "CAL-ABSTAIN-ALL"

def selection_acc(rows):
    ca = [r for r in rows if r["app"]]
    return (sum(1 for r in ca if r["mech"] == r["target"]) / len(ca)) if ca else None

# ------------------------------------------------------------------ bootstrap
def paired_family_bootstrap(diff_by_family, seed):
    """diff_by_family: {family: [paired diffs]}; percentile CI."""
    try:
        import numpy as np
    except Exception:
        return None
    np.random.seed(seed)
    fams = sorted(diff_by_family)
    boots = []
    for _ in range(N_BOOT):
        vals = []
        for fam in fams:
            arr = diff_by_family[fam]
            idx = np.random.randint(0, len(arr), len(arr))
            vals.extend([arr[i] for i in idx])
        boots.append(float(np.mean(vals)) if vals else float("nan"))
    boots = np.array([b for b in boots if not math.isnan(b)])
    if boots.size == 0:
        return None
    return dict(obs=float(np.mean([v for vs in diff_by_family.values() for v in vs])),
                lower=float(np.percentile(boots, 100 * ALPHA / 2)),
                upper=float(np.percentile(boots, 100 * (1 - ALPHA / 2))),
                n_resamples=int(boots.size), alpha=ALPHA, n_families=len(fams), seed=seed)

# ------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--mechanics-only", action="store_true")
    args = ap.parse_args()
    prereg_text = PREREG.read_text(encoding="utf-8")
    g1_app = jlines(extract_block(prereg_text, "GOAL-BANK-G1"))
    g1_oos = jlines(extract_block(prereg_text, "OOS-BANK-G1"))
    lex_g1 = json.loads(extract_block(prereg_text, "LEXICON-G1"))
    g2_app = jlines(extract_block(prereg_text, "GOAL-BANK-G2"))
    g2_oos = jlines(extract_block(prereg_text, "OOS-BANK-G2"))
    lex_ho = json.loads(extract_block(prereg_text, "LEXICON-G2-HELDOUT"))
    lex_alt = json.loads(extract_block(prereg_text, "LEXICON-G1-ALT"))
    g2_intents = jlines(extract_block(prereg_text, "G2-HELDOUT-INTENTS"))
    parent_text = PARENT_PREREG.read_text(encoding="utf-8")
    prior_parent = json.loads(extract_block(parent_text, "PRIOR-PARENT-BANK-TEXTS")) if "PRIOR-PARENT-BANK-TEXTS" in parent_text else []

    sys.path.insert(0, str(ROOT / "research/harness"))
    from goal_generator import INTENTS, PARAPHRASES, NO_APPLICABLE_TEMPLATES, OOD_PARAPHRASES
    gg = list(INTENTS.values()) + [v for vs in PARAPHRASES.values() for v in vs] + \
         list(NO_APPLICABLE_TEMPLATES) + list(OOD_PARAPHRASES)
    prior_full = gg + list(prior_parent)

    axes = {}
    for nm, (app, oos, lex, sm, priors) in {
        "AXIS-PRIMARY": (g1_app, g1_oos, lex_g1, 6, prior_full),
        "AXIS-ALTLEX": (g1_app, g1_oos, lex_alt, 6, prior_full),
        "AXIS-HELDOUT": (g2_app, g2_oos, lex_ho, 4, gg + [g["text"] for g in g1_app] + [g["text"] for g in g1_oos]),
    }.items():
        bound, flagged = build_axis(app, oos, lex, sm, priors)
        cal = [r for r in bound if not r["split"]]; test = [r for r in bound if r["split"]]
        tstar, cls = calibrate(cal)
        cal_m = metrics(cal, tstar)
        axes[nm] = dict(bound=len(bound), flagged=flagged, cal=cal, test=test, tstar=tstar,
                        cal_class=cls, cal_metrics=cal_m,
                        det_acc_cal=selection_acc(cal), det_acc_test=selection_acc(test))

    # ---- primary decision
    p = axes["AXIS-PRIMARY"]
    test_m = metrics(p["test"], p["tstar"]) if not args.mechanics_only else None
    gate_out = ("GATE-INVALID" if p["cal_class"] == "GATE-INVALID" else
                "GATE-MET" if (test_m is not None and test_m["pooled_false_accept"] is not None and test_m["pooled_false_accept"] <= FA_TARGET
                               and test_m["unknown_precision"] is not None and test_m["unknown_precision"] >= PREC_TARGET
                               and test_m["coverage"] is not None and test_m["coverage"] >= COV_TARGET)
                else "GATE-NOT-MET")
    if args.mechanics_only:
        print(json.dumps(dict(status="DESIGN-MECHANICS-ONLY",
                              axes={k: dict(bound=v["bound"], flagged=v["flagged"], tstar=v["tstar"],
                                            cal_class=v["cal_class"], cal_metrics=v["cal_metrics"])
                                    for k, v in axes.items()}), indent=2))
        return
    # boundary / matched-coverage controls on PRIMARY test
    def boundary(name, t, rows):
        return {name: metrics(rows, t)}
    ctrl = {}
    maxS = max(S(r) for r in p["cal"] + p["test"])
    ctrl.update(boundary("CTRL-EXEC-ALL", maxS + 1, p["test"]))
    ctrl.update(boundary("CTRL-ABSTAIN-ALL", -1, p["test"]))
    # matched-coverage random gate: abstain same count as treatment, randomly, seed fixed
    treated = metrics(p["test"], p["tstar"])
    import random
    rng = random.Random(SEED)
    idx = list(range(len(p["test"]))); rng.shuffle(idx)
    ab_n = sum(1 for r in p["test"] if not (r["mech"] is not None and S(r) <= p["tstar"]))
    abset = set(idx[:ab_n])
    ab_rows = [r for i, r in enumerate(p["test"]) if i in abset]
    ex_rows = [r for i, r in enumerate(p["test"]) if i not in abset]
    ctrl["CTRL-RANDOM-GATE"] = dict(
        pooled_false_accept=(sum(1 for r in ex_rows if not r["app"]) / sum(1 for r in p["test"] if not r["app"])) if any(not r["app"] for r in p["test"]) else None,
        unknown_precision=(sum(1 for r in ab_rows if not r["app"]) / len(ab_rows)) if ab_rows else None,
        matched_abstention_count=ab_n)

    # ---- retention arms (embedding comparator; optional)
    retention = {}
    embedding_status = "NOT_ATTEMPTED"
    try:
        import numpy as np  # noqa
        from sentence_transformers import SentenceTransformer
        from candidate_resolver import EmbeddingArgmaxResolver, create_fixture
        from types import SimpleNamespace
        model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
        g1_mechs = create_fixture()
        g1_embed = EmbeddingArgmaxResolver(g1_mechs, model)
        ho_mechs = [SimpleNamespace(mechanism_id=f"mech_{d['family']}_{d['op'].lower()}", intent=d["intent"]) for d in g2_intents]
        ho_embed = EmbeddingArgmaxResolver(ho_mechs, model)
        for nm, embed in (("AXIS-ALTLEX", g1_embed), ("AXIS-HELDOUT", ho_embed)):
            rows = axes[nm]["test"]
            diffs = {}
            cor = {"det": 0, "emb": 0, "n": 0}
            for r in rows:
                if not r["app"]:
                    continue
                emb = embed.resolve({"text": r["text"], "goal_id": r["gid"]})
                d = 1 if (r["mech"] == r["target"]) else 0
                e = 1 if (emb.mechanism_id == r["target"]) else 0
                cor["det"] += d; cor["emb"] += e; cor["n"] += 1
                fam = r["target"].split("_")[1]
                diffs.setdefault(fam, []).append(d - e)
            boot = paired_family_bootstrap(diffs, SEED)
            retention[nm] = dict(det_correct=cor["det"], emb_correct=cor["emb"], n=cor["n"],
                                 det_acc=cor["det"] / cor["n"] if cor["n"] else None,
                                 emb_acc=cor["emb"] / cor["n"] if cor["n"] else None, paired_diff=boot)
        embedding_status = "OK"
    except Exception as exc:  # noqa
        embedding_status = f"BLOCKED: {type(exc).__name__}: {exc}"

    ret_out = {}
    for nm in ("AXIS-ALTLEX", "AXIS-HELDOUT"):
        r = retention.get(nm)
        if r and r["paired_diff"]:
            ret_out[nm] = "RETAINED" if r["paired_diff"]["lower"] > 0 else ("LOST" if r["paired_diff"]["upper"] <= 0 else "MIXED")
        else:
            ret_out[nm] = "BLOCKED"

    out = dict(schema_version=1, experiment_id=EXP_ID, lane="graph",
               status="DESIGN-MECHANICS-ONLY" if args.mechanics_only else "COMPLETE",
               outcome={"D-PRIMARY": gate_out, "D-HELDOUT": ret_out["AXIS-HELDOUT"], "D-ALTLEX": ret_out["AXIS-ALTLEX"]},
               primary=dict(tstar=p["tstar"], cal_class=p["cal_class"], cal_metrics=p["cal_metrics"], test_metrics=test_m),
               controls=ctrl,
               axes={k: dict(bound=v["bound"], flagged=v["flagged"], tstar=v["tstar"], cal_class=v["cal_class"],
                             cal_metrics=v["cal_metrics"], det_acc_cal=v["det_acc_cal"], det_acc_test=v["det_acc_test"],
                             test_metrics=metrics(v["test"], v["tstar"]))
                     for k, v in axes.items()},
               retention=retention, embedding_status=embedding_status)
    print(json.dumps(out, indent=2))
    if not args.mechanics_only:
        RESULT_PATH.write_text(json.dumps(out, indent=2) + "\n")

if __name__ == "__main__":
    main()

<!-- END FROZEN-RUNNER -->

Runner sha256 = 5811a49524a012ba25483d61f78a0d696ccc82f0971386507217c0d9e2c9d6e5.

## 11. CANONICAL-HASHES

<!-- BEGIN CANONICAL-HASHES -->
{
  "G2-HELDOUT-INTENTS": "97c1225d261f69bbdab0b96cee8425755e8c763594d82c73ea08b00ea38a829d",
  "GOAL-BANK-G1": "fc9dfba5bdf17cfb09f7be8183969b7d5eb009f4c96eed7f2f05daad31bd50be",
  "GOAL-BANK-G2": "f4ed50e48c97d651d94e3f8bfdb3831dfa99ceb76fe50b066bcfb2fa343cd4a8",
  "LEXICON-G1": "6baa3ba8258451fdce17028ed5312c7e1f663c69e22c01abbba55645ce179e4e",
  "LEXICON-G1-ALT": "c28992a99076293b932b0bdc285f1974e4182d663ba426465beaf451fb86246e",
  "LEXICON-G2-HELDOUT": "145aa845e0caa6bce7f8410038551a32e0322862b16c8f55bc7af3f986ca811b",
  "OOS-BANK-G1": "d181cb01ed63ad4b59b3f23230206b7c564eac9e203dfe1c76f27901bf96875f",
  "OOS-BANK-G2": "5af8117d531801008b4981741824820726b2aefb792163de3eb16cb9853bdb86"
}
<!-- END CANONICAL-HASHES -->
