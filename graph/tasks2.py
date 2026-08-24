"""SPIDER TEAM GRAPH — cycle-32670239235 corpus.

DESIGN FROZEN BEFORE OUTCOME OBSERVATION (preregistration discipline):

Production tasks (executed cold by producer agentG) share NO complete route
with any target composite. Target composites reuse only independently
acquired parts (category navigation pattern, pagination, product opening,
login form, hub navigation). Subgoal `sig` strings are provenance/debug
labels ONLY — the blind consumer never looks fragments up by them.

Hand-authored elements that remain (disclosed in report):
  - acceptance predicates define what "task success" means (evaluation only);
  - per-subgoal keywords stand in for natural-language task descriptions;
  - generic browsing priors (hints: pager/check_first_input/input_press)
    are agent heuristics available equally in ALL conditions including cold,
    never a memory lookup.

Sites probed 2026-08-22/23 UTC: books.toscrape.com categories with real
page-2 pagination include Fiction, Fantasy, Mystery, Romance, ...;
Travel/History/Science have NO page-2. quotes.toscrape.com/tag/love/ has a
working Next control to /tag/love/page/2/. the-internet.herokuapp.com
key_presses shows "You entered: X"; status_codes exposes 200..500 links;
checkboxes renders box1 unchecked / box2 checked at load.
"""
from graph.explorer import elem_has
from urllib.parse import urlsplit

BOOKS = "https://books.toscrape.com/"
QUOTES = "https://quotes.toscrape.com/"
INTERNET = "https://the-internet.herokuapp.com/"

SITES = {"books": BOOKS, "quotes": QUOTES, "internet": INTERNET}


def url_contains(s, frag): return frag.lower() in s["url"].lower()
def elem_text(s, frag): return elem_has(s, frag)


# ---- structural URL predicates (cycle run2c evaluator correction) ----
# run2/run2b lesson: raw substring tests matched unintended pages
# ('science-fiction' satisfied 'fiction'; the GLOBAL /catalogue/page-2.html
# satisfied 'page-2'). Predicates below anchor on URL path structure.
def _path(s):
    return urlsplit(s["url"]).path


def is_books_category(s, slug_prefix):
    p = _path(s)
    parts = [x for x in p.split("/") if x]
    return (len(parts) >= 4 and parts[0] == "catalogue"
            and parts[1] == "category" and parts[2] == "books"
            and parts[3].startswith(slug_prefix))


def is_books_product(s):
    p = _path(s)
    parts = [x for x in p.split("/") if x]
    return (len(parts) >= 2 and parts[0] == "catalogue"
            and parts[1] != "category"
            and not parts[-1].startswith("page-"))


def books_category_paged(s, slug_prefix, n=2):
    p = _path(s)
    parts = [x for x in p.split("/") if x]
    return (is_books_category(s, slug_prefix)
            and any(x.startswith(f"page-{n}") for x in parts))


def _first_checkbox_checked(s):
    ins = s.get("inputs") or []
    return bool(ins) and bool(ins[0].get("c"))


def sg(sig, kws, url_frag=None, el_text=None, neg_url=None, fills=None,
       hint=None, requires_action=True, wait_text=None, wait_s=0,
       accept_fn=None, press_value=None):
    def accept(s):
        if accept_fn is not None:
            return accept_fn(s)
        if url_frag and not url_contains(s, url_frag): return False
        if el_text and not elem_text(s, el_text): return False
        if neg_url and url_contains(s, neg_url): return False
        return True
    return {"sig": sig, "keywords": kws, "accept": accept,
            "fills": fills or [], "hint": hint,
            "requires_action": requires_action,
            "wait_text": wait_text, "wait_s": wait_s,
            "press_value": press_value}


Q_LOGIN_FILLS = [{"hint_user": True, "value": "spiderbot"},
                 {"hint_pass": True, "value": "notasecret"}]
I_LOGIN_FILLS = [{"hint_user": True, "value": "tomsmith"},
                 {"hint_pass": True, "value": "SuperSecretPassword!"}]

