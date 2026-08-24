"""SPIDER TEAM GRAPH — cumulative operational knowledge store.

Schema covers states, actions, transformations, routes/fragments,
failures, provenance, confidence. SQLite in /tmp during runs; schema
and compact results are what get committed.
"""
import gzip, hashlib, json, math, sqlite3, time

SCHEMA = """
PRAGMA journal_mode=WAL;
CREATE TABLE IF NOT EXISTS sites(name TEXT PRIMARY KEY, domain TEXT);
CREATE TABLE IF NOT EXISTS states(
  id INTEGER PRIMARY KEY,
  site TEXT, url TEXT, url_shape TEXT, fingerprint TEXT,
  raw_json BLOB,
  first_seen REAL, last_seen REAL
);
CREATE UNIQUE INDEX IF NOT EXISTS ix_states_fp ON states(site, fingerprint);
CREATE TABLE IF NOT EXISTS actions(
  id INTEGER PRIMARY KEY,
  kind TEXT, target_sig TEXT,
  UNIQUE(kind, target_sig)
);
CREATE TABLE IF NOT EXISTS transitions(
  id INTEGER PRIMARY KEY,
  from_state INT, action_id INT, to_state INT,
  outcome TEXT,
  error_class TEXT DEFAULT '',
  task_id TEXT DEFAULT '', agent_id TEXT DEFAULT '',
  ts REAL,
  FOREIGN KEY(from_state) REFERENCES states(id),
  FOREIGN KEY(action_id) REFERENCES actions(id),
  FOREIGN KEY(to_state) REFERENCES states(id)
);
CREATE TABLE IF NOT EXISTS fragments(
  id INTEGER PRIMARY KEY,
  goal_sig TEXT,
  site TEXT,
  steps TEXT,
  meta_json TEXT DEFAULT '',
  success_count INT DEFAULT 0,
  failure_count INT DEFAULT 0,
  created REAL, last_validated REAL
);
CREATE INDEX IF NOT EXISTS ix_frag_goal ON fragments(goal_sig);
CREATE TABLE IF NOT EXISTS trajectories(
  id INTEGER PRIMARY KEY,
  task_id TEXT,
  site TEXT,
  profile_json TEXT,
  steps TEXT,
  created REAL
);
CREATE TABLE IF NOT EXISTS runs(
  id INTEGER PRIMARY KEY, agent_id TEXT, task_id TEXT, condition TEXT,
  metrics TEXT, ts REAL
);
"""


def now(): return time.time()


def _slug(s, n=24):
    return "".join(c if c.isalnum() else "-" for c in (s or "").lower())[:n].strip("-")


def target_sig(el: dict) -> str:
    """Canonical signature of an action target: structure + text token."""
    parts = [el["tag"], el["type"], el["role"], el["name"], el["cls"],
             _slug(el.get("text", ""))]
    return "|".join(parts)


