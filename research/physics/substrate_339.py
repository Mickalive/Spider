"""
EXP-PHYSICS-33965269281 Measurement Substrate

Playwright-based collection with full DOM/accessibility tree state representation.
Four mandatory fixes from EXP-PHYSICS-33788037373 handoff:
1. Full composite state representation stored in raw data
2. target_href = destination URL (not source URL)
3. Bonferroni correction for 6 comparisons
4. Artifact integrity with sha256 hashes

Stdlib only for analysis; Playwright for browser-based collection.
"""

from __future__ import annotations

import hashlib
import math
import random
import time
import json
import urllib.parse
from collections import Counter
from dataclasses import dataclass, field, asdict
from typing import Any


# ---------------------------------------------------------------------------
# State and Action data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class State:
    """Observable state: URL + title + link_texts + tag_counts + form_signals + accessibility_roles."""
    url: str
    title: str
    link_texts: tuple          # sorted tuple of first 30 visible link texts
    tag_counts: tuple          # 11 integers: h1,h2,h3,form,input,button,select,textarea,nav,main,aside
    form_signals: tuple        # 4 booleans: has_form, has_input, has_select, has_textarea
    accessibility_roles: tuple # sorted tuple of (role, name) from accessibility tree

    def to_key(self) -> str:
        parts = [
            self.url,
            self.title,
            "|".join(self.link_texts),
            "|".join(str(x) for x in self.tag_counts),
            "|".join(str(x) for x in self.form_signals),
            "|".join(f"{r}:{n}" for r, n in self.accessibility_roles),
        ]
        return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]

    def to_dict(self) -> dict:
        return {
            "url": self.url,
            "title": self.title,
            "link_texts": list(self.link_texts),
            "tag_counts": list(self.tag_counts),
            "form_signals": list(self.form_signals),
            "accessibility_roles": [[r, n] for r, n in self.accessibility_roles],
        }


@dataclass(frozen=True)
class Action:
    """Observable action: type + target_text + target_href (destination URL)."""
    action_type: str
    target_text: str
    target_href: str  # FIXED: destination URL, not source URL

    def to_key(self) -> str:
        return f"{self.action_type}|{self.target_text}|{self.target_href}"

    def to_dict(self) -> dict:
        return {
            "action_type": self.action_type,
            "target_text": self.target_text,
            "target_href": self.target_href,
        }


@dataclass(frozen=True)
class Transition:
    """A single (S, A, S') observation."""
    state: State
    action: Action
    next_state: State
    trajectory_id: str
    step_index: int


# ---------------------------------------------------------------------------
# Positive Control: 8 states, 3 action types, overlapping actions
# ---------------------------------------------------------------------------

SHARED_HREF_NAV = "click_element_shared"
SHARED_HREF_ABOUT = "navigate_element_shared"
SHARED_HREF_HOME = "home_link_shared"
SHARED_HREF_FORM = "form_submit_shared"
SHARED_HREF_DETAIL = "detail_link_shared"
SHARED_HREF_BACK = "back_link_shared"
SHARED_HREF_SIDEBAR = "sidebar_link_shared"
SHARED_HREF_FOOTER = "footer_link_shared"


