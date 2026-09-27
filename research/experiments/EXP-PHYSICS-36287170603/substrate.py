#!/usr/bin/env python3
"""
IVC Substrate: stdlib HTTP server with server-side ground-truth transition logging.
No external dependencies: no model credentials, no containers, no browser binaries.
"""

import json
import hashlib
import sqlite3
import threading
import time
import random
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from pathlib import Path
from typing import Dict, List, Tuple, Optional, Any
from dataclasses import dataclass, asdict
import uuid

# Fixed seeds for determinism
SEED = 44
random.seed(SEED)

# Regimes: deterministic vs stochastic transition kernels
REGIMES = ["deterministic", "stochastic"]
STATES_PER_REGIME = 8
ACTIONS = ["click", "fill", "select", "navigate", "type"]
N_ACTIONS = len(ACTIONS)

# Transition kernels
DETERMINISTIC_KERNEL = {}
STOCHASTIC_KERNEL = {}

rng = random.Random(SEED + 1000)

# Build deterministic kernel: each (state, action) -> single next_state
for regime in REGIMES:
    if regime == "deterministic":
        for s in range(STATES_PER_REGIME):
            for a in range(N_ACTIONS):
                # Deterministic: fixed mapping
                DETERMINISTIC_KERNEL[(s, a)] = (s + a + 1) % STATES_PER_REGIME
    else:
        for s in range(STATES_PER_REGIME):
            for a in range(N_ACTIONS):
                # Stochastic: dirichlet with noise=0.3
                base = [rng.random() for _ in range(STATES_PER_REGIME)]
                total = sum(base)
                probs = [b/total for b in base]
                # Add noise
                perturb = [rng.gauss(0, 0.3) for _ in range(STATES_PER_REGIME)]
                probs = [max(0.01, p + pert) for p, pert in zip(probs, perturb)]
                total = sum(probs)
                probs = [p/total for p in probs]
                STOCHASTIC_KERNEL[(s, a)] = probs


@dataclass
class TransitionLogEntry:
    """Server-side ground-truth transition log entry."""
    id: int = 0
    trajectory_id: str = ""
    step: int = 0
    state_before: int = 0
    regime_before: str = ""
    action: str = ""
    action_idx: int = 0
    state_after: int = 0
    regime_after: str = ""
    url_before: str = ""
    url_after: str = ""
    timestamp: float = 0.0
    # Ground truth latent variables for MI computation
    latent_state_before: int = 0
    latent_state_after: int = 0


