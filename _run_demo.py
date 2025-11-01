from app.agent import run_triage
r = run_triage("INC-102")
print("✅ Incident ID:", r["incidentId"])
print("🧠 TL;DR:", r["tldr"])
print("📊 Signals:", r["signals"])
print("🧩 Next actions:", r["next_actions"])
print("Status draft:", r["status_update"])
