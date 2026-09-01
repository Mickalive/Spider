#!/usr/bin/env python3
"""Debug script to understand resolution behavior."""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parents[3] / "src"))

from spider import Mechanism, Observation, ResolutionStatus
from spider.kernel import SpiderKernel
from spider.registry import MechanismRegistry
import tempfile

# Create a temporary registry
td = tempfile.TemporaryDirectory()
reg = MechanismRegistry(Path(td.name) / "mechanisms.jsonl")
kernel = SpiderKernel(reg)

# Create the parameterized mechanism manually
param_mechanism = Mechanism(
    mechanism_id="param-delete-item",
    intent="delete-item",
    preconditions={"authenticated": True, "role": "owner", "resource_type": "item"},
    action_template={"method": "DELETE", "path": "/api/items/${id}", "headers": {"Authorization": "Bearer ${token}"}},
    postconditions={"exists": False, "deleted_count": 1},
    parameter_slots=["id", "token"],
    confidence=0.9
)
reg.upsert(param_mechanism)

print("=== Mechanism registered ===")
print(f"Mechanism ID: {param_mechanism.mechanism_id}")
print(f"Parameter slots: {param_mechanism.parameter_slots}")
print(f"Action template: {param_mechanism.action_template}")
print(f"Confidence: {param_mechanism.confidence}")

print("\n=== Attempting resolution ===")
context = {"authenticated": True, "role": "owner", "resource_type": "item"}
params = {"id": "99", "token": "test-token-123"}

print(f"Context: {context}")
print(f"Params: {params}")

resolution = kernel.resolve("delete-item", context, params)
print(f"\nResolution status: {resolution.status}")
print(f"Resolution mechanism_id: {resolution.mechanism_id}")
print(f"Resolution bound_action: {resolution.bound_action}")
print(f"Resolution reason: {resolution.reason}")
print(f"Resolution confidence: {resolution.confidence}")

# Debug: check what mechanisms are in the registry
print("\n=== Registry contents ===")
for m in reg.all():
    print(f"  {m.mechanism_id}: intent={m.intent}, confidence={m.confidence}, slots={m.parameter_slots}")

td.cleanup()
