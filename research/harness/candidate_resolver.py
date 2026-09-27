"""
Candidate Resolver for EXP-GRAPH-36287167610
Dual-class fitted applicability gate resolver
"""
import json
import hashlib
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
from pathlib import Path
from sklearn.linear_model import LogisticRegression
from sentence_transformers import SentenceTransformer


@dataclass
class Mechanism:
    mechanism_id: str
    intent: str
    parameter_slots: List[str]
    action_template: str
    role: str  # create, read, update, delete
    family: str
    verb: str


@dataclass
class ResolutionResult:
    goal_id: str
    mechanism_id: str
    resolution_status: str  # EXECUTABLE, ABSTAIN, DEFER, EXPLORE
    p_applicable: float
    bound_parameters: Dict[str, Any]
    confidence: float
    outcome_class: str  # EXECUTABLE, UNKNOWN, DEFER
    abstain_reason: Optional[str] = None


class CandidateResolver:
    def __init__(
        self,
        mechanisms: List[Mechanism],
        embedding_model: SentenceTransformer,
        calibration_params: Optional[Dict[str, float]] = None,
        threshold: float = 0.02
    ):
        self.mechanisms = mechanisms
        self.embedding_model = embedding_model
        self.mechanism_intents = [m.intent for m in mechanisms]
        self.mechanism_ids = [m.mechanism_id for m in mechanisms]
        self.mechanism_by_id = {m.mechanism_id: m for m in mechanisms}

        # Pre-compute mechanism intent embeddings
        self.mechanism_embeddings = self.embedding_model.encode(
            self.mechanism_intents, convert_to_numpy=True, normalize_embeddings=True
        )

        # Calibration parameters (fitted)
        self.calibration_params = calibration_params
        self.threshold = threshold

        # Slot-filling keywords for parameter binding
        self.slot_keywords = self._build_slot_keywords()

    def _build_slot_keywords(self) -> Dict[str, List[str]]:
        """Build keyword mapping for slot filling"""
        return {
            "user_id": ["user", "userid", "user_id", "id"],
            "name": ["name", "username", "fullname"],
            "email": ["email", "mail", "address"],
            "post_id": ["post", "postid", "post_id"],
            "title": ["title", "subject", "headline"],
            "body": ["body", "content", "text", "message"],
            "comment_id": ["comment", "commentid", "comment_id"],
            "album_id": ["album", "albumid", "album_id"],
            "photo_id": ["photo", "photoid", "photo_id", "picture", "image"],
            "url": ["url", "link", "uri", "address"],
        }

    def fit_calibration(
        self,
        train_goals: List[Dict[str, Any]],
        validation_goals: List[Dict[str, Any]]
    ) -> Dict[str, float]:
        """Fit logistic regression on dual-class training data"""
        # Prepare training data: max cos_sim per goal + label (1=applicable, 0=no-applicable)
        X_train = []
        y_train = []

        for goal in train_goals:
            goal_text = goal["text"]
            label = 1 if goal["applicable"] else 0
            max_cos_sim = self._max_cos_sim(goal_text)
            X_train.append([max_cos_sim])
            y_train.append(label)

        X_train = np.array(X_train)
        y_train = np.array(y_train)

        # Fit logistic regression
        clf = LogisticRegression(random_state=42, max_iter=1000)
        clf.fit(X_train, y_train)

        w = float(clf.coef_[0][0])
        b = float(clf.intercept_[0])

        # Select threshold on validation split to optimize F1
        best_threshold = 0.02
        best_f1 = -1

        for threshold in np.linspace(0.01, 0.99, 99):
            val_preds = []
            val_true = []
            for goal in validation_goals:
                goal_text = goal["text"]
                label = 1 if goal["applicable"] else 0
                max_cos_sim = self._max_cos_sim(goal_text)
                p_applicable = 1 / (1 + np.exp(-(w * max_cos_sim + b)))
                pred = 1 if p_applicable >= threshold else 0
                val_preds.append(pred)
                val_true.append(label)

            # Compute F1
            tp = sum(1 for p, t in zip(val_preds, val_true) if p == 1 and t == 1)
            fp = sum(1 for p, t in zip(val_preds, val_true) if p == 1 and t == 0)
            fn = sum(1 for p, t in zip(val_preds, val_true) if p == 0 and t == 1)

            precision = tp / (tp + fp) if (tp + fp) > 0 else 0
            recall = tp / (tp + fn) if (tp + fn) > 0 else 0
            f1 = 2 * precision * recall / (precision + recall) if (precision + recall) > 0 else 0

            if f1 > best_f1:
                best_f1 = f1
                best_threshold = threshold

        self.calibration_params = {"w": w, "b": b}
        self.threshold = best_threshold

        return {
            "w": w,
            "b": b,
            "threshold": best_threshold,
            "val_f1": best_f1
        }

    def _max_cos_sim(self, goal_text: str) -> float:
        """Compute maximum cosine similarity between goal and mechanism intents"""
        goal_emb = self.embedding_model.encode([goal_text], convert_to_numpy=True, normalize_embeddings=True)[0]
        cos_sims = np.dot(self.mechanism_embeddings, goal_emb)
        return float(np.max(cos_sims))

    def _p_applicable(self, goal_text: str) -> float:
        """Compute p_applicable using fitted logistic regression"""
        if self.calibration_params is None:
            raise ValueError("Calibration not fitted")
        max_cos_sim = self._max_cos_sim(goal_text)
        w = self.calibration_params["w"]
        b = self.calibration_params["b"]
        return 1 / (1 + np.exp(-(w * max_cos_sim + b)))

    def _fill_parameters(self, goal_text: str, mechanism: Mechanism) -> Tuple[Dict[str, Any], List[str]]:
        """Fill mechanism parameters from goal text using keyword matching"""
        bound = {}
        unfilled = []

        goal_lower = goal_text.lower()

        for slot in mechanism.parameter_slots:
            keywords = self.slot_keywords.get(slot, [slot])
            found = False
            for kw in keywords:
                if kw.lower() in goal_lower:
                    # Simple extraction: use a placeholder value
                    bound[slot] = f"<{slot}>"
                    found = True
                    break
            if not found:
                unfilled.append(slot)

        return bound, unfilled

    def resolve(self, goal: Dict[str, Any]) -> ResolutionResult:
        """Resolve a single goal"""
        goal_text = goal["text"]
        goal_id = goal["goal_id"]

        # Compute p_applicable for each mechanism
        goal_emb = self.embedding_model.encode([goal_text], convert_to_numpy=True, normalize_embeddings=True)[0]
        cos_sims = np.dot(self.mechanism_embeddings, goal_emb)

        p_applicables = []
        for cos_sim in cos_sims:
            p = 1 / (1 + np.exp(-(self.calibration_params["w"] * cos_sim + self.calibration_params["b"])))
            p_applicables.append(p)

        p_applicables = np.array(p_applicables)
        max_p = np.max(p_applicables)
        max_idx = np.argmax(p_applicables)

        # Decision rule
        if max_p < self.threshold:
            return ResolutionResult(
                goal_id=goal_id,
                mechanism_id="",
                resolution_status="ABSTAIN",
                p_applicable=float(max_p),
                bound_parameters={},
                confidence=float(max_p),
                outcome_class="UNKNOWN",
                abstain_reason="below_applicability_threshold"
            )

        selected_mechanism = self.mechanisms[max_idx]

        # Parameter binding
        bound_params, unfilled = self._fill_parameters(goal_text, selected_mechanism)

        if unfilled:
            return ResolutionResult(
                goal_id=goal_id,
                mechanism_id=selected_mechanism.mechanism_id,
                resolution_status="DEFER",
                p_applicable=float(max_p),
                bound_parameters=bound_params,
                confidence=float(max_p),
                outcome_class="DEFER",
                abstain_reason=f"unfilled_parameter_slots: {unfilled}"
            )

        return ResolutionResult(
            goal_id=goal_id,
            mechanism_id=selected_mechanism.mechanism_id,
            resolution_status="EXECUTABLE",
            p_applicable=float(max_p),
            bound_parameters=bound_params,
            confidence=float(max_p),
            outcome_class="EXECUTABLE"
        )


