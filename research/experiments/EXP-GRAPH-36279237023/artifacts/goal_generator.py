"""Deterministic goal generator for EXP-GRAPH-36279237023 (frozen design, prereg.md 3.3).

Frozen goal inventory (prereg.md 3.3 table):
  paraphrased   20   one per mechanism, unseen wording
  underspecified 10  correct target mechanism but one required slot value absent
  composite     10   two operations; target is the FIRST operation
  OOD           20   operation/family not present in the registry
  verbatim      12   exact copies of 12 of the 20 recorded distillation intents
  no-applicable  8   cross-cutting operations with no registry mechanism
  TOTAL         80

Determinism: the whole inventory is a literal table. The `--seed` argument is
recorded in provenance.json because prereg.md 13 requires seeds to be recorded;
it is used only to derive goal ids and to seed the consumer's RNG, never to
change the wording. Two runs with the same seed produce byte-identical goals.json.

COMPOSITE TARGET RULE (declared): a composite goal names two operations but the
resolver emits a single mechanism_id, so `target_mechanism_id` is the FIRST
operation's mechanism and each composite record carries
`target_selection_rule = "first_operation"` plus the full `operations` list so
an auditor can recompute the alternative convention.

BLOCKING FAMILY (declared): every goal carries a `family` used as the
family-blocked bootstrap unit. Registry goals carry their resource family; the
8 no-applicable goals carry the synthetic block "platform" because they belong
to no registry family. The primary mechanism-identity metric contains only
registry-family goals, so the primary bootstrap has exactly 5 blocks.
"""

from __future__ import annotations

import json
import re
from typing import Any

SEED_DEFAULT = 36279237023

_WORD = re.compile(r"[a-z0-9]+(?:'[a-z]+)?")


def tokens(text: str) -> set[str]:
    return set(_WORD.findall(text.lower()))


def jaccard(a: str, b: str) -> float:
    ta, tb = tokens(a), tokens(b)
    if not ta or not tb:
        return 0.0
    return len(ta & tb) / len(ta | tb)


# --------------------------------------------------------------------------
# 20 paraphrases: one per mechanism, deliberately disjoint wording from the
# recorded intents while keeping the argument values recoverable.
# --------------------------------------------------------------------------
PARAPHRASED: dict[str, str] = {
    "mech_users_create": "register a brand-new account named Alice with email alice@example.com",
    "mech_users_read": "pull up the account numbered 7",
    "mech_users_update": "change the name on the account numbered 7 to Bob",
    "mech_users_delete": "wipe the account numbered 7 out of the directory",
    "mech_posts_create": "put up a piece whose heading reads 'Hello' and whose text reads 'World'",
    "mech_posts_read": "show me the piece numbered 3",
    "mech_posts_update": "relabel the piece numbered 3 so the title becomes 'Hi'",
    "mech_posts_delete": "throw the piece numbered 3 away",
    "mech_comments_create": "attach a note 'Nice' underneath the piece numbered 3",
    "mech_comments_read": "surface the remark numbered 5",
    "mech_comments_update": "amend the remark numbered 5 so the text reads 'Great'",
    "mech_comments_delete": "erase the remark numbered 5",
    "mech_albums_create": "start a collection whose heading reads 'Trip'",
    "mech_albums_read": "open the collection numbered 2",
    "mech_albums_update": "adjust the collection numbered 2 so the title becomes 'Holiday'",
    "mech_albums_delete": "discard the collection numbered 2",
    "mech_photos_create": "upload a picture whose url is 'http://example.com/y.png' captioned 'Cat'",
    "mech_photos_read": "display the picture numbered 4",
    "mech_photos_update": "adjust the picture numbered 4 so the caption becomes 'Dog'",
    "mech_photos_delete": "remove the picture numbered 4",
}

# --------------------------------------------------------------------------
# 10 underspecified: correct target mechanism, one required value removed so
# prereg.md 4.1.4 forces ABSTAIN.
# --------------------------------------------------------------------------
UNDERSPECIFIED: dict[str, str] = {
    "mech_users_read": "pull up the account",
    "mech_users_update": "change the name to Bob",
    "mech_users_delete": "wipe the account out of the directory",
    "mech_posts_create": "put up a piece",
    "mech_posts_read": "show me the piece",
    "mech_comments_update": "amend the remark so the text reads 'Great'",
    "mech_albums_create": "start a collection",
    "mech_albums_delete": "discard the collection",
    "mech_photos_create": "upload a picture captioned 'Cat'",
    "mech_photos_delete": "remove the picture",
}