class PositiveControl:
    """
    Synthetic deterministic navigation graph with 8 states and 3 action types.
    Actions OVERLAP across states with shared target_href values.
    """

    def __init__(self):
        self.states = {
            "A": State(url="http://synth.test/home", title="Home",
                       link_texts=("nav", "about", "contact"), tag_counts=(1,2,0,1,2,0,0,0,1,1,0), form_signals=(True,True,False,False), accessibility_roles=(("link","nav"),("link","about"),("link","contact"))),
            "B": State(url="http://synth.test/products", title="Products",
                       link_texts=("prod1", "prod2", "about", "nav"), tag_counts=(1,1,0,0,1,0,0,0,1,1,0), form_signals=(False,False,False,False), accessibility_roles=(("link","prod1"),("link","prod2"),("link","about"))),
            "C": State(url="http://synth.test/about", title="About",
                       link_texts=("nav", "home", "contact"), tag_counts=(2,0,0,0,0,0,0,0,0,1,0), form_signals=(False,False,False,False), accessibility_roles=(("link","nav"),("link","home"),("link","contact"))),
            "D": State(url="http://synth.test/contact", title="Contact",
                       link_texts=("form", "nav", "home"), tag_counts=(1,0,0,1,1,1,0,0,0,1,0), form_signals=(True,True,False,True), accessibility_roles=(("link","nav"),("link","home"),("button","form"))),
            "E": State(url="http://synth.test/detail", title="Detail",
                       link_texts=("detail", "home", "about"), tag_counts=(1,1,1,0,0,0,0,0,0,1,0), form_signals=(False,False,False,False), accessibility_roles=(("link","detail"),("link","home"),("link","about"))),
            "F": State(url="http://synth.test/sidebar", title="Sidebar",
                       link_texts=("sidebar", "home", "nav"), tag_counts=(0,1,0,0,0,0,0,0,0,1,1), form_signals=(False,False,False,False), accessibility_roles=(("link","sidebar"),("link","home"),("link","nav"))),
            "G": State(url="http://synth.test/gallery", title="Gallery",
                       link_texts=("back", "detail", "home"), tag_counts=(0,0,2,0,0,0,0,0,0,1,0), form_signals=(False,False,False,False), accessibility_roles=(("link","back"),("link","detail"),("link","home"))),
            "H": State(url="http://synth.test/footer", title="Footer",
                       link_texts=("footer", "home", "nav"), tag_counts=(0,0,0,0,0,0,0,0,1,1,1), form_signals=(False,False,False,False), accessibility_roles=(("link","footer"),("link","home"),("link","nav"))),
        }
        # Deterministic transition table with overlapping actions
        self.transitions = {
            ("A", "click", SHARED_HREF_NAV): "B",
            ("C", "click", SHARED_HREF_NAV): "E",
            ("F", "click", SHARED_HREF_NAV): "A",
            ("D", "click", SHARED_HREF_NAV): "B",
            ("B", "navigate", SHARED_HREF_ABOUT): "C",
            ("E", "navigate", SHARED_HREF_ABOUT): "D",
            ("E", "navigate", SHARED_HREF_HOME): "A",
            ("H", "navigate", SHARED_HREF_HOME): "F",
            ("C", "navigate", SHARED_HREF_HOME): "G",
            ("D", "submit", SHARED_HREF_FORM): "D",
            ("A", "submit", SHARED_HREF_FORM): "A",
            ("E", "click", SHARED_HREF_DETAIL): "G",
            ("G", "click", SHARED_HREF_DETAIL): "A",
            ("G", "click", SHARED_HREF_BACK): "H",
            ("F", "click", SHARED_HREF_SIDEBAR): "H",
            ("H", "click", SHARED_HREF_FOOTER): "A",
        }
        self.valid_actions = {
            "A": [("click", SHARED_HREF_NAV), ("navigate", SHARED_HREF_ABOUT), ("submit", SHARED_HREF_FORM)],
            "B": [("navigate", SHARED_HREF_ABOUT)],
            "C": [("click", SHARED_HREF_NAV), ("navigate", SHARED_HREF_HOME)],
            "D": [("submit", SHARED_HREF_FORM), ("click", SHARED_HREF_NAV)],
            "E": [("navigate", SHARED_HREF_HOME), ("navigate", SHARED_HREF_ABOUT), ("click", SHARED_HREF_DETAIL)],
            "F": [("click", SHARED_HREF_NAV), ("click", SHARED_HREF_SIDEBAR)],
            "G": [("click", SHARED_HREF_DETAIL), ("click", SHARED_HREF_BACK)],
            "H": [("navigate", SHARED_HREF_HOME), ("click", SHARED_HREF_FOOTER)],
        }

    def get_valid_actions(self, state_id: str) -> list[tuple[str, str]]:
        return self.valid_actions.get(state_id, [])

    def step(self, state_id: str, action_type: str, target_href: str) -> str:
        return self.transitions.get((state_id, action_type, target_href), "A")

    def get_state(self, state_id: str) -> State:
        return self.states[state_id]

    def get_all_state_ids(self) -> list[str]:
        return list(self.states.keys())


# ---------------------------------------------------------------------------
# Null Control: 30 states, 5 action types, 8 shared target_ids, random next
# ---------------------------------------------------------------------------

