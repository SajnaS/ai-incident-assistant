def render_triage(r: dict):
    bullets = "\\n".join([f"• {a}" for a in r.get("next_actions", [])]) or "• (none)"
    signals = "\\n".join([f"• {s}" for s in r.get("signals", [])]) or "• (none)"
    return [
        {"type":"section","text":{"type":"mrkdwn","text":f"*{r['incidentId']} — Triage Summary*\\n{r['tldr']}"}},
        {"type":"section","text":{"type":"mrkdwn","text":f"*Signals*\\n{signals}"}},
        {"type":"section","text":{"type":"mrkdwn","text":f"*Next actions*\\n{bullets}"}},
        {"type":"context","elements":[{"type":"mrkdwn","text": f"Status draft: {r.get('status_update','')}" }]}
    ]
