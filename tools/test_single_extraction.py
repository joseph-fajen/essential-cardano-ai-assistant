#!/usr/bin/env python3
"""
Focused test: Extract content from a single URL and save to file
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def extract_and_save_single_url(url: str, output_file: str = None):
    """Extract content from a single URL and save to JSON file"""

    api_key = os.getenv("FIRECRAWL_API_KEY")
    if not api_key:
        print("❌ FIRECRAWL_API_KEY not found in environment")
        return False

    # Create output directory
    output_dir = Path("test_extractions")
    output_dir.mkdir(exist_ok=True)

    if not output_file:
        # Generate filename from URL
        filename = url.replace("https://", "").replace("http://", "")
        filename = filename.replace("/", "_").replace("?", "_").replace("&", "_")
        filename = f"{filename}.json"
        output_file = output_dir / filename

    print(f"🔍 Extracting content from: {url}")
    print(f"💾 Will save to: {output_file}")

    # Firecrawl API configuration
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    payload = {
        "url": url,
        "formats": ["markdown", "html"],
        "includeTags": ["title", "meta"],
        "onlyMainContent": True
    }

    try:
        # Make API request
        response = requests.post(
            "https://api.firecrawl.dev/v0/scrape",
            headers=headers,
            json=payload,
            timeout=30
        )

        print(f"📡 API Response Status: {response.status_code}")

        if response.status_code != 200:
            print(f"❌ HTTP Error: {response.text}")
            return False

        data = response.json()

        if not data.get("success"):
            print(f"❌ Extraction failed: {data.get('error', 'Unknown error')}")
            return False

        result = data.get("data", {})

        # Extract and organize the content
        extracted_content = {
            "extraction_info": {
                "url": url,
                "extracted_at": datetime.now().isoformat(),
                "api_used": "firecrawl",
                "status": "success"
            },
            "metadata": {
                "title": result.get("metadata", {}).get("title", ""),
                "description": result.get("metadata", {}).get("description", ""),
                "author": result.get("metadata", {}).get("author", ""),
                "keywords": result.get("metadata", {}).get("keywords", ""),
                "canonical_url": result.get("metadata", {}).get("canonical", url),
                "og_title": result.get("metadata", {}).get("ogTitle", ""),
                "og_description": result.get("metadata", {}).get("ogDescription", "")
            },
            "content": {
                "markdown": result.get("markdown", ""),
                "html": result.get("html", ""),
                "text_length": len(result.get("markdown", "")),
                "html_length": len(result.get("html", ""))
            },
            "links": result.get("links", []),
            "raw_response": result  # Include full response for debugging
        }

        # Save to JSON file
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(extracted_content, f, indent=2, ensure_ascii=False)

        # Print summary
        print(f"✅ Extraction Successful!")
        print(f"   📄 Title: {extracted_content['metadata']['title']}")
        print(f"   📝 Content Length: {extracted_content['content']['text_length']} characters")
        print(f"   🔗 Links Found: {len(extracted_content.get('links', []))}")
        print(f"   💾 Saved to: {output_file}")

        # Show first few lines of content
        content_preview = extracted_content['content']['markdown'][:300]
        print(f"   📖 Content Preview: {content_preview}...")

        return True

    except Exception as e:
        print(f"❌ Extraction Error: {e}")
        return False

def main():
    """Test extraction with the Cardano docs introduction page"""
    test_url = "https://docs.cardano.org/about-cardano/introduction"

    print("🧪 Single URL Extraction Test")
    print("=" * 50)

    success = extract_and_save_single_url(test_url)

    if success:
        print("\n🎉 Test completed successfully!")
        print("Check the 'test_extractions/' directory for the saved content.")
    else:
        print("\n❌ Test failed. Check the error messages above.")

if __name__ == "__main__":
    main()