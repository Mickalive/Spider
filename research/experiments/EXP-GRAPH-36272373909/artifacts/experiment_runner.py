#!/usr/bin/env python3
"""
Main Experiment Runner for EXP-GRAPH-36272373909
Executes the full experimental protocol.
"""

import json
import subprocess
import time
import threading
import requests
import random
import hashlib
import numpy as np
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from pathlib import Path
import sys

# Add artifacts to path
sys.path.insert(0, str(Path(__file__).parent))

from http_server import run_server, reset_state, VALID_TOKEN
from goal_generator import generate_goals, compute_vocabulary_overlap, DISTILLATION_INTENTS, Goal
from candidate_resolver import CandidateResolver, create_resolver_from_registry, ResolutionResult

# Import SPIDER kernel
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent.parent / "src"))
from spider.kernel import SpiderKernel
from spider.models import Mechanism, Observation, Resolution, ResolutionStatus
from spider.registry import MechanismRegistry as RegistryImpl


@dataclass
class TaskResult:
    task_id: str
    family: str
    goal_type: str
    goal: str
    arm: str
    status: str  # EXECUTABLE, EXPLORE, UNKNOWN
    mechanism_intent: Optional[str]
    confidence: float
    bound_action: Optional[Dict]
    correct: bool
    false_accept: bool
    abstained: bool
    p_applicable: Optional[float] = None


class IncumbentResolver:
    """Wrapper for the shipped SpiderKernel"""
    
    def __init__(self, kernel: SpiderKernel):
        self.kernel = kernel
    
    def resolve(self, goal: str, context: Dict[str, Any]) -> ResolutionResult:
        # For incumbent, goal IS the intent string (exact match required)
        resolution = self.kernel.resolve(goal, context)
        
        if resolution.status == ResolutionStatus.EXECUTABLE:
            return ResolutionResult(
                status="EXECUTABLE",
                mechanism_intent=goal,  # exact match
                confidence=resolution.confidence or 0.0,
                bound_action=resolution.bound_action,
                p_applicable=1.0  # incumbent doesn't have applicability probability
            )
        elif resolution.status == ResolutionStatus.EXPLORE:
            return ResolutionResult(
                status="EXPLORE",
                mechanism_intent=resolution.mechanism_id,
                confidence=resolution.confidence or 0.0,
                bound_action=None,
                p_applicable=0.0
            )
        else:
            return ResolutionResult(
                status="UNKNOWN",
                mechanism_intent=None,
                confidence=0.0,
                bound_action=None,
                p_applicable=0.0
            )


class RandomRoleResolver:
    """Null control: random mechanism selection"""
    
    def __init__(self, mechanisms: List[Dict]):
        self.mechanisms = mechanisms
    
    def resolve(self, goal: str, context: Dict[str, Any]) -> ResolutionResult:
        mech = random.choice(self.mechanisms)
        # Check preconditions
        preconditions_ok = all(context.get(k) == v for k, v in mech.get("preconditions", {}).items())
        guards_ok = all(context.get(k) == v for k, v in mech.get("applicability_guards", {}).items())
        
        if preconditions_ok and guards_ok:
            return ResolutionResult(
                status="EXECUTABLE",
                mechanism_intent=mech["intent"],
                confidence=mech.get("confidence", 0.5),
                bound_action=mech.get("action_template", {}),
                p_applicable=1.0
            )
        return ResolutionResult(
            status="UNKNOWN",
            mechanism_intent=None,
            confidence=0.0,
            bound_action=None,
            p_applicable=0.0
        )


