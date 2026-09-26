#!/usr/bin/env python3
"""
Goal Generator for EXP-GRAPH-36272373909
Produces goal wordings independent of distillation intents.
"""

import json
import random
from typing import Dict, List, Any
from dataclasses import dataclass, asdict


# Distillation intents (used to verify independence)
DISTILLATION_INTENTS = [
    "create a new user",
    "retrieve a post by id",
    "update a comment",
    "delete an album",
    "list photos",
]

# Goal templates per resource family - DISJOINT from distillation intents
GOAL_TEMPLATES = {
    "users": {
        "paraphrased": [
            "add a user",
            "register a new user",
            "sign up a user",
            "make a new user account",
        ],
        "composite": [
            "create a user and then retrieve their profile",
            "add two users and list them",
        ],
        "underspecified": [
            "get the latest user",
            "find a user",
        ],
        "ood": [
            "archive a user",
            "ban a user",
            "merge two users",
            "export all users",
        ],
    },
    "posts": {
        "paraphrased": [
            "fetch a post by id",
            "get a specific post",
            "look up a post",
            "read a post",
        ],
        "composite": [
            "create a post and then update it",
            "get a post and its comments",
        ],
        "underspecified": [
            "show me the newest post",
            "find a post",
        ],
        "ood": [
            "archive a post",
            "publish a post",
            "schedule a post",
            "duplicate a post",
        ],
    },
    "comments": {
        "paraphrased": [
            "modify a comment",
            "edit a comment",
            "change a comment",
            "revise a comment",
        ],
        "composite": [
            "update a comment and then delete it",
            "add a comment to a post and edit it",
        ],
        "underspecified": [
            "get the latest comment",
            "find a comment",
        ],
        "ood": [
            "archive a comment",
            "pin a comment",
            "hide a comment",
            "report a comment",
        ],
    },
    "albums": {
        "paraphrased": [
            "remove an album",
            "erase an album",
            "discard an album",
            "get rid of an album",
        ],
        "composite": [
            "delete an album and its photos",
            "create an album then delete it",
        ],
        "underspecified": [
            "get the latest album",
            "find an album",
        ],
        "ood": [
            "archive an album",
            "share an album",
            "merge albums",
            "download an album",
        ],
    },
    "photos": {
        "paraphrased": [
            "show photos",
            "display photos",
            "get all photos",
            "view photos",
        ],
        "composite": [
            "list photos in an album and download them",
            "add a photo then list all photos",
        ],
        "underspecified": [
            "get the latest photo",
            "find a photo",
        ],
        "ood": [
            "archive a photo",
            "edit a photo",
            "rotate a photo",
            "crop a photo",
        ],
    },
}


@dataclass
class Goal:
    family: str
    type: str  # paraphrased, composite, underspecified, ood
    wording: str
    template_id: int


def generate_goals(seed: int = 42) -> List[Goal]:
    """Generate goals with fixed seed for reproducibility"""
    random.seed(seed)
    goals = []
    
    for family, templates in GOAL_TEMPLATES.items():
        # Paraphrased (4 per family)
        for i, wording in enumerate(templates["paraphrased"]):
            goals.append(Goal(family, "paraphrased", wording, i))
        
        # Composite (2 per family)
        for i, wording in enumerate(templates["composite"]):
            goals.append(Goal(family, "composite", wording, i))
        
        # Underspecified (2 per family)
        for i, wording in enumerate(templates["underspecified"]):
            goals.append(Goal(family, "underspecified", wording, i))
        
        # OOD (4 per family)
        for i, wording in enumerate(templates["ood"]):
            goals.append(Goal(family, "ood", wording, i))
    
    return goals


def compute_vocabulary_overlap(goals: List[Goal]) -> Dict[str, float]:
    """Compute token Jaccard overlap between goals and distillation intents"""
    # Tokenize distillation intents
    distill_tokens = set()
    for intent in DISTILLATION_INTENTS:
        distill_tokens.update(intent.lower().split())
    
    overlaps = {}
    for goal in goals:
        goal_tokens = set(goal.wording.lower().split())
        intersection = len(distill_tokens & goal_tokens)
        union = len(distill_tokens | goal_tokens)
        jaccard = intersection / union if union > 0 else 0.0
        overlaps[goal.wording] = jaccard
    
    return overlaps


def main():
    seed = 42
    goals = generate_goals(seed)
    overlaps = compute_vocabulary_overlap(goals)
    
    output = {
        "seed": seed,
        "distillation_intents": DISTILLATION_INTENTS,
        "goals": [asdict(g) for g in goals],
        "vocabulary_overlap": overlaps,
        "max_overlap": max(overlaps.values()) if overlaps else 0.0,
        "mean_overlap": sum(overlaps.values()) / len(overlaps) if overlaps else 0.0,
    }
    
    print(json.dumps(output, indent=2))
    return output


if __name__ == "__main__":
    main()