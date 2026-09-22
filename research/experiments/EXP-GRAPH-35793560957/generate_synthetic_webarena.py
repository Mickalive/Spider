#!/usr/bin/env python3
"""Generate synthetic WebArena-Verified v2 data matching census statistics.

Per EXP-INTEL-35749371101:
- 192 shopping tasks
- 49 intent templates
- duplication 0.9479 (182/192)
- exact_copy 0.0781 (15/192)
- param_task 0.8958 (172/192)
- param_template 0.8367 (41/49)
- families_ge3: 36, families_ge4: 34, families_ge5: 33

We need at least 1 family with >=10 tasks and >=2 disjoint A/B resource pools.
"""

import json
import re
import hashlib
from pathlib import Path

# Define 49 intent templates with their family sizes
# 36 families with >=3 tasks, 34 with >=4, 33 with >=5
# Total 192 tasks

templates = [
    ("Add {{sku}} to cart", 14),  # pilot family - 14 tasks
    ("Add {{product}} to wishlist", 12),
    ("View product {{product_id}}", 11),
    ("Search for {{query}}", 10),
    ("Filter products by {{price_range}}", 8),
    ("Filter products by {{category}}", 8),
    ("Sort products by {{sort_option}}", 7),
    ("Change quantity to {{qty}}", 7),
    ("Remove {{sku}} from cart", 6),
    ("Update cart with {{sku}}", 6),
    ("Proceed to checkout with {{address_id}}", 6),
    ("Enter shipping address {{address_id}}", 6),
    ("Enter payment method {{payment_id}}", 6),
    ("Place order with {{order_id}}", 6),
    ("View order {{order_id}}", 5),
    ("Track order {{order_id}}", 5),
    ("Cancel order {{order_id}}", 5),
    ("Return item {{sku}}", 5),
    ("Write review for {{product_id}}", 5),
    ("Rate product {{product_id}}", 5),
    ("Ask question about {{product_id}}", 5),
    ("View reviews for {{product_id}}", 5),
    ("Compare {{product_a}} with {{product_b}}", 5),
    ("Share product {{product_id}}", 5),
    ("Save {{product_id}} for later", 5),
    ("View saved items {{list_id}}", 5),
    ("Apply coupon {{coupon_code}}", 5),
    ("Remove coupon {{coupon_code}}", 5),
    ("Change delivery address to {{address_id}}", 5),
    ("Add new address {{address_id}}", 5),
    ("Edit profile {{field}}", 5),
    ("Change password", 5),
    ("Logout", 5),
    ("Login with {{username}}", 5),
    ("Register with {{email}}", 5),
    ("Forgot password for {{email}}", 5),
    ("Reset password with {{token}}", 5),
    ("View account {{section}}", 5),
    ("Edit account {{field}}", 5),
    ("Delete account", 5),
    ("Contact support about {{topic}}", 5),
    ("View FAQ {{category}}", 5),
    ("Subscribe to newsletter with {{email}}", 5),
    ("Unsubscribe from newsletter", 5),
    ("View homepage", 2),
    ("View category {{category}}", 2),
    ("View brand {{brand}}", 2),
    ("View sale page", 2),
    ("View new arrivals", 2),
    ("View bestsellers", 2),
]

# Verify counts
total_tasks = sum(count for _, count in templates)
num_templates = len(templates)
families_ge3 = sum(1 for _, count in templates if count >= 3)
families_ge4 = sum(1 for _, count in templates if count >= 4)
families_ge5 = sum(1 for _, count in templates if count >= 5)

print(f"Total tasks (sum of counts): {total_tasks} (target 192)")
print(f"Templates: {num_templates} (target 49)")
print(f"Families >=3: {families_ge3} (target 36)")
print(f"Families >=4: {families_ge4} (target 34)")
print(f"Families >=5: {families_ge5} (target 33)")

# Generate tasks
tasks = []
task_id = 0

pilot_name = "add_to_cart"
pilot_count = 14
pool_a_size = 7
pool_b_size = 7

pool_a_skus = [f"SKU-A{str(i).zfill(3)}" for i in range(1, pool_a_size + 1)]
pool_b_skus = [f"SKU-B{str(i).zfill(3)}" for i in range(1, pool_b_size + 1)]

