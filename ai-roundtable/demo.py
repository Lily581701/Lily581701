"""Zero-cost TURN-TAKING DEMO ONLY. No AI services are contacted."""
import json
from datetime import datetime, timezone
from pathlib import Path

CONFIG = json.loads(Path(__file__).with_name("protocol.json").read_text())
participants = CONFIG["participants"][:2]
primary = CONFIG["primary_participant"]
order = sorted(participants, key=lambda p: p["name"] != primary)
turns = min(CONFIG["max_total_turns"], 4)
transcript = []
for index in range(turns):
    actor = order[index % len(order)]["name"]
    message = f"[SIMULATION] {actor} speaks in turn {index + 1}. This is not a real model response."
    transcript.append({"turn": index + 1, "speaker": actor, "text": message})
    print(actor + ": " + message)
Path(__file__).with_name("demo-transcript.json").write_text(
    json.dumps({"generated_at": datetime.now(timezone.utc).isoformat(),
                "simulated": True, "messages": transcript}, indent=2) + "\n")
