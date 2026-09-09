#!/usr/bin/env python3
"""
Title Variance Pre-Survey: Test candidate sites for title variance.
Must verify at least 3 distinct document.title values per site.
"""

import json
import time
from playwright.sync_api import sync_playwright

# Candidate sites to test
CANDIDATE_SITES = [
    {
        "name": "GitHub",
        "entry_url": "https://github.com",
        "routes": [
            "https://github.com",
            "https://github.com/features",
            "https://github.com/pricing",
            "https://github.com/login",
            "https://github.com/about",
            "https://github.com/marketplace",
        ],
    },
    {
        "name": "MDN Web Docs",
        "entry_url": "https://developer.mozilla.org",
        "routes": [
            "https://developer.mozilla.org/en-US/",
            "https://developer.mozilla.org/en-US/docs/Web/JavaScript",
            "https://developer.mozilla.org/en-US/docs/Web/HTML",
            "https://developer.mozilla.org/en-US/docs/Web/CSS",
            "https://developer.mozilla.org/en-US/docs/Web/API/Document",
        ],
    },
    {
        "name": "TodoMVC React",
        "entry_url": "https://todomvc.com/examples/react/dist/",
        "routes": [
            "https://todomvc.com/examples/react/dist/",
            "https://todomvc.com/examples/react/dist/#/active",
            "https://todomvc.com/examples/react/dist/#/completed",
        ],
    },
    {
        "name": "StackBlitz",
        "entry_url": "https://stackblitz.com",
        "routes": [
            "https://stackblitz.com",
            "https://stackblitz.com/edit/react",
            "https://stackblitz.com/fork/react",
        ],
    },
    {
        "name": "CodeSandbox",
        "entry_url": "https://codesandbox.io",
        "routes": [
            "https://codesandbox.io",
            "https://codesandbox.io/p/react",
            "https://codesandbox.io/p/vue",
        ],
    },
]

def survey_site(page, site):
    """Survey a site for title variance across routes."""
    titles = []
    urls = []
    errors = []
    
    for route in site["routes"]:
        try:
            page.goto(route, timeout=15000, wait_until="domcontentloaded")
            time.sleep(1)
            title = page.title()[:100]
            url = page.url
            titles.append(title)
            urls.append(url)
        except Exception as e:
            errors.append(f"{route}: {str(e)[:50]}")
    
    unique_titles = len(set(titles))
    total_routes = len(titles)
    
    return {
        "name": site["name"],
        "entry_url": site["entry_url"],
        "total_routes": total_routes,
        "unique_titles": unique_titles,
        "title_variance": unique_titles / total_routes if total_routes > 0 else 0,
        "titles": titles,
        "urls": urls,
        "errors": errors,
        "passes": unique_titles >= 3,
    }

def main():
    print("=" * 70)
    print("TITLE VARIANCE PRE-SURVEY")
    print("=" * 70)
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(
            viewport={"width": 1280, "height": 720},
            user_agent="Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        )
        page = context.new_page()
        
        results = []
        for site in CANDIDATE_SITES:
            print(f"\n{'-' * 50}")
            print(f"Testing: {site['name']}")
            print(f"Entry: {site['entry_url']}")
            
            result = survey_site(page, site)
            results.append(result)
            
            print(f"  Routes tested: {result['total_routes']}")
            print(f"  Unique titles: {result['unique_titles']}")
            print(f"  Title variance: {result['title_variance']:.2f}")
            print(f"  Passes (>=3 unique titles): {result['passes']}")
            
            if result['errors']:
                print(f"  Errors: {result['errors']}")
            
            print(f"  Titles found:")
            for i, (title, url) in enumerate(zip(result['titles'], result['urls'])):
                print(f"    {i+1}. {title} -> {url}")
        
        browser.close()
    
    # Summary
    print(f"\n{'=' * 70}")
    print("SUMMARY")
    print(f"{'=' * 70}")
    
    passing_sites = [r for r in results if r['passes']]
    print(f"Sites with title variance >= 3: {len(passing_sites)}/{len(results)}")
    
    for r in passing_sites:
        print(f"  ✓ {r['name']}: {r['unique_titles']} unique titles")
    
    # Save results
    out_path = "research/experiments/EXP-PHYSICS-34348438464/title_survey_results.json"
    with open(out_path, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved to {out_path}")
    
    return passing_sites

if __name__ == "__main__":
    main()
