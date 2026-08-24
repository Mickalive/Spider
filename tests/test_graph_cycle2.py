"""Cycle 32670239235 Graph integrity tests."""
import os, tempfile, unittest

from graph.store import Store
from graph.explorer import _slug_tokens, NO_EFFECT_EXEMPT
from graph.addressing import address_fragments


def _mk_snap(elements=(), inputs=None):
    return {"site": "test", "url": "https://x.test/a", "title": "t",
            "url_shape": "x.test/*", "elements": list(elements),
            "forms": [], "inputs": inputs or [], "n_links": 0,
            "page_text": "", "dom_sha256": "0", "dom_bytes": 0}


def _el(i, tag="a", typ="", role="", name="", cls="", text=""):
    return {"i": i, "tag": tag, "type": typ, "role": role, "name": name,
            "aria": "", "ph": "", "text": text, "href": "/x", "ext": 0,
            "cls": cls, "xp": f"{tag}", "x": 0, "y": 0, "enabled": True}


class DynamicVariableSeparationTests(unittest.TestCase):
    def test_input_values_and_checked_do_not_change_fingerprint(self):
        s = Store(":memory:")
        a = _mk_snap(elements=[_el(0)], inputs=[
            {"n": "q", "t": "text", "v": "hello", "c": False}])
        b = _mk_snap(elements=[_el(0)], inputs=[
            {"n": "q", "t": "text", "v": "world!!", "c": True}])
        self.assertEqual(s.fingerprint(a), s.fingerprint(b))

    def test_structural_change_does_change_fingerprint(self):
        s = Store(":memory:")
        a = _mk_snap(elements=[_el(0)], inputs=[{"n": "q", "t": "text",
                                                 "v": "hello", "c": False}])
        b = _mk_snap(elements=[_el(0), _el(1)],
                     inputs=a["inputs"])
        self.assertNotEqual(s.fingerprint(a), s.fingerprint(b))

    def test_press_is_exempt_from_no_effect_rule(self):
        self.assertIn("press", NO_EFFECT_EXEMPT)


class AddressingTests(unittest.TestCase):
    def _store_with(self, frags):
        s = Store(":memory:")
        for goal_sig, meta, steps in frags:
            s.save_fragment(goal_sig, steps, "books", meta=meta)
        return s

    def test_content_match_without_goal_sig_lookup(self):
        meta = {"entry_url_shape": "books.toscrape.com/*",
                "kws_producer": ["fiction"],
                "steps_ctx": [{"kind": "click", "text_tokens": ["next"],
                               "href_tokens": []}]}
        s = self._store_with([("some.prov.label", meta,
                               [{"kind": "click", "target_sig": "a|b"}])])
        res = address_fragments(s, ["next", "page"], site="books")
        self.assertFalse(res["unknown"])
        self.assertEqual(res["candidates"][0]["content_hits"], 1)
        # provenance-only match must NOT pass the content gate
        res2 = address_fragments(s, ["fiction"], site="books")
        self.assertTrue(res2["unknown"])

    def test_unknown_stays_unknown(self):
        meta = {"entry_url_shape": "x.test/*", "kws_producer": [],
                "steps_ctx": [{"kind": "click", "text_tokens": ["next"],
                               "href_tokens": []}]}
        s = self._store_with([("g", meta, [{"kind": "click",
                                             "target_sig": "a|b"}])])
        res = address_fragments(s, ["completely", "unrelated"], site="books")
        self.assertTrue(res["unknown"])
        self.assertEqual(res["candidates"], [])

    def test_boilerplate_token_alone_does_not_retrieve(self):
        # IDF regression: 'catalogue' appears in nearly every books-site
        # fragment context; a query containing it plus an unseen token must
        # not confidently retrieve a cross-purpose fragment.
        frags = []
        for name in ("travel", "mystery", "romance"):
            frags.append((f"cat.{name}",
                          {"entry_url_shape": "books.toscrape.com/*",
                           "kws_producer": [name],
                           "steps_ctx": [{"kind": "click",
                                          "text_tokens": [name],
                                          "href_tokens": ["/catalogue/category/books"]}]},
                          [{"kind": "click", "target_sig": "a|b"}]))
        s = self._store_with(frags)
        res = address_fragments(s, ["catalogue", "product"], site="books")
        self.assertTrue(res["unknown"],
                        f"boilerplate match passed gates: {res['candidates']}")

    def test_specific_token_beats_boilerplate(self):
        frags = [
            ("cat.travel",
             {"entry_url_shape": "books.toscrape.com/*",
              "kws_producer": ["travel"],
              "steps_ctx": [{"kind": "click", "text_tokens": ["travel"],
                             "href_tokens": ["/catalogue/category/books/travel"]}]},
             [{"kind": "click", "target_sig": "a|b"}]),
            ("pager",
             {"entry_url_shape": "books.toscrape.com/*",
              "kws_producer": ["next", "page"],
              "steps_ctx": [{"kind": "click", "text_tokens": ["next"],
                             "href_tokens": []}]},
             [{"kind": "click", "target_sig": "a|b"}]),
        ]
        s = self._store_with(frags)
        res = address_fragments(s, ["travel"], site="books")
        self.assertFalse(res["unknown"])
        self.assertEqual(res["candidates"][0]["goal_sig"], "cat.travel")

    def test_site_mismatch_excluded(self):
        meta = {"entry_url_shape": "x/*", "kws_producer": [],
                "steps_ctx": [{"kind": "click", "text_tokens": ["login"],
                               "href_tokens": []}]}
        s = self._store_with([("g", meta, [{"kind": "click",
                                             "target_sig": "a|b"}])])
        res = address_fragments(s, ["login"], site="other")
        self.assertTrue(res["unknown"])

    def test_slug_tokens_drops_short_tokens(self):
        toks = _slug_tokens("A 200 next page-2")
        self.assertIn("200", toks)
        self.assertIn("next", toks)
        self.assertNotIn("a", toks)


class ReadGateTests(unittest.TestCase):
    def test_cold_store_returns_no_memory(self):
        s = Store(":memory:", allow_reads=False)
        s.save_fragment("g", [{"kind": "click", "target_sig": "a"}], "s")
        s.save_trajectory("t", "s", ["tok"],
                          [{"kind": "click", "target_sig": "a"}])
        self.assertIsNone(s.best_fragment("g"))
        self.assertEqual(s.iter_fragments(), [])
        self.assertEqual(s.iter_trajectories(), [])
        self.assertIsNone(s.state_id_by_fingerprint("x"))

    def test_fragment_counters_invariants_hold(self):
        with tempfile.TemporaryDirectory() as td:
            s = Store(os.path.join(td, "s.db"))
            fid = s.save_fragment("g", [{"kind": "click",
                                         "target_sig": "a"}], "s")
            s.save_fragment("g", [{"kind": "click", "target_sig": "a"}], "s")
            row = s.db.execute(
                "SELECT success_count,failure_count,created,last_validated"
                " FROM fragments WHERE id=?", (fid,)).fetchone()
            self.assertEqual(row[0], 2)
            self.assertGreaterEqual(row[3], row[2])


if __name__ == "__main__":
    unittest.main()