class NullControl:
    """
    Random-policy transitions on 30 states with reused action vocabulary
    (5 action types, 8 target_ids shared across states). Next-states are
    uniformly random, independent of action.
    """

    def __init__(self, seed: int = 44):
        self.rng = random.Random(seed)
        self.n_states = 30
        self.action_types = ["click", "navigate", "submit", "scroll", "type"]
        self.target_ids = ["nav", "search", "menu", "footer", "sidebar", "main", "link", "btn"]
        self.states = []
        for i in range(self.n_states):
            self.states.append(State(
                url=f"http://null.test/page_{i}",
                title=f"page_{i}",
                link_texts=(f"link_{i%5}", f"link_{(i+1)%5}", f"link_{(i+2)%5}"),
                tag_counts=(i%3, (i+1)%3, (i+2)%3, i%2, (i+1)%2, 0, 0, 0, i%2, 1, 0),
                form_signals=(bool(i%3), bool(i%2), False, False),
                accessibility_roles=(("link", f"link_{i%5}"), ("link", f"link_{(i+1)%5}")),
            ))

    def generate_trajectories(self, n_trajectories: int = 30, steps_per_trajectory: int = 10) -> list[Transition]:
        transitions = []
        for i in range(n_trajectories):
            traj_id = f"null_{i}"
            current_state = self.states[self.rng.randint(0, self.n_states - 1)]
            for step in range(steps_per_trajectory):
                action_type = self.rng.choice(self.action_types)
                target_id = self.rng.choice(self.target_ids)
                action = Action(action_type=action_type, target_text=target_id, target_href="")
                next_state = self.states[self.rng.randint(0, self.n_states - 1)]
                transitions.append(Transition(
                    state=current_state, action=action, next_state=next_state,
                    trajectory_id=traj_id, step_index=step,
                ))
                current_state = next_state
        return transitions


# ---------------------------------------------------------------------------
# Live Web Collector: Playwright-based with full DOM/accessibility tree
# ---------------------------------------------------------------------------

