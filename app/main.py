import os
from fastapi import FastAPI, Request, Response
from slack_bolt import App as SlackApp
from slack_bolt.adapter.fastapi import SlackRequestHandler
from .agent import run_triage
from .render import render_triage

slack_app = SlackApp(
    token=os.environ.get("SLACK_BOT_TOKEN"),
    signing_secret=os.environ.get("SLACK_SIGNING_SECRET"),
)
app = FastAPI()
handler = SlackRequestHandler(slack_app)

@slack_app.command("/aia")
def handle_aia_command(ack, respond, command, client):
    ack()
    text = (command.get("text") or "").strip()
    parts = text.split()
    if len(parts) != 2 or parts[0].lower() != "triage":
        return respond("Usage: `/aia triage <INC-ID>`")
    inc_id = parts[1]
    respond(f"🔍 Starting triage for *{inc_id}* …")
    result = run_triage(inc_id)
    blocks = render_triage(result)
    client.chat_postMessage(channel=command["channel_id"], text=result["tldr"], blocks=blocks)

@app.post("/slack/events")
async def slack_events(req: Request):
    body = await req.body()
    return Response(content=handler.handle(body, req.headers), media_type="application/json")
