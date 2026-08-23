"""SPIDER TEAM GRAPH — task corpus for inheritance experiments.

Each TASK = ordered SUBGOALS. A subgoal has:
  - a structural goal_sig (addressable key for fragments),
  - an acceptance predicate over the raw snapshot,
  - lightweight keyword hints (what any goal-conditioned agent has),
  - optional typed form-fill values.
Fragments are learned per-subgoal, enabling fragment-reuse and
cross-task composition tests (G4/G5).
"""

def _has(pred_list):
    return pred_list

# ---- acceptance predicates operate on snapshot dicts ----
def url_contains(s, frag): return frag.lower() in s["url"].lower()
def title_contains(s, frag): return frag.lower() in (s["title"] or "").lower()
def elem_text(s, frag):
    hay = [(e["text"] or "").lower() for e in s["elements"]]
    hay.append((s.get("page_text") or "").lower())
    return any(frag.lower() in h for h in hay)
def url_not_contains(s, frag): return frag.lower() not in s["url"].lower()

BOOKS = "https://books.toscrape.com/"
QUOTES = "https://quotes.toscrape.com/"
INTERNET = "https://the-internet.herokuapp.com/"
WIKI = "https://en.wikipedia.org/"

def sg(sig, kws, url_frag=None, title_frag=None, el_text=None, neg_url=None,
       fills=None, hint=None, requires_action=True, wait_text=None, wait_s=0):
    """Subgoal constructor."""
    def accept(s):
        if url_frag and not url_contains(s, url_frag): return False
        if title_frag and not title_contains(s, title_frag): return False
        if el_text and not elem_text(s, el_text): return False
        if neg_url and url_contains(s, neg_url): return False
        return True
    return {"sig": sig, "keywords": kws, "accept": accept,
            "fills": fills or [], "hint": hint, "requires_action": requires_action,
            "wait_text": wait_text, "wait_s": wait_s}

