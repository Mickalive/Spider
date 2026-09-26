#!/usr/bin/env python3
"""
Candidate Resolver for EXP-GRAPH-36272373909
Semantic goal-to-mechanism resolution via embeddings + calibration.
"""

import json
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
from dataclasses import dataclass
import re

# Try to import sentence-transformers, fall back to TF-IDF if not available
try:
    from sentence_transformers import SentenceTransformer
    HAS_SENTENCE_TRANSFORMERS = True
except ImportError:
    HAS_SENTENCE_TRANSFORMERS = False
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class MechanismView:
    """Public view of mechanism (no internal IDs)"""
    intent: str
    preconditions: Dict[str, Any]
    action_template: Dict[str, Any]
    postconditions: Dict[str, Any]
    confidence: float
    parameter_slots: List[str]
    applicability_guards: Dict[str, Any]


@dataclass
class ResolutionResult:
    status: str  # EXECUTABLE, EXPLORE, UNKNOWN
    mechanism_intent: Optional[str]
    confidence: float
    bound_action: Optional[Dict[str, Any]]
    p_applicable: float


class CandidateResolver:
    """Semantic goal-to-mechanism resolver with calibrated abstention."""
    
    def __init__(self, mechanisms: List[MechanismView], threshold: float = 0.5):
        self.mechanisms = mechanisms
        self.threshold = threshold  # Frozen before any run
        self.intents = [m.intent for m in mechanisms]
        
        # Initialize embedding model
        if HAS_SENTENCE_TRANSFORMERS:
            self.model = SentenceTransformer('all-MiniLM-L6-v2')
            self.intent_embeddings = self.model.encode(self.intents, convert_to_numpy=True)
        else:
            # Fallback: TF-IDF
            self.vectorizer = TfidfVectorizer()
            self.intent_vectors = self.vectorizer.fit_transform(self.intents)
    
    def _encode(self, text: str) -> np.ndarray:
        if HAS_SENTENCE_TRANSFORMERS:
            return self.model.encode([text], convert_to_numpy=True)[0]
        else:
            return self.vectorizer.transform([text]).toarray()[0]
    
    def _cosine_sim(self, a: np.ndarray, b: np.ndarray) -> float:
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b) + 1e-8))
    
    def _check_preconditions(self, preconditions: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if all preconditions match context"""
        return all(context.get(k) == v for k, v in preconditions.items())
    
    def _check_applicability_guards(self, guards: Dict[str, Any], context: Dict[str, Any]) -> bool:
        """Check if applicability guards match context"""
        return all(context.get(k) == v for k, v in guards.items())
    
    def _extract_params(self, goal: str, param_slots: List[str]) -> Dict[str, Any]:
        """Extract parameter values from goal using simple patterns"""
        params = {}
        for slot in param_slots:
            # Try to find pattern like "id=123" or "id 123" or similar
            patterns = [
                rf'{slot}[=:]\s*(\S+)',
                rf'{slot}\s+(\S+)',
                rf'{slot}\s*=\s*(\S+)',
            ]
            for pattern in patterns:
                match = re.search(pattern, goal, re.IGNORECASE)
                if match:
                    params[slot] = match.group(1)
                    break
        return params
    
    def _bind_action(self, action_template: Dict[str, Any], params: Dict[str, Any]) -> Dict[str, Any]:
        """Bind parameters into action template"""
        def bind_value(value: Any) -> Any:
            if isinstance(value, str):
                # Replace ${param} patterns
                def replace(match):
                    key = match.group(1)
                    return str(params.get(key, match.group(0)))
                return re.sub(r'\$\{([A-Za-z_][A-Za-z0-9_]*)\}', replace, value)
            elif isinstance(value, dict):
                return {k: bind_value(v) for k, v in value.items()}
            elif isinstance(value, list):
                return [bind_value(v) for v in value]
            return value
        
        return bind_value(action_template)
    
    def resolve(self, goal: str, context: Dict[str, Any]) -> ResolutionResult:
        """Resolve goal to mechanism"""
        # Encode goal
        goal_emb = self._encode(goal)
        
        # Compute similarities
        if HAS_SENTENCE_TRANSFORMERS:
            similarities = [self._cosine_sim(goal_emb, emb) for emb in self.intent_embeddings]
        else:
            goal_vec = self.vectorizer.transform([goal])
            similarities = cosine_similarity(goal_vec, self.intent_vectors).flatten()
        
        # Filter by preconditions and guards
        valid_candidates = []
        for i, mech in enumerate(self.mechanisms):
            if not self._check_preconditions(mech.preconditions, context):
                continue
            if not self._check_applicability_guards(mech.applicability_guards, context):
                continue
            valid_candidates.append((i, similarities[i], mech))
        
        if not valid_candidates:
            return ResolutionResult(
                status="UNKNOWN",
                mechanism_intent=None,
                confidence=0.0,
                bound_action=None,
                p_applicable=0.0
            )
        
        # Sort by similarity * confidence
        valid_candidates.sort(key=lambda x: x[1] * x[2].confidence, reverse=True)
        best_idx, best_sim, best_mech = valid_candidates[0]
        
        # Calibrated applicability probability (logistic on similarity)
        # Using a simple sigmoid calibrated on similarity
        p_applicable = 1.0 / (1.0 + np.exp(-10 * (best_sim - 0.3)))
        
        if p_applicable < self.threshold:
            return ResolutionResult(
                status="UNKNOWN",
                mechanism_intent=best_mech.intent,
                confidence=best_mech.confidence,
                bound_action=None,
                p_applicable=p_applicable
            )
        
        # Extract parameters and bind action
        params = self._extract_params(goal, best_mech.parameter_slots)
        bound_action = self._bind_action(best_mech.action_template, params)
        
        return ResolutionResult(
            status="EXECUTABLE",
            mechanism_intent=best_mech.intent,
            confidence=best_mech.confidence,
            bound_action=bound_action,
            p_applicable=p_applicable
        )


def create_resolver_from_registry(registry: List[Dict], threshold: float = 0.5) -> CandidateResolver:
    """Create resolver from mechanism registry (public view only)"""
    mechanisms = []
    for m in registry:
        mechanisms.append(MechanismView(
            intent=m["intent"],
            preconditions=m.get("preconditions", {}),
            action_template=m.get("action_template", {}),
            postconditions=m.get("postconditions", {}),
            confidence=m.get("confidence", 0.5),
            parameter_slots=m.get("parameter_slots", []),
            applicability_guards=m.get("applicability_guards", {}),
        ))
    return CandidateResolver(mechanisms, threshold)


if __name__ == "__main__":
    # Test with dummy data
    test_mechanisms = [
        {
            "intent": "create a new user",
            "preconditions": {"auth_token": "present"},
            "action_template": {"method": "POST", "url": "/users", "body": {"name": "${name}", "email": "${email}"}},
            "postconditions": {"status": 201},
            "confidence": 0.5,
            "parameter_slots": ["name", "email"],
            "applicability_guards": {},
        }
    ]
    
    resolver = create_resolver_from_registry(test_mechanisms)
    result = resolver.resolve("add a user named John with email john@example.com", {"auth_token": "present"})
    print(f"Status: {result.status}")
    print(f"Intent: {result.mechanism_intent}")
    print(f"P(applicable): {result.p_applicable:.3f}")
    print(f"Bound action: {result.bound_action}")