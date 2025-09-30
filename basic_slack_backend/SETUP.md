# Setup Guide for Essential Cardano AI Slack Bridge

This guide covers the steps needed to set up and deploy the Slack integration service while waiting for Google Cloud access.

## 1. Prerequisites

### Required Software
- Python 3.11+
- [uv package manager](https://docs.astral.sh/uv/getting-started/installation/)
- Docker (for containerization)
- Google Cloud SDK (for deployment)

### Required Accounts & Services
- Slack workspace with admin permissions
- Google Cloud Project access (pending request)
- Genexus/SAIA API access (from Globant platform)

## 2. Local Development Setup

### Step 1: Accept Xcode License (macOS only)
```bash
sudo xcodebuild -license
```

### Step 2: Install Dependencies
```bash
make install
```

### Step 3: Configure Environment Variables
```bash
# Copy template and edit with your values
cp .env.template .env
# Edit .env with your actual tokens and API keys
```

Required environment variables:
- `SLACK_BOT_TOKEN` - Bot User OAuth Token from Slack app
- `GENEXUS_API_KEY` - API key from Globant SAIA platform

### Step 4: Test Local Development
```bash
# Run with hot reload on port 8000
make run-local

# Or run with environment file on port 8080
make run-env
```

## 3. Slack App Configuration

### Create Slack App
1. Go to [api.slack.com/apps](https://api.slack.com/apps)
2. Click "Create New App" → "From an app manifest"
3. Use this manifest:

```yaml
display_information:
  name: Essential Cardano AI Assistant
  description: AI assistant for Cardano ecosystem questions
  background_color: "#004c9b"
features:
  bot_user:
    display_name: Essential Cardano AI
    always_online: true
  slash_commands:
    - command: /search
      url: https://your-service-url/slack/commands
      description: Search Cardano knowledge base
      usage_hint: your question here
    - command: /help
      url: https://your-service-url/slack/commands
      description: Get help using the bot
oauth_config:
  scopes:
    bot:
      - app_mentions:read
      - chat:write
      - im:history
      - im:read
      - im:write
      - users:read
event_subscriptions:
  request_url: https://your-service-url/slack/events
  bot_events:
    - app_mention
    - message.im
settings:
  interactivity:
    is_enabled: true
    request_url: https://your-service-url/slack/interactions
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

### Get Tokens
1. Install app to workspace
2. Copy "Bot User OAuth Token" from OAuth & Permissions
3. Add to your `.env` file

## 4. Testing Strategy

### Local Testing
```bash
# Test Docker build locally
make test-docker

# Test health endpoint
curl http://localhost:8080/health
```

### API Testing
Test the Genexus API integration:
```bash
curl -X POST "http://localhost:8080/slack/commands" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "command=/search&text=what is Cardano&user_id=test&channel_id=test"
```

### Slack Integration Testing
1. Send DM to bot
2. Mention bot in channel: `@bot what is Cardano?`
3. Use slash command: `/search what is Cardano?`

## 5. Deployment Preparation

### Update Makefile Variables
Edit the top of `Makefile` with correct values:
```makefile
PROJECT_ID ?= your-actual-gcp-project-id
SERVICE_ACCOUNT ?= your-service-account@project.iam.gserviceaccount.com
```

### Create Deployment Environment File
```bash
cp .env.yaml.template .env.yaml
# Edit .env.yaml with production values
```

### When Google Cloud Access is Ready
```bash
# One-time setup
make setup

# Deploy to Cloud Run
make deploy
```

## 6. Troubleshooting

### Common Issues
- **Xcode license**: Run `sudo xcodebuild -license`
- **uv not found**: Install with `curl -LsSf https://astral.sh/uv/install.sh | sh`
- **Docker build fails**: Ensure Docker is running
- **Slack verification fails**: Check request URL matches deployed service

### Logs and Monitoring
- Local logs: stdout from `make run-local`
- Production logs: `gcloud logs read --service=cardano-ai-slack-bridge`
- Health check: `curl https://your-service-url/health`

## 7. Next Steps While Waiting for GCP Access

1. ✅ Set up local development environment
2. ✅ Configure Slack app in test workspace
3. ✅ Test API integration locally
4. ⏳ Get Google Cloud project access
5. ⏳ Deploy to Cloud Run
6. ⏳ Update Slack app URLs to production
7. ⏳ Test with IOG Education team

## Security Notes

- Never commit `.env` or `.env.yaml` files
- Rotate tokens if compromised
- Use least-privilege IAM roles
- Monitor logs for unusual activity