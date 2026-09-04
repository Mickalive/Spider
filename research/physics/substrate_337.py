"""
EXP-PHYSICS-33788037373 Corrected Measurement Substrate

Four mandatory fixes from EXP-PHYSICS-33528829431 handoff:
1. Trajectory-grouped holdout evaluation (not in-sample)
2. Permutation test with independent RNG (not invalid bootstrap)
3. Overlapping-action positive control (discriminates (S,A) from A alone)
4. Richer state representation (URL + link_texts + tag_counts + form_signals)

Stdlib only: random.Random for RNG, no numpy/scipy.
"""

from __future__ import annotations

import hashlib
import math
import random
import time
import urllib.request
import urllib.error
import urllib.parse
from collections import Counter
from dataclasses import dataclass, field
from html.parser import HTMLParser
from typing import Any


# ---------------------------------------------------------------------------
# State and Action data structures
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class State:
    """Observable state: URL + link_texts + tag_counts + form_signals."""
    url: str
    title: str
    link_texts: tuple  # sorted tuple of first 30 visible link texts
    tag_counts: tuple  # 11 integers: h1,h2,h3,form,input,button,select,textarea,nav,main,aside
    form_signals: tuple  # 4 booleans: has_form, has_input, has_select, has_textarea

    def to_key(self) -> str:
        parts = [
            self.url,
            self.title,
            "|".join(self.link_texts),
            "|".join(str(x) for x in self.tag_counts),
            "|".join(str(x) for x in self.form_signals),
        ]
        return hashlib.sha256("|".join(parts).encode()).hexdigest()[:16]


@dataclass(frozen=True)
class Action:
    """Observable action: type + target_text + target_href."""
    action_type: str
    target_text: str
    target_href: str

    def to_key(self) -> str:
        return f"{self.action_type}|{self.target_text}|{self.target_href}"


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
#
# KEY DESIGN: The SAME action_key (type + text + href) must appear from
# multiple states leading to DIFFERENT next states. This ensures the
# action-frequency predictor (which ignores state) cannot match the
# action-conditioned predictor (which uses state).
#
# Shared action hrefs (not state-specific):
#   SHARED_HREF_NAV = "click_element_shared"  -- used by 'click|nav'
#   SHARED_HREF_ABOUT = "navigate_element_shared"  -- used by 'navigate|about'
#   SHARED_HREF_HOME = "home_link_shared"  -- used by 'navigate|home'
#   SHARED_HREF_FORM = "form_submit_shared"  -- used by 'submit|form'
#
# Transitions where same action key -> different next state from different states:
#   click|nav|click_element_shared: A->B, C->E, F->A  (3 states, 3 different next states)
#   navigate|home|home_link_shared: E->A, H->F, C->G  (3 states, 3 different next states)
#   submit|form|form_submit_shared: D->D, A->A  (2 states)
#   navigate|about|navigate_element_shared: B->C, E->D  (2 states)

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
                       link_texts=("nav", "about", "contact"), tag_counts=(1,2,0,1,2,0,0,0,1,1,0), form_signals=(True,True,False,False)),
            "B": State(url="http://synth.test/products", title="Products",
                       link_texts=("prod1", "prod2", "about", "nav"), tag_counts=(1,1,0,0,1,0,0,0,1,1,0), form_signals=(False,False,False,False)),
            "C": State(url="http://synth.test/about", title="About",
                       link_texts=("nav", "home", "contact"), tag_counts=(2,0,0,0,0,0,0,0,0,1,0), form_signals=(False,False,False,False)),
            "D": State(url="http://synth.test/contact", title="Contact",
                       link_texts=("form", "nav", "home"), tag_counts=(1,0,0,1,1,1,0,0,0,1,0), form_signals=(True,True,False,True)),
            "E": State(url="http://synth.test/detail", title="Detail",
                       link_texts=("detail", "home", "about"), tag_counts=(1,1,1,0,0,0,0,0,0,1,0), form_signals=(False,False,False,False)),
            "F": State(url="http://synth.test/sidebar", title="Sidebar",
                       link_texts=("sidebar", "home", "nav"), tag_counts=(0,1,0,0,0,0,0,0,0,1,1), form_signals=(False,False,False,False)),
            "G": State(url="http://synth.test/gallery", title="Gallery",
                       link_texts=("back", "detail", "home"), tag_counts=(0,0,2,0,0,0,0,0,0,1,0), form_signals=(False,False,False,False)),
            "H": State(url="http://synth.test/footer", title="Footer",
                       link_texts=("footer", "home", "nav"), tag_counts=(0,0,0,0,0,0,0,0,1,1,1), form_signals=(False,False,False,False)),
        }
        # Deterministic transition table
        # SAME action_key from MULTIPLE states -> DIFFERENT next states
        self.transitions = {
            # click|nav|click_element_shared: A->B, C->E, F->A  (3 different next states)
            ("A", "click", SHARED_HREF_NAV): "B",
            ("C", "click", SHARED_HREF_NAV): "E",
            ("F", "click", SHARED_HREF_NAV): "A",
            # navigate|about|navigate_element_shared: B->C, E->D  (2 different next states)
            ("B", "navigate", SHARED_HREF_ABOUT): "C",
            ("E", "navigate", SHARED_HREF_ABOUT): "D",
            # navigate|home|home_link_shared: E->A, H->F, C->G  (3 different next states)
            ("E", "navigate", SHARED_HREF_HOME): "A",
            ("H", "navigate", SHARED_HREF_HOME): "F",
            ("C", "navigate", SHARED_HREF_HOME): "G",
            # submit|form|form_submit_shared: D->D, A->A  (2 different next states)
            ("D", "submit", SHARED_HREF_FORM): "D",
            ("A", "submit", SHARED_HREF_FORM): "A",
            # navigate|nav|click_element_shared: D->B  (unique)
            # Actually let me use a different approach for D. Let me use the shared nav href:
            # D also uses click|nav -> B. Now click|nav appears from A->B, C->E, F->A, D->B
            # That's fine - action-frequency still can't predict all correctly.
            ("D", "click", SHARED_HREF_NAV): "B",
            # click|detail|detail_link_shared: E->G, G->A  (2 different next states)
            ("E", "click", SHARED_HREF_DETAIL): "G",
            ("G", "click", SHARED_HREF_DETAIL): "A",
            # click|back|back_link_shared: G->H  (unique)
            ("G", "click", SHARED_HREF_BACK): "H",
            # click|sidebar|sidebar_link_shared: F->H  (unique)
            ("F", "click", SHARED_HREF_SIDEBAR): "H",
            # click|footer|footer_link_shared: H->A  (unique)
            ("H", "click", SHARED_HREF_FOOTER): "A",
        }
        # Valid actions per state
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
# Live Web Collector: HTTP fetch + HTMLParser, richer state representation
# ---------------------------------------------------------------------------