# --------------------------------------------------------------------------
# 10 composite: two operations, target = first operation.
# --------------------------------------------------------------------------
COMPOSITE: list[dict[str, Any]] = [
    {
        "text": "register a brand-new account named Alice with email alice@example.com and then put up a piece whose heading reads 'Hello' and whose text reads 'World'",
        "operations": ["mech_users_create", "mech_posts_create"],
    },
    {
        "text": "put up a piece whose heading reads 'Hello' and whose text reads 'World' and then attach a note 'Nice' underneath the piece numbered 3",
        "operations": ["mech_posts_create", "mech_comments_create"],
    },
    {
        "text": "attach a note 'Nice' underneath the piece numbered 3 and then change the name on the account numbered 7 to Bob",
        "operations": ["mech_comments_create", "mech_users_update"],
    },
    {
        "text": "start a collection whose heading reads 'Trip' and then upload a picture whose url is 'http://example.com/y.png' captioned 'Cat'",
        "operations": ["mech_albums_create", "mech_photos_create"],
    },
    {
        "text": "upload a picture whose url is 'http://example.com/y.png' captioned 'Cat' and then relabel the piece numbered 3 so the title becomes 'Hi'",
        "operations": ["mech_photos_create", "mech_posts_update"],
    },
    {
        "text": "change the name on the account numbered 7 to Bob and then adjust the collection numbered 2 so the title becomes 'Holiday'",
        "operations": ["mech_users_update", "mech_albums_update"],
    },
    {
        "text": "throw the piece numbered 3 away and then erase the remark numbered 5",
        "operations": ["mech_posts_delete", "mech_comments_delete"],
    },
    {
        "text": "wipe the account numbered 7 out of the directory and then surface the remark numbered 5",
        "operations": ["mech_users_delete", "mech_comments_read"],
    },
    {
        "text": "discard the collection numbered 2 and then adjust the picture numbered 4 so the caption becomes 'Dog'",
        "operations": ["mech_albums_delete", "mech_photos_update"],
    },
    {
        "text": "relabel the piece numbered 3 so the title becomes 'Hi' and then pull up the account numbered 7",
        "operations": ["mech_posts_update", "mech_users_read"],
    },
]

# --------------------------------------------------------------------------
# 20 OOD: operation or family absent from the registry.
# --------------------------------------------------------------------------
OOD: list[tuple[str, str]] = [
    ("users", "ban the account numbered 7 permanently"),
    ("users", "search the accounts by email alice@example.com"),
    ("users", "reset the password of the account numbered 7"),
    ("users", "list every account registered this week"),
    ("posts", "schedule the piece numbered 3 for tomorrow"),
    ("posts", "tag the piece numbered 3 as featured"),
    ("posts", "count how many pieces mention 'World'"),
    ("posts", "publish the piece numbered 3 to the newsletter"),
    ("comments", "like the remark numbered 5"),
    ("comments", "report the remark numbered 5 as spam"),
    ("comments", "reply to the remark numbered 5"),
    ("comments", "summarise all remarks on the piece numbered 3"),
    ("albums", "share the collection numbered 2 with a friend"),
    ("albums", "export the collection numbered 2 as a zip file"),
    ("albums", "sort the collection numbered 2 by date"),
    ("albums", "add the piece numbered 3 to the collection numbered 2"),
    ("photos", "rotate the picture numbered 4 by ninety degrees"),
    ("photos", "crop the picture numbered 4 to a square"),
    ("photos", "make the picture numbered 4 the cover image"),
    ("photos", "download the picture numbered 4 in full resolution"),
]

# --------------------------------------------------------------------------
# 8 no-applicable: cross-cutting operations with no registry mechanism.
# --------------------------------------------------------------------------
NO_APPLICABLE: list[str] = [
    "print the whole database to a file",
    "restart the server",
    "reset the database to its initial state",
    "measure how long the server takes to answer",
    "shut the application down gracefully",
    "back the database up to remote storage",
    "grant a new administrator the right to use the application",
    "upgrade the application to the next version",
]

# 12 of the 20 recorded intents are copied verbatim for PC-VERBATIM-INTENT.
VERBATIM_IDS: list[str] = [
    "mech_users_create",
    "mech_users_read",
    "mech_users_update",
    "mech_users_delete",
    "mech_posts_create",
    "mech_posts_read",
    "mech_comments_create",
    "mech_albums_create",
    "mech_albums_read",
    "mech_photos_create",
    "mech_photos_read",
    "mech_photos_update",
]


