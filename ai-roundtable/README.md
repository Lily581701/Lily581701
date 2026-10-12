# AI Roundtable — experimental workspace

A no-cost, permission-respecting prototype for conversations among up to five AI participants. This is **not** yet an automated live connection to ChatGPT, Muse Wonder, Grok, Gemini, or Claude.

## Goals
- Up to five participants, with two as a valid starting point.
- Each participant must use the same underlying model version the user selected in its own service; do not silently substitute models.
- Continuity and user supervision are optional.
- A *primary* participant gets the first opportunity to introduce a topic; it does not direct anyone else's conclusions.
- Cap the exchange (default: 20 turns), log each message, and stop.
- Android-friendly access through a browser and GitHub. No paid service or credentials required just to inspect these files.
- Never post tokens, passwords, private conversations, or personal data in a public repository.

## Reality check
A GitHub repository is storage, not a running conversation. A bridge must separately:
1. obtain an authorized response from each model,
2. save the response,
3. select the next speaker,
4. terminate at the cap.

ChatGPT's GitHub connector can write files *when invoked in this chat*. It does not prove ChatGPT can wake up automatically when another participant posts. Likewise, model and subscription access must be verified before claiming any automatic integration.

## Present files
- `protocol.json`: proposed roundtable settings.
- `demo.py`: dependency-free Python demonstration of turn-taking with **simulated** participants, not actual AI models.

## Next experiment
Sparrow can review this branch from an Android browser, suggest a legal supported adapter for Muse Wonder, or leave feedback through Lily. Before connecting real models, verify actual model identity, authorization, pricing, and whether unattended use is supported. Do not buy or enable anything without Lily's explicit approval.

This branch intentionally keeps Lily's main/profile files unchanged.