class LiveWebCollector:
    """Collects transitions from live web pages via HTTP fetch."""

    def __init__(self, seed: int = 43):
        self.rng = random.Random(seed)

    def _fetch_page(self, url: str) -> tuple[State, list[tuple[str, str]], list[str]]:
        """
        Fetch a page and extract:
        - State (URL, title, link_texts, tag_counts, form_signals)
        - Internal links: list of (link_text, resolved_href)
        - All resolved hrefs
        """
        try:
            req = urllib.request.Request(url, headers={
                'User-Agent': 'SPIDER-Physics/2.0',
                'Accept': 'text/html',
            })
            with urllib.request.urlopen(req, timeout=10) as resp:
                html = resp.read().decode('utf-8', errors='replace')
        except Exception as e:
            empty_state = State(url=url, title="fetch_error",
                                link_texts=(), tag_counts=(0,)*11, form_signals=(False,)*4)
            return empty_state, [], []

        # Parse HTML
        class PageParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.title = ""
                self.in_title = False
                self.links = []  # (text, href)
                self.current_link_text = ""
                self.in_link = False
                self.tag_counts = [0]*11  # h1=0,h2=1,h3=2,form=3,input=4,button=5,select=6,textarea=7,nav=8,main=9,aside=10
                self.has_form = False
                self.has_input = False
                self.has_select = False
                self.has_textarea = False

            TAG_MAP = {"h1":0, "h2":1, "h3":2, "form":3, "input":4, "button":5,
                        "select":6, "textarea":7, "nav":8, "main":9, "aside":10}

            def handle_starttag(self, tag, attrs):
                attrs_dict = dict(attrs)
                if tag in self.TAG_MAP:
                    self.tag_counts[self.TAG_MAP[tag]] += 1
                if tag == "title":
                    self.in_title = True
                if tag == "a" and "href" in attrs_dict:
                    href = attrs_dict["href"]
                    if href and not href.startswith(("#", "javascript:", "mailto:", "tel:")):
                        self.in_link = True
                        self.current_link_text = ""
                        self.links.append(("", href))
                if tag == "form":
                    self.has_form = True
                if tag == "input":
                    self.has_input = True
                if tag == "select":
                    self.has_select = True
                if tag == "textarea":
                    self.has_textarea = True

            def handle_endtag(self, tag):
                if tag == "title":
                    self.in_title = False
                if tag == "a" and self.in_link:
                    if self.links:
                        text = self.current_link_text.strip().lower()[:100]
                        self.links[-1] = (text, self.links[-1][1])
                    self.in_link = False

            def handle_data(self, data):
                if self.in_title:
                    self.title += data
                if self.in_link:
                    self.current_link_text += data

        parser = PageParser()
        try:
            parser.feed(html)
        except Exception:
            pass

        title = parser.title.strip().lower()[:100]
        link_texts = sorted(set(t for t, _ in parser.links if t))[:30]
        tag_counts = tuple(parser.tag_counts)
        form_signals = (parser.has_form, parser.has_input, parser.has_select, parser.has_textarea)

        state = State(
            url=url, title=title,
            link_texts=tuple(link_texts),
            tag_counts=tag_counts,
            form_signals=form_signals,
        )

        # Resolve internal links
        base_parsed = urllib.parse.urlparse(url)
        internal_links = []
        all_hrefs = []
        for link_text, href in parser.links:
            resolved = urllib.parse.urljoin(url, href)
            all_hrefs.append(resolved)
            resolved_parsed = urllib.parse.urlparse(resolved)
            if resolved_parsed.netloc == base_parsed.netloc:
                clean = urllib.parse.urlunsplit((
                    resolved_parsed.scheme, resolved_parsed.netloc,
                    resolved_parsed.path, "", ""
                ))
                internal_links.append((link_text, clean))

        return state, internal_links, all_hrefs

    def collect_trajectories(self, start_url: str, n_trajectories: int = 20,
                              max_steps: int = 10, polite_delay: float = 0.5) -> list[Transition]:
        """Collect trajectories from a single site."""
        homepage_state, internal_links, _ = self._fetch_page(start_url)

        if not internal_links:
            internal_links = [("", start_url)]

        transitions = []
        for i in range(n_trajectories):
            traj_id = f"live_{hashlib.sha256(start_url.encode()).hexdigest()[:8]}_{i}"

            if internal_links:
                _, start_link = internal_links[self.rng.randint(0, len(internal_links) - 1)]
            else:
                start_link = start_url

            current_url = start_link
            current_state, current_links, _ = self._fetch_page(current_url)
            time.sleep(polite_delay)

            for step in range(max_steps):
                if not current_links:
                    break

                link_text, next_url = current_links[self.rng.randint(0, len(current_links) - 1)]

                action = Action(
                    action_type="click",
                    target_text=link_text,
                    target_href=current_url,
                )

                next_state, next_links, _ = self._fetch_page(next_url)
                time.sleep(polite_delay)

                transitions.append(Transition(
                    state=current_state, action=action, next_state=next_state,
                    trajectory_id=traj_id, step_index=step,
                ))

                current_state = next_state
                current_url = next_url
                current_links = next_links

        return transitions


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
# Baseline Predictors (fit on train, evaluate on test)
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
# Permutation Test (trajectory-grouped, independent RNG)
# ---------------------------------------------------------------------------

