# EXP-FRONTIER-38013774272 preregistration

- experiment_id: EXP-FRONTIER-38013774272
- lane: frontier
- claim_ids: [C-RESIDUAL-NOVELTY]
- design_contract_version: 2
- status: DESIGN COMPLETE, CERTIFICATE VERIFIED, AWAITING FREEZE (this file is the substantive preregistration; no freeze.json exists yet)

## 1. Scientific question (binding Director mandate)

On the credential-free GET-only stdlib-HTTP substrate, over a multi-host pool whose DEEP (hop >= 3) state-item sampling frame is CERTIFIED to exist before freeze (>= 2 distinct hosts/engines, >= 3 DEEP items per engine, >= 10 total), what fraction of those DEEP items is reachable in <= K = 3 fresh-agent GETs using ANY of the five frozen site-native discovery channels (robots.txt sitemap directives, sitemap.xml, on-site search/query URLs, RSS/Atom feeds, JSON-LD/structured-data enumeration) -- with a preregistered materiality threshold on >= 2 engines deciding whether shortest-path hop is NOT a fundamental acquisition-cost barrier (persistence of paths is not a core optimization target; effort moves to discovery and substrate expansion) versus fresh deep-instance acquisition remaining path-bound with a computable persistence break-even surface.

## 2. Context and inheritance (reading the exact parent handoff only)

- Parent EXP-FRONTIER-37984242167 was BLOCKED pre-measurement: it froze an empty sampling frame (0 seeds, 0 DEEP items, 0 hosts), an absent pre-freeze certificate (all_verified=false) and a 0/0 primary metric unreachable in both falsifier directions. It is a verified design/control-plane defect receipt, NOT a measurement and NOT a scientific negative (handoff carry_forward.established[0..2]; do_not_assume[0]).
- Established and carried: the credential-free GET substrate works (TCP 443 OK, Python 3.12 stdlib); parent EXP-FRONTIER-37950626378 context (persisted-path replay = hop+1 on 1532/1532 items, direct URL replay = 1 GET, BFS is item-blind) is INHERITED CONTEXT ONLY and is never paired into this experiment's primary metric (handoff carry_forward.established[4], do_not_assume[3]).
- Rejected: treating BLOCKED/NOT_APPLICABLE as FALSIFIES; post-freeze pool construction as confirmation; reading the pooled GROWING ratio as independent economics (handoff carry_forward.rejected).
- Do NOT assume: the discovery question is answered in either direction; C-RESIDUAL-NOVELTY effective state remains EXPERIMENTAL per codex/claim_state.json (registry line status HYPOTHESIS is not the effective epistemic state; the freezer only checks claim-id membership).

## 3. Claim mapping

