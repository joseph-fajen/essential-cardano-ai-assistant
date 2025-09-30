import os
import logging
import asyncio
from typing import Dict, Any, Optional, List
from urllib.parse import parse_qs
from contextlib import asynccontextmanager
import json
import requests
from concurrent.futures import ThreadPoolExecutor

from fastapi import FastAPI, Request, BackgroundTasks
from slack_sdk.web.async_client import AsyncWebClient
from slack_sdk.errors import SlackApiError
import uvicorn

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Environment variables - loaded once at module level
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
GENEXUS_API_KEY = os.getenv("GENEXUS_API_KEY")
MODEL_NAME = os.getenv("LLM_NAME", "saia:llama-3.1-8b-instruct")  # Provide default
PORT = int(os.getenv("PORT", 8080))

# Global instances
slack_client: Optional[AsyncWebClient] = None
BOT_USER_ID: Optional[str] = None
executor = ThreadPoolExecutor(max_workers=5)  # For running sync requests in async context


def genexus_rag_request(api_key: str, claim: str, model_name: str = None):
    """
    Internal helper for Genexus RAG calls.
    """
    model_name = model_name or MODEL_NAME  # Use default if not provided
    base_url = "https://workspace.saia.ai/api/chat/ece1d2ab-981e-4c24-b628-fec5757fe77e/b240017b-defa-42c4-8430-c364fadd77e3/67b580da-9f22-428e-b81f-5ac63452bad7"
    body = {
        "role": "user",
        "content": claim,
        "requestId": f"slack-{hash(claim) % 10000}",
        "application": "saia-chat"
    }
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.post(base_url, headers=headers, json=body)
        logger.info(f"Response status code: {response.status_code}")
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Request error: {e}")
        return f"Error making request: {e}"

    try:
        # Handle streaming JSON response with URL-encoded content
        import urllib.parse

        content_chunks = []
        files_info = []

        for line in response.text.strip().split('\n'):
            if line.strip():
                try:
                    chunk = json.loads(line)
                    if 'content' in chunk:
                        # URL decode the content
                        decoded_content = urllib.parse.unquote(chunk['content'])
                        content_chunks.append(decoded_content)
                    elif 'files' in chunk:
                        files_info = chunk.get('files', [])
                except json.JSONDecodeError:
                    continue

        # Combine all content chunks
        full_content = ''.join(content_chunks)

        # Create response in expected format
        data = {
            "content": full_content,
            "files": files_info
        }

    except Exception as e:
        logger.error(f"Response parsing error: {e}")
        logger.error(f"Full response content: {response.text[:200]}...")
        return f"Error parsing response: {str(e)}"

    # Return formatted result with content and sources
    result = {
        "question": claim,
        "content": data.get("content", ""),
        "files": data.get("files", []),
        "meta": {"query": claim}
    }

    return result


async def async_genexus_rag_request(api_key: str, claim: str, model_name: str = None):
    """
    Async wrapper for the Genexus RAG request.
    """
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(executor, genexus_rag_request, api_key, claim, model_name)