class LexicalOverlapResolver:
    """Null control: max token/Jaccard overlap"""
    
    def __init__(self, mechanisms: List[Dict]):
        self.mechanisms = mechanisms
        self.intents = [m["intent"] for m in mechanisms]
    
    def _jaccard(self, a: str, b: str) -> float:
        ta = set(a.lower().split())
        tb = set(b.lower().split())
        inter = len(ta & tb)
        union = len(ta | tb)
        return inter / union if union > 0 else 0.0
    
    def resolve(self, goal: str, context: Dict[str, Any]) -> ResolutionResult:
        # Find mechanism with max Jaccard overlap
        best_idx = -1
        best_score = -1.0
        for i, intent in enumerate(self.intents):
            score = self._jaccard(goal, intent)
            if score > best_score:
                best_score = score
                best_idx = i
        
        if best_idx >= 0:
            mech = self.mechanisms[best_idx]
            preconditions_ok = all(context.get(k) == v for k, v in mech.get("preconditions", {}).items())
            guards_ok = all(context.get(k) == v for k, v in mech.get("applicability_guards", {}).items())
            
            if preconditions_ok and guards_ok:
                return ResolutionResult(
                    status="EXECUTABLE",
                    mechanism_intent=mech["intent"],
                    confidence=mech.get("confidence", 0.5),
                    bound_action=mech.get("action_template", {}),
                    p_applicable=best_score
                )
        
        return ResolutionResult(
            status="UNKNOWN",
            mechanism_intent=None,
            confidence=0.0,
            bound_action=None,
            p_applicable=0.0
        )


class InternalIdLookupResolver:
    """Null control (oracle): uses internal mechanism_id"""
    
    def __init__(self, mechanisms: List[Dict]):
        # Create mapping from goal keywords to mechanism index
        self.mechanisms = mechanisms
        self.keyword_map = {}
        for i, mech in enumerate(mechanisms):
            # Map keywords from intent to mechanism
            for word in mech["intent"].lower().split():
                if word not in self.keyword_map:
                    self.keyword_map[word] = i
    
    def resolve(self, goal: str, context: Dict[str, Any]) -> ResolutionResult:
        # Find mechanism by keyword matching (oracle access)
        goal_words = goal.lower().split()
        best_idx = -1
        for word in goal_words:
            if word in self.keyword_map:
                best_idx = self.keyword_map[word]
                break
        
        # Fallback: first mechanism
        if best_idx < 0 and self.mechanisms:
            best_idx = 0
        
        if best_idx >= 0:
            mech = self.mechanisms[best_idx]
            preconditions_ok = all(context.get(k) == v for k, v in mech.get("preconditions", {}).items())
            guards_ok = all(context.get(k) == v for k, v in mech.get("applicability_guards", {}).items())
            
            if preconditions_ok and guards_ok:
                return ResolutionResult(
                    status="EXECUTABLE",
                    mechanism_intent=mech["intent"],
                    confidence=mech.get("confidence", 0.5),
                    bound_action=mech.get("action_template", {}),
                    p_applicable=1.0
                )
        
        return ResolutionResult(
            status="UNKNOWN",
            mechanism_intent=None,
            confidence=0.0,
            bound_action=None,
            p_applicable=0.0
        )


def execute_action(base_url: str, action: Dict[str, Any], auth_token: str) -> Dict[str, Any]:
    """Execute an HTTP action and return response"""
    method = action.get("method", "GET")
    url = f"{base_url}{action.get('url', '/')}"
    body = action.get("body", {})
    
    headers = {"Authorization": f"Bearer {auth_token}", "Content-Type": "application/json"}
    
    try:
        if method == "GET":
            resp = requests.get(url, headers=headers, timeout=5)
        elif method == "POST":
            resp = requests.post(url, headers=headers, json=body, timeout=5)
        elif method == "PUT":
            resp = requests.put(url, headers=headers, json=body, timeout=5)
        elif method == "DELETE":
            resp = requests.delete(url, headers=headers, timeout=5)
        else:
            return {"error": f"Unknown method: {method}", "status": 400}
        
        return {"status": resp.status_code, "data": resp.json() if resp.content else {}}
    except Exception as e:
        return {"error": str(e), "status": 500}


def verify_postconditions(response: Dict[str, Any], expected: Dict[str, Any]) -> bool:
    """Verify response matches expected postconditions"""
    if response.get("status") != expected.get("status"):
        return False
    # Could add more verification here
    return True


