"""Opt-in two-to-five-model conversation bridge. Python 3.10+; stdlib only."""
import argparse, datetime, json, os, urllib.request
from pathlib import Path

def load(path):
    data=json.loads(Path(path).read_text())
    seats=data["participants"]
    if not 2 <= len(seats) <= 5 or len({p["name"] for p in seats}) != len(seats):
        raise ValueError("Use two to five uniquely named seats")
    if not all(p.get("model") for p in seats):
        raise ValueError("Each seat needs an exact, verified model ID before live use")
    return data

def respond(seat,history,mock):
    if mock:
        return "[MOCK RESPONSE; not an AI model] This is a turn-taking test."
    url=seat.get("endpoint","")
    token=os.getenv(seat.get("key_env",""))
    if not url.startswith("https://") or not token:
        raise ValueError("This seat needs a verified HTTPS endpoint and an environment-variable API key")
    messages=[{"role":"system","content":"You are participating in an open roundtable. Reason independently, disagree freely, and choose topics naturally."}]
    messages += [{"role":"user","content":x["speaker"]+": "+x["text"]} for x in history]
    messages.append({"role":"user","content":"Your turn, "+seat["name"]+". Respond to the discussion."})
    body=json.dumps({"model":seat["model"],"messages":messages,"max_tokens":300}).encode()
    req=urllib.request.Request(url,data=body,headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"})
    with urllib.request.urlopen(req,timeout=45) as resp:
        return json.load(resp)["choices"][0]["message"]["content"]

def main():
    p=argparse.ArgumentParser()
    p.add_argument("--config",default="ai-roundtable/participants.example.json")
    p.add_argument("--turns",type=int,default=6)
    p.add_argument("--mock",action="store_true")
    p.add_argument("--output",default="roundtable-transcript.json")
    a=p.parse_args()
    if not 1 <= a.turns <= 20: p.error("Choose between one and twenty turns")
    cfg=load(a.config); seats=cfg["participants"]; names=[s["name"] for s in seats]
    if cfg.get("primary",names[0]) not in names: p.error("Unknown primary speaker")
    i=names.index(cfg.get("primary",names[0])); seats=seats[i:]+seats[:i]
    history=[{"speaker":"host","text":"Open conversation. Choose topics freely."}]
    for n in range(a.turns):
        seat=seats[n%len(seats)]
        try: answer=respond(seat,history,a.mock)
        except Exception as e:
            print("Stopped at turn",n+1,":",type(e).__name__,str(e)); break
        entry={"speaker":seat["name"],"model":seat["model"],"text":answer,"utc":datetime.datetime.now(datetime.timezone.utc).isoformat()}
        history.append(entry); print(entry["speaker"]+": "+entry["text"])
    Path(a.output).write_text(json.dumps({"mock":a.mock,"turns":history},indent=2))
    print("Saved",a.output)

if __name__=="__main__": main()