def format_rag_results(results: Any, query: str) -> str:
    """
    Format RAG results into a readable Slack message.
    """
    if isinstance(results, str):
        # Error message
        return f"❌ {results}"

    if not results:
        return f"No results found for: _{query}_"

    # Handle new response format
    if isinstance(results, dict) and 'content' in results:
        content = results.get('content', '')
        files = results.get('files', [])

        # Format the main content
        formatted_message = f"*Results for:* _{query}_\n\n"

        # Add the main content (truncate if too long)
        if len(content) > 2000:
            content = content[:1997] + "..."
        formatted_message += content

        # Add source files if available
        if files:
            formatted_message += "\n\n*📚 Sources:*\n"
            for i, file_info in enumerate(files[:3], 1):  # Limit to 3 sources
                caption = file_info.get('caption', f'Source {i}')
                formatted_message += f"• {caption}\n"

        return formatted_message

    # Legacy format (fallback)
    formatted_message = f"*Results for:* _{query}_\n\n"

    for i, result in enumerate(results[:5], 1):  # Limit to top 5 results
        formatted_message += f"*Result {i}:*\n"

        if result.get("title"):
            formatted_message += f"📌 *{result['title']}*\n"

        if result.get("description"):
            # Truncate long descriptions
            description = result["description"]
            if len(description) > 500:
                description = description[:497] + "..."
            formatted_message += f"{description}\n"

        if result.get("url"):
            formatted_message += f"🔗 <{result['url']}|Source>\n"

        formatted_message += "\n"

    return formatted_message


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management."""
    global slack_client, BOT_USER_ID
    
    logger.info("🚀 Starting Slack Bot...")
    
    # Check required environment variables
    if not SLACK_BOT_TOKEN:
        logger.error("❌ SLACK_BOT_TOKEN not found in environment variables")
    
    if not GENEXUS_API_KEY:
        logger.warning("⚠️ GENEXUS_API_KEY not found in environment variables")
    else:
        logger.info("✅ Genexus API key loaded")
    
    try:
        if SLACK_BOT_TOKEN:
            # Initialize Slack client
            slack_client = AsyncWebClient(token=SLACK_BOT_TOKEN)
            
            # Get bot user ID
            auth_response = await slack_client.auth_test()
            BOT_USER_ID = auth_response["user_id"]
            logger.info(f"Bot initialized with user ID: {BOT_USER_ID}")
        
    except Exception as e:
        logger.error(f"❌ Slack initialization failed: {e}")
        # Continue anyway for health checks
    
    yield
    
    # Cleanup
    executor.shutdown(wait=True)
    logger.info("👋 Slack bot shutdown complete")


# Create FastAPI app
app = FastAPI(
    title="My Bot",
    description="Generic bot for testing",
    version="1.0.0",
    lifespan=lifespan
)


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "message": "🤖 Your Bot is up and running!",
        "version": "1.0.0",
        "status": "healthy",
        "bot_id": BOT_USER_ID
    }


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "services": {
            "slack": bool(slack_client and BOT_USER_ID),
            "genexus_api": bool(GENEXUS_API_KEY)
        }
    }


def create_feedback_blocks(message_id: str) -> List[Dict[str, Any]]:
    """Create feedback button blocks for a message."""
    return [
        {
            "type": "actions",
            "block_id": f"feedback_{message_id}",
            "elements": [
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "button 1",
                        "emoji": True
                    },
                    "style": "primary",
                    "action_id": "feedback_positive",
                    "value": message_id
                },
                {
                    "type": "button",
                    "text": {
                        "type": "plain_text",
                        "text": "button 2",
                        "emoji": True
                    },
                    "action_id": "feedback_negative",
                    "value": message_id
                }
            ]
        }
    ]


async def send_message(
    channel: str, 
    text: str, 
    thread_ts: Optional[str] = None,
    blocks: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """Send a message to Slack."""
    if not slack_client:
        logger.error("Slack client not initialized")
        return {}
    
    try:
        kwargs = {
            "channel": channel,
            "text": text,
        }
        
        if thread_ts:
            kwargs["thread_ts"] = thread_ts
            
        if blocks:
            kwargs["blocks"] = blocks
            
        response = await slack_client.chat_postMessage(**kwargs)
        return response.data
    except SlackApiError as e:
        logger.error(f"Error sending message: {e}")
        return {}


async def send_message_with_feedback(
    channel: str,
    text: str,
    message_id: str,
    thread_ts: Optional[str] = None
) -> Dict[str, Any]:
    """Send a message with feedback buttons."""
    # Create blocks with the message text and feedback buttons
    blocks = [
        {
            "type": "section",
            "text": {
                "type": "mrkdwn",
                "text": text
            }
        }
    ] + create_feedback_blocks(message_id)
    
    return await send_message(channel, text, thread_ts, blocks)


async def handle_feedback(
    user_id: str,
    channel_id: str,
    message_id: str,
    feedback_type: str,
    response_url: Optional[str] = None
):
    """Handle feedback from users."""
    # Log feedback to stdout for now
    feedback_data = {
        "timestamp": asyncio.get_event_loop().time(),
        "user_id": user_id,
        "channel_id": channel_id,
        "message_id": message_id,
        "feedback_type": feedback_type
    }
    
    # Print to stdout as requested
    print(f"FEEDBACK RECEIVED: {json.dumps(feedback_data, indent=2)}")
    logger.info(f"Feedback received: {feedback_data}")
    
    # Send acknowledgment to user (ephemeral message) - only if we have a real Slack client
    if slack_client and response_url:
        emoji = "✅" if feedback_type == "positive" else "📝"
        message = f"{emoji} Thank you for your feedback!"
        
        try:
            # Try to send ephemeral message, but don't fail if channel doesn't exist (testing scenario)
            await slack_client.chat_postEphemeral(
                channel=channel_id,
                user=user_id,
                text=message
            )
        except SlackApiError as e:
            # Only log as warning if it's a channel_not_found error (common in testing)
            if e.response.get("error") == "channel_not_found":
                logger.debug(f"Channel not found (likely a test): {channel_id}")
            else:
                logger.warning(f"Could not send feedback acknowledgment: {e}")
        except Exception as e:
            logger.debug(f"Error sending feedback acknowledgment (non-critical): {e}")


async def process_user_request(
    user_id: str,
    channel: str,
    query: str,
    thread_ts: Optional[str] = None,
    interaction_type: str = "message"
):
    """Process a user's request using Genexus RAG API."""
    try:
        # Check API key
        if not GENEXUS_API_KEY:
            await send_message(
                channel,
                f"⚠️ <@{user_id}> API key not configured. Please contact the administrator.",
                thread_ts
            )
            return
        
        # Send initial acknowledgment (no feedback buttons for this)
        emoji_map = {"dm": "💬", "mention": "👋", "command": "🔍"}
        emoji = emoji_map.get(interaction_type, "🤖")
        
        await send_message(
            channel,
            f"{emoji} <@{user_id}> I'm working on answering your request: _{query}_\n⏳ This may take a moment...",
            thread_ts
        )
        
        # Make the RAG request
        results = await async_genexus_rag_request(GENEXUS_API_KEY, query, MODEL_NAME)
        
        # Format the results
        formatted_response = format_rag_results(results, query)
        
        # Generate unique message ID for tracking feedback
        message_id = f"{user_id}_{channel}_{int(asyncio.get_event_loop().time() * 1000)}"
        
        # Check message length and split if needed
        max_length = 3900  # Slack's limit is 4000
        
        if len(formatted_response) <= max_length:
            # Send single message with feedback buttons
            await send_message_with_feedback(
                channel,
                formatted_response,
                message_id,
                thread_ts
            )
        else:
            # Split into chunks at newline boundaries
            lines = formatted_response.split('\n')
            chunks = []
            current_chunk = []
            current_length = 0
            
            for line in lines:
                line_length = len(line) + 1
                
                if current_length + line_length > max_length:
                    if current_chunk:
                        chunks.append('\n'.join(current_chunk))
                    
                    if line_length > max_length:
                        while len(line) > max_length:
                            chunks.append(line[:max_length])
                            line = line[max_length:]
                        current_chunk = [line] if line else []
                        current_length = len(line) + 1 if line else 0
                    else:
                        current_chunk = [line]
                        current_length = line_length
                else:
                    current_chunk.append(line)
                    current_length += line_length
            
            if current_chunk:
                chunks.append('\n'.join(current_chunk))
            
            # Send chunks - only last one gets feedback buttons
            for i, chunk in enumerate(chunks):
                is_last = (i == len(chunks) - 1)
                
                if is_last:
                    # Last chunk gets feedback buttons
                    await send_message_with_feedback(
                        channel,
                        f"📄 Part {i+1}/{len(chunks)}:\n{chunk}",
                        message_id,
                        thread_ts
                    )
                else:
                    # Other chunks are sent normally
                    await send_message(
                        channel,
                        f"📄 Part {i+1}/{len(chunks)}:\n{chunk}",
                        thread_ts
                    )
                await asyncio.sleep(0.5)  # Avoid rate limits
            
    except Exception as e:
        logger.error(f"Error processing query: {e}", exc_info=True)
        # Error message - no feedback buttons needed
        await send_message(
            channel,
            f"❌ <@{user_id}> An error occurred: {str(e)}",
            thread_ts
        )


