# Discord Interaction Endpoint Architecture

## Goal

-   Keep the Interaction Endpoint URL fixed in Discord Developer Portal
-   Use Cloud Run as the single public entry point
-   In production: handle interactions normally
-   In development: forward requests to a local server via ngrok
-   Avoid changing the registered endpoint URL during development

------------------------------------------------------------------------

# Overall Architecture

    Discord
       ↓
    Cloud Run (public endpoint)
       ↓
     ┌─────────────────────────┐
     │ MODE=prod  → handle     │
     │ MODE=dev   → forward    │
     └─────────────────────────┘

The Interaction Endpoint URL registered in Discord Developer Portal
always points to Cloud Run.

------------------------------------------------------------------------

# Signature Verification Strategy

Discord sends:

-   X-Signature-Ed25519
-   X-Signature-Timestamp

Signature verification MUST be performed.

## Recommended Design

Perform signature verification inside Cloud Run before forwarding.

Reasons:

-   Security boundary stays in the cloud
-   Public key is not required on local machine
-   Local server can be treated as trusted internal target

Flow:

    Discord
      ↓
    Cloud Run
      ├─ Verify signature
      ├─ Handle PING
      └─ If dev → forward to ngrok

------------------------------------------------------------------------

# Environment Variables

Cloud Run configuration:

    MODE=prod or dev
    FORWARD_URL=https://xxxx.ngrok.io
    DISCORD_PUBLIC_KEY=xxxxx

------------------------------------------------------------------------

# Example Implementation (FastAPI)

``` python
import os
import httpx
from fastapi import FastAPI, Request, Response

app = FastAPI()

MODE = os.getenv("MODE", "prod")
FORWARD_URL = os.getenv("FORWARD_URL")

@app.post("/interactions")
async def interactions(request: Request):
    body = await request.body()

    verify_discord_signature(request, body)

    payload = await request.json()

    if payload["type"] == 1:
        return {"type": 1}

    if MODE == "dev" and FORWARD_URL:
        async with httpx.AsyncClient() as client:
            resp = await client.post(
                f"{FORWARD_URL}/interactions",
                content=body,
                headers=request.headers
            )
            return Response(
                content=resp.content,
                status_code=resp.status_code,
                headers=dict(resp.headers),
            )

    return await handle_interaction(payload)
```

------------------------------------------------------------------------

# Development Flow

1.  Start local API server
2.  Start ngrok:

```{=html}
<!-- -->
```
    ngrok http 8000

3.  Deploy Cloud Run with:

```{=html}
<!-- -->
```
    MODE=dev
    FORWARD_URL=https://xxxx.ngrok.io

Request path becomes:

    Discord
      ↓
    Cloud Run
      ↓
    ngrok
      ↓
    localhost

------------------------------------------------------------------------

# Production Switch

Redeploy Cloud Run with:

    MODE=prod

No change required in Discord Developer Portal.

------------------------------------------------------------------------

# Optional: Two-Service Pattern

Instead of switching modes, create two Cloud Run services:

  Service    Purpose
  ---------- ------------------------
  bot-prod   Production
  bot-dev    Development forwarding

Developer Portal registers only bot-prod.

------------------------------------------------------------------------

# Important Considerations

## 1. 3-Second Response Limit

Discord requires a response within 3 seconds.

Forwarding increases latency.

Possible mitigation:

-   Immediately ACK in Cloud Run
-   Use follow-up messages for heavy processing

## 2. ngrok URL Changes

Options:

-   Use paid fixed domain
-   Update Cloud Run env and redeploy
-   Automate via script

------------------------------------------------------------------------

# Advantages of This Architecture

-   Fixed public endpoint
-   No manual URL switching
-   Secure signature boundary
-   Compatible with Terraform and CI/CD
-   Scales cleanly as the bot evolves

------------------------------------------------------------------------

# Summary

Recommended approach:

-   Cloud Run as permanent public endpoint
-   Signature verification in Cloud Run
-   Forwarding mode enabled via environment variable
-   Local development via ngrok
-   Production via direct handling

This design keeps infrastructure clean, minimizes operational mistakes,
and supports future expansion (n8n, AI agents, etc.).