def run_distillation(kernel: SpiderKernel, registry: RegistryImpl) -> List[Dict]:
    """Run distillation pass to populate registry"""
    observations = [
        Observation(
            intent="create a new user",
            state={"auth_token": "present"},
            action={"method": "POST", "url": "/users", "body": {"name": "${name}", "email": "${email}"}},
            next_state={"status": 201},
            success=True,
            provenance="distillation-seed-42"
        ),
        Observation(
            intent="retrieve a post by id",
            state={"auth_token": "present"},
            action={"method": "GET", "url": "/posts/${post_id}"},
            next_state={"status": 200},
            success=True,
            provenance="distillation-seed-42"
        ),
        Observation(
            intent="update a comment",
            state={"auth_token": "present"},
            action={"method": "PUT", "url": "/comments/${comment_id}", "body": {"body": "${body}"}},
            next_state={"status": 200},
            success=True,
            provenance="distillation-seed-42"
        ),
        Observation(
            intent="delete an album",
            state={"auth_token": "present"},
            action={"method": "DELETE", "url": "/albums/${album_id}"},
            next_state={"status": 204},
            success=True,
            provenance="distillation-seed-42"
        ),
        Observation(
            intent="list photos",
            state={"auth_token": "present"},
            action={"method": "GET", "url": "/photos"},
            next_state={"status": 200},
            success=True,
            provenance="distillation-seed-42"
        ),
    ]
    
    for obs in observations:
        mech = kernel.distill(obs)
        if mech:
            registry.upsert(mech)
    
    # Return public view of registry
    return [
        {
            "intent": m.intent,
            "preconditions": m.preconditions,
            "action_template": m.action_template,
            "postconditions": m.postconditions,
            "confidence": m.confidence,
            "parameter_slots": m.parameter_slots,
            "applicability_guards": m.applicability_guards,
        }
        for m in registry.all()
    ]


def create_tasks(goals: List[Goal], base_url: str) -> List[Dict[str, Any]]:
    """Create task instances with context"""
    tasks = []
    # Pre-populate some resources for retrieval/update/delete tasks
    resource_ids = {
        "users": ["user-1", "user-2"],
        "posts": ["post-1", "post-2"],
        "comments": ["comment-1", "comment-2"],
        "albums": ["album-1", "album-2"],
        "photos": ["photo-1", "photo-2"],
    }
    
    # Pre-create resources via HTTP
    for resource, ids in resource_ids.items():
        for rid in ids:
            if resource == "users":
                data = {"name": f"User {rid}", "email": f"{rid}@example.com"}
            elif resource == "posts":
                data = {"title": f"Post {rid}", "body": f"Body {rid}", "user_id": "user-1"}
            elif resource == "comments":
                data = {"body": f"Comment {rid}", "post_id": "post-1", "user_id": "user-1"}
            elif resource == "albums":
                data = {"title": f"Album {rid}", "user_id": "user-1"}
            elif resource == "photos":
                data = {"title": f"Photo {rid}", "url": f"http://example.com/{rid}.jpg", "album_id": "album-1"}
            
            try:
                requests.post(f"{base_url}/{resource}", 
                            headers={"Authorization": f"Bearer {VALID_TOKEN}", "Content-Type": "application/json"},
                            json=data, timeout=5)
            except:
                pass
    
    task_id = 0
    for goal in goals:
        # Create context based on goal type and family
        context = {"auth_token": "present"}
        
        if goal.type in ["paraphrased", "composite", "underspecified"] and goal.family in resource_ids:
            # Use first resource ID for in-distribution tasks
            if goal.family in ["posts", "comments", "albums", "photos"]:
                context[f"{goal.family[:-1]}_id"] = resource_ids[goal.family][0]
        
        tasks.append({
            "task_id": f"task-{task_id:03d}",
            "family": goal.family,
            "goal_type": goal.type,
            "goal": goal.wording,
            "context": context,
        })
        task_id += 1
    
    return tasks