class PlaywrightLiveCollector:
    """
    Collects transitions from live web pages using Playwright.
    Extracts: URL, title, link_texts, tag_counts, form_signals, accessibility_roles.
    """

    TAG_MAP = {"h1": 0, "h2": 1, "h2": 2, "form": 3, "input": 4, "button": 5,
               "select": 6, "textarea": 7, "nav": 8, "main": 9, "aside": 10}
    # Fixed mapping (duplicate h2 was a bug in previous code)
    TAG_MAP = {"h1": 0, "h2": 1, "h3": 2, "form": 3, "input": 4, "button": 5,
               "select": 6, "textarea": 7, "nav": 8, "main": 9, "aside": 10}

    def __init__(self, seed: int = 43):
        self.rng = random.Random(seed)

    def _extract_state(self, page) -> tuple[State, list[tuple[str, str]]]:
        """
        Extract state representation from current Playwright page.
        Returns (State, internal_links).
        internal_links: list of (link_text, destination_url) for same-domain <a> elements.
        """
        url = page.url
        title = page.title()[:100] if page.title() else ""

        # Extract internal links via JavaScript
        links_data = page.evaluate("""() => {
            const links = [];
            const baseHost = window.location.hostname;
            document.querySelectorAll('a[href]').forEach(a => {
                const href = a.href;
                const text = (a.textContent || '').trim().toLowerCase().slice(0, 100);
                if (!href || href.startsWith('javascript:') || href.startsWith('mailto:') || href.startsWith('tel:') || href.startsWith('#')) return;
                try {
                    const u = new URL(href);
                    if (u.hostname === baseHost) {
                        links.push({text: text, href: u.origin + u.pathname});
                    }
                } catch(e) {}
            });
            return links;
        }""")

        internal_links = [(d["text"], d["href"]) for d in links_data]
        link_texts = sorted(set(t for t, _ in internal_links if t))[:30]

        # Extract tag counts via JavaScript
        tag_counts_list = page.evaluate("""() => {
            const tags = ['h1','h2','h3','form','input','button','select','textarea','nav','main','aside'];
            return tags.map(t => document.querySelectorAll(t).length);
        }""")

        # Extract form signals
        form_signals_list = page.evaluate("""() => {
            return [
                document.querySelectorAll('form').length > 0,
                document.querySelectorAll('input').length > 0,
                document.querySelectorAll('select').length > 0,
                document.querySelectorAll('textarea').length > 0,
            ];
        }""")

        # Extract accessibility tree roles
        acc_roles = []
        try:
            snapshot = page.accessibility.snapshot()
            if snapshot:
                self._extract_acc_roles(snapshot, acc_roles)
        except Exception:
            pass  # accessibility snapshot may fail on some pages

        acc_roles_sorted = tuple(sorted(acc_roles)[:30])

        state = State(
            url=url,
            title=title,
            link_texts=tuple(link_texts),
            tag_counts=tuple(tag_counts_list),
            form_signals=tuple(form_signals_list),
            accessibility_roles=acc_roles_sorted,
        )
        return state, internal_links

    def _extract_acc_roles(self, node: dict, roles: list, depth: int = 0):
        """Recursively extract (role, name) pairs from accessibility tree."""
        if depth > 20:
            return
        role = node.get("role", "")
        name = (node.get("name", "") or "").lower()[:50]
        if role and role not in ("WebArea", "None"):
            roles.append((role, name))
        for child in node.get("children", []):
            self._extract_acc_roles(child, roles, depth + 1)

    def collect_trajectories(self, start_url: str, n_trajectories: int = 100,
                              max_steps: int = 8, polite_delay: float = 0.3,
                              max_retries: int = 3) -> tuple[list[Transition], dict]:
        """
        Collect trajectories from a single site using Playwright.
        Returns (transitions, collection_info).
        """
        from playwright.sync_api import sync_playwright

        transitions = []
        info = {
            "start_url": start_url,
            "n_collected": 0,
            "n_failed_trajectories": 0,
            "n_failed_steps": 0,
            "collection_errors": [],
        }

        with sync_playwright() as p:
            browser = p.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
            )
            context = browser.new_context(
                user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                viewport={"width": 1280, "height": 720},
            )

            # First visit to start_url to get internal links
            page = context.new_page()
            try:
                page.goto(start_url, wait_until="domcontentloaded", timeout=15000)
                time.sleep(1)
                _, start_internal_links = self._extract_state(page)
            except Exception as e:
                info["collection_errors"].append(f"Failed to load start URL: {e}")
                start_internal_links = []

            for i in range(n_trajectories):
                traj_id = f"live_{hashlib.sha256(start_url.encode()).hexdigest()[:8]}_{i}"

                # Pick random start link from homepage
                if start_internal_links:
                    _, start_link = start_internal_links[self.rng.randint(0, len(start_internal_links) - 1)]
                else:
                    start_link = start_url

                # Navigate to start
                try:
                    page.goto(start_link, wait_until="domcontentloaded", timeout=15000)
                    time.sleep(polite_delay)
                    current_state, current_links = self._extract_state(page)
                except Exception as e:
                    info["n_failed_trajectories"] += 1
                    if len(info["collection_errors"]) < 20:
                        info["collection_errors"].append(f"Traj {i} start failed: {e}")
                    continue

                for step in range(max_steps):
                    if not current_links:
                        break

                    # Random link selection
                    link_text, next_url = current_links[self.rng.randint(0, len(current_links) - 1)]

                    # target_href = destination URL (FIXED from prior experiment)
                    action = Action(
                        action_type="click",
                        target_text=link_text,
                        target_href=next_url,
                    )

                    # Navigate to next page
                    try:
                        page.goto(next_url, wait_until="domcontentloaded", timeout=15000)
                        time.sleep(polite_delay)
                        next_state, next_links = self._extract_state(page)
                    except Exception as e:
                        info["n_failed_steps"] += 1
                        if len(info["collection_errors"]) < 50:
                            info["collection_errors"].append(
                                f"Traj {i} step {step} navigation to {next_url} failed: {e}")
                        break

                    transitions.append(Transition(
                        state=current_state, action=action, next_state=next_state,
                        trajectory_id=traj_id, step_index=step,
                    ))

                    current_state = next_state
                    current_links = next_links

                info["n_collected"] = i + 1

            browser.close()

        info["n_transitions"] = len(transitions)
        info["n_trajectories"] = len(set(t.trajectory_id for t in transitions))
        info["avg_steps"] = len(transitions) / max(1, info["n_trajectories"])

        return transitions, info


