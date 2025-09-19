#!/usr/bin/env python3
"""
Test script to verify Firecrawl API connection
"""

import os
import requests
import json
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def test_firecrawl_api():
    """Test basic Firecrawl API functionality"""
    api_key = os.getenv("FIRECRAWL_API_KEY")

    if not api_key:
        print("❌ FIRECRAWL_API_KEY environment variable not set")
        return False

    # Test with a simple Essential Cardano URL
    test_url = "https://www.essentialcardano.io/faq"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "url": test_url,
        "formats": ["markdown", "html"],
        "onlyMainContent": True
    }

    try:
        print(f"🧪 Testing Firecrawl API with: {test_url}")
        response = requests.post(
            "https://api.firecrawl.dev/v0/scrape",
            headers=headers,
            json=payload,
            timeout=60
        )

        print(f"Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            if data.get("success"):
                result = data.get("data", {})
                title = result.get("metadata", {}).get("title", "No title")
                content_length = len(result.get("markdown", ""))

                print(f"✅ API Test Successful!")
                print(f"   Title: {title}")
                print(f"   Content Length: {content_length} characters")
                print(f"   URL: {result.get('metadata', {}).get('canonical', test_url)}")
                return True
            else:
                print(f"❌ API returned success=false: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error {response.status_code}: {response.text}")
            return False

    except Exception as e:
        print(f"❌ API Test Failed: {e}")
        return False

if __name__ == "__main__":
    test_firecrawl_api()