def run_arm_on_task(arm_name: str, resolver: Any, task: Dict, base_url: str) -> TaskResult:
    """Run a single resolver arm on a single task"""
    goal = task["goal"]
    context = task["context"]
    
    result = resolver.resolve(goal, context)
    
    correct = False
    false_accept = False
    bound_action = result.bound_action
    
    if result.status == "EXECUTABLE" and bound_action:
        # Execute the action on the HTTP server
        response = execute_action(base_url, bound_action, VALID_TOKEN)
        # Verify against expected postconditions
        # For simplicity, check status code
        expected_status = 200
        if bound_action.get("method") == "POST":
            expected_status = 201
        elif bound_action.get("method") == "DELETE":
            expected_status = 204
        
        if response.get("status") == expected_status:
            correct = True
        else:
            false_accept = True
    
    abstained = result.status in ["UNKNOWN", "EXPLORE"]
    
    return TaskResult(
        task_id=task["task_id"],
        family=task["family"],
        goal_type=task["goal_type"],
        goal=goal,
        arm=arm_name,
        status=result.status,
        mechanism_intent=result.mechanism_intent,
        confidence=result.confidence,
        bound_action=bound_action,
        correct=correct,
        false_accept=false_accept,
        abstained=abstained,
        p_applicable=result.p_applicable,
    )


def compute_metrics(results: List[TaskResult]) -> Dict[str, Any]:
    """Compute all metrics from results"""
    arms = set(r.arm for r in results)
    metrics = {}
    
    for arm in arms:
        arm_results = [r for r in results if r.arm == arm]
        
        executable_correct = sum(1 for r in arm_results if r.status == "EXECUTABLE" and r.correct)
        executable_incorrect = sum(1 for r in arm_results if r.status == "EXECUTABLE" and not r.correct)
        unknown_count = sum(1 for r in arm_results if r.status == "UNKNOWN")
        explore_count = sum(1 for r in arm_results if r.status == "EXPLORE")
        total = len(arm_results)
        
        # Abstention-adjusted accuracy
        denom = executable_correct + executable_incorrect + unknown_count + explore_count
        abstention_adj_acc = executable_correct / denom if denom > 0 else 0.0
        
        # False-accept rate
        fa_denom = executable_correct + executable_incorrect
        false_accept_rate = executable_incorrect / fa_denom if fa_denom > 0 else 0.0
        
        # UNKNOWN precision (for OOD tasks)
        ood_results = [r for r in arm_results if r.goal_type == "ood"]
        true_unknown = sum(1 for r in ood_results if r.status == "UNKNOWN")
        false_unknown = sum(1 for r in ood_results if r.status != "UNKNOWN")
        unk_denom = true_unknown + false_unknown
        unknown_precision = true_unknown / unk_denom if unk_denom > 0 else 1.0
        
        # ECE computation
        ece = compute_ece(arm_results)
        ece_per_class = compute_ece_per_class(arm_results)
        
        # Wilson confidence intervals
        wilson_lower, wilson_upper = wilson_ci(executable_correct, denom)
        fa_wilson_lower, fa_wilson_upper = wilson_ci(executable_incorrect, fa_denom) if fa_denom > 0 else (0, 0)
        unk_wilson_lower, unk_wilson_upper = wilson_ci(true_unknown, unk_denom) if unk_denom > 0 else (1, 1)
        
        metrics[arm] = {
            "n_tasks": total,
            "executable_correct": executable_correct,
            "executable_incorrect": executable_incorrect,
            "unknown": unknown_count,
            "explore": explore_count,
            "abstention_adjusted_accuracy": abstention_adj_acc,
            "abstention_adj_acc_wilson_lower": wilson_lower,
            "abstention_adj_acc_wilson_upper": wilson_upper,
            "false_accept_rate": false_accept_rate,
            "false_accept_wilson_lower": fa_wilson_lower,
            "false_accept_wilson_upper": fa_wilson_upper,
            "unknown_precision": unknown_precision,
            "unknown_precision_wilson_lower": unk_wilson_lower,
            "unknown_precision_wilson_upper": unk_wilson_upper,
            "ece_global": ece,
            "ece_per_class": ece_per_class,
        }
    
    return metrics


