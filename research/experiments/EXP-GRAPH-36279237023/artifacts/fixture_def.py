"""Fixture definition for EXP-GRAPH-36279237023 (frozen design, prereg.md section 3).

Implements prereg.md 3.1/3.2/3.3/V11:
  * 5 resource families x 4 verbs = 20 mechanisms (several mechanisms per family
    across multiple verbs, so a shared-resource-noun choice is NOT the whole task);
  * every mechanism has a NON-EMPTY parameter_slots list;
  * every ${...} placeholder in an action_template is a declared parameter slot
    (no unbindable placeholder remains);
  * the HTTP application exposes 20 endpoints (5 families x 4 verbs).

SPECIFICATION RESOLUTION DECLARED HERE (frozen-packet internal tension, resolved
pre-outcome and reported in result.json.validity_notes):

  prereg.md 4.1.4 says "All slots filled -> EXECUTABLE. Any unfilled -> ABSTAIN."
  prereg.md 4.6 requires PC-VERBATIM-INTENT to reach mechanism-identity accuracy
  = 1.0 on goals that are "exact copies of the distillation intents", and
  prereg.md 6.1 counts an abstention as an incorrect mechanism-identity outcome.

  Those three clauses are jointly unsatisfiable if the recorded distillation
  intents carry no parameter VALUES (a verbatim copy of "create a new user"
  cannot bind name/email, so 4.1.4 forces ABSTAIN, so 4.6 cannot reach 1.0).
  The consistent reading, and the one implemented here, is that a mechanism
  records the FULL natural-language goal it was distilled from, values
  included -- which is what a distillation observation actually contains. Every
  verbatim goal is therefore an exact copy of a value-bearing recorded intent,
  and every mechanism's slots are extractable from its own intent text by the
  generic slot-filler in candidate_resolver.py. No special-case binding path
  exists for verbatim rows.

  The alternative (value-free intents, plus a recorded distillation-time
  default binding consulted only when the goal is a verbatim copy) was rejected
  because it gives the candidate a fixture-supplied shortcut on exactly the rows
  the positive control scores.
"""

from __future__ import annotations

FAMILIES = ["users", "posts", "comments", "albums", "photos"]
VERBS = ["create", "read", "update", "delete"]

