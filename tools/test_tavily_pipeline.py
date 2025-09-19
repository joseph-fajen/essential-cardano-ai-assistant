#!/usr/bin/env python3
"""
Test Tavily comprehensive pipeline with a small subset
"""

import json
from pathlib import Path
from tavily_comprehensive_extractor import TavilyComprehensiveExtractor
import os
from dotenv import load_dotenv

load_dotenv()

def test_pipeline_with_small_subset():
    """Test the pipeline with a small subset of URLs"""

    # Create test URLs file with just a few high-value URLs
    test_urls = [
        {"url": "https://www.essentialcardano.io/faq", "content_type": "faq"},
        {"url": "https://www.essentialcardano.io/glossary", "content_type": "glossary"},
        {"url": "https://www.essentialcardano.io/article", "content_type": "article"},
        {"url": "https://www.essentialcardano.io/development-update", "content_type": "development_update"},
        {"url": "https://www.essentialcardano.io/developer", "content_type": "developer"},
        {"url": "https://www.essentialcardano.io/video", "content_type": "videos"},
        {"url": "https://www.essentialcardano.io/infographic", "content_type": "infographics"},
        {"url": "https://www.essentialcardano.io/other", "content_type": "other"}
    ]

    # Create test URLs file
    test_urls_file = Path("test_tavily_urls.json")
    test_data = {
        "extracted_at": "2025-09-19T00:00:00",
        "sitemap_url": "https://www.essentialcardano.io/sitemap.xml",
        "total_urls": len(test_urls),
        "urls": test_urls
    }

    with open(test_urls_file, 'w', encoding='utf-8') as f:
        json.dump(test_data, f, indent=2, ensure_ascii=False)

    print(f"✅ Created test URLs file with {len(test_urls)} URLs")

    # Initialize extractor
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("❌ TAVILY_API_KEY not found")
        return False

    extractor = TavilyComprehensiveExtractor(api_key)

    # Run extraction on test set
    print(f"🧪 Testing comprehensive pipeline...")
    extractor.run_comprehensive_extraction(str(test_urls_file))

    # Clean up test file
    test_urls_file.unlink()

    return True

if __name__ == "__main__":
    test_pipeline_with_small_subset()