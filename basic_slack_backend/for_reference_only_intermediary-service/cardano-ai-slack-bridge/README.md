# Cardano AI Slack Bridge

An intermediary service that connects Slack to the Globant Enterprise AI "Unified Essential Cardano AI Assistant".

## Architecture

```
Slack → This Service (Google Cloud Run) → Globant Enterprise AI → Back to Slack
```

## Features

- ✅ Direct messages to the bot
- ✅ @mentions in channels
- ✅ `/cardano` slash command
- ✅ Automatic Slack signature verification
- ✅ Error handling and logging

## Setup Instructions

### 1. Slack App Configuration

1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From scratch"
3. Name: "Cardano AI Assistant"
4. Select your workspace

#### Bot Token Scopes
Under "OAuth & Permissions" → "Scopes", add these Bot Token Scopes:
- `app_mentions:read`
- `chat:write`
- `im:read`
- `im:write`
- `channels:read`

#### Event Subscriptions
Under "Event Subscriptions":
1. Enable Events: **On**
2. Request URL: `https://your-service-url.run.app/slack/events`
3. Subscribe to bot events:
   - `app_mention`
   - `message.im`

#### Slash Commands
Under "Slash Commands":
1. Create command: `/cardano`
2. Request URL: `https://your-service-url.run.app/slack/commands`
3. Description: "Ask the Cardano AI Assistant a question"

### 2. Environment Variables

Copy `.env.example` to `.env` and fill in your values:

```bash
cp .env.example .env
```

**Slack Configuration:**
- `SLACK_BOT_TOKEN`: Found under "OAuth & Permissions" → "Bot User OAuth Token"
- `SLACK_SIGNING_SECRET`: Found under "Basic Information" → "Signing Secret"

**Globant Configuration:**
- `GLOBANT_API_URL`: Your Globant Enterprise AI endpoint
- `GLOBANT_API_TOKEN`: Your Globant API token
- `GLOBANT_ASSISTANT_ID`: Your assistant ID

### 3. Local Testing

Install dependencies:
```bash
pip install -r requirements.txt
```

Run locally:
```bash
python main.py
```

For local Slack testing, use ngrok to expose your local server:
```bash
# Install ngrok if you haven't
ngrok http 8080
```

Update your Slack app's Request URLs to use the ngrok URL.

### 4. Google Cloud Deployment

#### Prerequisites
- Google Cloud account with billing enabled
- `gcloud` CLI installed and authenticated
- Docker installed (for local builds)

#### Deploy to Cloud Run

1. Set your project:
```bash
gcloud config set project YOUR_PROJECT_ID
```

2. Enable required APIs:
```bash
gcloud services enable run.googleapis.com
gcloud services enable cloudbuild.googleapis.com
```

3. Deploy using Cloud Build:
```bash
gcloud builds submit --config cloudbuild.yaml
```

4. Set environment variables in Cloud Run:
```bash
gcloud run services update cardano-ai-slack-bridge \
  --region us-central1 \
  --set-env-vars SLACK_BOT_TOKEN="your-bot-token" \
  --set-env-vars SLACK_SIGNING_SECRET="your-signing-secret" \
  --set-env-vars GLOBANT_API_URL="your-globant-url" \
  --set-env-vars GLOBANT_API_TOKEN="your-globant-token" \
  --set-env-vars GLOBANT_ASSISTANT_ID="your-assistant-id"
```

5. Get your service URL:
```bash
gcloud run services describe cardano-ai-slack-bridge \
  --region us-central1 \
  --format 'value(status.url)'
```

6. Update your Slack app configuration with the new service URL.

#### Alternative: Manual Docker Deployment

Build and push:
```bash
# Tag and build
docker build -t gcr.io/YOUR_PROJECT_ID/cardano-ai-slack-bridge .

# Push to Container Registry
docker push gcr.io/YOUR_PROJECT_ID/cardano-ai-slack-bridge

# Deploy to Cloud Run
gcloud run deploy cardano-ai-slack-bridge \
  --image gcr.io/YOUR_PROJECT_ID/cardano-ai-slack-bridge \
  --region us-central1 \
  --platform managed \
  --allow-unauthenticated
```

## Testing

1. **Health Check**: `GET https://your-service-url/` should return `{"status": "healthy"}`
2. **Direct Message**: Send a DM to your bot in Slack
3. **Channel Mention**: @mention your bot in a channel
4. **Slash Command**: Use `/cardano What is Cardano?` in any channel

## Troubleshooting

### Common Issues

**"Invalid request signature"**
- Check your `SLACK_SIGNING_SECRET` is correct
- Ensure your service URL in Slack matches your deployed service

**"AI service not configured"**
- Verify all Globant environment variables are set correctly
- Check Globant API endpoint and token validity

**"Bot doesn't respond"**
- Check Cloud Run logs: `gcloud logs tail cardano-ai-slack-bridge`
- Verify bot token has correct scopes
- Ensure Event Subscriptions are properly configured

### Logs

View service logs:
```bash
gcloud logs tail cardano-ai-slack-bridge --format='value(textPayload)'
```

## Security Notes

- All Slack requests are verified using signature verification
- Environment variables should never be committed to version control
- Use Google Secret Manager for production deployments
- Bot token should have minimal required scopes

## Next Steps

1. Set up monitoring and alerting
2. Implement rate limiting
3. Add conversation context/memory
4. Create user feedback mechanism
5. Add analytics and usage tracking