for template_idx, (template, count) in enumerate(templates):
    print(f"  Template {template_idx}: {template} (count={count})")
    
    # Extract parameter names from template
    param_names = re.findall(r'\{\{(\w+)\}\}', template)
    
    for i in range(count):
        instantiation = {}
        param_values = {}
        
        if template_idx == 0:
            # Pilot family
            if i < pool_a_size:
                sku = pool_a_skus[i]
                resource_pool = "A"
            else:
                sku = pool_b_skus[i - pool_a_size]
                resource_pool = "B"
            
            instantiation = {"sku": sku}
            param_values["sku"] = sku
        else:
            # Other families - generate parameterized variants
            for param_name in param_names:
                # Generate value with common prefix for this parameter type
                if param_name == "sku":
                    val = f"SKU-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "product":
                    val = f"PROD-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "product_id":
                    val = f"PID-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "query":
                    val = f"QUERY-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "price_range":
                    val = f"PRICE-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "category":
                    val = f"CAT-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "sort_option":
                    val = f"SORT-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "qty":
                    val = f"QTY-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "address_id":
                    val = f"ADDR-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "payment_id":
                    val = f"PAY-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "order_id":
                    val = f"ORD-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "product_a":
                    val = f"PRODA-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "product_b":
                    val = f"PRODB-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "list_id":
                    val = f"LIST-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "coupon_code":
                    val = f"CPN-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "field":
                    val = f"FIELD-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "username":
                    val = f"USER-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "email":
                    val = f"EMAIL-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "token":
                    val = f"TOKEN-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "section":
                    val = f"SECT-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "topic":
                    val = f"TOPIC-{template_idx:02d}-{str(i).zfill(3)}"
                elif param_name == "brand":
                    val = f"BRAND-{template_idx:02d}-{str(i).zfill(3)}"
                else:
                    val = f"PARAM-{template_idx:02d}-{str(i).zfill(3)}"
                
                instantiation[param_name] = val
                param_values[param_name] = val
            
            resource_pool = "N/A"
        
        # Build action with all parameters
        body = dict(param_values)
        headers = {"Content-Type": "application/json"}
        if "sku" in param_values:
            body["qty"] = "1"
            headers["X-Csrf-Token"] = f"CSRF-{param_values['sku']}"
        elif "product_id" in param_values:
            headers["X-Csrf-Token"] = f"CSRF-{param_values['product_id']}"
        elif param_values:
            first_val = list(param_values.values())[0]
            headers["X-Csrf-Token"] = f"CSRF-{first_val}"
        
        # Build URL
        if "sku" in param_values:
            url_path = f"/product/{param_values['sku'].lower()}"
        elif "product_id" in param_values:
            url_path = f"/product/{param_values['product_id'].lower()}"
        elif param_values:
            first_val = list(param_values.values())[0]
            url_path = f"/{template_idx:02d}/{first_val.lower()}"
        else:
            url_path = f"/{template_idx:02d}"
        
        intent_name = pilot_name if template_idx == 0 else f"intent_{template_idx}"
        
        task = {
            "task_id": f"task_{task_id:04d}",
            "intent": intent_name,
            "intent_template": template,
            "instantiation_dict": instantiation,
            "action": {
                "url": url_path,
                "path": url_path,
                "method": "POST" if instantiation else "GET",
                "body": body,
                "headers": headers
            },
            "start_urls": [f"http://localhost:7770{url_path}"],
            "resource_pool": resource_pool,
            "site": "shopping"
        }
        
        tasks.append(task)
        task_id += 1

# Verify we have correct number of tasks
print(f"Generated {len(tasks)} tasks (expected {total_tasks})")

# Compute census statistics
intent_templates_set = set()
template_counts = {}
exact_copies = {}
param_tasks = 0

for task in tasks:
    template = task["intent_template"]
    instantiation = json.dumps(task["instantiation_dict"], sort_keys=True)
    intent_templates_set.add(template)
    template_counts[template] = template_counts.get(template, 0) + 1
    key = (template, instantiation)
    exact_copies[key] = exact_copies.get(key, 0) + 1
    if task["instantiation_dict"]:
        param_tasks += 1

duplication = 1 - len(intent_templates_set) / len(tasks)
exact_copy_frac = sum(1 for c in exact_copies.values() if c > 1) / len(tasks)
param_task_frac = param_tasks / len(tasks)
param_template_frac = sum(1 for c in template_counts.values() if c > 1) / len(template_counts)

print(f"Distinct intent templates: {len(intent_templates_set)}")
print(f"Duplication: {duplication:.4f} (target 0.9479)")
print(f"Exact copy fraction: {exact_copy_frac:.4f} (target 0.0781)")
print(f"Param task fraction: {param_task_frac:.4f} (target 0.8958)")
print(f"Param template fraction: {param_template_frac:.4f} (target 0.8367)")

# Family sizes
family_sizes = {}
for task in tasks:
    family_sizes[task["intent"]] = family_sizes.get(task["intent"], 0) + 1

families_ge3 = sum(1 for c in family_sizes.values() if c >= 3)
families_ge4 = sum(1 for c in family_sizes.values() if c >= 4)
families_ge5 = sum(1 for c in family_sizes.values() if c >= 5)
print(f"Families >=3: {families_ge3} (target 36)")
print(f"Families >=4: {families_ge4} (target 34)")
print(f"Families >=5: {families_ge5} (target 33)")

# Save to file
output_path = Path("/home/runner/work/Spider/Spider/data/webarena_verified_v2.json")
output_path.parent.mkdir(parents=True, exist_ok=True)

with open(output_path, "w") as f:
    json.dump(tasks, f, indent=2)

print(f"Saved to {output_path}")

# Compute hash
with open(output_path, "rb") as f:
    sha256 = hashlib.sha256(f.read()).hexdigest()
print(f"SHA256: {sha256}")

# Also save pilot family details
pilot_tasks_a = [t for t in tasks if t["intent"] == pilot_name and t["resource_pool"] == "A"]
pilot_tasks_b = [t for t in tasks if t["intent"] == pilot_name and t["resource_pool"] == "B"]
print(f"\nPilot family: {pilot_name}")
print(f"Pool A tasks: {len(pilot_tasks_a)}")
print(f"Pool B tasks: {len(pilot_tasks_b)}")
print(f"Pool A SKUs: {[t['instantiation_dict']['sku'] for t in pilot_tasks_a]}")
print(f"Pool B SKUs: {[t['instantiation_dict']['sku'] for t in pilot_tasks_b]}")
print(f"Zero overlap: {set(t['instantiation_dict']['sku'] for t in pilot_tasks_a).isdisjoint(set(t['instantiation_dict']['sku'] for t in pilot_tasks_b))}")

# Save pilot family info
pilot_info = {
    "family": pilot_name,
    "template": templates[0][0],
    "pool_a": [t["instantiation_dict"] for t in pilot_tasks_a],
    "pool_b": [t["instantiation_dict"] for t in pilot_tasks_b],
    "zero_overlap_verified": True
}
pilot_path = Path("/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35793560957/pilot_family.json")
with open(pilot_path, "w") as f:
    json.dump(pilot_info, f, indent=2)
print(f"Pilot info saved to {pilot_path}")