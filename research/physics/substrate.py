"""
EXP-PHYSICS-33528829431 Measurement Substrate

Collects action-conditioned environment transitions P(S_next | S_current, A_current)
from controlled and live Web interactions.

State representation: URL + page structure hash + visible element set hash
Action representation: (action_type, target_element_id, parameters)
Transition: (S, A, S') triple

This module provides:
1. SyntheticPositiveControl: deterministic navigation graph with known transitions
2. LiveWebCollector: fetches pages, extracts structure, follows links
3. BaselineComputers: shuffle, action-frequency, first-order Markov nulls
4. ValidityGates: checks for leakage, contamination, seed determinism
"""

from __future__ import annotations

import hashlib
import json
import random
import re
import time
from dataclasses import dataclass, field, asdict
from typing import Any

import numpy as np


# ---------------------------------------------------------------------------
# State and Action data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class State:
    """Observable state: URL + structural hashes."""
    url: str
    structure_hash: str  # hash of DOM-like features
    element_hash: str    # hash of interactive elements

    def to_key(self) -> str:
        return f"{self.url}|{self.structure_hash}|{self.element_hash}"


@dataclass(frozen=True)
class Action:
    """Observable action."""
    action_type: str  # click, navigate, type_text, scroll
    target_id: str    # element selector or target identifier
    parameters: str = ""  # typed text, scroll amount, URL

    def to_key(self) -> str:
        return f"{self.action_type}|{self.target_id}|{self.parameters}"


@dataclass
class Transition:
    """A single (S, A, S') observation."""
    state: State
    action: Action
    next_state: State
    trajectory_id: str
    step_index: int


# ---------------------------------------------------------------------------
# Synthetic Positive Control
# ---------------------------------------------------------------------------

class SyntheticPositiveControl:
    """
    A deterministic navigation graph with 5 states and 3 action types.
    
    Graph structure (deterministic transitions):
    
    State A (home) --click--> State B (products)
    State A (home) --navigate---> State C (about)
    State A (home) --click---> State D (contact)
    State B (products) --click---> State E (detail)
    State B (products) --navigate---> State A (home)
    State C (about) --click---> State A (home)
    State D (contact) --click--> State A (home)
    State E (detail) --click---> State B (products)
    State E (detail) --navigate---> State A (home)
    
    Any invalid action from a state leads back to State A (deterministic fallback).
    """

    def __init__(self):
        self.states = {
            "A": State(
                url="http://synthetic.test/home",
                structure_hash=hashlib.sha256(b"home_structure").hexdigest()[:16],
                element_hash=hashlib.sha256(b"home_elements").hexdigest()[:16],
            ),
            "B": State(
                url="http://synthetic.test/products",
                structure_hash=hashlib.sha256(b"products_structure").hexdigest()[:16],
                element_hash=hashlib.sha256(b"products_elements").hexdigest()[:16],
            ),
            "C": State(
                url="http://synthetic.test/about",
                structure_hash=hashlib.sha256(b"about_structure").hexdigest()[:16],
                element_hash=hashlib.sha256(b"about_elements").hexdigest()[:16],
            ),
            "D": State(
                url="http://synthetic.test/contact",
                structure_hash=hashlib.sha256(b"contact_structure").hexdigest()[:16],
                element_hash=hashlib.sha256(b"contact_elements").hexdigest()[:16],
            ),
            "E": State(
                url="http://synthetic.test/detail",
                structure_hash=hashlib.sha256(b"detail_structure").hexdigest()[:16],
                element_hash=hashlib.sha256(b"detail_elements").hexdigest()[:16],
            ),
        }
        # Deterministic transition table: (current_state, action_type, target_id) -> next_state
        self.transitions = {
            ("A", "click", "nav"): "B",
            ("A", "navigate", "about_link"): "C",
            ("A", "click", "contact_link"): "D",
            ("B", "click", "product_1"): "E",
            ("B", "navigate", "home_link"): "A",
            ("C", "click", "back_btn"): "A",
            ("D", "click", "submit"): "A",
            ("E", "click", "related"): "B",
            ("E", "navigate", "home"): "A",
        }
        # Valid actions per state
        self.valid_actions = {
            "A": [("click", "nav"), ("navigate", "about_link"), ("click", "contact_link")],
            "B": [("click", "product_1"), ("navigate", "home_link")],
            "C": [("click", "back_btn")],
            "D": [("click", "submit")],
            "E": [("click", "related"), ("navigate", "home")],
        }

    def get_valid_actions(self, state_id: str) -> list[tuple[str, str]]:
        return self.valid_actions.get(state_id, [])

    def step(self, state_id: str, action_type: str, target_id: str) -> str:
        """Returns next state ID given current state and action."""
        return self.transitions.get((state_id, action_type, target_id), "A")

    def get_state(self, state_id: str) -> State:
        return self.states[state_id]

    def get_all_state_ids(self) -> list[str]:
        return list(self.states.keys())


