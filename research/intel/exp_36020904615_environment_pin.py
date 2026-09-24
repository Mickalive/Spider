"""
EXP-INTEL-36020904615 MV3/MV9 environment pin.

Records: pip freeze (hash + line count), pinned package versions, playwright version,
chromium validation, grammar file live hash + body-regex presence, docker images
--digests, container health for localhost:7770, viewport 1280x720, AX mode.
Writes artifacts/raw/environment_pin.json.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXP = ROOT / "experiments" / "EXP-INTEL-36020904615"
RAW = EXP / "artifacts" / "raw"
RAW.mkdir(parents=True, exist_ok=True)
EXP_ID = "EXP-INTEL-36020904615"

GRAMMAR = ROOT / "intel" / "grammar_fulltree_358885.py"  # ROOT == <repo>/research


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main() -> None:
    # pip freeze
    p = subprocess.run([sys.executable, "-m", "pip", "freeze"], capture_output=True, text=True, timeout=300)
    freeze_txt = p.stdout
    freeze_path = Path("/tmp/opencode/exp_36020904615_pip_freeze.txt")
    freeze_path.write_text(freeze_txt)

    def pkg(name: str) -> str | None:
        r = subprocess.run([sys.executable, "-m", "pip", "show", name], capture_output=True, text=True, timeout=120)
        for line in r.stdout.splitlines():
            if line.startswith("Version:"):
                return line.split(":", 1)[1].strip()
        return None

    pv = subprocess.run([sys.executable, "-m", "playwright", "--version"], capture_output=True, text=True, timeout=120)
    docker_digests = subprocess.run(["docker", "images", "--digests"], capture_output=True, text=True, timeout=120)
    (RAW / "docker_images_digests.txt").write_text(docker_digests.stdout)

    # container health (3 tries, as frozen baseline B-WEBARENA-SHOPPING-DOCKER)
    health = []
    for i in range(3):
        t0 = time.time()
        try:
            with urllib.request.urlopen("http://localhost:7770/", timeout=30) as r:
                health.append({"attempt": i + 1, "status": r.status, "bytes": len(r.read()),
                               "elapsed_s": round(time.time() - t0, 3)})
        except Exception as e:  # noqa: BLE001
            health.append({"attempt": i + 1, "status": None, "error": f"{type(e).__name__}: {e}",
                           "elapsed_s": round(time.time() - t0, 3)})
        time.sleep(1)

    # grammar live hash
    sys.path.insert(0, str(ROOT / "intel"))
    import grammar_fulltree_358885 as g  # noqa: E402
    grammar_hash = g.recompute_grammar_hash()
    grammar_src = GRAMMAR.read_text()
    body_regex_present = r"<body[^>]*>.*?</body>" in grammar_src and "re.DOTALL" in grammar_src
    fotorama_present = "fotorama" in grammar_src

    # chromium validation (launch + CDP Accessibility.getFullAXTree availability)
    chromium = {"version": None, "launch_ok": False, "cdp_fullaxtree": False, "viewport": "1280x720"}
    try:
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            b = pw.chromium.launch(headless=True)
            ctx = b.new_context(viewport={"width": 1280, "height": 720})
            page = ctx.new_page()
            page.goto("http://localhost:7770/", wait_until="domcontentloaded", timeout=45000)
            page.wait_for_timeout(1500)
            session = ctx.new_cdp_session(page)
            res = session.send("Accessibility.getFullAXTree")
            chromium = {"version": b.version, "launch_ok": True,
                        "cdp_fullaxtree": bool(res.get("nodes")),
                        "ax_nodes_homepage": len(res.get("nodes", [])),
                        "viewport": "1280x720"}
            b.close()
    except Exception as e:  # noqa: BLE001
        chromium["error"] = f"{type(e).__name__}: {e}"

    pin = {
        "experiment_id": EXP_ID,
        "python_version": sys.version.split()[0],
        "pip_freeze_sha256": sha256_file(freeze_path),
        "pip_freeze_path": str(freeze_path),
        "pip_freeze_lines": len(freeze_txt.splitlines()),
        "versions": {
            "browsergym-core": pkg("browsergym-core"),
            "browsergym": pkg("browsergym"),
            "agentlab": pkg("agentlab"),
            "playwright": pkg("playwright"),
            "flask": pkg("flask"),
        },
        "playwright_cli_version": pv.stdout.strip() or pv.stderr.strip(),
        "chromium": chromium,
        "viewport": "1280x720",
        "ax_mode": "CDP Accessibility.getFullAXTree",
        "grammar_module": "research/intel/grammar_fulltree_358885.py",
        "grammar_hash_live": grammar_hash,
        "grammar_hash_expected": "273eafbcb817e8981f843581a724594665cabdd357b318c701251929ee9c83de",
        "grammar_hash_matches_parent": grammar_hash == "273eafbcb817e8981f843581a724594665cabdd357b318c701251929ee9c83de",
        "body_regex_present": body_regex_present,
        "fotorama_expanded_present": fotorama_present,
        "container_url": "http://localhost:7770",
        "container_health": health,
        "docker_images_digests_path": "artifacts/raw/docker_images_digests.txt",
        "docker_images_digests_sha256": hashlib.sha256(docker_digests.stdout.encode()).hexdigest(),
    }
    (RAW / "environment_pin.json").write_text(json.dumps(pin, indent=1))
    print(json.dumps(pin, indent=1))


if __name__ == "__main__":
    main()
