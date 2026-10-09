from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable

from .models import Mechanism


class MechanismRegistry:
    """Small durable registry used by the first product kernel.

    It is intentionally boring: JSONL on disk, deterministic reads, no hidden model calls.
    Research is free to replace the storage layer after a validated gate.
    """

    def __init__(self, path: str | Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)

    def all(self) -> list[Mechanism]:
        if not self.path.exists():
            return []
        out: list[Mechanism] = []
        for line in self.path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            out.append(Mechanism(**json.loads(line)))
        return out

    def replace(self, mechanisms: Iterable[Mechanism]) -> None:
        payload = "\n".join(json.dumps(m.as_dict(), sort_keys=True) for m in mechanisms)
        self.path.write_text(payload + ("\n" if payload else ""), encoding="utf-8")

    def upsert(self, mechanism: Mechanism) -> None:
        items = {m.mechanism_id: m for m in self.all()}
        items[mechanism.mechanism_id] = mechanism
        self.replace(items[k] for k in sorted(items))

    def invalidate(self, mechanism_id: str) -> bool:
        items = self.all()
        found = False
        for item in items:
            if item.mechanism_id == mechanism_id:
                item.invalidated = True
                found = True
        if found:
            self.replace(items)
        return found