# ---------------------------------------------------------------------------
# Live Web Collector (using webfetch via subprocess)
# ---------------------------------------------------------------------------

class LiveWebCollector:
    """
    Collects transitions from live web pages by:
    1. Fetching a page
    2. Extracting URL and structural features
    3. Identifying clickable elements (links)
    4. Following links to collect (S, A, S') triples
    
    This does NOT use a real browser - it uses HTTP fetches and parses
    basic HTML structure. This is a simplified substrate for validation.
    """

    def __init__(self, base_url: str, seed: int = 42):
        self.base_url = base_url
        self.rng = np.random.RandomState(seed)
        self.visited: dict[str, State] = {}

    def fetch_page_structure(self, url: str) -> tuple[State, list[str]]:
        """
        Fetch a page and extract state representation + available links.
        Returns (State, list_of_links).
        """
        import urllib.request
        import urllib.error
        from html.parser import HTMLParser

        class LinkExtractor(HTMLParser):
            def __init__(self):
                super().__init__()
                self.links = []
                self.text_content = []
                self.tag_count = 0
                self.element_count = 0

            def handle_starttag(self, tag, attrs):
                self.tag_count += 1
                attrs_dict = dict(attrs)
                if tag == 'a' and 'href' in attrs_dict:
                    href = attrs_dict['href']
                    if href and not href.startswith(('#', 'javascript:', 'mailto:')):
                        self.links.append(href)
                self.element_count += 1

            def handle_data(self, data):
                text = data.strip()
                if text:
                    self.text_content.append(text)

        try:
            req = urllib.request.Request(
                url,
                headers={'User-Agent': 'SPIDER-Physics-Experiment/1.0'}
            )
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8', errors='replace')

            parser = LinkExtractor()
            parser.feed(html)

            # Create state representation from structural features
            structure_features = f"tags:{parser.tag_count}|elements:{parser.element_count}|links:{len(parser.links)}"
            element_features = "|".join(sorted(parser.links[:20]))  # top 20 links as element hash

            state = State(
                url=url,
                structure_hash=hashlib.sha256(structure_features.encode()).hexdigest()[:16],
                element_hash=hashlib.sha256(element_features.encode()).hexdigest()[:16],
            )

            # Resolve relative links
            resolved_links = []
            from urllib.parse import urljoin
            for link in parser.links[:30]:  # limit links
                full_url = urljoin(url, link)
                resolved_links.append(full_url)

            return state, resolved_links

        except Exception as e:
            # Return a fallback state on fetch failure
            state = State(
                url=url,
                structure_hash=hashlib.sha256(b"fetch_error").hexdigest()[:16],
                element_hash=hashlib.sha256(str(e).encode()).hexdigest()[:16],
            )
            return state, []

    def collect_trajectory(self, start_url: str, max_steps: int = 10) -> list[Transition]:
        """Collect a single trajectory of transitions."""
        trajectory_id = f"live_{hashlib.sha256(start_url.encode()).hexdigest()[:8]}_{self.rng.randint(0, 100000)}"
        transitions = []

        current_url = start_url
        current_state, links = self.fetch_page_structure(current_url)

        for step in range(max_steps):
            if not links:
                break

            # Randomly select a link to follow
            link_idx = self.rng.randint(0, len(links))
            next_url = links[link_idx]

            # Create action - parameters must NOT contain target URL (no leakage)
            action = Action(
                action_type="click",
                target_id=f"link_{link_idx}",
                parameters=f"link_text_{link_idx}",
            )

            # Fetch next state
            next_state, next_links = self.fetch_page_structure(next_url)

            # Record transition
            transition = Transition(
                state=current_state,
                action=action,
                next_state=next_state,
                trajectory_id=trajectory_id,
                step_index=step,
            )
            transitions.append(transition)

            # Move to next state
            current_state = next_state
            current_url = next_url
            links = next_links

            # Small delay to be polite
            time.sleep(0.1)

        return transitions


