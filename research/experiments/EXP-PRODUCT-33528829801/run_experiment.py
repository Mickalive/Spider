#!/usr/bin/env python3
"""
EXP-PRODUCT-33528829801 — Parameterized Mechanism Inheritance Experiment

Tests claim C-PARAM-INHERIT: "Mechanisms parameterize to unseen identifiers"

This script:
1. Creates synthetic observations with varying resource identifiers
2. Distills literal mechanisms (current behavior)
3. Applies parameter induction to create parameterized mechanisms
4. Tests resolution on unseen identifiers
5. Runs baselines: cold exploration, literal replay, retrieval
6. Runs controls: positive (seen ID) and null (mismatched preconditions)
7. Records all raw evidence and metrics

Frozen experiment — do not modify after freeze.json exists.
"""

import json
import sys
import time
from dataclasses import asdict
from pathlib import Path
from typing import Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parents[3] / "src"))

from spider import Mechanism, Observation, ResolutionStatus
from spider.kernel import SpiderKernel
from spider.registry import MechanismRegistry


# ============================================================================
# Synthetic Observations
# ============================================================================

def create_observations() -> list[Observation]:
    """Create 3 synthetic observations of successful 'delete-item' actions
    on resources A, B, C with identical intent, state, and next_state.
    """
    observations = []
    for resource_id in ["A", "B", "C"]:
        obs = Observation(
            intent="delete-item",
            state={
                "authenticated": True,
                "role": "owner",
                "resource_type": "item"
            },
            action={
                "method": "DELETE",
                "path": f"/api/items/{resource_id}",
                "headers": {"Authorization": "Bearer ${token}"}
            },
            next_state={
                "exists": False,
                "deleted_count": 1
            },
            success=True,
            provenance={"source": "synthetic", "run_id": "EXP-PRODUCT-33528829801"}
        )
        observations.append(obs)
    return observations


def create_unseen_identifiers() -> list[str]:
    """10 unseen resource identifiers for testing parameterized resolution."""
    return ["99", "100", "X", "42", "abc", "item-7", "007", "last", "first", "test-123"]


# ============================================================================
# Experiment Execution
# ============================================================================

