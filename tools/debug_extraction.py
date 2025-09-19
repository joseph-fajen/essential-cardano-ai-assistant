#!/usr/bin/env python3
"""
Debug extraction with detailed logging
"""

import os
import json
import requests
import time
from dotenv import load_dotenv

load_dotenv()

def debug_single_extraction():
    """Test single URL extraction with full debugging"""
    api_key = os.getenv("FIRECRAWL_API_KEY")
    test_url = "https://www.essentialcardano.io/faq"

    print(f"🔍 Debug extraction for: {test_url}")
    print(f"🔑 API Key: {api_key[:10]}...")

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "url": test_url,
        "formats": ["markdown"],
        "onlyMainContent": True
    }

    try:
        print("📤 Sending request to Firecrawl API...")
        start_time = time.time()

        response = requests.post(
            "https://api.firecrawl.dev/v0/scrape",
            headers=headers,
            json=payload,
            timeout=120
        )

        elapsed = time.time() - start_time
        print(f"⏱️  Request completed in {elapsed:.1f} seconds")
        print(f"📊 Status Code: {response.status_code}")

        if response.status_code == 200:
            data = response.json()
            print(f"✅ Response received")
            print(f"🔄 Success: {data.get('success')}")

            if data.get("success"):
                result = data.get("data", {})
                title = result.get("metadata", {}).get("title", "No title")
                content_length = len(result.get("markdown", ""))

                print(f"📄 Title: {title}")
                print(f"📝 Content Length: {content_length} characters")

                # Show first 200 characters of content
                content_preview = result.get("markdown", "")[:200]
                print(f"📖 Content Preview: {content_preview}...")

                return True
            else:
                print(f"❌ API Error: {data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ HTTP Error: {response.status_code}")
            print(f"Response text: {response.text[:500]}")
            return False

    except requests.exceptions.Timeout:
        print("⏰ Request timed out (120 seconds)")
        return False
    except Exception as e:
        print(f"❌ Exception: {e}")
        return False

if __name__ == "__main__":
    debug_single_extraction()