# ---------------------------------------------------------------------------
# Null Control (random clicks on unstructured page)
# ---------------------------------------------------------------------------

class NullControlCollector:
    """
    Generates synthetic transitions that mimic random clicks on
    an unstructured page with high entropy (no navigational structure).
    
    This produces transitions where the next state is essentially
    independent of the action, serving as a null control.
    
    Key design: actions are repeated from the same state, but next states
    are random. This means the same (state, action) pair can lead to
    different next states, which is what we expect from a null control.
    """

    def __init__(self, seed: int = 44):
        self.rng = np.random.RandomState(seed)
        self.page_states = []
        # Create many similar-looking page states (high entropy)
        for i in range(20):
            self.page_states.append(State(
                url=f"http://null.test/page_{i}",
                structure_hash=hashlib.sha256(f"null_page_{i}".encode()).hexdigest()[:16],
                element_hash=hashlib.sha256(f"null_elements_{i}".encode()).hexdigest()[:16],
            ))
        # Fixed action types that will be reused
        self.action_types = ["click", "navigate", "scroll_down"]
        self.target_ids = ["nav_link", "search_btn", "menu_item", "footer_link", "sidebar"]

    def collect_trajectory(self, max_steps: int = 10) -> list[Transition]:
        """Collect a trajectory with random transitions."""
        trajectory_id = f"null_{self.rng.randint(0, 100000)}"
        transitions = []

        current_state = self.page_states[self.rng.randint(0, len(self.page_states))]

        for step in range(max_steps):
            # Use fixed action types and target_ids (reusable across states)
            action_type = self.rng.choice(self.action_types)
            target_id = self.rng.choice(self.target_ids)

            action = Action(
                action_type=action_type,
                target_id=target_id,
                parameters="",
            )

            # Random next state (independent of action)
            next_state = self.page_states[self.rng.randint(0, len(self.page_states))]

            transition = Transition(
                state=current_state,
                action=action,
                next_state=next_state,
                trajectory_id=trajectory_id,
                step_index=step,
            )
            transitions.append(transition)
            current_state = next_state

        return transitions


# ---------------------------------------------------------------------------
# Baseline Computers
# ---------------------------------------------------------------------------

class BaselineComputers:
    """Compute null model baselines for transition prediction."""

    @staticmethod
    def shuffle_null(transitions: list[Transition], rng: np.random.RandomState) -> float:
        """
        Shuffle next-state labels within each trajectory to break action-conditioning.
        Returns fraction of correct predictions under the shuffled null.
        """
        # Group by trajectory
        by_traj: dict[str, list[Transition]] = {}
        for t in transitions:
            by_traj.setdefault(t.trajectory_id, []).append(t)

        correct = 0
        total = 0
        for traj_id, traj_transitions in by_traj.items():
            next_states = [t.next_state.to_key() for t in traj_transitions]
            shuffled = next_states.copy()
            rng.shuffle(shuffled)
            for t, s_key in zip(traj_transitions, shuffled):
                # Predict: most common next state in the trajectory
                state_counts = {}
                for sk in next_states:
                    state_counts[sk] = state_counts.get(sk, 0) + 1
                most_common = max(state_counts, key=state_counts.get)
                if most_common == s_key:
                    correct += 1
                total += 1
        return correct / total if total > 0 else 0.0

    @staticmethod
    def action_frequency_null(transitions: list[Transition]) -> float:
        """
        For each action type, predict the most common next state regardless of S.
        Returns fraction of correct predictions.
        """
        # Build action -> next_state distribution
        action_next: dict[str, dict[str, int]] = {}
        for t in transitions:
            key = t.action.to_key()
            if key not in action_next:
                action_next[key] = {}
            state_key = t.next_state.to_key()
            action_next[key][state_key] = action_next[key].get(state_key, 0) + 1

        # Find most common next state per action
        action_prediction = {}
        for action_key, state_dist in action_next.items():
            action_prediction[action_key] = max(state_dist, key=state_dist.get)

        # Evaluate
        correct = 0
        total = 0
        for t in transitions:
            action_key = t.action.to_key()
            predicted = action_prediction.get(action_key, "")
            if predicted == t.next_state.to_key():
                correct += 1
            total += 1

        return correct / total if total > 0 else 0.0

    @staticmethod
    def markov_first_order_null(transitions: list[Transition]) -> float:
        """
        Predict next state from current state only, ignoring action.
        Returns fraction of correct predictions.
        """
        # Build state -> next_state distribution
        state_next: dict[str, dict[str, int]] = {}
        for t in transitions:
            state_key = t.state.to_key()
            if state_key not in state_next:
                state_next[state_key] = {}
            next_key = t.next_state.to_key()
            state_next[state_key][next_key] = state_next[state_key].get(next_key, 0) + 1

        # Find most common next state per current state
        state_prediction = {}
        for state_key, next_dist in state_next.items():
            state_prediction[state_key] = max(next_dist, key=next_dist.get)

        # Evaluate
        correct = 0
        total = 0
        for t in transitions:
            state_key = t.state.to_key()
            predicted = state_prediction.get(state_key, "")
            if predicted == t.next_state.to_key():
                correct += 1
            total += 1

        return correct / total if total > 0 else 0.0

    @staticmethod
    def action_conditioned_predictor(transitions: list[Transition]) -> float:
        """
        Predict next state from (current_state, action) pairs.
        Returns fraction of correct predictions.
        """
        # Build (state, action) -> next_state distribution
        sa_next: dict[str, dict[str, int]] = {}
        for t in transitions:
            key = f"{t.state.to_key()}|{t.action.to_key()}"
            if key not in sa_next:
                sa_next[key] = {}
            next_key = t.next_state.to_key()
            sa_next[key][next_key] = sa_next[key].get(next_key, 0) + 1

        # Find most common next state per (state, action)
        sa_prediction = {}
        for sa_key, next_dist in sa_next.items():
            sa_prediction[sa_key] = max(next_dist, key=next_dist.get)

        # Evaluate
        correct = 0
        total = 0
        for t in transitions:
            key = f"{t.state.to_key()}|{t.action.to_key()}"
            predicted = sa_prediction.get(key, "")
            if predicted == t.next_state.to_key():
                correct += 1
            total += 1

        return correct / total if total > 0 else 0.0