class LexicalOverlapResolver:
    """B-LEXICAL-OVERLAP: Max token Jaccard similarity"""

    def __init__(self, mechanisms: List[Mechanism]):
        self.mechanisms = mechanisms
        self.mechanism_intents = [m.intent for m in mechanisms]
        self.mechanism_ids = [m.mechanism_id for m in mechanisms]

    def _jaccard(self, text1: str, text2: str) -> float:
        tokens1 = set(text1.lower().split())
        tokens2 = set(text2.lower().split())
        if not tokens1 or not tokens2:
            return 0.0
        intersection = tokens1 & tokens2
        union = tokens1 | tokens2
        return len(intersection) / len(union)

    def resolve(self, goal: Dict[str, Any]) -> ResolutionResult:
        goal_text = goal["text"]
        goal_id = goal["goal_id"]

        scores = [self._jaccard(goal_text, intent) for intent in self.mechanism_intents]
        max_idx = np.argmax(scores)
        max_score = scores[max_idx]

        return ResolutionResult(
            goal_id=goal_id,
            mechanism_id=self.mechanism_ids[max_idx],
            resolution_status="EXECUTABLE",
            p_applicable=float(max_score),
            bound_parameters={},
            confidence=float(max_score),
            outcome_class="EXECUTABLE"
        )