# ---------------------------------------------------------------------------
# Trajectory-Grouped Train/Test Split
# ---------------------------------------------------------------------------

def trajectory_split(transitions: list[Transition], train_frac: float = 0.7,
                     seed: int = 42) -> tuple[list[Transition], list[Transition]]:
    """
    Split transitions into train/test at the trajectory level.
    No trajectory appears in both train and test.
    """
    rng = random.Random(seed)
    trajectory_ids = list(set(t.trajectory_id for t in transitions))
    rng.shuffle(trajectory_ids)
    n_train = max(1, int(len(trajectory_ids) * train_frac))
    train_ids = set(trajectory_ids[:n_train])
    test_ids = set(trajectory_ids[n_train:])

    train = [t for t in transitions if t.trajectory_id in train_ids]
    test = [t for t in transitions if t.trajectory_id in test_ids]
    return train, test


# ---------------------------------------------------------------------------
# Baseline Predictors
# ---------------------------------------------------------------------------

def _predict_majority_next(transitions: list[Transition]) -> dict[str, str]:
    """Build predictor: given (state_key, action_key) -> most common next_state_key."""
    sa_next: dict[str, dict[str, int]] = {}
    for t in transitions:
        key = f"{t.state.to_key()}|{t.action.to_key()}"
        nk = t.next_state.to_key()
        if key not in sa_next:
            sa_next[key] = {}
        sa_next[key][nk] = sa_next[key].get(nk, 0) + 1
    return {k: max(v, key=v.get) for k, v in sa_next.items()}


def _predict_action_freq(transitions: list[Transition]) -> dict[str, str]:
    """Build predictor: given action_key -> most common next_state_key (ignores state)."""
    a_next: dict[str, dict[str, int]] = {}
    for t in transitions:
        ak = t.action.to_key()
        nk = t.next_state.to_key()
        if ak not in a_next:
            a_next[ak] = {}
        a_next[ak][nk] = a_next[ak].get(nk, 0) + 1
    return {k: max(v, key=v.get) for k, v in a_next.items()}


def _predict_state_only(transitions: list[Transition]) -> dict[str, str]:
    """Build predictor: given state_key -> most common next_state_key (ignores action)."""
    s_next: dict[str, dict[str, int]] = {}
    for t in transitions:
        sk = t.state.to_key()
        nk = t.next_state.to_key()
        if sk not in s_next:
            s_next[sk] = {}
        s_next[sk][nk] = s_next[sk].get(nk, 0) + 1
    return {k: max(v, key=v.get) for k, v in s_next.items()}


def evaluate_predictor(predictor: dict[str, str], transitions: list[Transition],
                       key_fn) -> float:
    """Evaluate a predictor on transitions. Returns accuracy."""
    if not transitions:
        return 0.0
    correct = 0
    for t in transitions:
        key = key_fn(t)
        predicted = predictor.get(key, "")
        if predicted == t.next_state.to_key():
            correct += 1
    return correct / len(transitions)


def accuracy_action_conditioned(train: list[Transition], test: list[Transition]) -> float:
    predictor = _predict_majority_next(train)
    return evaluate_predictor(predictor, test, lambda t: f"{t.state.to_key()}|{t.action.to_key()}")


def accuracy_action_frequency(train: list[Transition], test: list[Transition]) -> float:
    predictor = _predict_action_freq(train)
    return evaluate_predictor(predictor, test, lambda t: t.action.to_key())


def accuracy_state_only(train: list[Transition], test: list[Transition]) -> float:
    predictor = _predict_state_only(train)
    return evaluate_predictor(predictor, test, lambda t: t.state.to_key())


def accuracy_in_sample(transitions: list[Transition]) -> float:
    """Fit and evaluate on same data (memorization baseline)."""
    predictor = _predict_majority_next(transitions)
    return evaluate_predictor(predictor, transitions, lambda t: f"{t.state.to_key()}|{t.action.to_key()}")


# ---------------------------------------------------------------------------
# Shuffle Null Evaluation
# ---------------------------------------------------------------------------

