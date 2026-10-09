import json, time, hashlib, sys
from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langchain_openai import ChatOpenAI

base = sys.argv[1]
model = sys.argv[2]
api_key = sys.argv[3] if len(sys.argv) > 3 else "sk-noauth"

llm = ChatOpenAI(base_url=base, api_key=api_key, model=model, temperature=0, max_tokens=16, timeout=60)

class S(TypedDict):
    x: str
    y: str

def node_plan(state: S) -> S:
    r = llm.invoke([{"role":"user","content":"Reply with the single token SPIDER-PING"}])
    return {"y": r.content}

g = StateGraph(S)
g.add_node("plan", node_plan)
g.add_edge(START, "plan")
g.add_edge("plan", END)
app = g.compile()

t0 = time.time()
out = app.invoke({"x": "hello"})
dt = time.time() - t0
body = json.dumps(out, sort_keys=True)
print(json.dumps({
  "base_url": base, "model": model,
  "output": out["y"], "latency_s": round(dt, 3),
  "output_sha256": hashlib.sha256(body.encode()).hexdigest(),
  "framework": "langgraph",
}))
