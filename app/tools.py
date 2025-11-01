import json, pathlib, datetime
ROOT = pathlib.Path(__file__).resolve().parents[1]
def _read(p): return json.loads((ROOT / p).read_text(encoding="utf-8"))
def read_incident(id):     return _read(f"mock/incidents/{id}.json")
def get_metrics(id):       return _read(f"mock/metrics/{id}.json")
def get_logs(id):          return _read(f"mock/logs/{id}.json")
def get_deploys(service):  return _read(f"mock/deploys/{service}.json")
def write_jira_draft(id, data):
    out = ROOT / "out" / "jira"; out.mkdir(parents=True, exist_ok=True)
    (out / f"{id}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")
def append_event(incident_id, kind, content):
    out = ROOT / "out" / "timeline"; out.mkdir(parents=True, exist_ok=True)
    p = out / f"{incident_id}.json"
    arr = json.loads(p.read_text()) if p.exists() else []
    arr.append({"ts": datetime.datetime.utcnow().isoformat() + "Z", "kind": kind, "content": content})
    p.write_text(json.dumps(arr, indent=2), encoding="utf-8")