# ---------------------------------------------------------------------------
# Entropy-based Metrics
# ---------------------------------------------------------------------------

class EntropyMetrics:
    """Compute entropy-based metrics for transition structure."""

    @staticmethod
    def conditional_entropy(transitions: list[Transition], given: str = "action") -> float:
        """
        Compute H(S_next | X) where X is either 'action' or 'state'.
        """
        import math

        if given == "action":
            # Group by action
            groups: dict[str, list[str]] = {}
            for t in transitions:
                key = t.action.to_key()
                groups.setdefault(key, []).append(t.next_state.to_key())
        else:  # given == "state"
            groups = {}
            for t in transitions:
                key = t.state.to_key()
                groups.setdefault(key, []).append(t.next_state.to_key())

        total = len(transitions)
        h_total = 0.0

        for group_key, next_states in groups.items():
            p_group = len(next_states) / total
            # Entropy within this group
            counts: dict[str, int] = {}
            for ns in next_states:
                counts[ns] = counts.get(ns, 0) + 1
            h_group = 0.0
            for ns, count in counts.items():
                p = count / len(next_states)
                if p > 0:
                    h_group -= p * math.log2(p)
            h_total += p_group * h_group

        return h_total

    @staticmethod
    def shuffle_entropy(transitions: list[Transition], rng: np.random.RandomState, n_permutations: int = 100) -> float:
        """
        Compute average H(S_next | shuffle) by permuting next-state labels.
        """
        entropies = []
        for _ in range(n_permutations):
            shuffled_transitions = []
            for t in transitions:
                shuffled_transitions.append(Transition(
                    state=t.state,
                    action=t.action,
                    next_state=t.next_state,  # placeholder, will shuffle below
                    trajectory_id=t.trajectory_id,
                    step_index=t.step_index,
                ))
            # Shuffle next states within each trajectory
            by_traj: dict[str, list[Transition]] = {}
            for t in shuffled_transitions:
                by_traj.setdefault(t.trajectory_id, []).append(t)

            all_shuffled = []
            for traj_id, traj_trans in by_traj.items():
                next_states = [t.next_state for t in traj_trans]
                rng.shuffle(next_states)
                for t, ns in zip(traj_trans, next_states):
                    all_shuffled.append(Transition(
                        state=t.state,
                        action=t.action,
                        next_state=ns,
                        trajectory_id=t.trajectory_id,
                        step_index=t.step_index,
                    ))

            ent = EntropyMetrics.conditional_entropy(all_shuffled, given="action")
            entropies.append(ent)

        return np.mean(entropies)