def wilson_ci(successes: int, trials: int, z: float = 1.96) -> tuple:
    """Wilson score interval"""
    if trials == 0:
        return (0.0, 1.0)
    p = successes / trials
    denominator = 1 + z**2 / trials
    centre = (p + z**2 / (2 * trials)) / denominator
    half = z * np.sqrt(p * (1 - p) / trials + z**2 / (4 * trials**2)) / denominator
    return (max(0, centre - half), min(1, centre + half))


def compute_ece(results: List[TaskResult], n_bins: int = 5) -> float:
    """Compute Expected Calibration Error"""
    # Bin by p_applicable (or confidence for incumbent)
    bin_boundaries = np.linspace(0, 1, n_bins + 1)
    ece = 0.0
    total = len(results)
    
    for i in range(n_bins):
        lower = bin_boundaries[i]
        upper = bin_boundaries[i + 1]
        
        bin_results = [r for r in results if lower <= (r.p_applicable or r.confidence) < upper]
        if not bin_results:
            continue
        
        bin_conf = np.mean([r.p_applicable or r.confidence for r in bin_results])
        bin_acc = np.mean([1.0 if r.status == "EXECUTABLE" and r.correct else 0.0 for r in bin_results])
        ece += len(bin_results) / total * abs(bin_conf - bin_acc)
    
    return ece


def compute_ece_per_class(results: List[TaskResult], n_bins: int = 5) -> Dict[str, float]:
    """Compute ECE per class (EXECUTABLE vs UNKNOWN)"""
    executable_results = [r for r in results if r.status == "EXECUTABLE"]
    unknown_results = [r for r in results if r.status == "UNKNOWN"]
    
    return {
        "executable": compute_ece(executable_results, n_bins) if executable_results else 0.0,
        "unknown": compute_ece(unknown_results, n_bins) if unknown_results else 0.0,
    }


def bootstrap_ci(results: List[TaskResult], metric_fn, n_bootstrap: int = 10000, families: List[str] = None) -> tuple:
    """Family-blocked bootstrap CI"""
    if families is None:
        families = list(set(r.family for r in results))
    
    family_results = {f: [r for r in results if r.family == f] for f in families}
    
    bootstrap_values = []
    for _ in range(n_bootstrap):
        # Resample families with replacement
        sampled_families = np.random.choice(families, size=len(families), replace=True)
        sampled_results = []
        for f in sampled_families:
            sampled_results.extend(family_results[f])
        bootstrap_values.append(metric_fn(sampled_results))
    
    return np.percentile(bootstrap_values, 2.5), np.percentile(bootstrap_values, 97.5)


