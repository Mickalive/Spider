#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(message)


def main() -> None:
    guard = read("scripts/main_safety_anchor.sh")
    workflow = read(".github/workflows/main-safety-anchor.yml")
    codex = read(".github/workflows/codex-sync.yml")
    product = read(".github/workflows/product-promote.yml")

    require("safety/main-lkg" in guard, "main safety guard lost canonical rescue branch")
    require("merge-base --is-ancestor" in guard, "main safety guard lost ancestry checks")
    require("MAIN HISTORY REGRESSION DETECTED" in guard, "main safety guard must fail closed on regression")
    require("MAIN HISTORY DIVERGENCE DETECTED" in guard, "main safety guard must fail closed on divergence")
    require("spider-main-daily-" in guard, "main safety guard lost daily immutable recovery tag")

    forbidden = (
        "git push --force",
        "git push -f",
        ":refs/heads/main",
        "update-ref refs/heads/main",
        "branch -D main",
    )
    for token in forbidden:
        require(token not in guard, f"main safety guard contains destructive main operation: {token}")

    require("group: spider-main-writer" in workflow, "main safety workflow must serialize with main writers")
    require("contents: write" in workflow, "main safety workflow needs rescue-ref write permission")
    require("bash scripts/main_safety_anchor.sh" in workflow, "main safety workflow must call canonical guard")
    require("13,28,43,58" in workflow, "main safety workflow lost periodic backstop")

    for name, writer in (("Codex", codex), ("Product", product)):
        require("bash scripts/main_safety_anchor.sh || echo \"::warning::" in writer, f"{name} main writer must invoke safety anchor best-effort")

    print("SPIDER_MAIN_SAFETY_VALIDATE_OK")


if __name__ == "__main__":
    main()
