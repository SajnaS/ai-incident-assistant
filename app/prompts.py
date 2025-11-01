import json

SYSTEM_PROMPT = (
  "You are an AI Incident Assistant for a SaaS company. "
  "Be concise, action-oriented, and cite signals. "
  "When asked for results, OUTPUT STRICT JSON ONLY with no extra commentary."
)

def plan_prompt(inc: dict) -> str:
    # Planning can be light; we don't parse this as JSON
    return (
        "Plan the first triage steps for this alert. Keep it short.\n"
        f"Alert: {json.dumps(inc)}"
    )

def analyze_prompt(incident: dict, metrics: dict, logs: dict, deploys: dict) -> str:
    # This is the critical one: force JSON with the exact keys we need
    schema = {
        "output": {
            "tldr": "1-sentence summary of likely cause & context",
            "signals": ["bullet list of key signals (metrics/logs/deploys)"],
            "hypotheses": ["top 1-3 likely root causes"],
            "next_actions": ["ordered, concrete actions for the on-call"],
            "status_update": "one-line Slack status draft"
        }
    }
    return (
        "Analyze the following incident context and RETURN ONLY STRICT JSON that matches this Python-dict-shaped schema "
        "(no Markdown, no prose before/after, no code fences):\n"
        f"{json.dumps(schema)}\n\n"
        f"Incident: {json.dumps(incident)}\n"
        f"Metrics: {json.dumps(metrics)}\n"
        f"Logs: {json.dumps(logs)}\n"
        f"Deploys: {json.dumps(deploys)}\n"
    )

def reflect_prompt(incident: dict, plan: str, act: str) -> str:
    schema = {
        "output": {
            "tldr": "refined 1-sentence TL;DR",
            "next_actions": ["deduped, prioritized actions"],
            "notes": "short notes on assumptions/risks"
        }
    }
    return (
      "Review your earlier analysis and RETURN ONLY STRICT JSON matching this schema (no extra text):\n"
      f"{json.dumps(schema)}\n\n"
      f"Incident: {json.dumps(incident)}\n"
      f"Plan: {plan}\n"
      f"Analysis: {act}\n"
    )
