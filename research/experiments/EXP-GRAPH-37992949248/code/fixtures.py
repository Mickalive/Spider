"""Frozen instrument fixtures for EXP-GRAPH-37992949248 (adapted from
EXP-GRAPH-37978902447; extraction/guard fixture semantics unchanged per SB-06,
plus the NEW estimator capability fixtures introduced by this packet).

SYNTHETIC BYTES PERMITTED ONLY FOR INSTRUMENT SELF-TEST (V08/CC-J).  Fixtures
are unit tests only, are never part of the scored population, and no claim
depends on them.  They constrain the extraction paths, the guard's firing
logic and the anchor-clustered estimator.

Extraction fixtures (bytes):
- SYN-CANARY-BOTH : positive instrument fixture. Non-GET form with an in-list
  hidden input carrying a literal value, plus an in-list meta token with
  content. Both paths must recover exactly the same 2 (name, value) pairs.
- SYN-EMPTY-VALUE : empty-value instrument fixture. In-list hidden input with no
  value attribute and in-list meta token with empty content. Both paths must
  classify PRESENT-EMPTY and agree.
- SYN-JSSTRING : representation-loss instrument fixture. An in-list token name
  appearing only inside a JavaScript string literal. Both paths must recover 0
  non-empty values.

Guard-logic fixtures (abstract channel-fire patterns, not bytes):
- SYN-GUARD-D1V     : byte-identical structure/transport, rotated value.
                      incumbent must REUSE; value-aware must ABSTAIN.
- SYN-GUARD-FRESH   : identical value and structure. both must REUSE.
- SYN-GUARD-POSTCOND: same value but a changed in-list field-name set.
                      CH-POSTCOND-SEM must fire and incumbent must ABSTAIN.

Estimator capability fixtures (NEW; synthetic pseudo-anchor D1V trial lists,
never scored; CC-J):
- SYN-ESTIMATOR-2ANCHOR      : 2 pseudo-anchors with heterogeneous per-anchor
                               paired false-accept differences 1/2 and 1/3,
                               both strictly inside (0,1). The shared
                               anchor-clustered bootstrap MUST return
                               LOW=1/3 > 0, UB97=1/2 < 1 and LOW < UB97.
- SYN-ESTIMATOR-1ANCHOR      : 1 pseudo-anchor. The bootstrap MUST return the
                               degenerate/null bound (LOW=null, UB97=null).
- SYN-ESTIMATOR-HOMOGENEOUS  : 2 pseudo-anchors with identical paired
                               differences 1/2. The bootstrap MUST return a
                               zero-width interval (LOW == UB97 == 1/2).
"""
from __future__ import annotations

SYN_CANARY_BOTH = (
    b"<!DOCTYPE html><html><head>"
    b'<meta name="csrf-token" content="fixture-meta-canary-91bd"/>'
    b"</head><body>"
    b'<form method="post" action="https://example.invalid/submit">'
    b'<input type="hidden" name="authenticity_token" value="fixture-canary-value-7f3a"/>'
    b"</form></body></html>"
)

SYN_EMPTY_VALUE = (
    b"<!DOCTYPE html><html><head>"
    b'<meta name="csrf-token" content=""/>'
    b"</head><body>"
    b'<form method="post" action="https://example.invalid/x">'
    b'<input type="hidden" name="authenticity_token"/>'
    b"</form></body></html>"
)

SYN_JSSTRING = (
    b"<!DOCTYPE html><html><body>"
    b"<script>"
    b'var t = "authenticity_token"; var o = {"csrf_token": "rendered-later"};'
    b"</script>"
    b'<form method="post" action="https://example.invalid/y"></form>'
    b"</body></html>"
)

FIXTURES = {
    "SYN-CANARY-BOTH": SYN_CANARY_BOTH,
    "SYN-EMPTY-VALUE": SYN_EMPTY_VALUE,
    "SYN-JSSTRING": SYN_JSSTRING,
}

