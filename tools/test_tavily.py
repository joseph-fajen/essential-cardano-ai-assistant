#!/usr/bin/env python3
"""
Test Tavily Extract API for Essential Cardano content extraction
"""

import os
import json
import time
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Check if tavily-python is installed, if not provide instructions
try:
    from tavily import TavilyClient
except ImportError:
    print("❌ Tavily Python library not installed")
    print("📦 Install with: pip install tavily-python")
    print("🔗 Get API key from: https://app.tavily.com/")
    exit(1)

def test_tavily_extraction():
    """Test Tavily Extract API with Essential Cardano URLs"""

    # Get API key from environment or prompt
    api_key = os.getenv("TAVILY_API_KEY")
    if not api_key:
        print("❌ TAVILY_API_KEY environment variable not set")
        print("🔑 Get your API key from https://app.tavily.com/")
        print("📝 Set it with: export TAVILY_API_KEY='your_api_key_here'")
        return False

    print(f"🔑 API Key found: {api_key[:10]}...")

    # Test URLs from Essential Cardano
    test_urls = [
        "https://www.essentialcardano.io/faq",
        "https://www.essentialcardano.io/glossary",
        "https://www.essentialcardano.io/article",
        "https://www.essentialcardano.io/development-update"
    ]

    print(f"🧪 Testing Tavily Extract API with {len(test_urls)} URLs")

    try:
        # Initialize Tavily client
        tavily_client = TavilyClient(api_key=api_key)

        # Test basic extraction first
        print("\n📄 Testing Basic Extraction...")
        start_time = time.time()

        basic_response = tavily_client.extract(
            urls=test_urls,
            include_images=False
        )

        basic_time = time.time() - start_time

        print(f"⏱️  Basic extraction completed in {basic_time:.2f} seconds")
        print(f"📊 Results: {len(basic_response.get('results', []))} successful extractions")

        # Analyze results
        successful_extractions = 0
        failed_extractions = 0
        total_content_length = 0

        for result in basic_response.get('results', []):
            if result.get('content'):
                successful_extractions += 1
                content_length = len(result.get('content', ''))
                total_content_length += content_length

                print(f"✅ {result.get('url', 'Unknown URL')}")
                print(f"   Title: {result.get('title', 'No title')[:50]}...")
                print(f"   Content: {content_length} characters")
                print(f"   Raw URL: {result.get('raw_url', 'Not provided')}")
            else:
                failed_extractions += 1
                print(f"❌ Failed: {result.get('url', 'Unknown URL')}")

        print(f"\n📈 BASIC EXTRACTION SUMMARY:")
        print(f"   ✅ Successful: {successful_extractions}")
        print(f"   ❌ Failed: {failed_extractions}")
        print(f"   📝 Total content: {total_content_length} characters")
        print(f"   ⏱️  Time: {basic_time:.2f} seconds")
        print(f"   🚀 Rate: {len(test_urls)/basic_time:.2f} URLs/second")

        # Test advanced extraction with fewer URLs
        print("\n📄 Testing Advanced Extraction...")
        start_time = time.time()

        advanced_response = tavily_client.extract(
            urls=test_urls[:2],  # Test with fewer URLs for advanced
            include_images=True,
            extract_depth="advanced"
        )

        advanced_time = time.time() - start_time

        print(f"⏱️  Advanced extraction completed in {advanced_time:.2f} seconds")

        # Compare content quality
        for i, result in enumerate(advanced_response.get('results', [])):
            if result.get('content'):
                advanced_length = len(result.get('content', ''))
                basic_length = len(basic_response.get('results', [{}])[i].get('content', ''))

                print(f"📊 URL {i+1}: Advanced={advanced_length} chars vs Basic={basic_length} chars")

        # Save sample results for analysis
        output_dir = Path("tavily_test_results")
        output_dir.mkdir(exist_ok=True)

        # Save basic results
        with open(output_dir / "tavily_basic_test.json", 'w', encoding='utf-8') as f:
            json.dump({
                'test_timestamp': datetime.now().isoformat(),
                'test_urls': test_urls,
                'extraction_time': basic_time,
                'api_response': basic_response
            }, f, indent=2, ensure_ascii=False)

        # Save advanced results
        with open(output_dir / "tavily_advanced_test.json", 'w', encoding='utf-8') as f:
            json.dump({
                'test_timestamp': datetime.now().isoformat(),
                'test_urls': test_urls[:2],
                'extraction_time': advanced_time,
                'api_response': advanced_response
            }, f, indent=2, ensure_ascii=False)

        print(f"\n💾 Test results saved to: {output_dir}")

        # URL preservation analysis
        print(f"\n🔗 URL PRESERVATION ANALYSIS:")
        for result in basic_response.get('results', []):
            original_url = result.get('url', '')
            raw_url = result.get('raw_url', '')

            if original_url and raw_url:
                if original_url == raw_url:
                    print(f"✅ URL preserved: {original_url}")
                else:
                    print(f"⚠️  URL changed: {original_url} → {raw_url}")
            else:
                print(f"❓ URL info incomplete for: {original_url}")

        # Performance vs Firecrawl comparison
        urls_per_second = len(test_urls) / basic_time
        estimated_time_998_urls = 998 / urls_per_second / 60  # minutes

        print(f"\n🏆 PERFORMANCE PROJECTION:")
        print(f"   🚀 Current rate: {urls_per_second:.2f} URLs/second")
        print(f"   ⏱️  Estimated time for 998 URLs: {estimated_time_998_urls:.1f} minutes")
        print(f"   💰 Estimated cost for 998 URLs (basic): ${(998/5) * 0.0016:.2f}")
        print(f"   💰 Estimated cost for 998 URLs (advanced): ${(998/5) * 0.0032:.2f}")

        if successful_extractions > 0:
            print(f"\n✅ TAVILY TEST PASSED!")
            print(f"   Ready for bulk extraction with significant advantages over Firecrawl")
            return True
        else:
            print(f"\n❌ TAVILY TEST FAILED!")
            print(f"   No successful extractions")
            return False

    except Exception as e:
        print(f"❌ Tavily test failed with error: {e}")
        return False

def compare_with_firecrawl():
    """Print comparison summary"""
    print(f"\n📊 TAVILY vs FIRECRAWL COMPARISON:")
    print(f"{'Metric':<20} {'Tavily':<25} {'Firecrawl':<25}")
    print(f"{'-'*70}")
    print(f"{'Cost (1000 URLs)':<20} {'~$1.60-3.20':<25} {'~$10+':<25}")
    print(f"{'Batch Size':<20} {'Up to 20 URLs':<25} {'1 URL only':<25}")
    print(f"{'Rate Limiting':<20} {'Enterprise-ready':<25} {'Severe limits':<25}")
    print(f"{'Failed Billing':<20} {'No charge':<25} {'Full charge':<25}")
    print(f"{'Speed':<20} {'Bulk optimized':<25} {'Slow/timeouts':<25}")
    print(f"{'AI Optimization':<20} {'Built for RAG/LLM':<25} {'General scraping':<25}")

if __name__ == "__main__":
    print("🚀 Testing Tavily Extract API for Essential Cardano")
    print("="*50)

    success = test_tavily_extraction()

    compare_with_firecrawl()

    if success:
        print(f"\n🎯 RECOMMENDATION: Use Tavily for bulk extraction!")
        print(f"   - 10x more cost effective than Firecrawl")
        print(f"   - Built for AI/RAG workloads")
        print(f"   - No rate limiting issues")
        print(f"   - Batch processing up to 20 URLs")
    else:
        print(f"\n⚠️  Consider hybrid approach or troubleshooting Tavily setup")