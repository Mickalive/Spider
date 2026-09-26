"""Arm package for EXP-FRONTIER-36249071934.

Arms (prereg.md section 15):
    deopt_ratchet     -> Arm A, B-NO-MEMORY-DETERMINISTIC
    inherited_spider  -> Arm B, B-INHERITED-SPIDER
    cold_exploration  -> Arm C, B-COLD-EXPLORATION
"""

from __future__ import annotations

__all__ = ["common", "deopt_ratchet", "inherited_spider", "cold_exploration"]