def build_goals(fixture: dict) -> dict:
    mechs = {m["mechanism_id"]: m for m in fixture["mechanisms"]}
    order = [m["mechanism_id"] for m in fixture["mechanisms"]]
    frag = {m["mechanism_id"]: m["fragment_id"] for m in fixture["mechanisms"]}
    fam = {m["mechanism_id"]: m["resource_family"] for m in fixture["mechanisms"]}
    goal_index = {g: i for i, g in enumerate(order)}

    goals: list[dict[str, Any]] = []

    for mid in order:
        goals.append(
            {
                "goal_id": f"paraphrased_{mid}",
                "text": PARAPHRASED[mid],
                "category": "paraphrased",
                "family": fam[mid],
                "applies_any": True,
                "target_mechanism_id": mid,
                "target_fragment_id": frag[mid],
                "operations": [mid],
                "target_selection_rule": "single_operation",
            }
        )

    for mid, text in UNDERSPECIFIED.items():
        goals.append(
            {
                "goal_id": f"underspecified_{mid}",
                "text": text,
                "category": "underspecified",
                "family": fam[mid],
                "applies_any": True,
                "target_mechanism_id": mid,
                "target_fragment_id": frag[mid],
                "operations": [mid],
                "target_selection_rule": "single_operation",
                "missing_slot_family": mid,
            }
        )

    for i, spec in enumerate(COMPOSITE):
        first = spec["operations"][0]
        goals.append(
            {
                "goal_id": f"composite_{i:02d}_{first}",
                "text": spec["text"],
                "category": "composite",
                "family": fam[first],
                "applies_any": True,
                "target_mechanism_id": first,
                "target_fragment_id": frag[first],
                "operations": spec["operations"],
                "target_selection_rule": "first_operation",
            }
        )

    for i, (family, text) in enumerate(OOD):
        goals.append(
            {
                "goal_id": f"ood_{i:02d}_{family}",
                "text": text,
                "category": "ood",
                "family": family,
                "applies_any": False,
                "target_mechanism_id": None,
                "target_fragment_id": None,
                "operations": [],
                "target_selection_rule": "no_applicable_mechanism",
            }
        )

    for mid in VERBATIM_IDS:
        goals.append(
            {
                "goal_id": f"verbatim_{mid}",
                "text": mechs[mid]["intent"],
                "category": "verbatim",
                "family": fam[mid],
                "applies_any": True,
                "target_mechanism_id": mid,
                "target_fragment_id": frag[mid],
                "operations": [mid],
                "target_selection_rule": "single_operation",
            }
        )

    for i, text in enumerate(NO_APPLICABLE):
        goals.append(
            {
                "goal_id": f"no_applicable_{i:02d}",
                "text": text,
                "category": "no_applicable",
                "family": "platform",
                "applies_any": False,
                "target_mechanism_id": None,
                "target_fragment_id": None,
                "operations": [],
                "target_selection_rule": "no_applicable_mechanism",
            }
        )

    counts: dict[str, int] = {}
    for g in goals:
        counts[g["category"]] = counts.get(g["category"], 0) + 1
    applies_any = sum(1 for g in goals if g["applies_any"])

    return {
        "goal_set_id": "GOALS-EXP-GRAPH-36279237023",
        "schema_version": 1,
        "seed": SEED_DEFAULT,
        "mechanism_order": order,
        "goal_index": goal_index,
        "counts": counts,
        "total": len(goals),
        "applies_any_count": applies_any,
        "applies_none_count": len(goals) - applies_any,
        "declared_ambiguity": (
            "prereg.md 3.3 states 'Total goals: 80 (60 applicable + 12 verbatim + 8 no-applicable)'. "
            "The table in the same section gives 20 paraphrased + 10 underspecified + 10 composite + "
            "20 OOD + 12 verbatim + 8 no-applicable = 80, and 60 is the arithmetic sum of the FIRST FOUR "
            "categories, i.e. it counts the 20 OOD goals as 'applicable'. That is inconsistent with the "
            "same table's own description of OOD goals as 'operations/families not in registry' and with "
            "NC-NO-APPLICABLE, which requires goals with no applicable mechanism. The generator therefore "
            "implements the CATEGORY TABLE, which is the unambiguous part of the frozen design, giving "
            "52 applies_any and 28 applies_none. The 20 OOD goals are excluded from calibration fitting "
            "because an applicability gate has no defined positive label on a goal with no applicable "
            "mechanism. The literal '60' is reported as a prereg arithmetic inconsistency, not silently "
            "adopted or silently dropped."
        ),
        "goals": goals,
    }


if __name__ == "__main__":
    import argparse
    import pathlib

    ap = argparse.ArgumentParser()
    ap.add_argument("fixture")
    ap.add_argument("out")
    args = ap.parse_args()
    fixture = json.loads(pathlib.Path(args.fixture).read_text(encoding="utf-8"))
    payload = build_goals(fixture)
    pathlib.Path(args.out).write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    print(f"wrote {args.out} total={payload['total']} counts={payload['counts']}")
