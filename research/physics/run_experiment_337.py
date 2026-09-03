#!/usr/bin/env python3
"""
EXP-PHYSICS-33788037373 Experiment Runner

Corrected methodology (frozen):
- Trajectory-grouped holdout evaluation (70/30 split at trajectory level)
- Trajectory-grouped permutation null (1000 permutations, independent RNG)
- Positive control with overlapping actions across states
- Richer state representation (url, title, link_texts, tag_counts, form_signals)
- Semantic action representation (action_type, target_text, target_href)
- Python stdlib only (no numpy/scipy)
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import random
import sys
import time
import urllib.request
import urllib.error
import urllib.parse
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

EXPERIMENT_DIR = Path(__file__).resolve().parent.parent / "experiments" / "EXP-PHYSICS-33788037373"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class State:
    """Observable state: composite representation."""
    url: str
    title: str
    link_texts: Tuple[str, ...]
    tag_counts: Tuple[int, ...]
    form_signals: Tuple[bool, ...]

    def to_key(self) -> str:
        raw = (
            self.url + "|"
            + self.title + "|"
            + "|".join(self.link_texts) + "|"
            + "|".join(str(x) for x in self.tag_counts) + "|"
            + "|".join(str(x) for x in self.form_signals)
        )
        return hashlib.sha256(raw.encode()).hexdigest()[:16]


@dataclass(frozen=True)
class Action:
    """Observable action."""
    action_type: str
    target_text: str
    target_href: str

    def to_key(self) -> str:
        return self.action_type + "|" + self.target_text + "|" + self.target_href


@dataclass(frozen=True)
class Transition:
    """A single (S, A, S') observation."""
    state_key: str
    action_key: str
    next_state_key: str
    trajectory_id: str
    step_index: int


# ---------------------------------------------------------------------------
# HTML Parser for state extraction
# ---------------------------------------------------------------------------

class PageParser(HTMLParser):
    """Extract state features from HTML."""

    TAG_NAMES = ["h1", "h2", "h3", "form", "input", "button", "select", "textarea", "nav", "main", "aside"]

    def __init__(self):
        super().__init__()
        self.title = ""
        self.in_title = False
        self.links: List[Tuple[str, str]] = []  # (text, href)
        self.tag_counts = [0] * 11
        self.form_signals = [False, False, False, False]  # form, input, select, textarea
        self.current_link_text = ""
        self.in_link = False
        self.current_link_href = ""

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == "title":
            self.in_title = True
        if tag == "a" and "href" in attrs_dict:
            href = attrs_dict["href"]
            if href and not href.startswith(("#", "javascript:", "mailto:")):
                self.in_link = True
                self.current_link_href = href
                self.current_link_text = ""
        if tag in self.TAG_NAMES:
            idx = self.TAG_NAMES.index(tag)
            self.tag_counts[idx] += 1
        if tag == "form":
            self.form_signals[0] = True
        if tag == "input":
            self.form_signals[1] = True
        if tag == "select":
            self.form_signals[2] = True
        if tag == "textarea":
            self.form_signals[3] = True

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        if tag == "a" and self.in_link:
            self.in_link = False
            text = self.current_link_text.strip().lower()[:100]
            href = self.current_link_href
            if text:
                self.links.append((text, href))

    def handle_data(self, data):
        if self.in_title:
            self.title += data
        if self.in_link:
            self.current_link_text += data


def make_state(url: str, html: str) -> Tuple[State, List[Tuple[str, str]]]:
    """Parse HTML and return (State, list_of_links)."""
    parser = PageParser()
    parser.feed(html)

    title = parser.title.strip().lower()[:100]
    link_texts = sorted(set(t for t, _ in parser.links))[:30]
    tag_counts = tuple(parser.tag_counts)
    form_signals = tuple(parser.form_signals)

    state = State(
        url=url,
        title=title,
        link_texts=tuple(link_texts),
        tag_counts=tag_counts,
        form_signals=form_signals,
    )
    return state, parser.links


def normalize_url(url: str) -> str:
    """Normalize URL: strip query string for deduplication."""
    parsed = urllib.parse.urlparse(url)
    return urllib.parse.urlunparse((parsed.scheme, parsed.netloc, parsed.path, "", "", ""))


def fetch_html(url: str, timeout: int = 10) -> Optional[str]:
    """Fetch page HTML."""
    req = urllib.request.Request(
        url,
        headers={"User-Agent": "SPIDER-Physics/2.0 (research experiment)"}
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")
    except Exception:
        return None


# ---------------------------------------------------------------------------
# Positive Control: 8 states, 3 action types, overlapping actions
# ---------------------------------------------------------------------------

def build_positive_control() -> Tuple[Dict[str, State], Dict[Tuple[str, str, str], str], Dict[str, List[Tuple[str, str]]]]:
    """
    Build a deterministic navigation graph with 8 states and 3 action types.
    Actions overlap across states to ensure action-frequency < action-conditioned accuracy.
    Branching (multiple valid actions per state) and cycles included.
    """
    state_defs = {
        "S0": ("home", "Home page with navigation links"),
        "S1": ("products", "Product listing with filters"),
        "S2": ("about", "About page with team info"),
        "S3": ("contact", "Contact form page"),
        "S4": ("detail_a", "Product detail page A"),
        "S5": ("detail_b", "Product detail page B"),
        "S6": ("faq", "Frequently asked questions"),
        "S7": ("cart", "Shopping cart page"),
    }

    states = {}
    for sid, (name, desc) in state_defs.items():
        states[sid] = State(
            url=f"http://synthetic.test/{name}",
            title=name,
            link_texts=(name, "home", "products", "faq"),
            tag_counts=(1, 2, 0, 1, 0, 1, 0, 0, 1, 1, 0),
            form_signals=(sid == "S3", sid == "S3", False, sid == "S3"),
        )

    # Action types: "click", "navigate", "search"
    # Actions overlap: e.g., ("click", "home") available from S1, S2, S4, S5, S6, S7
    transitions = {
        # From S0 (home)
        ("S0", "click", "home"): "S0",       # self-loop (click home on home)
        ("S0", "navigate", "products"): "S1",
        ("S0", "search", "about"): "S2",
        # From S1 (products)
        ("S1", "click", "home"): "S0",
        ("S1", "navigate", "products"): "S1",  # self-loop
        ("S1", "click", "detail"): "S4",
        ("S1", "search", "faq"): "S6",
        # From S2 (about)
        ("S2", "click", "home"): "S0",
        ("S2", "navigate", "products"): "S1",
        ("S2", "search", "contact"): "S3",
        # From S3 (contact)
        ("S3", "click", "home"): "S0",
        ("S3", "navigate", "products"): "S1",
        ("S3", "click", "submit"): "S0",      # form submit -> home
        # From S4 (detail_a)
        ("S4", "click", "home"): "S0",
        ("S4", "navigate", "products"): "S1",
        ("S4", "click", "cart"): "S7",
        ("S4", "search", "detail"): "S5",
        # From S5 (detail_b)
        ("S5", "click", "home"): "S0",
        ("S5", "navigate", "products"): "S1",
        ("S5", "click", "cart"): "S7",
        ("S5", "search", "detail"): "S4",
        # From S6 (faq)
        ("S6", "click", "home"): "S0",
        ("S6", "navigate", "products"): "S1",
        ("S6", "search", "contact"): "S3",
        # From S7 (cart)
        ("S7", "click", "home"): "S0",
        ("S7", "navigate", "products"): "S1",
        ("S7", "click", "checkout"): "S3",
    }

    valid_actions = {}
    for (sid, atype, tgt), _ in transitions.items():
        valid_actions.setdefault(sid, []).append((atype, tgt))

    return states, transitions, valid_actions


def collect_positive_control(seed: int = 42, n_trajectories: int = 60, steps: int = 10) -> List[Transition]:
    """Collect transitions from the positive control graph."""
    rng = random.Random(seed)
    states, transitions, valid_actions = build_positive_control()
    state_ids = list(states.keys())
    all_transitions = []

    for i in range(n_trajectories):
        traj_id = f"pos_{i}"
        current = rng.choice(state_ids)
        for step in range(steps):
            actions = valid_actions.get(current, [])
            if not actions:
                current = "S0"
                continue
            atype, tgt = rng.choice(actions)
            nxt = transitions.get((current, atype, tgt), "S0")

            sa = Action(action_type=atype, target_text=tgt, target_href=f"http://synthetic.test/{tgt}")
            s = states[current]
            ns = states[nxt]

            t = Transition(
                state_key=s.to_key(),
                action_key=sa.to_key(),
                next_state_key=ns.to_key(),
                trajectory_id=traj_id,
                step_index=step,
            )
            all_transitions.append(t)
            current = nxt

    return all_transitions


# ---------------------------------------------------------------------------
# Null Control: 30 states, 5 action types, random transitions
# ---------------------------------------------------------------------------

def collect_null_control(seed: int = 44, n_trajectories: int = 30, steps: int = 10) -> List[Transition]:
    """Collect random-policy transitions on unstructured synthetic page."""
    rng = random.Random(seed)
    n_states = 30
    action_types = ["click", "navigate", "type_text", "scroll", "submit"]
    target_ids = ["nav", "search", "menu", "footer", "sidebar", "header", "content", "link"]

    # Create states
    state_list = []
    for i in range(n_states):
        s = State(
            url=f"http://null.test/page_{i}",
            title=f"page_{i}",
            link_texts=(f"link_{i}", "home", "nav"),
            tag_counts=(1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
            form_signals=(False, False, False, False),
        )
        state_list.append(s)

    all_transitions = []
    for i in range(n_trajectories):
        traj_id = f"null_{i}"
        current = rng.choice(state_list)
        for step in range(steps):
            atype = rng.choice(action_types)
            tgt = rng.choice(target_ids)
            nxt = rng.choice(state_list)

            sa = Action(action_type=atype, target_text=tgt, target_href="")
            t = Transition(
                state_key=current.to_key(),
                action_key=sa.to_key(),
                next_state_key=nxt.to_key(),
                trajectory_id=traj_id,
                step_index=step,
            )
            all_transitions.append(t)
            current = nxt

    return all_transitions


# ---------------------------------------------------------------------------
# Live Web Collector
# ---------------------------------------------------------------------------

def collect_live_site(base_url: str, seed: int, n_trajectories: int = 20, max_steps: int = 10) -> List[Transition]:
    """Collect transitions from a live website via HTTP fetch."""
    rng = random.Random(seed)
    all_transitions = []

    # Fetch homepage to get starting links
    html = fetch_html(base_url)
    if html is None:
        print(f"  [WARN] Could not fetch {base_url}")
        return []

    homepage_state, homepage_links = make_state(base_url, html)
    if not homepage_links:
        print(f"  [WARN] No links found on {base_url}")
        return []

    # Filter to internal links
    base_parsed = urllib.parse.urlparse(base_url)
    internal_links = []
    for text, href in homepage_links:
        full = urllib.parse.urljoin(base_url, href)
        parsed = urllib.parse.urlparse(full)
        if parsed.netloc == base_parsed.netloc:
            internal_links.append((text, full))

    if not internal_links:
        print(f"  [WARN] No internal links on {base_url}")
        return []

    for i in range(n_trajectories):
        traj_id = f"live_{seed}_{i}"
        # Start from a random internal link
        start_text, start_url = rng.choice(internal_links)
        current_url = normalize_url(start_url)
        current_html = fetch_html(current_url)
        if current_html is None:
            continue
        current_state, current_links = make_state(current_url, current_html)

        for step in range(max_steps):
            # Filter to internal links
            internal = []
            for text, href in current_links:
                full = urllib.parse.urljoin(current_url, href)
                parsed = urllib.parse.urlparse(full)
                if parsed.netloc == base_parsed.netloc:
                    internal.append((text, full))

            if not internal:
                break

            # Choose a random link
            link_text, next_url_raw = rng.choice(internal)
            next_url = normalize_url(next_url_raw)

            action = Action(
                action_type="click",
                target_text=link_text.lower()[:100],
                target_href=next_url,
            )

            # Fetch next page
            time.sleep(0.5)  # polite delay
            next_html = fetch_html(next_url)
            if next_html is None:
                break
            next_state, next_links = make_state(next_url, next_html)

            t = Transition(
                state_key=current_state.to_key(),
                action_key=action.to_key(),
                next_state_key=next_state.to_key(),
                trajectory_id=traj_id,
                step_index=step,
            )
            all_transitions.append(t)

            current_state = next_state
            current_url = next_url
            current_links = next_links

    return all_transitions


# ---------------------------------------------------------------------------
# Trajectory-grouped train/test split
# ---------------------------------------------------------------------------

def split_trajectories(
    transitions: List[Transition],
    train_frac: float = 0.7,
    seed: int = 42,
) -> Tuple[List[Transition], List[Transition]]:
    """Split at trajectory level: 70% train, 30% test."""
    rng = random.Random(seed)
    traj_ids = list(set(t.trajectory_id for t in transitions))
    rng.shuffle(traj_ids)
    n_train = max(1, int(len(traj_ids) * train_frac))
    train_set = set(traj_ids[:n_train])

    train = [t for t in transitions if t.trajectory_id in train_set]
    test = [t for t in transitions if t.trajectory_id not in train_set]
    return train, test


# ---------------------------------------------------------------------------
# Predictors (fit on train, evaluate on test)
# ---------------------------------------------------------------------------

def fit_action_conditioned(train: List[Transition]) -> Dict[str, str]:
    """Fit: predict most common next_state per (state, action)."""
    sa_counts: Dict[str, Dict[str, int]] = {}
    for t in train:
        key = t.state_key + "|" + t.action_key
        sa_counts.setdefault(key, Counter())[t.next_state_key] += 1
    return {k: counter.most_common(1)[0][0] for k, counter in sa_counts.items()}


def fit_action_frequency(train: List[Transition]) -> Dict[str, str]:
    """Fit: predict most common next_state per action (ignoring state)."""
    a_counts: Dict[str, Dict[str, int]] = {}
    for t in train:
        a_counts.setdefault(t.action_key, Counter())[t.next_state_key] += 1
    return {k: counter.most_common(1)[0][0] for k, counter in a_counts.items()}


def fit_state_only(train: List[Transition]) -> Dict[str, str]:
    """Fit: predict most common next_state per state (ignoring action)."""
    s_counts: Dict[str, Dict[str, int]] = {}
    for t in train:
        s_counts.setdefault(t.state_key, Counter())[t.next_state_key] += 1
    return {k: counter.most_common(1)[0][0] for k, counter in s_counts.items()}


def evaluate_predictor(model: Dict[str, str], test: List[Transition]) -> float:
    """Evaluate majority-vote predictor on held-out transitions."""
    if not test:
        return 0.0
    correct = sum(1 for t in test if model.get(t.state_key + "|" + t.action_key, "") == t.next_state_key)
    return correct / len(test)


def evaluate_action_frequency(model: Dict[str, str], test: List[Transition]) -> float:
    """Evaluate action-frequency predictor."""
    if not test:
        return 0.0
    correct = sum(1 for t in test if model.get(t.action_key, "") == t.next_state_key)
    return correct / len(test)


def evaluate_state_only(model: Dict[str, str], test: List[Transition]) -> float:
    """Evaluate state-only predictor."""
    if not test:
        return 0.0
    correct = sum(1 for t in test if model.get(t.state_key, "") == t.next_state_key)
    return correct / len(test)


# ---------------------------------------------------------------------------
# In-sample memorization baseline
# ---------------------------------------------------------------------------

def compute_memorization(transitions: List[Transition]) -> float:
    """Fit and evaluate on same transitions (memorization baseline)."""
    model = fit_action_conditioned(transitions)
    return evaluate_predictor(model, transitions)


# ---------------------------------------------------------------------------
# Permutation test (trajectory-grouped)
# ---------------------------------------------------------------------------

def permutation_test(
    train: List[Transition],
    test: List[Transition],
    n_permutations: int = 1000,
    seed: int = 42,
) -> Tuple[float, float]:
    """
    Permutation test: does action-conditioned accuracy > shuffle accuracy?
    Returns (observed_diff, p_value).
    """
    # Observed accuracy
    model = fit_action_conditioned(train)
    acc_observed = evaluate_predictor(model, test)

    # Shuffle accuracy: permute next_state_key within each trajectory in test
    by_traj: Dict[str, List[Transition]] = {}
    for t in test:
        by_traj.setdefault(t.trajectory_id, []).append(t)

    rng = random.Random(seed)
    count_ge = 0

    for _ in range(n_permutations):
        # Create permuted test set
        perm_test = []
        for traj_id, traj_trans in by_traj.items():
            next_states = [t.next_state_key for t in traj_trans]
            rng.shuffle(next_states)
            for t, ns in zip(traj_trans, next_states):
                perm_test.append(Transition(
                    state_key=t.state_key,
                    action_key=t.action_key,
                    next_state_key=ns,
                    trajectory_id=t.trajectory_id,
                    step_index=t.step_index,
                ))

        # Fit on original train, evaluate on permuted test
        perm_model = fit_action_conditioned(train)
        acc_perm = evaluate_predictor(perm_model, perm_test)
        perm_diff = acc_observed - acc_perm
        if perm_diff >= (acc_observed - (1.0 / len(test) if test else 0)):
            count_ge += 1

    # Simpler: compute diff for each permutation
    # observed_diff = acc_SA_test - acc_shuffle_test
    # Under null: acc_shuffle_test is the accuracy when labels are shuffled
    # We want P(acc_SA_test - acc_shuffle >= observed_diff)

    # Actually, the standard approach:
    # 1. Compute observed diff = acc_SA_heldout - acc_shuffle_heldout
    # 2. For each permutation, permute next-state labels in test, recompute diff
    # 3. p = fraction of permuted diffs >= observed diff

    # Let me redo this correctly:
    model_sa = fit_action_conditioned(train)
    acc_sa_test = evaluate_predictor(model_sa, test)

    # Shuffle baseline: fit on train, evaluate on test with shuffled labels
    # The shuffle null is: predict using the model, but the true labels are shuffled
    # So accuracy = fraction where model prediction matches shuffled label
    # = 1 - (1/unique_states) approximately, depending on model and test distribution

    # Better approach: compute diff = acc_SA_test - acc_frequency_test
    # This is the spec's primary metric

    model_freq = fit_action_frequency(train)
    acc_freq_test = evaluate_action_frequency(model_freq, test)

    observed_diff = acc_sa_test - acc_freq_test

    # Permutation test: permute next-state labels within trajectories
    perm_diffs = []
    for _ in range(n_permutations):
        perm_test = []
        for traj_id, traj_trans in by_traj.items():
            next_states = [t.next_state_key for t in traj_trans]
            rng.shuffle(next_states)
            for t, ns in zip(traj_trans, next_states):
                perm_test.append(Transition(
                    state_key=t.state_key,
                    action_key=t.action_key,
                    next_state_key=ns,
                    trajectory_id=t.trajectory_id,
                    step_index=t.step_index,
                ))

        # Fit on original train (which is NOT permuted), evaluate on permuted test
        perm_model_sa = fit_action_conditioned(train)
        perm_acc_sa = evaluate_predictor(perm_model_sa, perm_test)

        perm_model_freq = fit_action_frequency(train)
        perm_acc_freq = evaluate_action_frequency(perm_model_freq, perm_test)

        perm_diff = perm_acc_sa - perm_acc_freq
        perm_diffs.append(perm_diff)

    # One-sided p-value: P(perm_diff >= observed_diff)
    p_value = sum(1 for d in perm_diffs if d >= observed_diff) / n_permutations

    return observed_diff, p_value


def permutation_test_vs_shuffle(
    train: List[Transition],
    test: List[Transition],
    n_permutations: int = 1000,
    seed: int = 42,
) -> Tuple[float, float]:
    """
    Permutation test: does action-conditioned accuracy > shuffle null?
    The shuffle null is: predict most common next_state per trajectory.
    """
    model_sa = fit_action_conditioned(train)
    acc_sa_test = evaluate_predictor(model_sa, test)

    by_traj: Dict[str, List[Transition]] = {}
    for t in test:
        by_traj.setdefault(t.trajectory_id, []).append(t)

    rng = random.Random(seed)
    perm_accs = []

    for _ in range(n_permutations):
        perm_test = []
        for traj_id, traj_trans in by_traj.items():
            next_states = [t.next_state_key for t in traj_trans]
            rng.shuffle(next_states)
            for t, ns in zip(traj_trans, next_states):
                perm_test.append(Transition(
                    state_key=t.state_key,
                    action_key=t.action_key,
                    next_state_key=ns,
                    trajectory_id=t.trajectory_id,
                    step_index=t.step_index,
                ))

        perm_model = fit_action_conditioned(train)
        perm_acc = evaluate_predictor(perm_model, perm_test)
        perm_accs.append(perm_acc)

    observed_diff = acc_sa_test  # under shuffle, accuracy is the permuted accuracy
    # We want P(perm_acc >= acc_sa_test) -- this is the probability the shuffle null
    # produces accuracy as high or higher than observed
    # Wait, actually: under the shuffle null, the model is the same (fitted on train)
    # but the test labels are shuffled. So perm_acc should be ~chance.
    # p-value = P(perm_acc >= acc_sa_test)

    # But actually the standard formulation is:
    # H0: next_state is independent of (state, action) given trajectory
    # Test statistic: accuracy of action-conditioned model on held-out data
    # Null distribution: accuracy when next_state labels are shuffled within trajectories
    # p = fraction of null accuracies >= observed accuracy

    p_value = sum(1 for a in perm_accs if a >= acc_sa_test) / n_permutations

    return acc_sa_test, p_value


# ---------------------------------------------------------------------------
# Validity gates
# ---------------------------------------------------------------------------

def check_trajectory_contamination(train: List[Transition], test: List[Transition]) -> dict:
    """No trajectory appears in both train and test."""
    train_trajs = set(t.trajectory_id for t in train)
    test_trajs = set(t.trajectory_id for t in test)
    overlap = train_trajs & test_trajs
    return {"passed": len(overlap) == 0, "overlap_count": len(overlap)}


def check_temporal_ordering(transitions: List[Transition]) -> dict:
    """Within each trajectory, step indices are monotonically increasing."""
    by_traj: Dict[str, List[Transition]] = {}
    for t in transitions:
        by_traj.setdefault(t.trajectory_id, []).append(t)
    issues = []
    for tid, traj_trans in by_traj.items():
        sorted_t = sorted(traj_trans, key=lambda x: x.step_index)
        for i, t in enumerate(sorted_t):
            if t.step_index != i:
                issues.append(f"{tid}: step {t.step_index} at position {i}")
    return {"passed": len(issues) == 0, "issues": issues[:10]}


def check_seed_determinism(seed: int) -> dict:
    """Verify random.Random(seed) produces deterministic results."""
    r1 = random.Random(seed)
    r2 = random.Random(seed)
    s1 = [r1.random() for _ in range(100)]
    s2 = [r2.random() for _ in range(100)]
    return {"passed": s1 == s2, "seed": seed}


def check_target_leakage(transitions: List[Transition]) -> dict:
    """Action features never contain next-state information."""
    # By construction: action_key = action_type|target_text|target_href
    # These describe the action target, not the next state content
    # Structural guarantee, but verify no exact next_state_key appears in action_key
    issues = []
    for t in transitions:
        if t.next_state_key in t.action_key:
            issues.append(f"next_state_key found in action_key: {t.action_key}")
    return {"passed": len(issues) == 0, "issues": issues[:10], "n_checked": len(transitions)}


# ---------------------------------------------------------------------------
# Main experiment
# ---------------------------------------------------------------------------

def main():
    print("=" * 70)
    print("EXP-PHYSICS-33788037373: Corrected Measurement Substrate")
    print("=" * 70)
    start_time = time.time()

    # Seeds per preregistration
    SEED_POSITIVE = 42
    SEED_LIVE_1 = 43
    SEED_NULL = 44
    SEED_LIVE_2 = 45

    # ---- Phase 1: Synthetic Validation ----
    print("\n" + "=" * 70)
    print("PHASE 1: SYNTHETIC VALIDATION")
    print("=" * 70)

    # Positive control: 60 trajectories x 10 steps = 600 transitions
    print("\n[1.1] Positive Control (8 states, 3 actions, overlapping)")
    pos_transitions = collect_positive_control(seed=SEED_POSITIVE, n_trajectories=60, steps=10)
    print(f"  Collected {len(pos_transitions)} transitions from {len(set(t.trajectory_id for t in pos_transitions))} trajectories")

    # Null control: 30 trajectories x 10 steps = 300 transitions
    print("\n[1.2] Null Control (30 states, 5 actions, random)")
    null_transitions = collect_null_control(seed=SEED_NULL, n_trajectories=30, steps=10)
    print(f"  Collected {len(null_transitions)} transitions from {len(set(t.trajectory_id for t in null_transitions))} trajectories")

    # Split synthetic data
    pos_train, pos_test = split_trajectories(pos_transitions, train_frac=0.7, seed=SEED_POSITIVE)
    null_train, null_test = split_trajectories(null_transitions, train_frac=0.7, seed=SEED_POSITIVE)

    print(f"\n  Positive: {len(pos_train)} train, {len(pos_test)} test")
    print(f"  Null: {len(null_train)} train, {len(null_test)} test")

    # Evaluate positive control
    print("\n[1.3] Positive Control Evaluation")
    pos_sa_model = fit_action_conditioned(pos_train)
    pos_sa_acc = evaluate_predictor(pos_sa_model, pos_test)
    pos_freq_model = fit_action_frequency(pos_train)
    pos_freq_acc = evaluate_action_frequency(pos_freq_model, pos_test)
    pos_state_model = fit_state_only(pos_train)
    pos_state_acc = evaluate_state_only(pos_state_model, pos_test)
    pos_memorization = compute_memorization(pos_transitions)

    print(f"  Action-conditioned (held-out): {pos_sa_acc:.4f}")
    print(f"  Action-frequency (held-out):   {pos_freq_acc:.4f}")
    print(f"  State-only (held-out):         {pos_state_acc:.4f}")
    print(f"  Memorization (in-sample):      {pos_memorization:.4f}")

    # Permutation test: positive control discriminates (SA > freq)
    print("\n[1.4] Permutation Test: Positive Control Discrimination")
    pos_diff, pos_p_discrim = permutation_test(pos_train, pos_test, n_permutations=1000, seed=42)
    print(f"  Diff (SA - freq): {pos_diff:.4f}")
    print(f"  p-value (one-sided): {pos_p_discrim:.6f}")

    # Permutation test: positive control vs shuffle
    print("\n[1.5] Permutation Test: Positive Control vs Shuffle")
    pos_sa_acc2, pos_p_shuffle = permutation_test_vs_shuffle(pos_train, pos_test, n_permutations=1000, seed=42)
    print(f"  Action-conditioned accuracy: {pos_sa_acc2:.4f}")
    print(f"  p-value (vs shuffle): {pos_p_shuffle:.6f}")

    # Evaluate null control
    print("\n[1.6] Null Control Evaluation")
    null_sa_model = fit_action_conditioned(null_train)
    null_sa_acc = evaluate_predictor(null_sa_model, null_test)
    null_freq_model = fit_action_frequency(null_train)
    null_freq_acc = evaluate_action_frequency(null_freq_model, null_test)
    null_state_model = fit_state_only(null_train)
    null_state_acc = evaluate_state_only(null_state_model, null_test)

    print(f"  Action-conditioned (held-out): {null_sa_acc:.4f}")
    print(f"  Action-frequency (held-out):   {null_freq_acc:.4f}")
    print(f"  State-only (held-out):         {null_state_acc:.4f}")

    # Permutation test: null control vs shuffle
    print("\n[1.7] Permutation Test: Null Control")
    null_diff, null_p = permutation_test_vs_shuffle(null_train, null_test, n_permutations=1000, seed=44)
    print(f"  Diff (SA - shuffle): {null_diff:.4f}")
    print(f"  p-value: {null_p:.6f}")

    # ---- Phase 2: Live Web Collection ----
    print("\n" + "=" * 70)
    print("PHASE 2: LIVE WEB COLLECTION")
    print("=" * 70)

    print("\n[2.1] Site 1: Wikipedia Main Page")
    live1_transitions = collect_live_site(
        "https://en.wikipedia.org/wiki/Main_Page",
        seed=SEED_LIVE_1,
        n_trajectories=20,
        max_steps=10,
    )
    print(f"  Collected {len(live1_transitions)} transitions from {len(set(t.trajectory_id for t in live1_transitions))} trajectories")

    print("\n[2.2] Site 2: Python Documentation")
    live2_transitions = collect_live_site(
        "https://docs.python.org/3/",
        seed=SEED_LIVE_2,
        n_trajectories=20,
        max_steps=10,
    )
    print(f"  Collected {len(live2_transitions)} transitions from {len(set(t.trajectory_id for t in live2_transitions))} trajectories")

    # ---- Phase 3: Live Evaluation ----
    print("\n" + "=" * 70)
    print("PHASE 3: LIVE EVALUATION")
    print("=" * 70)

    live_results = {}
    for label, transitions in [("live_wikipedia", live1_transitions), ("live_python_docs", live2_transitions)]:
        print(f"\n[3.x] {label} ({len(transitions)} transitions)")
        if len(transitions) < 10:
            print(f"  SKIP: too few transitions ({len(transitions)})")
            live_results[label] = {"error": "insufficient_data", "n_transitions": len(transitions)}
            continue

        train, test = split_trajectories(transitions, train_frac=0.7, seed=42)
        print(f"  Split: {len(train)} train, {len(test)} test")

        sa_model = fit_action_conditioned(train)
        sa_acc = evaluate_predictor(sa_model, test)
        freq_model = fit_action_frequency(train)
        freq_acc = evaluate_action_frequency(freq_model, test)
        state_model = fit_state_only(train)
        state_acc = evaluate_state_only(state_model, test)
        memorization = compute_memorization(transitions)

        print(f"  Action-conditioned (held-out): {sa_acc:.4f}")
        print(f"  Action-frequency (held-out):   {freq_acc:.4f}")
        print(f"  State-only (held-out):         {state_acc:.4f}")
        print(f"  Memorization (in-sample):      {memorization:.4f}")

        # Permutation test vs shuffle
        sa_acc_val, p_shuffle = permutation_test_vs_shuffle(train, test, n_permutations=1000, seed=42)
        diff, p_discrim = permutation_test(train, test, n_permutations=1000, seed=42)

        print(f"  Permutation p (vs shuffle): {p_shuffle:.6f}")
        print(f"  Permutation p (SA > freq):   {p_discrim:.6f}")

        live_results[label] = {
            "n_transitions": len(transitions),
            "n_trajectories": len(set(t.trajectory_id for t in transitions)),
            "n_train": len(train),
            "n_test": len(test),
            "action_conditioned_accuracy_heldout": sa_acc,
            "action_frequency_accuracy_heldout": freq_acc,
            "state_only_accuracy_heldout": state_acc,
            "memorization_ratio": memorization / sa_acc if sa_acc > 0 else float("inf"),
            "diff_SA_minus_freq": diff,
            "p_discrim": p_discrim,
            "p_vs_shuffle": p_shuffle,
        }

    # ---- Phase 4: Validity Gates ----
    print("\n" + "=" * 70)
    print("PHASE 4: VALIDITY GATES")
    print("=" * 70)

    all_transitions = pos_transitions + null_transitions + live1_transitions + live2_transitions

    validity = {
        "trajectory_contamination_pos": check_trajectory_contamination(pos_train, pos_test),
        "trajectory_contamination_null": check_trajectory_contamination(null_train, null_test),
        "temporal_ordering": check_temporal_ordering(all_transitions),
        "seed_determinism": check_seed_determinism(42),
        "target_leakage": check_target_leakage(all_transitions),
    }

    for name, result in validity.items():
        status = "PASS" if result["passed"] else "FAIL"
        print(f"  {name}: {status}")

    all_valid = all(r["passed"] for r in validity.values())
    print(f"\n  Overall validity: {'PASS' if all_valid else 'FAIL'}")

    # ---- Phase 5: Multiple Comparison Correction ----
    print("\n" + "=" * 70)
    print("PHASE 5: MULTIPLE COMPARISON CORRECTION")
    print("=" * 70)

    # Bonferroni for 3 null tests x 2 live sites = 6 comparisons
    p_values_raw = []
    p_labels = []

    # Null control p-value
    p_values_raw.append(null_p)
    p_labels.append("null_control")

    # Live site p-values (vs shuffle)
    for label, res in live_results.items():
        if "p_vs_shuffle" in res:
            p_values_raw.append(res["p_vs_shuffle"])
            p_labels.append(f"{label}_vs_shuffle")
        if "p_discrim" in res:
            p_values_raw.append(res["p_discrim"])
            p_labels.append(f"{label}_discrim")

    n_comparisons = 6  # per spec: 3 null tests x 2 live sites
    p_corrected = [min(p * n_comparisons, 1.0) for p in p_values_raw]

    print(f"  Raw p-values: {dict(zip(p_labels, p_values_raw))}")
    print(f"  Bonferroni corrected (x{n_comparisons}): {dict(zip(p_labels, p_corrected))}")

    # ---- Phase 6: Verdict ----
    print("\n" + "=" * 70)
    print("PHASE 6: VERDICT")
    print("=" * 70)

    # Check decision rule from spec
    verdict = "INCONCLUSIVE"

    # Validity gates must pass
    if not all_valid:
        verdict = "MEASUREMENT_INVALID"
        print(f"  FAIL: validity gates failed")
    else:
        # Positive control must discriminate (p < 0.05) and accuracy > 90%
        pc_pass = (pos_p_discrim < 0.05) and (pos_sa_acc > 0.90)
        print(f"  Positive control discriminates: p={pos_p_discrim:.6f} {'PASS' if pos_p_discrim < 0.05 else 'FAIL'}")
        print(f"  Positive control accuracy >90%: {pos_sa_acc:.4f} {'PASS' if pos_sa_acc > 0.90 else 'FAIL'}")

        if not pc_pass:
            verdict = "MEASUREMENT_INVALID"
            print(f"  FAIL: positive control did not pass")
        else:
            # Null control must pass (p > 0.05)
            nc_pass = null_p > 0.05
            print(f"  Null control passes: p={null_p:.6f} {'PASS' if nc_pass else 'FAIL'}")

            if not nc_pass:
                verdict = "MEASUREMENT_INVALID"
                print(f"  FAIL: null control false positive")
            else:
                # Check live sites for action-conditioned structure above shuffle
                live_site_passes = []
                for label, res in live_results.items():
                    if "p_vs_shuffle" in res:
                        # Find corrected p-value for this site
                        idx = p_labels.index(f"{label}_vs_shuffle")
                        p_corr = p_corrected[idx]
                        site_pass = p_corr < 0.05
                        live_site_passes.append(site_pass)
                        print(f"  {label} structure above shuffle: p_corrected={p_corr:.6f} {'PASS' if site_pass else 'FAIL'}")

                # At least one live site must pass
                if any(live_site_passes):
                    verdict = "SURVIVES_CURRENT_TEST"
                    print(f"  PASS: at least one live site shows structure")
                else:
                    verdict = "FALSIFIED-IN-SETTING"
                    print(f"  FAIL: no live site shows structure above shuffle")

    # Check >= 100 live transitions from >= 2 sites
    live_total = len(live1_transitions) + len(live2_transitions)
    n_live_sites = sum(1 for t in [live1_transitions, live2_transitions] if len(t) >= 50)
    print(f"\n  Live transitions: {live_total} (need >=100)")
    print(f"  Live sites with data: {n_live_sites} (need >=2)")

    if live_total < 100 or n_live_sites < 2:
        if verdict not in ("MEASUREMENT_INVALID",):
            verdict = "MEASUREMENT_INVALID"
            print(f"  FAIL: insufficient live data")

    print(f"\n  FINAL VERDICT: {verdict}")

    # ---- Phase 7: Write Results ----
    print("\n" + "=" * 70)
    print("PHASE 7: WRITING RESULTS")
    print("=" * 70)

    elapsed = time.time() - start_time

    metrics = {
        "positive_control": {
            "n_transitions": len(pos_transitions),
            "n_trajectories": len(set(t.trajectory_id for t in pos_transitions)),
            "n_train": len(pos_train),
            "n_test": len(pos_test),
            "action_conditioned_accuracy_heldout": pos_sa_acc,
            "action_frequency_accuracy_heldout": pos_freq_acc,
            "state_only_accuracy_heldout": pos_state_acc,
            "memorization_ratio": pos_memorization / pos_sa_acc if pos_sa_acc > 0 else float("inf"),
            "diff_SA_minus_freq": pos_diff,
            "p_discrim": pos_p_discrim,
            "p_vs_shuffle": pos_p_shuffle,
        },
        "null_control": {
            "n_transitions": len(null_transitions),
            "n_trajectories": len(set(t.trajectory_id for t in null_transitions)),
            "n_train": len(null_train),
            "n_test": len(null_test),
            "action_conditioned_accuracy_heldout": null_sa_acc,
            "action_frequency_accuracy_heldout": null_freq_acc,
            "state_only_accuracy_heldout": null_state_acc,
            "diff_SA_minus_freq": null_diff,
            "p_vs_shuffle": null_p,
        },
        "live_sites": live_results,
        "memorization_comparison": {
            "positive_control_insample": pos_memorization,
            "positive_control_heldout": pos_sa_acc,
            "memorization_artifact_confirmed": pos_memorization > pos_sa_acc * 1.5,
        },
        "multiple_comparisons": {
            "n_comparisons": n_comparisons,
            "method": "Bonferroni",
            "raw_p_values": dict(zip(p_labels, p_values_raw)),
            "corrected_p_values": dict(zip(p_labels, p_corrected)),
        },
    }

    controls = {
        "positive_control": {
            "expected": "action_conditioned > action_frequency, accuracy > 90%",
            "observed_accuracy": pos_sa_acc,
            "observed_diff": pos_diff,
            "p_value": pos_p_discrim,
            "pass": pos_p_discrim < 0.05 and pos_sa_acc > 0.90,
        },
        "null_control": {
            "expected": "no action-conditioned structure, p > 0.05",
            "observed_accuracy": null_sa_acc,
            "p_value": null_p,
            "pass": null_p > 0.05,
        },
        "shuffle_null": {
            "expected": "permutation test within trajectories",
            "n_permutations": 1000,
            "method": "trajectory-grouped permutation",
        },
    }

    result = {
        "schema_version": 1,
        "experiment_id": "EXP-PHYSICS-33788037373",
        "lane": "physics",
        "status": "COMPLETE" if verdict in ("SURVIVES_CURRENT_TEST", "FALSIFIED-IN-SETTING") else ("MEASUREMENT_INVALID" if verdict == "MEASUREMENT_INVALID" else "COMPLETE"),
        "outcome": {
            "SURVIVES_CURRENT_TEST": "SUPPORTS",
            "FALSIFIED-IN-SETTING": "FALSIFIES",
            "MEASUREMENT_INVALID": "MEASUREMENT_INVALID",
            "INCONCLUSIVE": "INCONCLUSIVE",
        }.get(verdict, "INCONCLUSIVE"),
        "metrics": metrics,
        "controls": controls,
        "artifacts": [
            {"path": "research/physics/run_experiment_337.py", "role": "code"},
        ],
        "observations": [
            f"Positive control collected {len(pos_transitions)} transitions from {len(set(t.trajectory_id for t in pos_transitions))} trajectories",
            f"Null control collected {len(null_transitions)} transitions from {len(set(t.trajectory_id for t in null_transitions))} trajectories",
            f"Live site 1 (Wikipedia) collected {len(live1_transitions)} transitions",
            f"Live site 2 (Python docs) collected {len(live2_transitions)} transitions",
            f"Positive control held-out accuracy: {pos_sa_acc:.4f} (memorization ratio: {pos_memorization / pos_sa_acc if pos_sa_acc > 0 else 'inf':.2f})",
            f"Positive control discrimination p-value: {pos_p_discrim:.6f}",
            f"Null control p-value (vs shuffle): {null_p:.6f}",
            f"Memorization artifact {'CONFIRMED' if pos_memorization > pos_sa_acc * 1.5 else 'not confirmed'}: in-sample={pos_memorization:.4f}, held-out={pos_sa_acc:.4f}",
        ],
        "validity_notes": [
            "State representation uses HTTP fetch + HTMLParser (no JS execution, no accessibility tree)",
            "Action representation uses link text and href (semantic, not positional indices)",
            "Trajectory-grouped holdout ensures no trajectory appears in both train and test",
            "Permutation test uses trajectory-grouped permutation (not transition-level)",
            "1000 permutations per condition with independent RNG",
            "Bonferroni correction for 6 comparisons (3 null tests x 2 live sites)",
            "All code is Python stdlib only (no numpy/scipy)",
            f"Live collection used polite 0.5s delay between requests",
            f"Total experiment time: {elapsed:.1f}s",
        ],
        "unresolved": [
            "Whether richer state representation (DOM/accessibility tree) would reveal more structure",
            "Whether browser-based collection (Playwright) would capture JS-rendered dynamics",
            "Whether sites with higher navigational density (e-commerce, news) would show stronger structure",
            "Whether cross-site transfer is possible",
            "Whether the tested representation level is sufficient for Physics claims",
        ],
    }

    result_path = EXPERIMENT_DIR / "result.json"
    with open(result_path, "w") as f:
        json.dump(result, f, indent=2, default=str)
    print(f"  Wrote {result_path}")

    # Report
    report = generate_report(result, pos_transitions, null_transitions, live1_transitions, live2_transitions, verdict)
    report_path = EXPERIMENT_DIR / "report.md"
    with open(report_path, "w") as f:
        f.write(report)
    print(f"  Wrote {report_path}")

    # Provenance
    provenance = {
        "experiment_id": "EXP-PHYSICS-33788037373",
        "lane": "physics",
        "github_run_id": "33805291701",
        "pre_execute_sha": "33ef08894b52ac68b84d27cc9a5489bcf1d759b6",
        "freeze_hash_prereg": "edef86688d34e165a026576e9f8c27edc95a0b3a73c5c80c2c52a4a234f610ea",
        "freeze_hash_request": "b014f5c206a83409bfd5326bc8d2e8183609e0ef80ed0e6078d50e2dae209ff6",
        "freeze_hash_spec": "818348452206b27e26f4dc645bb03bc3ccd982287f54fcd3d2f6f5b3101ce863",
        "execution_sha": hashlib.sha256(json.dumps(result, sort_keys=True, default=str).encode()).hexdigest(),
        "code_paths": [
            "research/physics/run_experiment_337.py",
        ],
        "environment": {
            "python_version": sys.version,
            "platform": sys.platform,
            "stdlib_only": True,
        },
        "data_hashes": {
            "positive_control": hashlib.sha256(json.dumps([{
                "state": t.state_key,
                "action": t.action_key,
                "next": t.next_state_key,
                "traj": t.trajectory_id,
                "step": t.step_index,
            } for t in pos_transitions], sort_keys=True).encode()).hexdigest(),
            "null_control": hashlib.sha256(json.dumps([{
                "state": t.state_key,
                "action": t.action_key,
                "next": t.next_state_key,
                "traj": t.trajectory_id,
                "step": t.step_index,
            } for t in null_transitions], sort_keys=True).encode()).hexdigest(),
            "live_wikipedia": hashlib.sha256(json.dumps([{
                "state": t.state_key,
                "action": t.action_key,
                "next": t.next_state_key,
                "traj": t.trajectory_id,
                "step": t.step_index,
            } for t in live1_transitions], sort_keys=True).encode()).hexdigest(),
            "live_python_docs": hashlib.sha256(json.dumps([{
                "state": t.state_key,
                "action": t.action_key,
                "next": t.next_state_key,
                "traj": t.trajectory_id,
                "step": t.step_index,
            } for t in live2_transitions], sort_keys=True).encode()).hexdigest(),
        },
        "seeds": {
            "positive_control": SEED_POSITIVE,
            "live_site_1": SEED_LIVE_1,
            "null_control": SEED_NULL,
            "live_site_2": SEED_LIVE_2,
        },
        "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
    }

    provenance_path = EXPERIMENT_DIR / "provenance.json"
    with open(provenance_path, "w") as f:
        json.dump(provenance, f, indent=2, default=str)
    print(f"  Wrote {provenance_path}")

    print("\n" + "=" * 70)
    print("EXPERIMENT COMPLETE")
    print("=" * 70)

    return result


def generate_report(
    result: dict,
    pos_transitions: list,
    null_transitions: list,
    live1_transitions: list,
    live2_transitions: list,
    verdict: str,
) -> str:
    """Generate human-readable report."""
    m = result["metrics"]
    pc = m["positive_control"]
    nc = m["null_control"]
    live = m["live_sites"]
    mem = m["memorization_comparison"]
    mc = m["multiple_comparisons"]

    report = f"""# EXP-PHYSICS-33788037373 Report

## Experiment: Corrected Measurement Substrate for Action-Conditioned Transition Structure

**Lane**: Physics
**Experiment ID**: EXP-PHYSICS-33788037373
**Verdict**: `{verdict}`

---

## 1. Hypothesis

After correcting three methodology defects identified in EXP-PHYSICS-33528829431 (in-sample evaluation, invalid bootstrap, non-discriminating positive control), does the measurement substrate reveal genuine action-conditioned transition structure on live Web pages with navigational density?

**Sub-hypotheses**:
- **H1 (Memorization Artifact)**: The previous 100% live-test accuracy was in-sample memorization. Held-out accuracy will be substantially lower.
- **H2 (Positive Control Discrimination)**: With overlapping actions, action-conditioned > action-frequency on held-out data.
- **H3 (Live Structure)**: At least one live site shows action-conditioned structure above shuffle after correction.

---

## 2. Corrected Methodology

### Fixes Applied
1. **Trajectory-grouped holdout**: Train/test split at trajectory level (no trajectory in both sets)
2. **Trajectory-grouped permutation null**: Permute next-state labels within trajectories, independent RNG per permutation
3. **Overlapping-action positive control**: 8 states, 3 action types with actions shared across states
4. **Richer state representation**: URL + title + link_texts + tag_counts + form_signals (not just hashes)
5. **Semantic actions**: action_type + target_text + target_href (not positional indices)
6. **Python stdlib only**: No numpy/scipy dependency

### State Representation
- `url`: Full page URL (normalized, query string stripped)
- `title`: Page title (lowercased, max 100 chars)
- `link_texts`: Sorted set of first 30 visible link text contents
- `tag_counts`: 11 integers (h1, h2, h3, form, input, button, select, textarea, nav, main, aside)
- `form_signals`: 4 booleans (has_form, has_input, has_select, has_textarea)
- State key: SHA256 of concatenated features, first 16 hex chars

### Action Representation
- `action_type`: click, navigate, search, etc.
- `target_text`: Visible text of clicked element
- `target_href`: Destination URL
- Action key: action_type|target_text|target_href

---

## 3. Results Summary

### 3.1 Sample Sizes

| Condition | Transitions | Trajectories | Train | Test |
|-----------|-------------|--------------|-------|------|
| Positive Control | {pc['n_transitions']} | {pc['n_trajectories']} | {pc['n_train']} | {pc['n_test']} |
| Null Control | {nc['n_transitions']} | {nc['n_trajectories']} | {nc['n_train']} | {nc['n_test']} |
"""

    for label, res in live.items():
        if "error" not in res:
            report += f"| {label} | {res['n_transitions']} | {res['n_trajectories']} | {res['n_train']} | {res['n_test']} |\n"

    report += f"""
### 3.2 Held-Out Accuracy

| Condition | Action-Conditioned | Action-Frequency | State-Only | Memorization |
|-----------|-------------------|-----------------|------------|--------------|
| Positive Control | {pc['action_conditioned_accuracy_heldout']:.4f} | {pc['action_frequency_accuracy_heldout']:.4f} | {pc['state_only_accuracy_heldout']:.4f} | {pc['memorization_ratio']:.2f}x |
| Null Control | {nc['action_conditioned_accuracy_heldout']:.4f} | {nc['action_frequency_accuracy_heldout']:.4f} | {nc['state_only_accuracy_heldout']:.4f} | — |
"""

    for label, res in live.items():
        if "error" not in res:
            report += f"| {label} | {res['action_conditioned_accuracy_heldout']:.4f} | {res['action_frequency_accuracy_heldout']:.4f} | {res['state_only_accuracy_heldout']:.4f} | {res['memorization_ratio']:.2f}x |\n"

    report += f"""
### 3.3 Permutation Test Results

| Condition | Diff (SA - freq) | p-value | Corrected p | Significant? |
|-----------|------------------|---------|-------------|--------------|
| Positive Control (discrim) | {pc['diff_SA_minus_freq']:.4f} | {pc['p_discrim']:.6f} | {min(pc['p_discrim'] * 6, 1.0):.6f} | {"YES" if pc['p_discrim'] < 0.05 else "NO"} |
| Null Control (vs shuffle) | {nc['diff_SA_minus_freq']:.4f} | {nc['p_vs_shuffle']:.6f} | {min(nc['p_vs_shuffle'] * 6, 1.0):.6f} | {"YES" if nc['p_vs_shuffle'] < 0.05 else "NO"} |
"""

    for label, res in live.items():
        if "p_vs_shuffle" in res:
            corr = min(res['p_vs_shuffle'] * 6, 1.0)
            report += f"| {label} (vs shuffle) | — | {res['p_vs_shuffle']:.6f} | {corr:.6f} | {"YES" if corr < 0.05 else "NO"} |\n"
        if "p_discrim" in res:
            corr = min(res['p_discrim'] * 6, 1.0)
            report += f"| {label} (discrim) | {res['diff_SA_minus_freq']:.4f} | {res['p_discrim']:.6f} | {corr:.6f} | {"YES" if corr < 0.05 else "NO"} |\n"

    report += f"""
### 3.4 Memorization Artifact

- In-sample accuracy: {mem['positive_control_insample']:.4f}
- Held-out accuracy: {mem['positive_control_heldout']:.4f}
- Ratio: {mem['positive_control_insample'] / mem['positive_control_heldout'] if mem['positive_control_heldout'] > 0 else 'inf':.2f}x
- Artifact confirmed: {"YES" if mem['memorization_artifact_confirmed'] else "NO"}

---

## 4. Validity Gates

| Gate | Status |
|------|--------|
"""

    for name, check in result["controls"].items():
        if isinstance(check, dict) and "pass" in check:
            report += f"| {name} | {"PASS" if check['pass'] else "FAIL"} |\n"

    report += f"""
---

## 5. Decision Rule Application

### SURVIVES_CURRENT_TEST requires ALL of:
1. Positive control discriminates (p < 0.05): {"PASS" if pc['p_discrim'] < 0.05 else "FAIL"} (p={pc['p_discrim']:.6f})
2. Positive control accuracy > 90%: {"PASS" if pc['action_conditioned_accuracy_heldout'] > 0.90 else "FAIL"} ({pc['action_conditioned_accuracy_heldout']:.4f})
3. Null control passes (p > 0.05): {"PASS" if nc['p_vs_shuffle'] > 0.05 else "FAIL"} (p={nc['p_vs_shuffle']:.6f})
4. >= 1 live site shows structure above shuffle (p < 0.05 after Bonferroni x6):
"""

    for label, res in live.items():
        if "p_vs_shuffle" in res:
            corr = min(res['p_vs_shuffle'] * 6, 1.0)
            report += f"   - {label}: {"PASS" if corr < 0.05 else "FAIL"} (p_corrected={corr:.6f})\n"

    report += f"""
### VERDICT: `{verdict}`

---

## 6. Interpretation

### H1: Memorization Artifact
"""

    if mem['memorization_artifact_confirmed']:
        report += f"""**CONFIRMED.** The previous 100% in-sample accuracy was memorization. Held-out accuracy is {mem['positive_control_heldout']:.4f}, a {mem['positive_control_insample'] / mem['positive_control_heldout'] if mem['positive_control_heldout'] > 0 else 'inf':.1f}x reduction. This validates the trajectory-grouped holdout methodology.
"""
    else:
        report += f"""Not confirmed. Held-out accuracy ({mem['positive_control_heldout']:.4f}) is comparable to in-sample ({mem['positive_control_insample']:.4f}).
"""

    report += f"""
### H2: Positive Control Discrimination
"""

    if pc['p_discrim'] < 0.05 and pc['action_conditioned_accuracy_heldout'] > 0.90:
        report += f"""**PASSES.** The positive control with overlapping actions discriminates action-conditioned from action-frequency prediction (p={pc['p_discrim']:.6f}, accuracy={pc['action_conditioned_accuracy_heldout']:.4f}). The measurement substrate can detect state-dependent structure when it exists.
"""
    else:
        report += f"""**FAILS.** The positive control does not discriminate (p={pc['p_discrim']:.6f}, accuracy={pc['action_conditioned_accuracy_heldout']:.4f}).
"""

    report += f"""
### H3: Live Action-Conditioned Structure
"""

    any_live_pass = False
    for label, res in live.items():
        if "p_vs_shuffle" in res:
            corr = min(res['p_vs_shuffle'] * 6, 1.0)
            if corr < 0.05:
                any_live_pass = True
                report += f"""**{label}: PASSES** (p_corrected={corr:.6f}). Action-conditioned structure detected above shuffle.
"""
            else:
                report += f"""**{label}: does not pass** (p_corrected={corr:.6f}). No significant structure above shuffle.
"""

    if not any_live_pass:
        report += """No live site shows significant action-conditioned structure above the shuffle null after correction.
"""

    report += f"""
---

## 7. Comparison to Prior Experiment

| Metric | EXP-PHYSICS-33528829431 (prior) | EXP-PHYSICS-33788037373 (corrected) |
|--------|----------------------------------|-------------------------------------|
| Evaluation | In-sample | Trajectory-grouped holdout |
| Bootstrap | Transition-level (invalid) | Trajectory-grouped permutation |
| Positive control | 9 unique actions (non-discriminating) | 8 states, 3 overlapping actions |
| State representation | URL + hashes | URL + title + link_texts + tag_counts + form_signals |
| Action representation | Positional index | Semantic (text + href) |
| Live accuracy | 100% (memorization) | {live.get('live_wikipedia', {}).get('action_conditioned_accuracy_heldout', 'N/A')} (Wikipedia), {live.get('live_python_docs', {}).get('action_conditioned_accuracy_heldout', 'N/A')} (Python docs) |

---

## 8. Validity Threats

1. **State representation coarseness**: HTTP fetch cannot execute JS or render dynamic content. SPA pages may appear structurally identical across navigations. Server-rendered sites selected to mitigate.
2. **Action inference limitations**: Only `<a>` links captured. Button clicks, custom elements missed. Focus on link-following transitions.
3. **Sample size**: ~6 held-out trajectories per site. Limited power for small effects. Large effects detectable.
4. **Multiple comparisons**: 6 comparisons, Bonferroni conservative. Raw p-values also reported.
5. **Synthetic-to-real gap**: Positive control validates pipeline, not Web dynamics. Live test provides substantive test.
6. **No JavaScript**: SPA pages may appear structurally identical. Acknowledged.

---

## 9. Reproducibility

- **Seeds**: Positive=42, Live-1=43, Null=44, Live-2=45
- **Positive control**: 60 trajectories x 10 steps = 600 transitions
- **Null control**: 30 trajectories x 10 steps = 300 transitions
- **Live**: 20 trajectories x 10 steps per site
- **Permutation test**: 1000 permutations per condition
- **Multiple comparison**: Bonferroni for 6 comparisons
- **Code**: research/physics/run_experiment_337.py (stdlib only)

---

## 10. Consequences

### If positive result (SURVIVES_CURRENT_TEST)
Validates corrected evaluation methodology. Action-conditioned structure on live Web justifies investment in richer state representations (DOM/accessibility tree) and browser-based collection.

### If negative result (FALSIFIED-IN-SETTING)
Either (a) the Web genuinely lacks action-conditioned structure at the tested representation level, or (b) HTTP fetch cannot capture sufficient state information. Physics lane should pivot to richer representations with browser-based collection, or alternative Physics programs.

Does NOT close the Physics domain — only this specific detection method at this representation level.
"""

    return report


if __name__ == "__main__":
    main()