class RandomRoleResolver:
    """B-RANDOM-ROLE: Random selection within inferred role"""

    def __init__(self, mechanisms: List[Mechanism], seed: int = 4242):
        self.mechanisms = mechanisms
        self.mechanism_by_role = {}
        for m in mechanisms:
            if m.role not in self.mechanism_by_role:
                self.mechanism_by_role[m.role] = []
            self.mechanism_by_role[m.role].append(m)
        self.rng = np.random.RandomState(seed)

        self.role_keywords = {
            "create": ["create", "add", "new", "make", "register", "publish", "write", "upload"],
            "read": ["get", "retrieve", "fetch", "look up", "find", "show", "view"],
            "update": ["update", "edit", "modify", "change", "alter"],
            "delete": ["delete", "remove", "erase", "delete", "take down", "drop"],
        }

    def _infer_role(self, goal_text: str) -> str:
        goal_lower = goal_text.lower()
        scores = {}
        for role, keywords in self.role_keywords.items():
            scores[role] = sum(1 for kw in keywords if kw in goal_lower)
        if max(scores.values()) == 0:
            return self.rng.choice(list(self.mechanism_by_role.keys()))
        return max(scores, key=scores.get)

    def resolve(self, goal: Dict[str, Any]) -> ResolutionResult:
        goal_text = goal["text"]
        goal_id = goal["goal_id"]

        role = self._infer_role(goal_text)
        candidates = self.mechanism_by_role.get(role, [])
        if not candidates:
            candidates = self.mechanisms

        selected = self.rng.choice(candidates)

        return ResolutionResult(
            goal_id=goal_id,
            mechanism_id=selected.mechanism_id,
            resolution_status="EXECUTABLE",
            p_applicable=1.0 / len(candidates),
            bound_parameters={},
            confidence=1.0 / len(candidates),
            outcome_class="EXECUTABLE"
        )


class EmbeddingArgmaxResolver:
    """B-EMBEDDING-ARGMAX: Raw embedding argmax, never abstains"""

    def __init__(self, mechanisms: List[Mechanism], embedding_model: SentenceTransformer):
        self.mechanisms = mechanisms
        self.embedding_model = embedding_model
        self.mechanism_intents = [m.intent for m in mechanisms]
        self.mechanism_ids = [m.mechanism_id for m in mechanisms]
        self.mechanism_embeddings = self.embedding_model.encode(
            self.mechanism_intents, convert_to_numpy=True, normalize_embeddings=True
        )

    def resolve(self, goal: Dict[str, Any]) -> ResolutionResult:
        goal_text = goal["text"]
        goal_id = goal["goal_id"]

        goal_emb = self.embedding_model.encode([goal_text], convert_to_numpy=True, normalize_embeddings=True)[0]
        cos_sims = np.dot(self.mechanism_embeddings, goal_emb)
        max_idx = np.argmax(cos_sims)
        max_sim = cos_sims[max_idx]

        return ResolutionResult(
            goal_id=goal_id,
            mechanism_id=self.mechanism_ids[max_idx],
            resolution_status="EXECUTABLE",
            p_applicable=float(max_sim),
            bound_parameters={},
            confidence=float(max_sim),
            outcome_class="EXECUTABLE"
        )


class InternalIdOracle:
    """B-INTERNAL-ID-ORACLE: Receives true mechanism_id"""

    def __init__(self, mechanisms: List[Mechanism]):
        self.mechanism_by_id = {m.mechanism_id: m for m in mechanisms}

    def resolve(self, goal: Dict[str, Any]) -> ResolutionResult:
        goal_id = goal["goal_id"]
        target_mech_id = goal["target_mechanism_id"]

        if target_mech_id and target_mech_id in self.mechanism_by_id:
            return ResolutionResult(
                goal_id=goal_id,
                mechanism_id=target_mech_id,
                resolution_status="EXECUTABLE",
                p_applicable=1.0,
                bound_parameters={},
                confidence=1.0,
                outcome_class="EXECUTABLE"
            )
        else:
            # No applicable mechanism
            return ResolutionResult(
                goal_id=goal_id,
                mechanism_id="",
                resolution_status="ABSTAIN",
                p_applicable=0.0,
                bound_parameters={},
                confidence=0.0,
                outcome_class="UNKNOWN"
            )


def load_mechanisms(fixture_path: str) -> List[Mechanism]:
    """Load mechanisms from fixture.json"""
    with open(fixture_path, 'r') as f:
        data = json.load(f)
    return [Mechanism(**m) for m in data]


def create_fixture() -> List[Mechanism]:
    """Create the standard 20-mechanism fixture"""
    mechanisms = []
    families = ["users", "posts", "comments", "albums", "photos"]
    verbs = ["create", "read", "update", "delete"]

    for family in families:
        for verb in verbs:
            mech_id = f"mech_{family}_{verb}"
            intent = INTENTS[mech_id]
            parameter_slots = PARAM_SLOTS[mech_id]
            action_template = f"{verb.upper()} /{family}/{{{parameter_slots[0]}}}" if parameter_slots else f"{verb.upper()} /{family}"
            mechanisms.append(Mechanism(
                mechanism_id=mech_id,
                intent=intent,
                parameter_slots=parameter_slots,
                action_template=action_template,
                role=verb,
                family=family,
                verb=verb.upper()
            ))

    return mechanisms


# Import INTENTS and PARAM_SLOTS from goal_generator
from goal_generator import INTENTS, PARAM_SLOTS


if __name__ == "__main__":
    # Test
    mechs = create_fixture()
    print(f"Created {len(mechs)} mechanisms")
    for m in mechs:
        print(f"  {m.mechanism_id}: {m.intent} | slots: {m.parameter_slots} | role: {m.role}")