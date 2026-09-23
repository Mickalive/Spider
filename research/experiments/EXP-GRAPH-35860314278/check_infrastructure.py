#!/usr/bin/env python3
"""
Infrastructure check for EXP-GRAPH-35860314278 C-DELTA-REPAIR.
Verifies required substrate per frozen spec.
"""
import os
import subprocess
import json
import hashlib

def check_infrastructure():
    results = {
        "experiment_id": "EXP-GRAPH-35860314278",
        "llm_api_key_present": bool(os.environ.get("OPENAI_API_KEY")),
        "openai_package_installed": False,
        "playwright_installed": False,
        "playwright_browsers": False,
        "nginx_available": False,
        "nginx_version": None,
        "nginx_proxy_cache_configured": False,
        "flask_backend_deployed": False,
        "flask_hs256_backend": False,
        "repair_agent_implemented": False,
        "kernel_available": False,
        "models_available": False,
        "registry_available": False,
    }
    
    # Check openai package
    try:
        import openai
        results["openai_package_installed"] = True
        results["openai_version"] = openai.__version__
    except ImportError:
        pass
    
    # Check playwright
    try:
        import playwright
        results["playwright_installed"] = True
        results["playwright_version"] = playwright.__version__
        # Check browsers
        try:
            result = subprocess.run(["playwright", "install", "--help"], capture_output=True, text=True, timeout=5)
            results["playwright_browsers"] = result.returncode == 0
        except:
            pass
    except ImportError:
        pass
    
    # Check nginx
    try:
        result = subprocess.run(["nginx", "-v"], capture_output=True, text=True, timeout=5)
        results["nginx_available"] = True
        results["nginx_version"] = result.stderr.strip() or result.stdout.strip()
    except:
        pass
    
    # Check nginx config for proxy_cache
    nginx_conf_paths = [
        "/etc/nginx/nginx.conf",
        "/etc/nginx/sites-enabled/default",
        "/usr/local/nginx/conf/nginx.conf"
    ]
    for path in nginx_conf_paths:
        if os.path.exists(path):
            with open(path) as f:
                content = f.read()
                if "proxy_cache" in content and ("HIT" in content or "stale-while-revalidate" in content or "stale-if-error" in content):
                    results["nginx_proxy_cache_configured"] = True
                    break
    
    # Check Flask backend
    testbed_paths = [
        "/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35860314278/testbed_server.py",
        "/home/runner/work/Spider/Spider/substrates/testbed_server.py",
    ]
    for path in testbed_paths:
        if os.path.exists(path):
            results["flask_backend_deployed"] = True
            with open(path) as f:
                if "HS256" in f.read() or "PyJWT" in f.read():
                    results["flask_hs256_backend"] = True
            break
    
    # Check kernel
    try:
        from src.spider import kernel, models, registry
        results["kernel_available"] = True
        results["models_available"] = True
        results["registry_available"] = True
    except ImportError:
        pass
    
    # Check repair agent implementation
    repair_agent_path = "/home/runner/work/Spider/Spider/research/graph/delta_repair/execute_delta_repair_real.py"
    if os.path.exists(repair_agent_path):
        results["repair_agent_implemented"] = True
    
    return results

if __name__ == "__main__":
    results = check_infrastructure()
    print(json.dumps(results, indent=2))
    
    # Save raw evidence
    with open("/home/runner/work/Spider/Spider/research/experiments/EXP-GRAPH-35860314278/raw_evidence/infrastructure_check.json", "w") as f:
        json.dump(results, f, indent=2)
    
    # Determine if MEASUREMENT_INVALID/BLOCKED
    critical_missing = []
    if not results["llm_api_key_present"]:
        critical_missing.append("OPENAI_API_KEY")
    if not results["openai_package_installed"]:
        critical_missing.append("openai package")
    if not results["playwright_installed"]:
        critical_missing.append("playwright")
    if not results["nginx_proxy_cache_configured"]:
        critical_missing.append("nginx proxy_cache HIT/SWR/SIE/304")
    if not results["flask_backend_deployed"]:
        critical_missing.append("Flask HS256 backend")
    if not results["repair_agent_implemented"]:
        critical_missing.append("real LLM+Playwright+verify repair agent")
    
    if critical_missing:
        print(f"\nBLOCKED: Missing critical infrastructure: {', '.join(critical_missing)}")
        exit(1)
    else:
        print("\nAll critical infrastructure present")
        exit(0)
