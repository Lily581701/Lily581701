# AI Roundtable: first prototype

**Status:** basic turn-taking engine built, real assistant connections **not yet available or verified**.

This is a free-to-run Python standard-library prototype for **two to five** seats, a user-selected primary speaker, a maximum of **twenty** total turns, and a saved JSON transcript. In mock mode it makes no requests and charges nothing. **Mock participants are not actual AI assistants.**

Run it from repository root with Python 3.10+:

```bash
python ai-roundtable/roundtable.py --mock --turns 6
```

The sample configuration is `ai-roundtable/participants.example.json`. To run against real models, the *exact underlying model* must first be verified, and each provider must offer an authorized compatible HTTPS chat-completions API. A consumer app subscription is not necessarily API access. Muse Wonder availability is unverified. The script stops when an endpoint or key is missing; it does not substitute a different model.

The live adapter uses environment-variable API keys, **never keys pasted into chat or checked into GitHub**. Confirm pricing before using live mode. No Android background process, polling schedule, or existing ChatGPT/Muse session connection is supplied by this prototype. Android use via Termux is plausible but untested.

This branch is in a PUBLIC repository. Do not add sensitive personal data, access tokens, private conversation records or bank details. No unauthorized UI automation or scraping.
