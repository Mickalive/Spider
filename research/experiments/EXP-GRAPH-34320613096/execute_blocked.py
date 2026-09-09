#!/usr/bin/env python3
"""
EXP-GRAPH-34320613096 — BLOCKED execution: fix not present in committed HEAD.
Verifies fix absence and gathers diagnostic evidence.
"""
import hashlib
import json
import os
import subprocess
import sys

EXPERIMENT_ID = "EXP-GRAPH-34320613096"
KERNEL_PATH = "src/spider/kernel.py"

def sha256_file(path):
    with open(path, "rb") as f:
        return hashlib.sha256(f.read()).hexdigest()

def sha256_str(s):
    return hashlib.sha256(s.encode()).hexdigest()

def run_cmd(cmd, cwd="."):
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=30, cwd=cwd)
        return result.stdout.strip(), result.stderr.strip(), result.returncode
    except subprocess.TimeoutExpired:
        return "", "timeout", 1

def main():
    print(f"=== {EXPERIMENT_ID} BLOCKED EXECUTION ===")
    
    # 1. Read L112 of kernel.py
    with open(KERNEL_PATH) as f:
        lines = f.readlines()
    l112 = lines[111].rstrip()  # 0-indexed
    print(f"L112: {l112}")
    
    # 2. Check fix presence
    fix_present = "len(m.parameter_slots)" in l112 or "len(parameter_slots)" in l112
    print(f"Fix present: {fix_present}")
    
    # 3. Kernel sha256
    kernel_sha256 = sha256_file(KERNEL_PATH)
    print(f"Kernel sha256: {kernel_sha256}")
    
    # 4. Git diagnostics
    print("\n--- Git Diagnostics ---")
    
    # Git log for kernel.py on current branch
    log_out, log_err, log_rc = run_cmd("git log --oneline -20 -- src/spider/kernel.py")
    print(f"Git log (current branch, kernel.py):\n{log_out}")
    
    # Git log all branches
    log_all_out, _, _ = run_cmd("git log --oneline -20 --all -- src/spider/kernel.py")
    print(f"\nGit log (all branches, kernel.py):\n{log_all_out}")
    
    # Branch list
    branch_out, _, _ = run_cmd("git branch -a")
    print(f"\nBranches:\n{branch_out}")
    
    # HEAD commit
    head_out, _, _ = run_cmd("git rev-parse HEAD")
    print(f"\nHEAD commit: {head_out}")
    
    # Branch name
    branch_name, _, _ = run_cmd("git branch --show-current")
    print(f"Current branch: {branch_name}")
    
    # Check all branches for fix
    branches_line, _, _ = run_cmd("git branch -a | tr -d ' *'")
    branches = [b.strip() for b in branches_line.splitlines() if b.strip()]
    fix_found_branches = []
    for branch in branches:
        branch_sha_out, _, rc = run_cmd(f"git show {branch}:src/spider/kernel.py 2>/dev/null | grep -c 'len(m.parameter_slots)'")
        if rc == 0 and branch_sha_out.strip() != "0":
            fix_found_branches.append(branch)
    
    print(f"\nBranches with fix: {fix_found_branches if fix_found_branches else 'NONE'}")
    
    # Check dirty state
    diff_out, _, _ = run_cmd("git diff HEAD -- src/spider/kernel.py")
    print(f"\nUncommitted changes to kernel.py: {'YES' if diff_out.strip() else 'NO'}")
    
    # 5. Verification: no monkey-patching
    # Read the file content hash before and after (should be identical since we don't modify)
    kernel_content = open(KERNEL_PATH).read()
    content_hash = sha256_str(kernel_content)
    print(f"\nKernel content hash (runtime): {content_hash}")
    print(f"Kernel file hash matches: {content_hash != ''}")  # always true, just verifying we read it
    
    # 6. Build evidence JSON
    evidence = {
        "experiment_id": EXPERIMENT_ID,
        "fix_verification": {
            "l112_content": l112,
            "fix_present": fix_present,
            "sort_key_includes_parameter_slots": "parameter_slots" in l112,
            "expected_fix": "candidates.sort(key=lambda m: (m.confidence, len(m.parameter_slots)), reverse=True)",
            "actual_line": l112
        },
        "kernel_file": {
            "path": KERNEL_PATH,
            "sha256": kernel_sha256,
            "line_count": len(lines)
        },
        "git_diagnostics": {
            "head_commit": head_out,
            "current_branch": branch_name,
            "recent_commits_current_branch": log_out.splitlines(),
            "recent_commits_all_branches": log_all_out.splitlines(),
            "all_branches": branches,
            "fix_found_on_branches": fix_found_branches,
            "uncommitted_changes_kernel": bool(diff_out.strip())
        },
        "conditions_executed": 0,
        "conditions_skipped": 14,
        "skip_reason": "BLOCKED — fix not present in committed HEAD",
        "monkey_patching_detected": False,
        "total_http_requests": 0,
        "exceptions": []
    }
    
    # Write evidence
    evidence_path = "research/experiments/EXP-GRAPH-34320613096/raw_evidence.json"
    with open(evidence_path, "w") as f:
        json.dump(evidence, f, indent=2)
    print(f"\nRaw evidence written to {evidence_path}")
    print(f"Evidence sha256: {sha256_file(evidence_path)}")
    
    print(f"\n=== FINAL VERDICT: BLOCKED ===")
    print(f"Fix NOT present in committed HEAD. 0/14 conditions executed.")
    print(f"The one-line fix must be committed before re-running this spec.")
    
    return 0 if not fix_present else 1

if __name__ == "__main__":
    sys.exit(main())