# --- per-family content slots used by CREATE / UPDATE -----------------------
# Each entry maps a verb to (list_of_parameter_slots, action_template, intent).
# Slots are given in the order the slot-filler should prefer them.
FAMILY_SPEC: dict[str, dict] = {
    "users": {
        "create": {
            "slots": ["name", "email"],
            "template": {"method": "POST", "path": "/users", "body": {"name": "${name}", "email": "${email}"}},
            "intent": "create a new user named Alice with email alice@example.com",
        },
        "read": {
            "slots": ["user_id"],
            "template": {"method": "GET", "path": "/users/${user_id}"},
            "intent": "retrieve the user with id 7",
        },
        "update": {
            "slots": ["user_id", "name"],
            "template": {"method": "PUT", "path": "/users/${user_id}", "body": {"name": "${name}"}},
            "intent": "update the name of the user with id 7 to Bob",
        },
        "delete": {
            "slots": ["user_id"],
            "template": {"method": "DELETE", "path": "/users/${user_id}"},
            "intent": "delete the user with id 7",
        },
    },
    "posts": {
        "create": {
            "slots": ["title", "body"],
            "template": {"method": "POST", "path": "/posts", "body": {"title": "${title}", "body": "${body}"}},
            "intent": "create a post titled 'Hello' with body 'World'",
        },
        "read": {
            "slots": ["post_id"],
            "template": {"method": "GET", "path": "/posts/${post_id}"},
            "intent": "retrieve the post with id 3",
        },
        "update": {
            "slots": ["post_id", "title"],
            "template": {"method": "PUT", "path": "/posts/${post_id}", "body": {"title": "${title}"}},
            "intent": "update the title of the post with id 3 to 'Hi'",
        },
        "delete": {
            "slots": ["post_id"],
            "template": {"method": "DELETE", "path": "/posts/${post_id}"},
            "intent": "delete the post with id 3",
        },
    },
    "comments": {
        "create": {
            "slots": ["post_id", "text"],
            "template": {"method": "POST", "path": "/comments", "body": {"post_id": "${post_id}", "text": "${text}"}},
            "intent": "create a comment on the post with id 3 saying 'Nice'",
        },
        "read": {
            "slots": ["comment_id"],
            "template": {"method": "GET", "path": "/comments/${comment_id}"},
            "intent": "retrieve the comment with id 5",
        },
        "update": {
            "slots": ["comment_id", "text"],
            "template": {"method": "PUT", "path": "/comments/${comment_id}", "body": {"text": "${text}"}},
            "intent": "update the text of the comment with id 5 to 'Great'",
        },
        "delete": {
            "slots": ["comment_id"],
            "template": {"method": "DELETE", "path": "/comments/${comment_id}"},
            "intent": "delete the comment with id 5",
        },
    },
    "albums": {
        "create": {
            "slots": ["title"],
            "template": {"method": "POST", "path": "/albums", "body": {"title": "${title}"}},
            "intent": "create an album titled 'Trip'",
        },
        "read": {
            "slots": ["album_id"],
            "template": {"method": "GET", "path": "/albums/${album_id}"},
            "intent": "retrieve the album with id 2",
        },
        "update": {
            "slots": ["album_id", "title"],
            "template": {"method": "PUT", "path": "/albums/${album_id}", "body": {"title": "${title}"}},
            "intent": "update the title of the album with id 2 to 'Holiday'",
        },
        "delete": {
            "slots": ["album_id"],
            "template": {"method": "DELETE", "path": "/albums/${album_id}"},
            "intent": "delete the album with id 2",
        },
    },
    "photos": {
        "create": {
            "slots": ["url", "caption"],
            "template": {"method": "POST", "path": "/photos", "body": {"url": "${url}", "caption": "${caption}"}},
            "intent": "create a photo with url 'http://example.com/y.png' captioned 'Cat'",
        },
        "read": {
            "slots": ["photo_id"],
            "template": {"method": "GET", "path": "/photos/${photo_id}"},
            "intent": "retrieve the photo with id 4",
        },
        "update": {
            "slots": ["photo_id", "caption"],
            "template": {"method": "PUT", "path": "/photos/${photo_id}", "body": {"caption": "${caption}"}},
            "intent": "update the caption of the photo with id 4 to 'Dog'",
        },
        "delete": {
            "slots": ["photo_id"],
            "template": {"method": "DELETE", "path": "/photos/${photo_id}"},
            "intent": "delete the photo with id 4",
        },
    },
}

# Confidence stamped on the registry entries handed to the incumbent kernel.
# kernel.py:distill() hardcodes confidence=0.5; the incumbent arm must be given
# the same value so that min_confidence=0.5 is exactly the EXECUTABLE boundary
# (prereg.md 4.2 / inherited_next_question "the value an independent audit probe
# found to be the minimum for EXECUTABLE").
DISTILLED_CONFIDENCE = 0.5


def mechanism_id(family: str, verb: str) -> str:
    return f"mech_{family}_{verb}"


def build_fixture() -> dict:
    mechanisms = []
    for family in FAMILIES:
        for verb in VERBS:
            spec = FAMILY_SPEC[family][verb]
            mechanisms.append(
                {
                    "mechanism_id": mechanism_id(family, verb),
                    "fragment_id": f"frag_{family}_{verb}",
                    "resource_family": family,
                    "verb": verb,
                    "intent": spec["intent"],
                    "parameter_slots": list(spec["slots"]),
                    "action_template": spec["template"],
                    "confidence": DISTILLED_CONFIDENCE,
                }
            )
    return {
        "fixture_id": "FIXTURE-EXP-GRAPH-36279237023",
        "schema_version": 1,
        "families": list(FAMILIES),
        "verbs": list(VERBS),
        "endpoints": sorted(
            f"{m['action_template']['method']} {m['action_template']['path']}" for m in mechanisms
        ),
        "mechanisms": mechanisms,
    }


if __name__ == "__main__":
    import json
    import pathlib
    import sys

    out = pathlib.Path(sys.argv[1]) if len(sys.argv) > 1 else pathlib.Path("fixture.json")
    out.write_text(json.dumps(build_fixture(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"wrote {out}")