class Store:
    def __init__(self, path, allow_reads=True):
        self.db = sqlite3.connect(path)
        self.db.executescript(SCHEMA)
        # Read gate: `cold` conditions still WRITE observed knowledge but must
        # not READ anything back (first-agent semantics). This makes the
        # read/write asymmetry explicit instead of scattering conditionals.
        self.allow_reads = allow_reads

    def upsert_state(self, snap: dict) -> int:
        fp = self.fingerprint(snap)
        blob = gzip.compress(json.dumps(snap).encode())
        cur = self.db.execute(
            "INSERT INTO states(site,url,url_shape,fingerprint,raw_json,first_seen,last_seen)"
            " VALUES(?,?,?,?,?,?,?) ON CONFLICT(site,fingerprint)"
            " DO UPDATE SET last_seen=? RETURNING id",
            (snap["site"], snap["url"], snap["url_shape"], fp, blob, now(), now(), now()))
        rid = cur.fetchone()[0]
        self.db.commit()
        return rid

    @staticmethod
    def fingerprint(snap: dict) -> str:
        """Structural identity only.

        Dynamic form values are deliberately excluded from the structural
        fingerprint. They remain raw observables and must be represented as
        separate dynamic state variables when they are causally relevant.
        """
        sigs = sorted(target_sig(e) for e in snap["elements"])
        form = json.dumps([{"t": f["fields"], "m": f["method"]} for f in snap["forms"]],
                          sort_keys=True)
        bucket = lambda n: min(n // 10, 9)
        key = json.dumps([snap["url_shape"], sigs, form,
                          bucket(len(sigs)), bucket(snap["n_links"])])
        return hashlib.sha256(key.encode()).hexdigest()[:24]

    def record_transition(self, from_sid, action: dict, to_sid, outcome,
                          error_class="", task_id="", agent_id=""):
        aid = self.db.execute(
            "INSERT INTO actions(kind,target_sig) VALUES(?,?)"
            " ON CONFLICT(kind,target_sig) DO UPDATE SET kind=kind"
            " RETURNING id",
            (action["kind"], action.get("target_sig", ""))).fetchone()[0]
        self.db.execute(
            "INSERT INTO transitions(from_state,action_id,to_state,outcome,"
            "error_class,task_id,agent_id,ts) VALUES(?,?,?,?,?,?,?,?)",
            (from_sid, aid, to_sid, outcome, error_class, task_id, agent_id, now()))
        self.db.commit()
        return aid

    def save_fragment(self, goal_sig, steps, site, meta=None):
        """Save a fragment validated end-to-end at observation time.

        Run-1 had a positional INSERT bug that put a timestamp into
        success_count and 1 into created. Keep this explicit mapping and
        assert the row after every write so that the failure cannot silently
        recur.

        `meta` carries AUTO-DERIVED addressing metadata (entry/final URL
        shape, clicked-element text tokens, step kinds). It is derived from
        the execution context only; it never contains consumer-side query
        information. goal_sig itself is retained as provenance/debug label.
        """
        cur = self.db.execute(
            "SELECT id FROM fragments WHERE goal_sig=? AND site=?",
            (goal_sig, site)).fetchone()
        t = now()
        meta_json = json.dumps(meta or {})
        if cur:
            self.db.execute(
                "UPDATE fragments SET steps=?, meta_json=?, success_count=success_count+1,"
                " last_validated=? WHERE id=?", (json.dumps(steps), meta_json, t, cur[0]))
            fid = cur[0]
        else:
            row = self.db.execute(
                "INSERT INTO fragments(goal_sig,site,steps,meta_json,success_count,failure_count,"
                "created,last_validated) VALUES(?,?,?,?,1,0,?,?) RETURNING id",
                (goal_sig, site, json.dumps(steps), meta_json, t, t)).fetchone()
            fid = row[0]
        self.db.commit()
        self._assert_fragment_invariants(fid)
        return fid

    def _assert_fragment_invariants(self, fid):
        sc, fc, created, validated = self.db.execute(
            "SELECT success_count,failure_count,created,last_validated FROM fragments WHERE id=?",
            (fid,)).fetchone()
        assert isinstance(sc, int) and 0 <= sc < 1_000_000, ("bad success_count", sc)
        assert isinstance(fc, int) and 0 <= fc < 1_000_000, ("bad failure_count", fc)
        assert created and created > 1_500_000_000, ("bad created timestamp", created)
        assert validated and validated >= created, ("bad validation timestamp", created, validated)

    def best_fragment(self, goal_sig, site=None):
        if not self.allow_reads:
            return None
        q = ("SELECT id, site, steps, meta_json, success_count, failure_count, last_validated"
             " FROM fragments WHERE goal_sig=?")
        args = [goal_sig]
        if site:
            q += " AND site=?"
            args.append(site)
        rows = self.db.execute(q + " ORDER BY success_count - failure_count DESC,"
                                    " last_validated DESC", args).fetchall()
        if not rows:
            return None
        fid, s_site, steps, meta_json, sc, fc, lv = rows[0]
        assert isinstance(sc, int) and isinstance(fc, int), (sc, fc)
        return {"id": fid, "site": s_site, "steps": json.loads(steps),
                "meta": json.loads(meta_json or "{}"),
                "goal_sig": goal_sig,
                "success_count": sc, "failure_count": fc,
                "confidence": self.confidence(sc, fc, lv)}

    def iter_fragments(self, site=None):
        """All fragments with metadata; used by the addressing layer."""
        if not self.allow_reads:
            return []
        q = ("SELECT id, goal_sig, site, steps, meta_json, success_count,"
             " failure_count, created, last_validated FROM fragments")
        args = []
        if site:
            q += " WHERE site=?"
            args.append(site)
        out = []
        for r in self.db.execute(q + " ORDER BY id", args):
            fid, gsig, s_site, steps, meta_json, sc, fc, cr, lv = r
            assert isinstance(sc, int) and isinstance(fc, int), (sc, fc)
            out.append({"id": fid, "goal_sig": gsig, "site": s_site,
                        "steps": json.loads(steps),
                        "meta": json.loads(meta_json or "{}"),
                        "success_count": sc, "failure_count": fc,
                        "created": cr, "last_validated": lv,
                        "confidence": self.confidence(sc, fc, lv)})
        return out

    # ---- trajectories (nearest-trajectory baseline memory) ----
    def save_trajectory(self, task_id, site, profile_tokens, steps):
        self.db.execute(
            "INSERT INTO trajectories(task_id,site,profile_json,steps,created)"
            " VALUES(?,?,?,?,?)",
            (task_id, site, json.dumps(sorted(set(profile_tokens))),
             json.dumps(steps), now()))
        self.db.commit()

    def iter_trajectories(self, site=None):
        if not self.allow_reads:
            return []
        q = "SELECT task_id, site, profile_json, steps FROM trajectories"
        args = []
        if site:
            q += " WHERE site=?"
            args.append(site)
        return [{"task_id": t, "site": s,
                 "profile": json.loads(p), "steps": json.loads(st)}
                for t, s, p, st in self.db.execute(q, args)]

    @staticmethod
    def confidence(successes, failures, last_validated, halflife_s=7 * 86400):
        """Laplace success rate × exponential recency weight.

        This is an engineering score only until G8/G9 calibrate its mapping
        to empirical future success. The half-life must not be presented as a
        learned quantity before that calibration exists.
        """
        assert isinstance(successes, int) and successes >= 0
        assert isinstance(failures, int) and failures >= 0
        recency = 0.5 ** max(0.0, (now() - (last_validated or now())) / halflife_s)
        n = successes + failures
        rate = (successes + 1) / (n + 2) if n else 0.0
        return round(rate * (0.3 + 0.7 * recency), 4)

    def log_run(self, agent_id, task_id, condition, metrics):
        self.db.execute("INSERT INTO runs(agent_id,task_id,condition,metrics,ts)"
                        " VALUES(?,?,?,?,?)",
                        (agent_id, task_id, condition, json.dumps(metrics), now()))
        self.db.commit()

    def stats(self):
        s = lambda q: self.db.execute(q).fetchone()[0]
        return {"states": s("SELECT COUNT(*) FROM states"),
                "transitions": s("SELECT COUNT(*) FROM transitions"),
                "actions": s("SELECT COUNT(*) FROM actions"),
                "fragments": s("SELECT COUNT(*) FROM fragments")}

    # ---- concrete-graph accessors (graph-BFS baseline) ----
    def state_id_by_fingerprint(self, fp):
        if not self.allow_reads:
            return None
        r = self.db.execute("SELECT id FROM states WHERE fingerprint=?", (fp,)).fetchone()
        return r[0] if r else None

    def state_raw(self, sid):
        """Decompress stored raw snapshot JSON for a state id."""
        r = self.db.execute("SELECT raw_json, url_shape, url FROM states WHERE id=?",
                            (sid,)).fetchone()
        if not r:
            return None
        blob, shape, url = r
        try:
            raw = json.loads(gzip.decompress(blob).decode())
        except Exception:
            raw = {}
        return {"id": sid, "url_shape": shape, "url": url,
                "page_text": raw.get("page_text", ""),
                "title": raw.get("title", "")}

    def out_edges(self, sid):
        """Outgoing transitions of a state: [(action_kind, target_sig, to_sid)]."""
        if not self.allow_reads:
            return []
        return [(k, ts_, to) for k, ts_, to in self.db.execute(
            "SELECT a.kind, a.target_sig, t.to_state FROM transitions t"
            " JOIN actions a ON a.id=t.action_id WHERE t.from_state=?", (sid,))
            if to is not None]


def copy_store(src_path, dst_path):
    """Physical copy so independent methods start from identical knowledge."""
    import shutil
    shutil.copyfile(src_path, dst_path)
    return Store(dst_path)