C-RESIDUAL-NOVELTY (Director mandate allocation REOPEN, frontier priority claim). Effective state EXPERIMENTAL (codex/claim_state.json#effective_event_by_claim, effective event EXP-PRODUCT-37989728440; registry.json line status HYPOTHESIS is a local snapshot field and is not authoritative per SPIDER_MASTER_PROMPT.md). This experiment measures a constituent mechanism of residual-novelty economics: whether depth itself is a material acquisition barrier on a certified multi-engine DEEP frame given site-native discovery channels.

## 4. Frozen design decisions (all resolved before freeze; none left open)

D1 Engine frame: exactly 4 host engines, 10 admitted DEEP items each, 40 total: vitepress.dev (VitePress, page-level content sitemap), nix.dev (mdBook, sitemap excludes /manual/ subtree, static search index present), doc.rust-lang.org (mdBook, seed /book/, version-level sitemap.txt only + book-scoped search index), rust-lang.github.io (mdBook, seed /async-book/, no robots/sitemap, async-book-scoped search index).
D2 Synthetic identifier format for the null control: 'spider-nonexistent-item-38013774272' and 'spider-fake-deep-item-38013774272' per host (8 probes total).
D3 Search query-parameter mapping (ON_SITE_SEARCH form branch): use the item's last canonical path segment, decoded, extensions stripped, hyphens to spaces, as the query value; only forms with an EXPLICIT action attribute are invoked; mdBook forms with default (self) action are not invoked.
D4 JSON-LD vocabulary: all <script type=application/ld+json> blocks on the seed root; URLs from url/@id/mainEntityOfPage/itemListElement; same-host http(s) only; the item page itself is never its own discovery hub (anti-tautology).
D5 sitemap handling: gzip-decoded when .gz; namespace-agnostic ElementTree; sitemapindex recursion cap 12 children; 20000-URL parse cap per host.
D6 Redirect accounting: every 3xx hop counts as 1 GET against K=3; all 40 admitted items serve direct (final == url), so the item-page GET is exactly 1.
D7 Engine definition: distinct (host, engine label) pairs; per-engine fractions are reported per host; cross-engine items are never merged for the E count.
D8 Canonical match key: final URL after redirects; strip fragment, query, trailing slash, terminal .html/.htm; applied identically to items and channel outputs.
D9 K=3 budget: discovery GET(s) + item-page GET <= 3 per item per channel; each channel probed in its own fresh episode.
D10 Baseline rules: B_LINK_FOLLOWING_BFS re-run at EXECUTE with the frozen item-blind BFS (B=250, D=6); B_DIRECT_URL_REPLAY = 1; B_PERSISTED_PATH_REACQUISITION_CONTEXT is context-only, never a comparator.
D11 Outcome mapping: E = count of available engines with per-engine fraction >= 0.50; SUPPORTS iff E>=2; MIXED iff E==1; FALSIFIES iff E==0; MEASUREMENT_INVALID on control failure, with the failing control named.

## 5. Hypothesis and falsifier (two-sided, both branches arithmetically satisfiable)

- H1 DISCOVERY_COLLAPSES_DEPTH: on >=2 distinct host engines, >=0.50 of admitted DEEP items reachable in <=K=3 GETs via some frozen channel -> hop is not a fundamental acquisition-cost barrier.
- H0 DEPTH_REMAINS_BARRIER: on fewer than 2 engines does the per-engine fraction reach 0.50 -> path-bound acquisition with a computable persistence break-even.
- Falsifier denominator: 40 (never 0); per-engine denominators: 10 (never 0). E ∈ {0,1,2} are all arithmetically reachable: the frozen record contains only aggregate channel scope facts (272 sitemap locs, 1933 search-index doc_urls, 0-under-manual, 3 sitemap.txt lines), never a per-item membership witness, so every per-engine fraction is an open EXECUTE measurement.
- Disclosed structural floors (calibration, cannot force outcome, disclosed as aggregate instrument facts): doc.rust-lang.org expected 0/10 (sitemap.txt has exactly 3 version roots, none cargo; /sitemap.xml 404; book search index has 0 cargo-prefix entries -> ON_SITE_SEARCH cannot reach the cargo frame); rust-lang.github.io structural max 3/10 = 0.30 < 0.50 (async-book search index covers 3 of 10 frame items; rfcs/wg-async items have zero entries). These two floors make E decided by the two live engines and keep the >=2 boundary genuinely at risk.

## 6. Pre-freeze control certificate (summary; full record inline in spec.json#pre_freeze_control_certificate, hash-bound via freeze.json.hashes['spec.json'])

- Verified 2026-10-10, re-verified in one consolidated run at 2026-10-10T18:14:47Z (probe outputs hashed: final_cert.json e3a0aaf1..., frame_hop_audit.json 0471fdd2..., certified_bfs2.json 59d6c164..., final_channels.json b69a2e4e..., final_scope.json 8d14bd34...).
- Frame gate: 40/40 admitted URLs final-2xx direct with named_controls >= 1; all 40 at certified hop exactly 3 (browser-correct BFS hop maps, engine-native form matching; below_3 = []); 4/4 seed roots 200.
- Positive control PC_DISCOVERY_CHANNEL_LIVENESS: aggregate channel liveness verified (vitepress.dev sitemap.xml 200/272 locs; nix.dev sitemap.xml 200/58 locs with 0 under /manual/ AND searchindex.js 200/1933 doc_urls; doc.rust-lang.org robots 200 -> sitemap.txt 200/3 lines; rust-lang.github.io 404 on every channel). AGGREGATE ONLY - no per-item witness computed at DESIGN.
- Null control NC_SYNTHETIC_UNREACHABLE_ITEM: 8/8 synthetic pages 404; 0 synthetic ids in parsed URL sets.
- Substrate: stdlib urllib GET only, TLS, UA 'SPIDER-research-frontier-38013774272/1.0', timeout 12s, body cap 600000 B (12 MB cap for searchindex/sitemap artifacts), no credentials/cookies/browser/write verbs.

## 7. Measurement protocol (EXECUTE, frozen)

1. Re-run the frozen item-blind BFS once per seed (B=250, D=6, same-host static-<a>, document order) to record hop_depth and bfs_requests_to_first_reach per admitted item (baseline B_LINK_FOLLOWING_BFS).
2. Per engine, per admitted item, probe each of the five channels in its own fresh K=3 episode: ROBOTS_SITEMAP, SITEMAP_XML, ON_SITE_SEARCH (form branch then static-index branch), RSS_ATOM, JSON_LD, per frozen channel definitions; a channel succeeds iff the item's canonical match key appears in the channel output AND the item page fetches final-2xx within remaining budget.
3. Record per-item per-channel success, per-engine fraction, aggregate fraction, E, and per-channel diagnostics.
4. Re-run null control (8 synthetic probes) and positive control (channel liveness) at EXECUTE on the frozen URLs.
5. Item URLs that no longer resolve are excluded with reason (never counted as discovery-failure); an unreachable host marks that engine unavailable (excluded from E with reason); control failures mark the outcome MEASUREMENT_INVALID with the failing control named.

## 8. Metrics (stable identifiers for EXECUTE/AUDIT)

- discovery_reachable_fraction_per_engine[host] (primary per-engine; denominator 10)
- discovery_reachable_fraction (aggregate; denominator 40)
- E (decision variable)
- discovery_reachable_fraction_per_channel[channel] (diagnostic)
- per_item_reachability[item] (per channel union)
- bfs_requests_to_first_reach[item], hop_depth[item] (baseline B_LINK_FOLLOWING_BFS)
- direct_url_replay_requests[item] == 1 (baseline B_DIRECT_URL_REPLAY)
- controls: PC_DISCOVERY_CHANNEL_LIVENESS, NC_SYNTHETIC_UNREACHABLE_ITEM (each with pass/fail)

## 9. Outcome mapping and consequences

- SUPPORTS (E>=2): hop is NOT a fundamental acquisition-cost barrier where site-native discovery channels exist; persistence of paths is not the primary optimization target; effort moves to discovery-channel coverage, engine/index-artifact detection, hybrid discovery+traversal, substrate expansion. C-RESIDUAL-NOVELTY moves toward VALIDATED for the discovery-mechanism constituent.
- MIXED (E==1): evidence is engine-dependent; weak support only; persistence retains value on index-less engines; recommend a follow-up mapping index artifacts across a wider engine sample before architecture decisions.
- FALSIFIES (E==0): fresh deep-instance acquisition remains path-bound with a computable persistence break-even surface (re-validation GETs/bytes + stale-replay false-accept vs re-derivation, scaling with hop/elapsed); persistence architecture is validated as a core optimization lever; feeds the recorded maintenance/invalidation alternative question.
- MEASUREMENT_INVALID: on control failure or infrastructure failure; no claim update, smallest unblocking action recorded.

## 10. Validity threats (disclosed, not hidden)

- VN-V9 bimodality: per-engine discovery is close to a deterministic function of whether a machine-readable content index covers the frame subtree. Two engines are live (vitepress sitemap, nix.dev search index), two are disclosed structural floors. E ∈ {0,1,2}; the boundary is concentrated on the static search-index mechanism on nix.dev. Reduced power for intermediate fractions is the central trade-off, disclosed.
- VN-V2 static-parser-only: JS-executed search is not followed (representation loss disclosed).
- VN-V8 selection bias: purposive documentation-engine sample; no generalization beyond these engines.
- VN-V11 temporal drift: live hosts can change between DESIGN and EXECUTE; drift recorded, not silently re-sampled.
- Admitted items are all at hop 3 (the shallow member of DEEP {3,4,5,6}); hop-4 pages exist in every crawl but are not admitted by the first-10 rule. Disclosed.
- No per-item channel membership was computed during DESIGN; every per-engine fraction is measured only at EXECUTE (anti-foreclosure).