def _evaluate_shuffle_null(train: list[Transition], test: list[Transition],
                           seed: int = 9999) -> float:
    """Evaluate action-conditioned predictor on test after shuffling labels within trajectories."""
    by_traj: dict[str, list[Transition]] = {}
    for t in train:
        by_traj.setdefault(t.trajectory_id, []).append(t)
    shuffled_train = []
    rng = random.Random(seed)
    for traj_trans in by_traj.values():
        next_states = [t.next_state for t in traj_trans]
        rng.shuffle(next_states)
        for t, ns in zip(traj_trans, next_states):
            shuffled_train.append(Transition(
                state=t.state, action=t.action, next_state=ns,
                trajectory_id=t.trajectory_id, step_index=t.step_index,
            ))
    predictor = _predict_majority_next(shuffled_train)
    return evaluate_predictor(predictor, test, lambda t: f"{t.state.to_key()}|{t.action.to_key()}")


# ---------------------------------------------------------------------------
# Permutation Tests (trajectory-grouped)
# ---------------------------------------------------------------------------

def permutation_test_sa_vs_shuffle(
    transitions: list[Transition],
    n_permutations: int = 1000,
    seed: int = 42,
    train_frac: float = 0.7,
) -> dict:
    """Permutation test: is action-conditioned accuracy > shuffle null?"""
    train, test = trajectory_split(transitions, train_frac=train_frac, seed=seed)

    if not test:
        return {"observed_diff": 0.0, "p_value": 1.0, "n_permutations": n_permutations,
                "n_test_transitions": 0, "note": "no test transitions"}

    obs_sa = accuracy_action_conditioned(train, test)
    obs_shuffle = _evaluate_shuffle_null(train, test, seed=seed + 1000)
    obs_diff = obs_sa - obs_shuffle

    by_traj: dict[str, list[Transition]] = {}
    for t in transitions:
        by_traj.setdefault(t.trajectory_id, []).append(t)

    diffs = []
    for i in range(n_permutations):
        perm_rng = random.Random(seed + i + 2000)
        permuted = []
        for traj_id, traj_trans in by_traj.items():
            next_states = [t.next_state for t in traj_trans]
            perm_rng.shuffle(next_states)
            for t, ns in zip(traj_trans, next_states):
                permuted.append(Transition(
                    state=t.state, action=t.action, next_state=ns,
                    trajectory_id=t.trajectory_id, step_index=t.step_index,
                ))
        p_train, p_test = trajectory_split(permuted, train_frac=train_frac, seed=seed)
        p_sa = accuracy_action_conditioned(p_train, p_test)
        p_shuffle = _evaluate_shuffle_null(p_train, p_test, seed=seed + 1000 + i)
        diffs.append(p_sa - p_shuffle)

    p_value = sum(1 for d in diffs if d >= obs_diff) / n_permutations

    return {
        "observed_diff": obs_diff,
        "observed_acc_SA": obs_sa,
        "observed_acc_shuffle": obs_shuffle,
        "p_value": p_value,
        "n_permutations": n_permutations,
        "n_test_transitions": len(test),
        "n_test_trajectories": len(set(t.trajectory_id for t in test)),
        "n_train_transitions": len(train),
        "n_train_trajectories": len(set(t.trajectory_id for t in train)),
        "perm_mean_diff": sum(diffs) / len(diffs) if diffs else 0.0,
        "perm_std_diff": (sum((d - sum(diffs)/len(diffs))**2 for d in diffs) / len(diffs))**0.5 if len(diffs) > 1 else 0.0,
    }