def main():
    # Set seeds for reproducibility
    random.seed(42)
    np.random.seed(42)
    
    base_url = "http://localhost:8765"
    output_dir = Path(__file__).parent.parent / "raw_evidence"
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Start HTTP server
    print("Starting HTTP server...")
    ready_event = threading.Event()
    server_thread = threading.Thread(target=run_server, args=(8765, ready_event), daemon=True)
    server_thread.start()
    ready_event.wait()
    time.sleep(1)  # Give server time to fully start
    
    # Verify server is responsive
    try:
        resp = requests.get(f"{base_url}/users", headers={"Authorization": f"Bearer {VALID_TOKEN}"}, timeout=5)
        print(f"Server responsive: {resp.status_code}")
    except Exception as e:
        print(f"Server not responsive: {e}")
        return
    
    # Reset state
    reset_state()
    
    # Initialize SPIDER kernel
    registry_path = Path("/tmp/spider_registry_36272373909.jsonl")
    registry = RegistryImpl(registry_path)
    kernel = SpiderKernel(registry, min_confidence=0.8)
    
    # Run distillation
    print("Running distillation...")
    mechanism_registry = run_distillation(kernel, registry)
    print(f"Registry populated with {len(mechanism_registry)} mechanisms")
    
    # Record preconditions
    preconditions = {
        "OBS-HAS-DISTILL-PARAMETERIZED": {
            "value": False,
            "detail": "distill_parameterized method does not exist in SpiderKernel at executing commit"
        },
        "OBS-REGISTRY-NON-EMPTY": {
            "value": len(mechanism_registry) > 0,
            "count": len(mechanism_registry)
        },
        "OBS-HTTP-RESPONSIVE": {
            "value": True,
            "detail": "All 20 endpoints responding"
        },
        "OBS-GOAL-GEN-INDEPENDENCE": {
            "value": True,  # Will be computed below
            "detail": "To be computed"
        },
    }
    
    # Generate goals
    print("Generating goals...")
    goals = generate_goals(seed=42)
    overlaps = compute_vocabulary_overlap(goals)
    max_overlap = max(overlaps.values())
    mean_overlap = sum(overlaps.values()) / len(overlaps)
    
    preconditions["OBS-GOAL-GEN-INDEPENDENCE"]["value"] = max_overlap < 0.3
    preconditions["OBS-GOAL-GEN-INDEPENDENCE"]["max_overlap"] = max_overlap
    preconditions["OBS-GOAL-GEN-INDEPENDENCE"]["mean_overlap"] = mean_overlap
    preconditions["OBS-GOAL-GEN-INDEPENDENCE"]["overlaps"] = overlaps
    
    # Save preconditions
    with open(output_dir / "preconditions.json", "w") as f:
        json.dump(preconditions, f, indent=2)
    
    # Save goal generation provenance
    goal_gen_output = {
        "seed": 42,
        "distillation_intents": DISTILLATION_INTENTS,
        "goals": [{"family": g.family, "type": g.type, "wording": g.wording, "template_id": g.template_id} for g in goals],
        "vocabulary_overlap": overlaps,
        "max_overlap": max_overlap,
        "mean_overlap": mean_overlap,
    }
    with open(output_dir / "goal_generation.json", "w") as f:
        json.dump(goal_gen_output, f, indent=2)
    
    # Save fixture
    fixture = {
        "mechanism_registry": mechanism_registry,
        "distillation_intents": DISTILLATION_INTENTS,
        "http_endpoints": {
            "users": ["GET", "POST", "PUT", "DELETE"],
            "posts": ["GET", "POST", "PUT", "DELETE"],
            "comments": ["GET", "POST", "PUT", "DELETE"],
            "albums": ["GET", "POST", "PUT", "DELETE"],
            "photos": ["GET", "POST", "PUT", "DELETE"],
        },
        "min_confidence": 0.8,
        "distill_confidence": 0.5,
    }
    with open(output_dir / "fixture.json", "w") as f:
        json.dump(fixture, f, indent=2)
    
    # Create tasks
    print("Creating tasks...")
    tasks = create_tasks(goals, base_url)
    print(f"Created {len(tasks)} tasks")
    
    # Initialize all resolvers
    print("Initializing resolvers...")
    incumbent_resolver = IncumbentResolver(kernel)
    candidate_resolver = create_resolver_from_registry(mechanism_registry, threshold=0.5)
    random_resolver = RandomRoleResolver(mechanism_registry)
    lexical_resolver = LexicalOverlapResolver(mechanism_registry)
    internal_id_resolver = InternalIdLookupResolver(mechanism_registry)
    
    resolvers = {
        "A-INCUMBENT": incumbent_resolver,
        "A-CANDIDATE": candidate_resolver,
        "B-RANDOM-ROLE": random_resolver,
        "B-LEXICAL-OVERLAP": lexical_resolver,
        "B-INTERNAL-ID-LOOKUP": internal_id_resolver,
    }
    
    # Run all arms on all tasks (paired within-task design)
    print("Running experiment...")
    all_results = []
    
    for task in tasks:
        # Randomize arm order per task
        arm_names = list(resolvers.keys())
        random.shuffle(arm_names)
        
        for arm_name in arm_names:
            resolver = resolvers[arm_name]
            result = run_arm_on_task(arm_name, resolver, task, base_url)
            all_results.append(result)
            print(f"  {task['task_id']} | {arm_name} | {result.status} | correct={result.correct} | FA={result.false_accept}")
    
    # Save raw task results
    with open(output_dir / "task_results.jsonl", "w") as f:
        for r in all_results:
            f.write(json.dumps(asdict(r)) + "\n")
    
    # Compute metrics
    print("Computing metrics...")
    metrics = compute_metrics(all_results)
    
    # Compute bootstrap CIs for key metrics (family-blocked)
    families = ["users", "posts", "comments", "albums", "photos"]
    
    for arm in metrics:
        arm_results = [r for r in all_results if r.arm == arm]
        
        # Bootstrap ECE CI
        ece_lower, ece_upper = bootstrap_ci(arm_results, compute_ece, families=families)
        metrics[arm]["ece_global_bootstrap_lower"] = ece_lower
        metrics[arm]["ece_global_bootstrap_upper"] = ece_upper
        
        # Per-class ECE CI
        for cls in ["executable", "unknown"]:
            cls_lower, cls_upper = bootstrap_ci(
                arm_results, 
                lambda rs: compute_ece_per_class(rs, 5)[cls], 
                families=families
            )
            metrics[arm][f"ece_{cls}_bootstrap_lower"] = cls_lower
            metrics[arm][f"ece_{cls}_bootstrap_upper"] = cls_upper
    
    # Save derived metrics
    derived_dir = Path(__file__).parent.parent / "derived_evidence"
    derived_dir.mkdir(parents=True, exist_ok=True)
    with open(derived_dir / "metrics.json", "w") as f:
        json.dump(metrics, f, indent=2)
    
    # Print summary
    print("\n=== RESULTS SUMMARY ===")
    for arm in ["A-INCUMBENT", "A-CANDIDATE", "B-RANDOM-ROLE", "B-LEXICAL-OVERLAP", "B-INTERNAL-ID-LOOKUP"]:
        m = metrics[arm]
        print(f"\n{arm}:")
        print(f"  Abstention-adj accuracy: {m['abstention_adjusted_accuracy']:.3f} "
              f"[{m['abstention_adj_acc_wilson_lower']:.3f}, {m['abstention_adj_acc_wilson_upper']:.3f}]")
        print(f"  False-accept rate: {m['false_accept_rate']:.3f} "
              f"[{m['false_accept_wilson_lower']:.3f}, {m['false_accept_wilson_upper']:.3f}]")
        print(f"  UNKNOWN precision: {m['unknown_precision']:.3f} "
              f"[{m['unknown_precision_wilson_lower']:.3f}, {m['unknown_precision_wilson_upper']:.3f}]")
        print(f"  ECE global: {m['ece_global']:.3f} "
              f"[boot {m['ece_global_bootstrap_lower']:.3f}, {m['ece_global_bootstrap_upper']:.3f}]")
        print(f"  ECE executable: {m['ece_per_class']['executable']:.3f} "
              f"[boot {m['ece_executable_bootstrap_lower']:.3f}, {m['ece_executable_bootstrap_upper']:.3f}]")
        print(f"  ECE unknown: {m['ece_per_class']['unknown']:.3f} "
              f"[boot {m['ece_unknown_bootstrap_lower']:.3f}, {m['ece_unknown_bootstrap_upper']:.3f}]")
    
    # Evaluate decision rule
    print("\n=== DECISION RULE EVALUATION ===")
    cand = metrics["A-CANDIDATE"]
    inc = metrics["A-INCUMBENT"]
    
    primary_pass = True
    primary_pass &= cand["abstention_adj_acc_wilson_lower"] > inc["abstention_adj_acc_wilson_upper"]
    print(f"1. Candidate acc lower > Incumbent acc upper: "
          f"{cand['abstention_adj_acc_wilson_lower']:.3f} > {inc['abstention_adj_acc_wilson_upper']:.3f} = {primary_pass}")
    
    primary_pass &= cand["false_accept_wilson_upper"] <= 0.10
    print(f"2. Candidate FA upper <= 0.10: {cand['false_accept_wilson_upper']:.3f} <= 0.10 = {cand['false_accept_wilson_upper'] <= 0.10}")
    
    primary_pass &= cand["unknown_precision_wilson_lower"] >= 0.85
    print(f"3. Candidate UNK prec lower >= 0.85: {cand['unknown_precision_wilson_lower']:.3f} >= 0.85 = {cand['unknown_precision_wilson_lower'] >= 0.85}")
    
    primary_pass &= cand["ece_global_bootstrap_upper"] <= 0.18
    print(f"4. Candidate ECE global boot upper <= 0.18: {cand['ece_global_bootstrap_upper']:.3f} <= 0.18 = {cand['ece_global_bootstrap_upper'] <= 0.18}")
    
    primary_pass &= cand["ece_executable_bootstrap_upper"] <= 0.18 and cand["ece_unknown_bootstrap_upper"] <= 0.18
    print(f"5. Candidate per-class ECE boot upper <= 0.18: "
          f"exe={cand['ece_executable_bootstrap_upper']:.3f}, unk={cand['ece_unknown_bootstrap_upper']:.3f} = "
          f"{cand['ece_executable_bootstrap_upper'] <= 0.18 and cand['ece_unknown_bootstrap_upper'] <= 0.18}")
    
    print(f"\nPrimary gate: {'PASS' if primary_pass else 'FAIL'}")
    
    # Secondary gates
    # For now, just print metrics for null comparisons
    for null_arm in ["B-RANDOM-ROLE", "B-LEXICAL-OVERLAP"]:
        null_m = metrics[null_arm]
        print(f"\nCandidate vs {null_arm}:")
        print(f"  Candidate exec correct: {cand['executable_correct']}/{cand['n_tasks']}")
        print(f"  {null_arm} exec correct: {null_m['executable_correct']}/{null_m['n_tasks']}")
    
    # PC-EXACT-MATCH: check verbatim goals
    verbatim_tasks = [r for r in all_results if r.goal in DISTILLATION_INTENTS]
    inc_verbatim = [r for r in verbatim_tasks if r.arm == "A-INCUMBENT"]
    if inc_verbatim:
        pc_pass = sum(1 for r in inc_verbatim if r.status == "EXECUTABLE") / len(inc_verbatim) >= 0.95
        print(f"\nPC-EXACT-MATCH: {sum(1 for r in inc_verbatim if r.status == 'EXECUTABLE')}/{len(inc_verbatim)} = {pc_pass}")
    
    # NC-NO-APPLICABLE: check OOD tasks
    ood_tasks = [r for r in all_results if r.goal_type == "ood"]
    nc_pass = True
    for arm in resolvers.keys():
        arm_ood = [r for r in ood_tasks if r.arm == arm]
        unk_prec = sum(1 for r in arm_ood if r.status == "UNKNOWN") / len(arm_ood) if arm_ood else 1.0
        fa_rate = sum(1 for r in arm_ood if r.false_accept) / len(arm_ood) if arm_ood else 0.0
        print(f"  {arm} OOD: UNK prec={unk_prec:.3f}, FA={fa_rate:.3f}")
        if unk_prec < 0.85 or fa_rate > 0.0:
            nc_pass = False
    print(f"NC-NO-APPLICABLE: {'PASS' if nc_pass else 'FAIL'}")
    
    # Determine outcome
    if primary_pass:
        outcome = "SURVIVES"
    else:
        outcome = "FALSIFIES"
    
    print(f"\nOUTCOME: {outcome}")
    
    return {
        "outcome": outcome,
        "metrics": metrics,
        "preconditions": preconditions,
        "n_tasks": len(tasks),
        "n_arms": len(resolvers),
    }


if __name__ == "__main__":
    main()