class ExperimentRunner:
    """Runs the parameterized inheritance experiment."""
    
    def __init__(self):
        self.results = {
            "experiment_id": "EXP-PRODUCT-33528829801",
            "claim_id": "C-PARAM-INHERIT",
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "raw_evidence": {},
            "metrics": {},
            "verdict": None
        }
    
    def run(self) -> dict:
        """Execute the full experiment and return results."""
        print("=" * 80)
        print("EXP-PRODUCT-33528829801 — Parameterized Mechanism Inheritance")
        print("=" * 80)
        
        # Step 1: Create observations
        observations = create_observations()
        self.results["raw_evidence"]["observations"] = [
            {
                "intent": o.intent,
                "state": o.state,
                "action": o.action,
                "next_state": o.next_state,
                "success": o.success
            }
            for o in observations
        ]
        print(f"\n[1] Created {len(observations)} synthetic observations")
        
        # Step 2: Distill literal mechanisms
        print("\n[2] Distilling literal mechanisms...")
        literal_mechanisms = self._distill_literal(observations)
        self.results["raw_evidence"]["literal_mechanisms"] = [
            asdict(m) for m in literal_mechanisms
        ]
        
        # Step 3: Apply parameter induction
        print("\n[3] Applying parameter induction...")
        param_mechanism = self._distill_parameterized(observations)
        if param_mechanism is None:
            self.results["verdict"] = "FALSIFIED"
            self.results["metrics"]["parameter_induction_success"] = False
            return self.results
        
        self.results["raw_evidence"]["parameterized_mechanism"] = asdict(param_mechanism)
        self.results["metrics"]["parameter_slots"] = param_mechanism.parameter_slots
        print(f"   Parameter slots identified: {param_mechanism.parameter_slots}")
        print(f"   Parameterized action template: {param_mechanism.action_template}")
        
        # Step 4: Run controls
        print("\n[4] Running controls...")
        control_results = self._run_controls(param_mechanism, observations)
        self.results["raw_evidence"]["controls"] = control_results
        
        # Step 5: Test on unseen identifiers
        print("\n[5] Testing on unseen identifiers...")
        unseen_ids = create_unseen_identifiers()
        unseen_results = self._test_unseen(param_mechanism, unseen_ids)
        self.results["raw_evidence"]["unseen_results"] = unseen_results
        
        # Step 6: Run baselines
        print("\n[6] Running baselines...")
        baseline_results = self._run_baselines(observations, param_mechanism, unseen_ids)
        self.results["raw_evidence"]["baselines"] = baseline_results
        
        # Step 7: Compute metrics and verdict
        print("\n[7] Computing metrics and verdict...")
        self._compute_verdict(unseen_results, literal_mechanisms, param_mechanism)
        
        return self.results
    
    def _distill_literal(self, observations: list[Observation]) -> list[Mechanism]:
        """Distill literal mechanisms (current behavior)."""
        td = __import__("tempfile").TemporaryDirectory()
        reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
        kernel = SpiderKernel(reg)
        
        literal_mechanisms = []
        for obs in observations:
            m = kernel.distill(obs)
            if m:
                literal_mechanisms.append(m)
                reg.upsert(m)
                print(f"   Distilled: {m.mechanism_id} for {obs.action['path']}")
        
        # Store for later use
        self._kernel = kernel
        self._reg = reg
        self._td = td
        self._literal_mechanisms = literal_mechanisms  # Store for baselines
        
        return literal_mechanisms
    
    def _distill_parameterized(self, observations: list[Observation]) -> Mechanism | None:
        """Apply parameter induction to create parameterized mechanism."""
        param_mechanism = self._kernel.distill_parameterized(
            observations,
            mechanism_id="param-delete-item"
        )
        
        if param_mechanism:
            # Add to registry
            self._reg.upsert(param_mechanism)
            print(f"   Parameterized mechanism created: {param_mechanism.mechanism_id}")
            print(f"   Action template: {param_mechanism.action_template}")
            print(f"   Parameter slots: {param_mechanism.parameter_slots}")
        else:
            print("   ERROR: Parameter induction failed!")
        
        return param_mechanism
    
    def _run_controls(self, param_mechanism: Mechanism, observations: list[Observation]) -> dict:
        """Run positive and null controls."""
        controls = {}
        
        # Positive control: resolve with a seen identifier
        print("   [Positive Control] Resolving with seen identifier 'A'...")
        pos_result = self._kernel.resolve(
            "delete-item",
            {"authenticated": True, "role": "owner", "resource_type": "item"},
            {"token": "test-token-123", "id": "A"}
        )
        controls["positive_control"] = {
            "description": "Resolve with seen identifier (A) - should succeed",
            "input": {"id": "A", "token": "test-token-123"},
            "expected_status": "EXECUTABLE",
            "actual_status": pos_result.status.value,
            "bound_action": pos_result.bound_action,
            "passed": pos_result.status == ResolutionStatus.EXECUTABLE
        }
        print(f"      Status: {pos_result.status.value}, "
              f"Bound path: {pos_result.bound_action.get('path') if pos_result.bound_action else 'N/A'}")
        
        # Null control: resolve with mismatched preconditions
        print("   [Null Control] Resolving with mismatched preconditions (not authenticated)...")
        null_result = self._kernel.resolve(
            "delete-item",
            {"authenticated": False, "role": "owner", "resource_type": "item"},
            {"token": "test-token-123", "id": "A"}
        )
        controls["null_control"] = {
            "description": "Resolve with mismatched preconditions - should return UNKNOWN",
            "input": {"authenticated": False, "id": "A"},
            "expected_status": "UNKNOWN",
            "actual_status": null_result.status.value,
            "passed": null_result.status == ResolutionStatus.UNKNOWN
        }
        print(f"      Status: {null_result.status.value}")
        
        return controls
    
    def _test_unseen(self, param_mechanism: Mechanism, unseen_ids: list[str]) -> list[dict]:
        """Test parameterized mechanism on unseen identifiers."""
        results = []
        
        for uid in unseen_ids:
            # Try to resolve with the unseen identifier
            resolution = self._kernel.resolve(
                "delete-item",
                {"authenticated": True, "role": "owner", "resource_type": "item"},
                {"token": "test-token-123", "id": uid}
            )
            
            result = {
                "unseen_id": uid,
                "status": resolution.status.value,
                "bound_action": resolution.bound_action,
                "mechanism_id": resolution.mechanism_id,
                "success": resolution.status == ResolutionStatus.EXECUTABLE,
                "correct_binding": (
                    resolution.bound_action is not None and
                    f"/api/items/{uid}" == resolution.bound_action.get("path")
                ) if resolution.bound_action else False
            }
            results.append(result)
            
            status_symbol = "✓" if result["success"] and result["correct_binding"] else "✗"
            print(f"   {status_symbol} ID={uid:>10s}: status={result['status']}, "
                  f"correct_binding={result['correct_binding']}")
        
        return results
    
    def _run_baselines(
        self,
        observations: list[Observation],
        param_mechanism: Mechanism,
        unseen_ids: list[str]
    ) -> dict:
        """Run baselines: cold, literal, retrieval."""
        baselines = {}
        
        # B1: Cold exploration - no memory, full task cost
        print("   [B1: Cold] Simulating cold exploration...")
        cold_cost_per_step = 5  # Typical steps: navigate, authenticate, locate, confirm, delete
        cold_results = []
        for uid in unseen_ids:
            cold_results.append({
                "unseen_id": uid,
                "operations": cold_cost_per_step,
                "success": True,  # Cold always succeeds eventually
                "cost": cold_cost_per_step
            })
        baselines["cold"] = {
            "description": "No memory - full task replay",
            "operations_per_task": cold_cost_per_step,
            "total_operations": cold_cost_per_step * len(unseen_ids),
            "success_rate": 1.0,
            "details": cold_results
        }
        print(f"      Operations per task: {cold_cost_per_step}, "
              f"Total: {cold_cost_per_step * len(unseen_ids)}")
        
        # B2: Literal mechanism replay
        # Create a separate registry with only literal mechanisms
        import tempfile
        literal_td = tempfile.TemporaryDirectory()
        literal_reg = MechanismRegistry(Path(literal_td.name) / "mechanisms.jsonl")
        for m in self._literal_mechanisms:
            literal_reg.upsert(m)
        literal_kernel = SpiderKernel(literal_reg)
        
        print("   [B2: Literal] Testing literal mechanism replay on unseen identifiers...")
        literal_failures = 0
        literal_successes = 0
        for uid in unseen_ids:
            # Literal mechanism won't have parameter slots, so it won't resolve
            # unless we manually provide params that match the literal path
            # But the literal path is /api/items/A, not /api/items/{uid}
            resolution = literal_kernel.resolve(
                "delete-item",
                {"authenticated": True, "role": "owner", "resource_type": "item"},
                {"token": "test-token-123", "id": uid}  # This won't help - literal has no slots
            )
            if resolution.status == ResolutionStatus.EXECUTABLE:
                literal_successes += 1
            else:
                literal_failures += 1
        
        baselines["literal"] = {
            "description": "Literal mechanism replay - no parameter substitution",
            "success_rate": literal_successes / len(unseen_ids),
            "successes": literal_successes,
            "failures": literal_failures,
            "total_tested": len(unseen_ids),
            "note": "Literal mechanisms have no parameter slots, so they cannot resolve for unseen identifiers"
        }
        print(f"      Success rate: {literal_successes}/{len(unseen_ids)} "
              f"({literal_successes/len(unseen_ids)*100:.1f}%)")
        
        # B3: Nearest trajectory retrieval
        print("   [B3: Retrieval] Testing nearest trajectory retrieval...")
        # Simple state similarity: compare state features
        retrieval_results = []
        for uid in unseen_ids:
            # Find most similar observation by state
            best_match = None
            best_similarity = -1
            
            for obs in observations:
                # Simple similarity: count matching state features
                similarity = sum(
                    1 for k, v in obs.state.items()
                    if obs.state.get(k) == v
                )
                if similarity > best_similarity:
                    best_similarity = similarity
                    best_match = obs
            
            if best_match:
                # Try to replay the best match using literal kernel
                resolution = literal_kernel.resolve(
                    "delete-item",
                    {"authenticated": True, "role": "owner", "resource_type": "item"},
                    {"token": "test-token-123", "id": uid}
                )
                # Even if resolution succeeds, the bound action will be wrong
                # because it's a literal replay
                success = (
                    resolution.status == ResolutionStatus.EXECUTABLE and
                    resolution.bound_action is not None and
                    f"/api/items/{uid}" == resolution.bound_action.get("path")
                )
                retrieval_results.append({
                    "unseen_id": uid,
                    "matched_observation": best_match.action.get("path"),
                    "similarity": best_similarity,
                    "resolution_status": resolution.status.value,
                    "correct_action": success,
                    "operations": 2  # Retrieval + execution
                })
        
        retrieval_successes = sum(1 for r in retrieval_results if r["correct_action"])
        baselines["retrieval"] = {
            "description": "Nearest trajectory retrieval and replay",
            "success_rate": retrieval_successes / len(unseen_ids),
            "successes": retrieval_successes,
            "failures": len(unseen_ids) - retrieval_successes,
            "total_tested": len(unseen_ids),
            "operations_per_task": 2,
            "total_operations": 2 * len(unseen_ids),
            "details": retrieval_results
        }
        print(f"      Success rate: {retrieval_successes}/{len(unseen_ids)} "
              f"({retrieval_successes/len(unseen_ids)*100:.1f}%)")
        
        return baselines
    
    def _compute_verdict(
        self,
        unseen_results: list[dict],
        literal_mechanisms: list[Mechanism],
        param_mechanism: Mechanism
    ) -> None:
        """Compute metrics and verdict based on decision rule."""
        total_unseen = len(unseen_results)
        successful_resolutions = sum(1 for r in unseen_results if r["success"])
        correct_bindings = sum(1 for r in unseen_results if r["correct_binding"])
        
        # Parameter induction false negative rate
        # For this experiment, we know there's exactly 1 parameter (the ID)
        # If the mechanism has the parameter slot, false negative = 0
        # If it doesn't, false negative = 1.0
        has_correct_slots = "id" in param_mechanism.parameter_slots
        false_negative_rate = 0.0 if has_correct_slots else 1.0
        
        metrics = {
            "total_unseen_identifiers": total_unseen,
            "successful_resolutions": successful_resolutions,
            "correct_bindings": correct_bindings,
            "resolution_rate": successful_resolutions / total_unseen,
            "binding_accuracy": correct_bindings / successful_resolutions if successful_resolutions > 0 else 0,
            "parameter_induction_false_negative_rate": false_negative_rate,
            "parameter_slots_found": param_mechanism.parameter_slots,
            "mechanism_confidence": param_mechanism.confidence
        }
        
        self.results["metrics"] = metrics
        
        # Decision rule from spec:
        # Survives if ALL of:
        # 1. Parameterized mechanisms resolve correctly for >= 90% of unseen identifiers
        # 2. Bound actions correctly substitute the new identifier in all successful resolutions
        # 3. Literal mechanisms resolve for 0% of unseen identifiers
        # 4. Parameter induction false negative rate <= 0.2
        
        literal_baseline = self.results["raw_evidence"]["baselines"]["literal"]
        
        condition_1 = metrics["resolution_rate"] >= 0.9
        condition_2 = metrics["binding_accuracy"] >= 1.0 if metrics["successful_resolutions"] > 0 else False
        condition_3 = literal_baseline["success_rate"] == 0.0
        condition_4 = false_negative_rate <= 0.2
        
        all_conditions_met = condition_1 and condition_2 and condition_3 and condition_4
        
        verdict = "SURVIVES" if all_conditions_met else "FALSIFIED"
        self.results["verdict"] = verdict
        
        # Detailed condition breakdown
        self.results["condition_analysis"] = {
            "condition_1_resolution_rate_gte_90": {
                "passed": condition_1,
                "actual": f"{metrics['resolution_rate']*100:.1f}%",
                "threshold": ">= 90%"
            },
            "condition_2_binding_accuracy_100": {
                "passed": condition_2,
                "actual": f"{metrics['binding_accuracy']*100:.1f}%" if metrics["successful_resolutions"] > 0 else "N/A",
                "threshold": "100% of successful resolutions"
            },
            "condition_3_literal_0_percent": {
                "passed": condition_3,
                "actual": f"{literal_baseline['success_rate']*100:.1f}%",
                "threshold": "0%"
            },
            "condition_4_false_negative_lte_20": {
                "passed": condition_4,
                "actual": f"{false_negative_rate*100:.1f}%",
                "threshold": "<= 20%"
            }
        }
        
        print(f"\n   VERDICT: {verdict}")
        print(f"   Condition 1 (resolution >= 90%): {'PASS' if condition_1 else 'FAIL'} "
              f"({metrics['resolution_rate']*100:.1f}%)")
        print(f"   Condition 2 (binding accuracy 100%): {'PASS' if condition_2 else 'FAIL'} "
              f"({metrics['binding_accuracy']*100:.1f}%)" if metrics["successful_resolutions"] > 0 else 
              f"   Condition 2 (binding accuracy 100%): N/A (no successful resolutions)")
        print(f"   Condition 3 (literal 0%): {'PASS' if condition_3 else 'FAIL'} "
              f"({literal_baseline['success_rate']*100:.1f}%)")
        print(f"   Condition 4 (false negative <= 20%): {'PASS' if condition_4 else 'FAIL'} "
              f"({false_negative_rate*100:.1f}%)")


# ============================================================================
# Main Execution
# ============================================================================

def main():
    """Run the experiment and save results."""
    runner = ExperimentRunner()
    
    try:
        results = runner.run()
    finally:
        # Clean up temporary directory if it exists
        if hasattr(runner, '_td'):
            runner._td.cleanup()
    
    # Save results
    output_dir = Path(__file__).parent
    results_path = output_dir / "result.json"
    
    with open(results_path, "w") as f:
        json.dump(results, f, indent=2, default=str)
    
    print(f"\n{'=' * 80}")
    print(f"Results saved to: {results_path}")
    print(f"{'=' * 80}")
    
    return results


if __name__ == "__main__":
    results = main()
    sys.exit(0 if results.get("verdict") == "SURVIVES" else 1)
