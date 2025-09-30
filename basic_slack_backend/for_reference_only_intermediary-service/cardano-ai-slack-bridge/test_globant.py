"""
Test script to validate Globant API connection
Run this to verify your API configuration before deploying
"""

import os
import asyncio
import httpx
import uuid
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

async def test_globant_api():
    """Test the Globant API connection"""

    # Get configuration
    api_url = os.getenv("GLOBANT_API_URL")
    api_token = os.getenv("GLOBANT_API_TOKEN")
    assistant_name = os.getenv("GLOBANT_ASSISTANT_NAME")

    print("🔍 Testing Globant API Configuration...")
    print(f"API URL: {api_url}")
    print(f"API Token: {'✅ Set' if api_token else '❌ Missing'}")
    print(f"Assistant Name: {assistant_name}")
    print()

    if not all([api_url, api_token, assistant_name]):
        print("❌ Missing required configuration. Please check your .env file.")
        return False

    # Test API call
    try:
        headers = {
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        }

        payload = {
            "role": "user",
            "content": "Hello! This is a test message to verify the API connection. What is Cardano?",
            "requestId": str(uuid.uuid4()),
            "application": "saia-chat"
        }

        print("📡 Making test API call...")

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                api_url,
                headers=headers,
                json=payload
            )

            print(f"Status Code: {response.status_code}")

            if response.status_code == 200:
                print("✅ API call successful!")
                try:
                    result = response.json()
                    print(f"JSON Response preview: {str(result)[:200]}...")
                except:
                    # Handle streaming or multi-line responses
                    text_response = response.text
                    print(f"Text Response preview: {text_response[:200]}...")
                return True
            else:
                print("❌ API call failed!")
                print(f"Error: {response.text}")
                return False

    except httpx.TimeoutException:
        print("❌ Request timed out!")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(test_globant_api())