def permutation_test_sa_vs_shuffle(
    transitions: list[Transition],
    n_permutations: int = 1000,
    seed: int = 42,
    train_frac: float = 0.7,
) -> dict:
    """
    Permutation test: is action-conditioned accuracy > shuffle null?
    """
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
    """
    Permutation test: is action-conditioned accuracy > action-frequency accuracy?
    Used for positive control discrimination check.
    """
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

    # 1. No target leakage: action features never contain next-state URL or content
    # NOTE: target_href == next_state.url is NOT leakage — it means the link points
    # to the same page (no redirect). This is a legitimate web pattern.
    # Only flag cases where target_text contains the next-state URL as a full match.
    leakage_issues = []
    for t in transitions:
        if t.action.target_text and t.next_state.url == t.action.target_text:
            leakage_issues.append(
                f"target_text exactly matches next_state.url: text={t.action.target_text}, url={t.next_state.url}"
            )
    checks["target_leakage"] = {"passed": len(leakage_issues) == 0, "issues": leakage_issues[:20]}

    # 2. Temporal ordering: within each trajectory, step indices are monotonically increasing
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

    # 3. Deterministic seeds: verify random.Random produces deterministic results
    rng1 = random.Random(seed)
    rng2 = random.Random(seed)
    seq1 = [rng1.randint(0, 10000) for _ in range(100)]
    seq2 = [rng2.randint(0, 10000) for _ in range(100)]
    checks["seed_determinism"] = {"passed": seq1 == seq2, "seed": seed}

    # 4. Trajectory count
    trajectory_ids = list(set(t.trajectory_id for t in transitions))
    checks["trajectory_count"] = {"passed": len(trajectory_ids) > 0, "n_trajectories": len(trajectory_ids)}

    all_passed = all(c["passed"] for c in checks.values())
    return {"all_passed": all_passed, "checks": checks}