# ------------------------- PRODUCTION TASKS -------------------------
PRODUCTION_TASKS = {
 "B_travel_first_book": {"site": "books", "start": BOOKS, "subgoals": [
    sg("books.cat.travel", ["travel"],
       accept_fn=lambda s: is_books_category(s, "travel")),
    sg("books.open.product", ["catalogue", "product"],
       accept_fn=is_books_product)]},
 "B_fiction_paged": {"site": "books", "start": BOOKS, "subgoals": [
    # neg_url guard: 'fiction' would also match historical-fiction_4/
    sg("books.cat.fiction", ["fiction"],
       accept_fn=lambda s: is_books_category(s, "fiction_")),
    sg("books.paginate.next", ["next", "page"], hint="pager",
       accept_fn=lambda s: books_category_paged(s, "fiction_", 2))]},
 "B_romance_first_book": {"site": "books", "start": BOOKS, "subgoals": [
    sg("books.cat.romance", ["romance"],
       accept_fn=lambda s: is_books_category(s, "romance")),
    sg("books.open.product.romance", ["catalogue", "product"],
       accept_fn=is_books_product)]},
 "Q_login": {"site": "quotes", "start": QUOTES, "subgoals": [
    sg("quotes.login", ["login"], el_text="logout", fills=Q_LOGIN_FILLS)]},
 "I_login": {"site": "internet", "start": INTERNET, "subgoals": [
    sg("int.login", ["login"], el_text="you logged into a secure area",
       fills=I_LOGIN_FILLS)]},
 "I_checkboxes_check_first": {"site": "internet", "start": INTERNET,
    "subgoals": [
    sg("int.checkbox.nav", ["checkboxes"], url_frag="checkboxes"),
    sg("int.checkbox.first", ["checkbox", "toggle"],
       accept_fn=_first_checkbox_checked, hint="check_first_input")]},
 "I_dynamic_loading_ex1": {"site": "internet", "start": INTERNET,
    "subgoals": [
    sg("int.dyn.nav", ["dynamic", "loading"], url_frag="dynamic_loading"),
    sg("int.dyn.ex1", ["example"], url_frag="dynamic_loading/1"),
    sg("int.dyn.start.ex1", ["start"], el_text="hello world",
       wait_text="Hello World!", wait_s=14)]},
 "I_key_presses_a": {"site": "internet", "start": INTERNET, "subgoals": [
    sg("int.keypress.nav", ["key", "presses"], url_frag="key_presses"),
    sg("int.keypress.a", ["press", "key"], el_text="you entered: a",
       hint="input_press", press_value="A")]},
 "I_status_200": {"site": "internet", "start": INTERNET, "subgoals": [
    sg("int.status.nav", ["status", "codes"], url_frag="status_codes"),
    sg("int.status.200", ["status", "200"],
       el_text="200 status code")]},
 "Q_tag_love_nav": {"site": "quotes", "start": QUOTES, "subgoals": [
    sg("quotes.tag.love", ["love", "tag"], url_frag="/tag/love")]},
}

# --------------------- HELD-OUT COMPOSITE TARGETS ---------------------
# Full routes below were never executed during production; each recombines
# independently learned parts plus glue.
TARGET_TASKS = {
 "C_books_fantasy_paged_product": {"site": "books", "start": BOOKS,
    "composite": True, "subgoals": [
    sg("tgt.books.cat.fantasy", ["fantasy"],
       accept_fn=lambda s: is_books_category(s, "fantasy")),
    sg("tgt.books.paginate.fantasy", ["next", "page"], hint="pager",
       accept_fn=lambda s: books_category_paged(s, "fantasy_", 2)),
    sg("tgt.books.open.product.p2", ["catalogue", "product"],
       accept_fn=lambda s: (is_books_product(s)
                            and books_category_paged(s, "fantasy_", 2)))]},
 "C_internet_login_checkboxes": {"site": "internet", "start": INTERNET,
    "composite": True, "subgoals": [
    sg("tgt.int.login", ["login"],
       el_text="you logged into a secure area", fills=I_LOGIN_FILLS),
    sg("tgt.int.checkbox.nav", ["checkboxes"], url_frag="checkboxes"),
    sg("tgt.int.checkbox.first", ["checkbox", "toggle"],
       accept_fn=_first_checkbox_checked, hint="check_first_input")]},
 "C_quotes_login_love_p2": {"site": "quotes", "start": QUOTES,
    "composite": True, "subgoals": [
    sg("tgt.quotes.login", ["login"], el_text="logout",
       fills=Q_LOGIN_FILLS),
    sg("tgt.quotes.tag.love", ["love", "tag"], url_frag="/tag/love"),
    sg("tgt.quotes.tag.love.p2", ["next", "page"], hint="pager",
       accept_fn=lambda s: (
           _path(s).startswith("/tag/love/")
           and "page/2" in _path(s)))]},
 "C_internet_login_dyn_ex2": {"site": "internet", "start": INTERNET,
    "composite": True, "subgoals": [
    sg("tgt.int.login.dyn", ["login"],
       el_text="you logged into a secure area", fills=I_LOGIN_FILLS),
    sg("tgt.int.dyn.nav", ["dynamic", "loading"], url_frag="dynamic_loading"),
    sg("tgt.int.dyn.ex2", ["example"], url_frag="dynamic_loading/2"),
    sg("tgt.int.dyn.start.ex2", ["start"], el_text="hello world",
       wait_text="Hello World!", wait_s=14)]},
 "C_internet_login_status_500": {"site": "internet", "start": INTERNET,
    "composite": True, "subgoals": [
    sg("tgt.int.login.st", ["login"],
       el_text="you logged into a secure area", fills=I_LOGIN_FILLS),
    sg("tgt.int.status.nav", ["status", "codes"], url_frag="status_codes"),
    # deliberately UNTRAINED final step: production only ever clicked 200.
    # The stored fragment should NOT silently satisfy this subgoal; novelty
    # must localize to choosing 500.
    sg("tgt.int.status.500", ["status", "500"],
       el_text="500 status code")]},
}