TASKS = {
 # ---------------- books.toscrape ----------------
 "B_travel_first_book": {
    "site": "books", "start": BOOKS, "type": "action",
    "subgoals": [
        sg("books.cat.travel", ["travel"], url_frag="travel"),
        sg("books.open.first.book", [], url_frag="/catalogue/",
           neg_url="category", hint="first_product_link"),
    ]},
 "B_fiction_paged": {   # seeds pagination + fiction fragments
    "site": "books", "start": BOOKS, "type": "action",
    "subgoals": [
        sg("books.cat.fiction", ["fiction"], url_frag="fiction"),
        sg("books.paginate.next", ["next"], url_frag="page-2",
           hint="pager"),
    ]},
 "B_COMPOSITE_fiction_p2_first": {  # never seen end-to-end; parts learned above
    "site": "books", "start": BOOKS, "type": "action", "composite": True,
    "subgoals": [
        sg("books.cat.fiction", ["fiction"], url_frag="fiction"),
        sg("books.paginate.next", ["next"], url_frag="page-2"),
        sg("books.open.first.book", [], url_frag="/catalogue/",
           neg_url="category"),
    ]},
 # ---------------- quotes.toscrape ----------------
 "Q_login": {
    "site": "quotes", "start": QUOTES, "type": "action",
    "subgoals": [
        sg("quotes.login", ["login"], el_text="logout",
           fills=[{"hint_user": True, "value": "spiderbot"},
                  {"hint_pass": True, "value": "notasecret"}]),
    ]},
 "Q_logout": {
    "site": "quotes", "start": QUOTES, "type": "action",
    "subgoals": [
        sg("quotes.logout", ["logout"], url_frag="quotes.toscrape",
           neg_url="logout"),
    ]},
 "Q_COMPOSITE_login_page5_extract": {
    "site": "quotes", "start": QUOTES, "type": "info", "composite": True,
    "subgoals": [
        sg("quotes.login", ["login"], el_text="logout",
           fills=[{"hint_user": True, "value": "spiderbot"},
                  {"hint_pass": True, "value": "notasecret"}]),
        sg("quotes.page.5", ["next"], url_frag="page/5", hint="pager"),
        sg("quotes.extract.first", [], requires_action=False),
    ]},
 # ---------------- the-internet ----------------
 "I_login": {
    "site": "internet", "start": INTERNET, "type": "action",
    "subgoals": [
        sg("int.login", ["form authentication"], el_text="you logged into a secure area",
           fills=[{"hint_user": True, "value": "tomsmith"},
                  {"hint_pass": True, "value": "SuperSecretPassword!"}]),
    ]},
 "I_dynamic_loading": {
    "site": "internet", "start": INTERNET, "type": "action",
    "subgoals": [
        sg("int.dyn.nav", ["dynamic loading"], url_frag="dynamic_loading"),
        sg("int.dyn.ex2", ["example 2"], url_frag="dynamic_loading/2"),
        sg("int.dyn.start", ["start"], el_text="hello world",
           hint="button_start", wait_text="Hello World!", wait_s=14),
    ]},
 "I_checkboxes": {
    "site": "internet", "start": INTERNET, "type": "action",
    "subgoals": [
        sg("int.checkbox.nav", ["checkboxes"], url_frag="checkboxes"),
        sg("int.checkbox.first", [], el_text="checkbox", hint="check_first_input"),
    ]},
 "I_COMPOSITE_login_then_dyn": {
    "site": "internet", "start": INTERNET, "type": "action", "composite": True,
    "subgoals": [
        sg("int.login", ["form authentication"],
           fills=[{"hint_user": True, "value": "tomsmith"},
                  {"hint_pass": True, "value": "SuperSecretPassword!"}],
           el_text="you logged into a secure area"),
        sg("int.dyn.nav", ["dynamic loading"], url_frag="dynamic_loading"),
        sg("int.dyn.ex2", ["example 2"], url_frag="dynamic_loading/2"),
        sg("int.dyn.start", ["start"], el_text="hello world",
           hint="button_start", wait_text="Hello World!", wait_s=14),
    ]},
 # ---------------- wikipedia (info/navigation) ----------------
 "W_spider_to_silk": {
    "site": "wikipedia", "start": WIKI + "wiki/Spider", "type": "info",
    "subgoals": [sg("wiki.link.silk", ["silk"], url_frag="/wiki/Silk")]},
 "W_coffee_to_caffeine": {
    "site": "wikipedia", "start": WIKI + "wiki/Coffee", "type": "info",
    "subgoals": [sg("wiki.link.caffeine", ["caffeine"], url_frag="/wiki/Caffeine")]},
}

AGENT_SEQUENCE_COLD_FIRST = [
    # agent G explores cold, building the store
    ("agentG", "B_travel_first_book", "cold"),
    ("agentG", "B_fiction_paged", "cold"),
    ("agentG", "Q_login", "cold"),
    ("agentG", "I_login", "cold"),
    ("agentG", "I_dynamic_loading", "cold"),
    ("agentG", "W_spider_to_silk", "cold"),
]
AGENT_SEQUENCE_INHERIT = [
    # different policy consumes G's knowledge (model/policy transfer proxy, G10)
    ("agentB", "Q_COMPOSITE_login_page5_extract", "inherit"),
    ("agentB", "B_COMPOSITE_fiction_p2_first", "inherit"),
    ("agentB", "I_COMPOSITE_login_then_dyn", "inherit"),
    ("agentB", "W_coffee_to_caffeine", "inherit-cold"),   # genuinely new
    # full-route replay of exactly-seen tasks
    ("agentG", "Q_login", "replay"),
    ("agentG", "I_login", "replay"),
    ("agentG", "B_travel_first_book", "replay"),
    # second-generation inheritance: B's composites feed back into store
    ("agentB", "Q_COMPOSITE_login_page5_extract", "replay"),
]
