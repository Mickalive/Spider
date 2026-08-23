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
  raw_json BLOB,           -- gzipped full snapshot (raw observables)
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
  outcome TEXT,             -- success|failure
  error_class TEXT DEFAULT '',
  task_id TEXT DEFAULT '', agent_id TEXT DEFAULT '',
  ts REAL,
  FOREIGN KEY(from_state) REFERENCES states(id),
  FOREIGN KEY(action_id) REFERENCES actions(id),
  FOREIGN KEY(to_state) REFERENCES states(id)
);
CREATE TABLE IF NOT EXISTS fragments(
  id INTEGER PRIMARY KEY,
  goal_sig TEXT,            -- semantic/structural descriptor of subgoal achieved
  site TEXT,
  steps TEXT,               -- JSON [{state_fp, kind, target_sig, expect_fp}]
  success_count INT DEFAULT 0,
  failure_count INT DEFAULT 0,
  created REAL, last_validated REAL
);
CREATE INDEX IF NOT EXISTS ix_frag_goal ON fragments(goal_sig);
CREATE TABLE IF NOT EXISTS runs(
  id INTEGER PRIMARY KEY, agent_id TEXT, task_id TEXT, condition TEXT,
  metrics TEXT, ts REAL     -- metrics JSON per §13
);
"""


def now(): return time.time()


def _slug(s, n=24):
    return "".join(c if c.isalnum() else "-" for c in (s or "").lower())[:n].strip("-")


def target_sig(el: dict) -> str:
    """Canonical signature of an action target: structure + text token.
    Text adds discrimination within a site; cross-site transfer must
    survive its absence (measured, not assumed)."""
    parts = [el["tag"], el["type"], el["role"], el["name"], el["cls"],
             _slug(el.get("text", ""))]
    return "|".join(parts)


class Store:
    def __init__(self, path):
        self.db = sqlite3.connect(path)
        self.db.executescript(SCHEMA)

    # ---------- states ----------
    def upsert_state(self, snap: dict) -> int:
        fp = self.fingerprint(snap)
        blob = gzip.compress(json.dumps(snap).encode())
        cur = self.db.execute(
            "INSERT INTO states(site,url,url_shape,fingerprint,raw_json,first_seen,last_seen)"
            " VALUES(?,?,?,?,?,?,?) ON CONFLICT(site,fingerprint)"
            " DO UPDATE SET last_seen=? RETURNING id",
            (snap["site"], snap["url"], snap["url_shape"], fp, blob, now(), now(), now()))
        rid = cur.fetchone()[0]; self.db.commit()
        return rid

    @staticmethod
    def fingerprint(snap: dict) -> str:
        """Structural state fingerprint: url shape + sorted target signatures +
        form structure + link density bucket. Deliberately text-free."""
        import hashlib
        sigs = sorted(target_sig(e) for e in snap["elements"])
        form = json.dumps([{ "t": f["fields"], "m": f["method"]} for f in snap["forms"]],
                          sort_keys=True)
        bucket = lambda n: min(n // 10, 9)
        key = json.dumps([snap["url_shape"], sigs, form,
                          bucket(len(sigs)), bucket(snap["n_links"])])
        return hashlib.sha256(key.encode()).hexdigest()[:24]

    # ---------- actions / transitions ----------
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

    # ---------- fragments ----------
    def save_fragment(self, goal_sig, steps, site):
        """steps: list of {kind, target_sig}; validated end-to-end at save time."""
        cur = self.db.execute(
            "SELECT id, success_count FROM fragments WHERE goal_sig=? AND site=?",
            (goal_sig, site)).fetchone()
        if cur:
            self.db.execute(
                "UPDATE fragments SET steps=?, success_count=success_count+1,"
                " last_validated=? WHERE id=?", (json.dumps(steps), now(), cur[0]))
        else:
            self.db.execute(
                "INSERT INTO fragments(goal_sig,site,steps,success_count,created,"
                "last_validated) VALUES(?,?,?,?,1,?)", (goal_sig, site,
                                                        json.dumps(steps), now(), now()))
        self.db.commit()

    def best_fragment(self, goal_sig, site=None):
        q = ("SELECT id, site, steps, success_count, failure_count, last_validated"
             " FROM fragments WHERE goal_sig=?")
        args = [goal_sig]
        if site:
            q += " AND site=?"; args.append(site)
        rows = self.db.execute(q + " ORDER BY success_count - failure_count DESC,"
                                    " last_validated DESC", args).fetchall()
        if not rows:
            return None
        fid, s_site, steps, sc, fc, lv = rows[0]
        return {"id": fid, "site": s_site, "steps": json.loads(steps),
                "success_count": sc, "failure_count": fc,
                "confidence": self.confidence(sc, fc, lv)}

    @staticmethod
    def confidence(successes, failures, last_validated, halflife_s=7 * 86400):
        """Empirical Laplace success rate × exponential recency weight.
        Halflife is a parameter to be measured (G8/G9), not asserted truth."""
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
