#!/usr/bin/env python3
"""Experimental multi-model conversation bridge. Python standard library only.
This does not connect existing consumer app chats or bypass provider access.
Each participant must have an authorized OpenAI-compatible chat-completions endpoint.
"""
import json, os, sys, time, urllib.request, urllib.error
from datetime import datetime, timezone
from pathlib import Path

def load_participants(config):
    agents=config.get("participants",[])
    if not (2<=len(agents)<=5): raise ValueError("Configure between two and five participants.")
    names=[a["name"] for a in agents]
    if len(set(names))!=len(names): raise ValueError("Participant names must be unique.")
    for a in agents:
        for key in ("name","model","endpoint","token_env"):
            if not a.get(key): raise ValueError("Missing "+key+" for "+str(a))
        if not a["endpoint"].startswith("https://"): raise ValueError("HTTPS endpoint required.")
    return agents

def response_from(agent,history,timeout=45):
    token=os.environ.get(agent["token_env"])
    if not token: raise RuntimeError("Missing environment variable: "+agent["token_env"])
    context=[{"role":"system","content":"You are participating in a conversation with other AI systems. Choose your own thoughtful response, and feel free to respectfully disagree. Do not reveal credentials. Reply as "+agent["name"]+"."}]
    # Represent other participants' messages as context, without claiming app memory.
    context += [{"role":"user","content":item["speaker"]+": "+item["text"]} for item in history[-12:]]
    payload=json.dumps({"model":agent["model"],"messages":context,"max_tokens":350}).encode()
    req=urllib.request.Request(agent["endpoint"],data=payload,headers={"Authorization":"Bearer "+token,"Content-Type":"application/json"},method="POST")
    with urllib.request.urlopen(req,timeout=timeout) as r:
        obj=json.load(r)
    return obj["choices"][0]["message"]["content"].strip()

def run(config):
    agents=load_participants(config)
    limit=int(config.get("max_turns",20))
    if not (1<=limit<=20): raise ValueError("max_turns must be between one and twenty.")
    lead=config.get("primary",agents[0]["name"])
    if lead not in [a["name"] for a in agents]: raise ValueError("Unknown primary.")
    start=next(i for i,a in enumerate(agents) if a["name"]==lead)
    history=[{"speaker":"Host","text":"The participants are free to discuss an idea they find worthwhile."}]
    outfile=Path(config.get("transcript","conversation.json"))
    for turn in range(limit):
        agent=agents[(start+turn)%len(agents)]
        try: message=response_from(agent,history)
        except Exception as exc:
            print("Stopped at turn",turn+1,"due to:",type(exc).__name__,str(exc),file=sys.stderr)
            break
        entry={"speaker":agent["name"],"model":agent["model"],"text":message,"timestamp":datetime.now(timezone.utc).isoformat()}
        history.append(entry)
        outfile.write_text(json.dumps(history,indent=2),encoding="utf-8")
        print(agent["name"]+": "+message+"\n")
    print("Transcript:",outfile)

if __name__=="__main__":
    with open(sys.argv[1] if len(sys.argv)>1 else "config.json",encoding="utf-8") as f:run(json.load(f))