class GroundTruthDB:
    """SQLite WAL database for ground-truth transition logging."""
    
    def __init__(self, db_path: str = "/tmp/ivc_ground_truth.db"):
        self.db_path = db_path
        self.lock = threading.Lock()
        self._init_db()
    
    def _init_db(self):
        with self.lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("""
                CREATE TABLE IF NOT EXISTS transitions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    trajectory_id TEXT NOT NULL,
                    step INTEGER NOT NULL,
                    state_before INTEGER NOT NULL,
                    regime_before TEXT NOT NULL,
                    action TEXT NOT NULL,
                    action_idx INTEGER NOT NULL,
                    state_after INTEGER NOT NULL,
                    regime_after TEXT NOT NULL,
                    url_before TEXT NOT NULL,
                    url_after TEXT NOT NULL,
                    timestamp REAL NOT NULL,
                    latent_state_before INTEGER NOT NULL,
                    latent_state_after INTEGER NOT NULL
                )
            """)
            conn.execute("CREATE INDEX IF NOT EXISTS idx_trajectory ON transitions(trajectory_id)")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_step ON transitions(step)")
            conn.commit()
            conn.close()
    
    def log_transition(self, entry: TransitionLogEntry):
        with self.lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute("""
                INSERT INTO transitions 
                (trajectory_id, step, state_before, regime_before, action, action_idx,
                 state_after, regime_after, url_before, url_after, timestamp,
                 latent_state_before, latent_state_after)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                entry.trajectory_id, entry.step, entry.state_before, entry.regime_before,
                entry.action, entry.action_idx, entry.state_after, entry.regime_after,
                entry.url_before, entry.url_after, entry.timestamp,
                entry.latent_state_before, entry.latent_state_after
            ))
            conn.commit()
            conn.close()
    
    def get_all_transitions(self) -> List[TransitionLogEntry]:
        with self.lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM transitions ORDER BY trajectory_id, step")
            rows = cursor.fetchall()
            conn.close()
            return [TransitionLogEntry(**dict(row)) for row in rows]
    
    def get_transitions_by_trajectory(self, trajectory_id: str) -> List[TransitionLogEntry]:
        with self.lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute(
                "SELECT * FROM transitions WHERE trajectory_id=? ORDER BY step", 
                (trajectory_id,)
            )
            rows = cursor.fetchall()
            conn.close()
            return [TransitionLogEntry(**dict(row)) for row in rows]
    
    def clear(self):
        with self.lock:
            conn = sqlite3.connect(self.db_path, check_same_thread=False)
            conn.execute("DELETE FROM transitions")
            conn.commit()
            conn.close()


# Global ground truth database
GROUND_TRUTH_DB = GroundTruthDB()


def generate_url(state: int, regime: str) -> str:
    return f"http://localhost:18888/state/{regime}/{state}"


def sample_next_state(state: int, action_idx: int, regime: str) -> int:
    """Sample next state from the appropriate kernel."""
    if regime == "deterministic":
        return DETERMINISTIC_KERNEL[(state, action_idx)]
    else:
        probs = STOCHASTIC_KERNEL[(state, action_idx)]
        return random.choices(range(STATES_PER_REGIME), weights=probs)[0]


class IVCRequestHandler(BaseHTTPRequestHandler):
    """HTTP request handler with ground-truth logging."""
    
    # Session storage: trajectory_id -> (current_state, current_regime, step_count)
    sessions: Dict[str, Tuple[int, str, int]] = {}
    sessions_lock = threading.Lock()
    
    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == "/health":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "ok"}).encode())
            return
        
        if path == "/reset":
            # Reset all sessions
            with self.sessions_lock:
                self.sessions.clear()
            GROUND_TRUTH_DB.clear()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "reset"}).encode())
            return
        
        if path == "/ground_truth":
            # Export ground truth log
            transitions = GROUND_TRUTH_DB.get_all_transitions()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps([asdict(t) for t in transitions]).encode())
            return
        
        if path.startswith("/state/"):
            # Parse: /state/{regime}/{state}
            parts = path.split("/")
            if len(parts) != 4:
                self.send_response(404)
                self.end_headers()
                return
            
            regime = parts[2]
            if regime not in REGIMES:
                self.send_response(404)
                self.end_headers()
                return
            
            try:
                state = int(parts[3])
                if not (0 <= state < STATES_PER_REGIME):
                    self.send_response(404)
                    self.end_headers()
                    return
            except ValueError:
                self.send_response(404)
                self.end_headers()
                return
            
            # Get or create session
            trajectory_id = self.headers.get("X-Trajectory-ID")
            if not trajectory_id:
                trajectory_id = str(uuid.uuid4())
            
            with self.sessions_lock:
                if trajectory_id not in self.sessions:
                    # New trajectory: random initial state and regime
                    init_state = random.randint(0, STATES_PER_REGIME - 1)
                    init_regime = random.choice(REGIMES)
                    self.sessions[trajectory_id] = (init_state, init_regime, 0)
                
                current_state, current_regime, step = self.sessions[trajectory_id]
                
                # Verify the requested state matches current (for deterministic transitions)
                # In this substrate, the client requests a specific state, we serve it
                # but log the ground truth transition
                
                # For the transition log, we need the action
                # The action is encoded in the query parameter
                query = parse_qs(parsed.query)
                action = query.get("action", ["click"])[0]
                try:
                    action_idx = ACTIONS.index(action)
                except ValueError:
                    action_idx = 0
                    action = "click"
                
                # Sample next state based on current state and action
                next_state = sample_next_state(current_state, action_idx, current_regime)
                
                # Regime can switch with small probability (for stochastic regime)
                next_regime = current_regime
                if current_regime == "stochastic" and random.random() < 0.1:
                    next_regime = "deterministic"
                elif current_regime == "deterministic" and random.random() < 0.1:
                    next_regime = "stochastic"
                
                # Log ground truth transition
                timestamp = time.time()
                url_before = generate_url(current_state, current_regime)
                url_after = generate_url(next_state, next_regime)
                
                entry = TransitionLogEntry(
                    trajectory_id=trajectory_id,
                    step=step,
                    state_before=current_state,
                    regime_before=current_regime,
                    action=action,
                    action_idx=action_idx,
                    state_after=next_state,
                    regime_after=next_regime,
                    url_before=url_before,
                    url_after=url_after,
                    timestamp=timestamp,
                    latent_state_before=current_state,
                    latent_state_after=next_state
                )
                GROUND_TRUTH_DB.log_transition(entry)
                
                # Update session
                self.sessions[trajectory_id] = (next_state, next_regime, step + 1)
            
            # Respond with the requested state's page
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("X-Trajectory-ID", trajectory_id)
            self.send_header("X-State", str(state))
            self.send_header("X-Regime", regime)
            self.end_headers()
            
            html = f"""
            <html>
            <head><title>State {state} ({regime})</title></head>
            <body>
                <h1>State {state} - Regime: {regime}</h1>
                <p>Trajectory: {trajectory_id}</p>
                <p>Step: {step}</p>
                <div id="actions">
                    <a href="/state/{regime}/{(state+1)%STATES_PER_REGIME}?action=click">Click</a><br>
                    <a href="/state/{regime}/{(state+2)%STATES_PER_REGIME}?action=fill">Fill</a><br>
                    <a href="/state/{regime}/{(state+3)%STATES_PER_REGIME}?action=select">Select</a><br>
                    <a href="/state/{regime}/{(state+4)%STATES_PER_REGIME}?action=navigate">Navigate</a><br>
                    <a href="/state/{regime}/{(state+5)%STATES_PER_REGIME}?action=type">Type</a><br>
                </div>
            </body>
            </html>
            """
            self.wfile.write(html.encode())
            return
        
        self.send_response(404)
        self.end_headers()
    
    def log_message(self, format, *args):
        # Suppress default log messages
        pass
    
    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == "/reset":
            # Reset all sessions
            with self.sessions_lock:
                self.sessions.clear()
            GROUND_TRUTH_DB.clear()
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status": "reset"}).encode())
            return
        
        if path == "/ground_truth":
            # Export ground truth log
            try:
                transitions = GROUND_TRUTH_DB.get_all_transitions()
                data = json.dumps([asdict(t) for t in transitions]).encode()
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Content-Length", str(len(data)))
                self.end_headers()
                self.wfile.write(data)
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
            return
        
        self.send_response(404)
        self.end_headers()


def run_server(port: int = 18888):
    """Run the HTTP server."""
    server = HTTPServer(("localhost", port), IVCRequestHandler)
    print(f"IVC Substrate server running on http://localhost:{port}")
    server.serve_forever()


if __name__ == "__main__":
    run_server()