# Guard-logic fixtures: channel-fire patterns plus the pre-declared decisions.
# A channel "fires" when its activation input differs between recorded and
# current.  CH-PRECOND-BINDING fires exactly when the exact value rotated.
GUARD_FIXTURES = {
    "SYN-GUARD-D1V": {
        "fired": {
            "CH-STRUCT-SIG": False,
            "CH-TRANSPORT-VALIDATOR": False,
            "CH-POSTCOND-SEM": False,
            "CH-PRECOND-BINDING": True,
        },
        "expected": {
            "B-INCUMBENT-SIGNAL-ONLY": "REUSE",
            "B-VALUE-AWARE": "ABSTAIN",
            "B-FULL-GUARD": "ABSTAIN",
        },
    },
    "SYN-GUARD-FRESH": {
        "fired": {
            "CH-STRUCT-SIG": False,
            "CH-TRANSPORT-VALIDATOR": False,
            "CH-POSTCOND-SEM": False,
            "CH-PRECOND-BINDING": False,
        },
        "expected": {
            "B-INCUMBENT-SIGNAL-ONLY": "REUSE",
            "B-VALUE-AWARE": "REUSE",
            "B-FULL-GUARD": "REUSE",
        },
    },
    "SYN-GUARD-POSTCOND": {
        "fired": {
            "CH-STRUCT-SIG": False,
            "CH-TRANSPORT-VALIDATOR": False,
            "CH-POSTCOND-SEM": True,
            "CH-PRECOND-BINDING": False,
        },
        "expected": {
            "B-INCUMBENT-SIGNAL-ONLY": "ABSTAIN",
            "B-VALUE-AWARE": "REUSE",
            "B-FULL-GUARD": "ABSTAIN",
        },
    },
}


# ---------------------------------------------------------------------------
# Estimator capability fixtures (NEW; synthetic pseudo-anchor trial lists).
# Each trial dict carries only the keys the shared bootstrap reads:
# anchor_id + the two guard decisions.  INSTRUMENT UNIT TEST ONLY (CC-J):
# these pseudo-anchors ("EA-*") are NEVER part of the scored population and
# their numbers must never be reported as a measure of real anchors.
# ---------------------------------------------------------------------------
def _d1v_trial(anchor_id, incumbent_reuse, valueaware_reuse):
    return {
        "anchor_id": anchor_id,
        "B-INCUMBENT-SIGNAL-ONLY": "REUSE" if incumbent_reuse else "ABSTAIN",
        "B-VALUE-AWARE": "REUSE" if valueaware_reuse else "ABSTAIN",
    }


def estimator_trials_2anchor_heterogeneous():
    """SYN-ESTIMATOR-2ANCHOR: per-anchor paired differences {1/2, 1/3}.

    EA-1: 2 D1V trials, incumbent false-accepts 1/2, value-aware 0/2
          -> diff 1/2 (strictly inside (0,1)).
    EA-2: 3 D1V trials, incumbent false-accepts 1/3, value-aware 0/3
          -> diff 1/3 (strictly inside (0,1), heterogeneous vs EA-1).
    Pre-freeze reference arithmetic (B=10000, pooled-cluster pooling):
    LOW = 1/3, UB97 = 1/2, width = 1/6 > 0.
    """
    trials = [
        _d1v_trial("EA-1", True, False),
        _d1v_trial("EA-1", False, False),
        _d1v_trial("EA-2", True, False),
        _d1v_trial("EA-2", False, False),
        _d1v_trial("EA-2", False, False),
    ]
    return trials


def estimator_trials_1anchor():
    """SYN-ESTIMATOR-1ANCHOR: single pseudo-anchor (1 D1V trial, incumbent
    REUSE, value-aware ABSTAIN). Bootstrap MUST return LOW=null, UB97=null."""
    return [_d1v_trial("EA-SINGLE", True, False)]


def estimator_trials_homogeneous():
    """SYN-ESTIMATOR-HOMOGENEOUS: 2 pseudo-anchors with IDENTICAL paired
    differences (both 1/2: each anchor has 2 D1V trials, incumbent
    false-accepts 1/2, value-aware 0/2). Bootstrap MUST return a ZERO-WIDTH
    interval (LOW == UB97 == 1/2), proving interval width tracks
    between-anchor heterogeneity rather than being manufactured."""
    trials = [
        _d1v_trial("EA-H1", True, False),
        _d1v_trial("EA-H1", False, False),
        _d1v_trial("EA-H2", True, False),
        _d1v_trial("EA-H2", False, False),
    ]
    return trials


ESTIMATOR_FIXTURES = {
    "SYN-ESTIMATOR-2ANCHOR": estimator_trials_2anchor_heterogeneous,
    "SYN-ESTIMATOR-1ANCHOR": estimator_trials_1anchor,
    "SYN-ESTIMATOR-HOMOGENEOUS": estimator_trials_homogeneous,
}
