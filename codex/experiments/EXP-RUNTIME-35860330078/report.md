# EXP-RUNTIME-35860330078 — Execution Report

## Status: COMPLETE
## Outcome: MIXED

## Phase 1: Distributed C-FRESHNESS (B-SHARED-STORE)

- **Samples:** 1200 total, 1200 non-304
- **TN mean:** 1.000 (target >=0.85)
- **TN session_status:** 1.000 (target >=0.85)
- **Stratified r:** 0.0000 (target |r|<0.15)
- **CI upper:** 0.0566 (target <0.15)
- **TOST p_upper:** 0.0100 (target <0.05)
- **Noise FP:** 0.000 (target <=0.15)
- **Worker distribution:** {'unknown': 1200}

## Phase 2: Browser C-MEAS-VALID (Playwright 1280x720)

- **AX nodes median (on /resource):** 0 (target >10)
- **PC-HEALTH (on /resource):** 0% (target >=80%)
- **DOM nodes median (on /resource):** 0 (target 21-82)
- **Browser body AvsC full:** 0.000 (target >0.5)
- **Browser header AvsE full:** 0.000 (target >0.5)
- **Null body full:** 0.000 (target <=0.05)
- **Null header full:** 0.000 (target <=0.05)

## Validity Notes

- Phase 2 browser C-MEAS-VALID failed: BrowserType.launch: Executable doesn't exist at /home/runner/.cache/ms-playwright/chromium-1117/chrome-linux/chrome
╔════════════════════════════════════════════════════════════╗
║ Looks like Playwright was just installed or updated.       ║
║ Please run the following command to download new browsers: ║
║                                                            ║
║     playwright install                                     ║
║                                                            ║
║ <3 Playwright Team                                         ║
╚════════════════════════════════════════════════════════════╝

## Unresolved

- None
