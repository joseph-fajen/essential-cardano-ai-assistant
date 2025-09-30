"""
Cardano AI Slack Bridge Service
Intermediary service connecting Slack to Globant Enterprise AI
"""

import os
import logging
from typing import Dict, Any
import httpx
from fastapi import FastAPI, Request, HTTPException
from slack_sdk import WebClient
from slack_sdk.signature import SignatureVerifier
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(title="Cardano AI Slack Bridge", version="1.0.0")

# Environment variables
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_SIGNING_SECRET = os.getenv("SLACK_SIGNING_SECRET")
GLOBANT_API_URL = os.getenv("GLOBANT_API_URL")
GLOBANT_API_TOKEN = os.getenv("GLOBANT_API_TOKEN")
GLOBANT_ASSISTANT_NAME = os.getenv("GLOBANT_ASSISTANT_NAME")

# Initialize Slack client
slack_client = WebClient(token=SLACK_BOT_TOKEN) if SLACK_BOT_TOKEN else None
signature_verifier = SignatureVerifier(SLACK_SIGNING_SECRET) if SLACK_SIGNING_SECRET else None

# Health check endpoint
@app.get("/")
async def health_check():
    return {"status": "healthy", "service": "cardano-ai-slack-bridge"}

# Slack event endpoint
@app.post("/slack/events")
async def slack_events(request: Request):
    """Handle Slack events (messages, mentions, etc.)"""
    try:
        # Get request body
        body = await request.body()

        # Verify Slack signature
        if signature_verifier:
            if not signature_verifier.is_valid_request(body, request.headers):
                raise HTTPException(status_code=403, detail="Invalid request signature")

        # Parse JSON
        event_data = json.loads(body)

        # Handle URL verification challenge
        if event_data.get("type") == "url_verification":
            return {"challenge": event_data.get("challenge")}

        # Handle events
        if event_data.get("type") == "event_callback":
            event = event_data.get("event", {})
            await handle_slack_event(event)

        return {"status": "ok"}

    except Exception as e:
        logger.error(f"Error processing Slack event: {e}")
        raise HTTPException(status_code=500, detail="Internal server error")

# Slack slash command endpoint
@app.post("/slack/commands")
async def slack_commands(request: Request):
    """Handle Slack slash commands like /cardano"""
    try:
        # Get form data from slash command
        form_data = await request.form()

        # Verify Slack signature
        body = await request.body()
        if signature_verifier:
            if not signature_verifier.is_valid_request(body, request.headers):
                raise HTTPException(status_code=403, detail="Invalid request signature")

        # Extract command data
        command = form_data.get("command")
        text = form_data.get("text", "")
        user_id = form_data.get("user_id")
        channel_id = form_data.get("channel_id")

        logger.info(f"Received command: {command} from user {user_id}")

        # Process the command
        if command == "/cardano":
            response_text = await query_globant_ai(text or "Hello! How can I help you with Cardano?")

            # Send response back to Slack
            if slack_client:
                await slack_client.chat_postMessage(
                    channel=channel_id,
                    text=response_text,
                    thread_ts=form_data.get("thread_ts")  # Reply in thread if applicable
                )

            return {"response_type": "ephemeral", "text": "Processing your question..."}

        return {"response_type": "ephemeral", "text": "Unknown command"}

    except Exception as e:
        logger.error(f"Error processing slash command: {e}")
        return {"response_type": "ephemeral", "text": "Sorry, there was an error processing your request."}

async def handle_slack_event(event: Dict[str, Any]):
    """Process individual Slack events"""
    event_type = event.get("type")

    # Handle direct messages and mentions
    if event_type == "message":
        # Skip bot messages and message changes
        if event.get("bot_id") or event.get("subtype"):
            return

        text = event.get("text", "")
        user = event.get("user")
        channel = event.get("channel")

        # Check if this is a direct message or mention
        is_dm = channel and channel.startswith("D")  # DM channels start with 'D'
        is_mention = "<@" in text  # Simple mention detection

        if is_dm or is_mention:
            logger.info(f"Processing message from user {user} in channel {channel}")

            # Clean up the message text (remove mentions)
            clean_text = text.replace(f"<@{slack_client.auth_test()['user_id']}>", "").strip() if slack_client else text

            # Query the AI
            response_text = await query_globant_ai(clean_text)

            # Send response back to Slack
            if slack_client:
                await slack_client.chat_postMessage(
                    channel=channel,
                    text=response_text,
                    thread_ts=event.get("ts")  # Reply in thread for channel mentions
                )

async def query_globant_ai(message: str) -> str:
    """Send query to Globant Enterprise AI and return response"""
    try:
        if not all([GLOBANT_API_URL, GLOBANT_API_TOKEN, GLOBANT_ASSISTANT_NAME]):
            logger.error("Missing Globant API configuration")
            return "Sorry, the AI service is not properly configured."

        # Prepare the request to Globant API
        headers = {
            "Authorization": f"Bearer {GLOBANT_API_TOKEN}",
            "Content-Type": "application/json"
        }

        # Use the correct Globant API format
        import uuid
        payload = {
            "role": "user",
            "content": message,
            "requestId": str(uuid.uuid4()),
            "application": "saia-chat"
        }

        # Make the API call
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                GLOBANT_API_URL,
                headers=headers,
                json=payload
            )

            if response.status_code == 200:
                # Handle streaming response from Globant API
                response_text = response.text

                # Parse streaming JSON responses and combine content
                ai_response = ""
                for line in response_text.strip().split('\n'):
                    if line.strip():
                        try:
                            chunk = json.loads(line)
                            content = chunk.get("content", "")
                            # URL decode the content
                            import urllib.parse
                            decoded_content = urllib.parse.unquote(content)
                            ai_response += decoded_content
                        except:
                            continue

                logger.info(f"Successfully got AI response: {len(ai_response)} characters")
                return ai_response if ai_response else "Sorry, I couldn't process the response properly."
            else:
                logger.error(f"Globant API error: {response.status_code} - {response.text}")
                return "Sorry, I'm having trouble connecting to the AI service right now."

    except httpx.TimeoutException:
        logger.error("Timeout calling Globant API")
        return "Sorry, the request timed out. Please try again."
    except Exception as e:
        logger.error(f"Error calling Globant API: {e}")
        return "Sorry, there was an error processing your request."

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)