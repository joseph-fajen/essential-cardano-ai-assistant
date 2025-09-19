#!/usr/bin/env python3
"""
Test small-scale extraction to verify pipeline before full run
"""

import os
import json
from comprehensive_extractor import ComprehensiveExtractor
from dotenv import load_dotenv

load_dotenv()

def test_small_extraction():
    """Test extraction with just a few URLs"""
    api_key = os.getenv("FIRECRAWL_API_KEY")

    if not api_key:
        print("❌ API key not found")
        return

    # Create test URLs
    test_urls = [
        {
            "url": "https://www.essentialcardano.io/faq",
            "content_type": "faq"
        },
        {
            "url": "https://www.essentialcardano.io/glossary",
            "content_type": "glossary"
        },
        {
            "url": "https://www.essentialcardano.io/article",
            "content_type": "article"
        }
    ]

    print(f"🧪 Testing extraction with {len(test_urls)} URLs")

    extractor = ComprehensiveExtractor(api_key)

    # Process test URLs
    successful = 0
    for i, url_info in enumerate(test_urls):
        print(f"\n📄 Processing {i+1}/{len(test_urls)}: {url_info['url']}")

        content = extractor.extract_content(url_info['url'], url_info['content_type'])

        if content and content.firecrawl_success:
            if extractor.save_content(content):
                successful += 1
                print(f"✅ Success: {content.title[:50]}...")
            else:
                print(f"❌ Failed to save content")
        else:
            error = content.error_message if content else "Unknown error"
            print(f"❌ Extraction failed: {error}")

    print(f"\n🎯 Test Results: {successful}/{len(test_urls)} successful")

    if successful > 0:
        print("✅ Pipeline working! Ready for full extraction.")
        return True
    else:
        print("❌ Pipeline issues detected. Check errors above.")
        return False

if __name__ == "__main__":
    test_small_extraction()