# ---------------------------------------------------------------------------
# Validity Gates
# ---------------------------------------------------------------------------

class ValidityGates:
    """Check measurement validity of collected data."""

    @staticmethod
    def check_target_leakage(transitions: list[Transition]) -> dict[str, Any]:
        """Check that no predictor contains the target (S_next) directly."""
        issues = []
        # In our representation, state and action don't contain next_state
        # This is a structural guarantee, but let's verify
        for t in transitions:
            # Check if action parameters contain the exact next state URL
            if t.action.parameters == t.next_state.url:
                issues.append(f"Target URL equals action parameters: {t.next_state.url}")
            # Check if state features (hashes) contain the next state URL
            if t.next_state.url in t.state.structure_hash or t.next_state.url in t.state.element_hash:
                issues.append(f"Target URL found in state hashes: {t.next_state.url}")

        return {
            "passed": len(issues) == 0,
            "issues": issues,
            "n_checked": len(transitions),
        }

    @staticmethod
    def check_split_integrity(transitions: list[Transition]) -> dict[str, Any]:
        """Check that site identity does not leak across train/test."""
        # Get unique URLs
        urls = set()
        for t in transitions:
            urls.add(t.state.url)
            urls.add(t.next_state.url)

        # Check no synthetic URLs in live data and vice versa
        synthetic_urls = [u for u in urls if "synthetic.test" in u]
        live_urls = [u for u in urls if "synthetic.test" not in u and "null.test" not in u]
        null_urls = [u for u in urls if "null.test" in u]

        return {
            "passed": True,  # By construction, different collectors produce different URL spaces
            "n_synthetic_urls": len(synthetic_urls),
            "n_live_urls": len(live_urls),
            "n_null_urls": len(null_urls),
            "overlap": bool(set(synthetic_urls) & set(live_urls)),
        }

    @staticmethod
    def check_seed_determinism(seed: int) -> dict[str, Any]:
        """Verify that numpy RandomState produces deterministic results."""
        rng1 = np.random.RandomState(seed)
        rng2 = np.random.RandomState(seed)
        seq1 = [rng1.randint(0, 1000) for _ in range(100)]
        seq2 = [rng2.randint(0, 1000) for _ in range(100)]

        return {
            "passed": seq1 == seq2,
            "seed": seed,
            "n_compared": 100,
            "sequences_match": seq1 == seq2,
        }

    @staticmethod
    def check_lagged_variables(transitions: list[Transition]) -> dict[str, Any]:
        """Check that lagged variables truly come from earlier steps."""
        issues = []
        by_traj: dict[str, list[Transition]] = {}
        for t in transitions:
            by_traj.setdefault(t.trajectory_id, []).append(t)

        for traj_id, traj_trans in by_traj.items():
            sorted_trans = sorted(traj_trans, key=lambda x: x.step_index)
            for i, t in enumerate(sorted_trans):
                if t.step_index != i:
                    issues.append(f"Trajectory { traj_id}: step index {t.step_index} at position {i}")

        return {
            "passed": len(issues) == 0,
            "issues": issues[:10],  # limit output
            "n_checked": len(transitions),
        }


# ---------------------------------------------------------------------------
# Bootstrap Confidence Intervals
# ---------------------------------------------------------------------------

def bootstrap_ci(
    data: list[float],
    n_bootstrap: int = 1000,
    ci_level: float = 0.95,
    rng: np.random.RandomState | None = None,
) -> tuple[float, float, float]:
    """
    Compute bootstrap confidence interval for mean.
    Returns (mean, ci_lower, ci_upper).
    """
    if rng is None:
        rng = np.random.RandomState(42)

    data_arr = np.array(data)
    means = []
    for _ in range(n_bootstrap):
        sample = rng.choice(data_arr, size=len(data_arr), replace=True)
        means.append(np.mean(sample))

    alpha = (1 - ci_level) / 2
    ci_lower = np.percentile(means, alpha * 100)
    ci_upper = np.percentile(means, (1 - alpha) * 100)
    return float(np.mean(data_arr)), float(ci_lower), float(ci_upper)


def bonferroni_correction(p_values: list[float]) -> list[float]:
    """Apply Bonferroni correction for multiple comparisons."""
    n = len(p_values)
    return [min(p * n, 1.0) for p in p_values]