@app.post("/slack/interactions")
async def slack_interactions(request: Request, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Handle interactive components (buttons, select menus, etc.)."""
    try:
        # Parse the payload
        body = await request.body()
        parsed_data = parse_qs(body.decode('utf-8'))
        payload_str = parsed_data.get('payload', [''])[0]
        
        if not payload_str:
            return {"status": "ok"}
            
        payload = json.loads(payload_str)
        
        # Handle button interactions
        if payload.get("type") == "block_actions":
            user = payload.get("user", {})
            user_id = user.get("id")
            channel = payload.get("channel", {})
            channel_id = channel.get("id")
            
            # Process each action
            for action in payload.get("actions", []):
                action_id = action.get("action_id")
                message_id = action.get("value")
                
                if action_id == "feedback_positive":
                    background_tasks.add_task(
                        handle_feedback,
                        user_id,
                        channel_id,
                        message_id,
                        "positive",
                        payload.get("response_url")
                    )
                elif action_id == "feedback_negative":
                    background_tasks.add_task(
                        handle_feedback,
                        user_id,
                        channel_id,
                        message_id,
                        "negative",
                        payload.get("response_url")
                    )
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error handling interaction: {e}", exc_info=True)
        return {"status": "ok"}


@app.post("/slack/events")
async def slack_events(request: Request, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Handle Slack Events API (direct messages and mentions)."""
    try:
        # Parse JSON
        data = await request.json()
        
        # Handle URL verification
        if data.get("type") == "url_verification":
            return {"challenge": data.get("challenge")}
        
        # Handle event callbacks
        if data.get("type") == "event_callback":
            event = data.get("event", {})
            event_type = event.get("type")
            
            # Skip bot's own messages
            if event.get("user") == BOT_USER_ID:
                return {"status": "ok"}
            
            # Handle direct messages
            if event_type == "message" and event.get("channel_type") == "im":
                user = event.get("user")
                channel = event.get("channel")
                text = event.get("text", "")
                
                if user and text:
                    logger.info(f"DM from {user}: {text}")
                    background_tasks.add_task(
                        process_user_request,
                        user,
                        channel,
                        text,
                        None,
                        "dm"
                    )
            
            # Handle app mentions
            elif event_type == "app_mention":
                user = event.get("user")
                channel = event.get("channel")
                text = event.get("text", "")
                thread_ts = event.get("thread_ts")
                
                if user and text:
                    # Remove bot mention from text
                    query = text.replace(f"<@{BOT_USER_ID}>", "").strip()
                    logger.info(f"Mention from {user}: {query}")
                    
                    background_tasks.add_task(
                        process_user_request,
                        user,
                        channel,
                        query,
                        thread_ts,
                        "mention"
                    )
        
        return {"status": "ok"}
        
    except Exception as e:
        logger.error(f"Error handling event: {e}", exc_info=True)
        return {"status": "ok"}


@app.post("/slack/commands")
async def slack_commands(request: Request, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Handle slash commands like /search."""
    try:
        # Parse form data
        body = await request.body()
        parsed_data = parse_qs(body.decode('utf-8'))
        
        # Convert to flat dict
        data = {key: values[0] for key, values in parsed_data.items()}
        
        command = data.get("command", "")
        text = data.get("text", "")
        user_id = data.get("user_id", "")
        channel_id = data.get("channel_id", "")
        
        logger.info(f"Command {command} from {user_id}: {text}")
        
        if command == "/search":
            if not text:
                return {
                    "response_type": "ephemeral",
                    "text": "📝 Please provide a query. Example: `/search <your question here>`"
                }
            
            # Process in background
            background_tasks.add_task(
                process_user_request,
                user_id,
                channel_id,
                text,
                None,
                "command"
            )
            
            # Immediate response
            return {
                "response_type": "ephemeral",
                "text": f"🔍 Working on answering your question: _{text}_\n⏳ I'll post the results shortly..."
            }
        
        elif command == "/help":
            return {
                "response_type": "ephemeral",
                "text": """*Bot Help*

*Available commands:*
• `/search <query>` - Answer questions absed on documents in our DB
• `/help` - Show this help message

*Other ways to interact:*
• Send me a direct message
• Mention me in a channel: @bot <your question>

*Examples:*
• `/search who is Joe Doe`
• `@bot explain neural networks`
• DM: `What is Leios?`"""
            }
        
        return {
            "response_type": "ephemeral",
            "text": f"Unknown command: {command}"
        }
        
    except Exception as e:
        logger.error(f"Error handling command: {e}", exc_info=True)
        return {
            "response_type": "ephemeral",
            "text": "❌ An error occurred processing your command."
        }


if __name__ == "__main__":
    logger.info(f"Starting server on port {PORT}")
    uvicorn.run(app, host="0.0.0.0", port=PORT)