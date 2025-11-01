AI Incident Assistant (Agentic AIOps)

An autonomous SRE agent that runs a Plan → Act → Reflect loop to triage incidents. When an alert lands in Slack, the agent analyzes metrics, logs, and deploys, then posts a TL;DR, signals, and prioritized next actions. It also writes a Jira‑ready draft and a timeline.

https://github.com//ai-incident-assistant

 Why

First 15 minutes of incident triage are repetitive: check dashboards, skim logs, confirm recent deploys. This project automates that initial pass to cut MTTU and get engineers to action faster.

What makes it agentic

Plan: decide what to inspect

Act: fetch/analyze signals via tools (mock data here)

Reflect: critique and refine outputs

State: write timeline + Jira draft for downstream use

🧱 Stack

Python, FastAPI, Slack Bolt (Python)

LLM provider: Gemini 1.5 (switchable from OpenAI)

Pydantic, python‑dotenv

Structure
app/
  main.py       # FastAPI + Slack Bolt (/slack/events, /aia)
  agent.py      # run_triage(): plan → act → reflect
  prompts.py    # SYSTEM_PROMPT + analyze/reflect/plan prompts
  tools.py      # read mock data, write outputs, append timeline
  render.py     # Slack Block Kit builder
  schemas.py    # Pydantic models
mock/           # incidents, metrics, logs, deploys
out/            # jira drafts, timelines
_run_demo.py    # local runner

 Quick start
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt


# .env
# SLACK_BOT_TOKEN=xoxb-...
# SLACK_SIGNING_SECRET=...
# GOOGLE_API_KEY=AIza...


python _run_demo.py  # local demo
uvicorn app.main:app --reload --port 3000  # API / Slack
ngrok http 3000  # expose locally
🧪 Try it in Slack

Create Slack app → scopes: commands, chat:write → Install.

Set Slash Command /aia → https://<ngrok>/slack/events.

Invite bot → /invite @AI Incident Assistant.

Run /aia triage INC-102.

Prompts (schema‑constrained)

analyze_prompt → {tldr, signals, hypotheses, next_actions, status_update}

reflect_prompt → refine {tldr, next_actions}

🛣️ Roadmap

Real integrations: Datadog/CloudWatch/GitHub/Jira

Buttons: “Create Jira”, “Escalate”, “Ack”

Background worker for long triage jobs
