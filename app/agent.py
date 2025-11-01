import os, json
from dotenv import load_dotenv
from .prompts import SYSTEM_PROMPT, plan_prompt, reflect_prompt,analyze_prompt
from .tools import read_incident, get_metrics, get_logs, get_deploys, write_jira_draft, append_event
from .schemas import TriageResult

# --- Gemini setup ---
load_dotenv()
import google.generativeai as genai
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# pick a model (flash = fast/cheap, pro = stronger)
MODEL_ID = "gemini-2.5-flash"

def _chat_single(prompt_text: str) -> str:
    """
    Send a single-turn prompt to Gemini and return text.
    We use 'system prompt' by prepending SYSTEM_PROMPT to the user content.
    """
    model = genai.GenerativeModel(MODEL_ID)
    # Use a single-turn generate call for simplicity
    resp = model.generate_content(
        f"{SYSTEM_PROMPT}\n\n{prompt_text}",
        generation_config={"temperature": 0.2},
    )
    # Some SDK versions return .text, some need concatenation of parts:
    return getattr(resp, "text", None) or "".join(p.text for p in resp.candidates[0].content.parts if hasattr(p, "text"))

def _safe(obj_or_str):
    if isinstance(obj_or_str, dict):
        return obj_or_str
    try:
        return json.loads(obj_or_str)
    except Exception:
        # try lenient parse if model added comments/trailing commas etc.
        try:
            import json5
            return json5.loads(obj_or_str)
        except Exception:
            return {}

def run_triage(incident_id: str) -> dict:
    inc = read_incident(incident_id)

    # 1) PLAN
    plan = _chat_single(plan_prompt(inc))
    append_event(incident_id, "plan", plan)

    # 2) ACT — collect mock signals and ask Gemini to analyze in JSON
    metrics = get_metrics(incident_id)
    logs = get_logs(incident_id)
    deploys = get_deploys(inc["service"])

    act_prompt = analyze_prompt(incident=inc, metrics=metrics, logs=logs, deploys=deploys)
    act = _chat_single(act_prompt)
    append_event(incident_id, "act", act)


    # 3) REFLECT — ask for refined TL;DR + next_actions
    reflect = _chat_single(reflect_prompt(incident=inc, plan=plan, act=act))
    append_event(incident_id, "reflect", reflect)

    # Parse model outputs
    out = _safe(act).get("output", _safe(act))
    refined = _safe(reflect).get("output", {})
    tldr = refined.get("tldr", out.get("tldr", "")) or ""
    next_actions = refined.get("next_actions", out.get("next_actions", [])) or []

    triage = TriageResult(
        incidentId=incident_id,
        tldr=tldr,
        signals=out.get("signals", []) or [],
        hypotheses=out.get("hypotheses", []) or [],
        next_actions=next_actions,
        status_update=out.get("status_update", "") or "",
    )
    write_jira_draft(incident_id, triage.model_dump())
    return triage.model_dump()