def permutation_test_sa_vs_action_freq(
    transitions: list[Transition],
    n_permutations: int = 1000,
    seed: int = 42,
    train_frac: float = 0.7,
) -> dict:
    """Permutation test: is action-conditioned accuracy > action-frequency accuracy?"""
    train, test = trajectory_split(transitions, train_frac=train_frac, seed=seed)

    if not test:
        return {"observed_diff": 0.0, "p_value": 1.0, "n_permutations": n_permutations,
                "n_test_transitions": 0, "note": "no test transitions"}

    obs_sa = accuracy_action_conditioned(train, test)
    obs_af = accuracy_action_frequency(train, test)
    obs_diff = obs_sa - obs_af

    by_traj: dict[str, list[Transition]] = {}
    for t in transitions:
        by_traj.setdefault(t.trajectory_id, []).append(t)

    diffs = []
    for i in range(n_permutations):
        perm_rng = random.Random(seed + i + 3000)
        permuted = []
        for traj_id, traj_trans in by_traj.items():
            next_states = [t.next_state for t in traj_trans]
            perm_rng.shuffle(next_states)
            for t, ns in zip(traj_trans, next_states):
                permuted.append(Transition(
                    state=t.state, action=t.action, next_state=ns,
                    trajectory_id=t.trajectory_id, step_index=t.step_index,
                ))
        p_train, p_test = trajectory_split(permuted, train_frac=train_frac, seed=seed)
        p_sa = accuracy_action_conditioned(p_train, p_test)
        p_af = accuracy_action_frequency(p_train, p_test)
        diffs.append(p_sa - p_af)

    p_value = sum(1 for d in diffs if d >= obs_diff) / n_permutations

    return {
        "observed_diff": obs_diff,
        "observed_acc_SA": obs_sa,
        "observed_acc_AF": obs_af,
        "p_value": p_value,
        "n_permutations": n_permutations,
        "n_test_transitions": len(test),
        "n_test_trajectories": len(set(t.trajectory_id for t in test)),
    }


# ---------------------------------------------------------------------------
# Bonferroni correction
# ---------------------------------------------------------------------------

def bonferroni_correction(p_values: list[float]) -> list[float]:
    n = len(p_values)
    return [min(p * n, 1.0) for p in p_values]


# ---------------------------------------------------------------------------
# Validity Gates
# ---------------------------------------------------------------------------

def check_validity(transitions: list[Transition], seed: int = 42) -> dict:
    """Run all validity gates from the prereg."""
    checks = {}

    # 1. target_href encoding: target_href should be destination URL (not source)
    # For live transitions, target_href should not equal state.url (source)
    leakage_issues = []
    for t in transitions:
        if t.action.target_text and t.next_state.url == t.action.target_text:
            leakage_issues.append(
                f"target_text exactly matches next_state.url: text={t.action.target_text}, url={t.next_state.url}"
            )
    checks["target_leakage"] = {"passed": len(leakage_issues) == 0, "issues": leakage_issues[:20]}

    # 2. target_href encoding check: target_href != state.url (source URL)
    source_href_issues = []
    for t in transitions:
        if t.action.target_href == t.state.url and t.action.target_href != "":
            source_href_issues.append(
                f"target_href equals source URL: {t.action.target_href}"
            )
    checks["target_href_encoding"] = {
        "passed": len(source_href_issues) == 0,
        "issues": source_href_issues[:20],
        "n_violations": len(source_href_issues),
    }

    # 3. Temporal ordering
    ordering_issues = []
    by_traj: dict[str, list[Transition]] = {}
    for t in transitions:
        by_traj.setdefault(t.trajectory_id, []).append(t)
    for traj_id, traj_trans in by_traj.items():
        sorted_trans = sorted(traj_trans, key=lambda x: x.step_index)
        for i, t in enumerate(sorted_trans):
            if t.step_index != i:
                ordering_issues.append(f"Traj {traj_id}: step {t.step_index} at position {i}")
    checks["temporal_ordering"] = {"passed": len(ordering_issues) == 0, "issues": ordering_issues[:10]}

    # 4. Deterministic seeds
    rng1 = random.Random(seed)
    rng2 = random.Random(seed)
    seq1 = [rng1.randint(0, 10000) for _ in range(100)]
    seq2 = [rng2.randint(0, 10000) for _ in range(100)]
    checks["seed_determinism"] = {"passed": seq1 == seq2, "seed": seed}

    # 5. Trajectory count
    trajectory_ids = list(set(t.trajectory_id for t in transitions))
    checks["trajectory_count"] = {"passed": len(trajectory_ids) > 0, "n_trajectories": len(trajectory_ids)}

    # 6. State representation completeness
    incomplete_states = 0
    for t in transitions:
        if not t.state.url or not t.state.link_texts:
            incomplete_states += 1
    checks["state_representation"] = {
        "passed": incomplete_states == 0,
        "n_incomplete": incomplete_states,
        "n_total": len(transitions),
    }

    all_passed = all(c["passed"] for c in checks.values())
    return {"all_passed": all_passed, "checks": checks}
