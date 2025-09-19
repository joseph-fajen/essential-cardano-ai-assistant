#!/usr/bin/env python3
"""
Optimized Essential Cardano Content Extractor
Handles API rate limiting and timeouts properly for reliable extraction
"""

import os
import json
import time
import requests
from datetime import datetime
from typing import Dict, List, Optional
from dataclasses import dataclass
from pathlib import Path
from dotenv import load_dotenv
import random

# Load environment variables
load_dotenv()

@dataclass
class ExtractedContent:
    """Data structure for extracted content"""
    url: str
    title: str
    content: str
    html: str
    metadata: Dict
    extracted_at: str
    source_site: str
    content_category: str
    firecrawl_success: bool
    error_message: str = ""
    retry_count: int = 0

class OptimizedExtractor:
    """Optimized extractor with proper rate limiting and error handling"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.firecrawl.dev/v0"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Output directories
        self.output_dir = Path("comprehensive_extraction")
        self.content_dir = self.output_dir / "extracted_content"
        self.progress_dir = self.output_dir / "progress"

        # Create directories
        self.content_dir.mkdir(parents=True, exist_ok=True)
        self.progress_dir.mkdir(parents=True, exist_ok=True)

        # Progress tracking files
        self.progress_file = self.progress_dir / "extraction_progress.json"
        self.stats_file = self.progress_dir / "extraction_stats.json"

        # Optimized rate limiting for Firecrawl API
        self.base_delay = 5      # Base delay between requests (seconds)
        self.max_delay = 30      # Maximum delay for backoff
        self.timeout = 180       # Request timeout (3 minutes)
        self.max_retries = 3     # Maximum retry attempts

        # Statistics
        self.stats = {
            'total_urls': 0,
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'timeouts': 0,
            'rate_limited': 0,
            'started_at': None,
            'last_update': None
        }

    def load_urls(self, urls_file: str) -> List[Dict]:
        """Load URLs from sitemap parser output"""
        with open(urls_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data.get('urls', [])

    def load_progress(self) -> Dict:
        """Load previous extraction progress"""
        if not self.progress_file.exists():
            return {'completed_urls': set(), 'failed_urls': set()}

        with open(self.progress_file, 'r', encoding='utf-8') as f:
            progress = json.load(f)

        return {
            'completed_urls': set(progress.get('completed_urls', [])),
            'failed_urls': set(progress.get('failed_urls', []))
        }

    def save_progress(self, completed_urls: set, failed_urls: set):
        """Save extraction progress"""
        progress = {
            'completed_urls': list(completed_urls),
            'failed_urls': list(failed_urls),
            'last_saved': datetime.now().isoformat()
        }

        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

    def save_stats(self):
        """Save extraction statistics"""
        self.stats['last_update'] = datetime.now().isoformat()
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)

    def extract_content_with_retry(self, url: str, content_type: str) -> Optional[ExtractedContent]:
        """Extract content with retry logic and proper error handling"""

        for attempt in range(self.max_retries):
            try:
                # Calculate delay with exponential backoff
                if attempt > 0:
                    delay = min(self.base_delay * (2 ** attempt), self.max_delay)
                    jitter = random.uniform(0.5, 1.5)  # Add jitter to avoid thundering herd
                    delay *= jitter
                    print(f"🔄 Retry {attempt + 1}/{self.max_retries} for {url} (waiting {delay:.1f}s)")
                    time.sleep(delay)

                # Make the API request
                result = self._make_api_request(url, content_type)

                if result:
                    return result

            except Exception as e:
                error_msg = str(e)
                print(f"❌ Attempt {attempt + 1} failed for {url}: {error_msg}")

                if "timeout" in error_msg.lower():
                    self.stats['timeouts'] += 1
                elif "rate" in error_msg.lower() or "limit" in error_msg.lower():
                    self.stats['rate_limited'] += 1
                    # Longer delay for rate limiting
                    time.sleep(self.max_delay)

        # All retries failed
        print(f"💥 All retries exhausted for {url}")
        return ExtractedContent(
            url=url,
            title="",
            content="",
            html="",
            metadata={},
            extracted_at=datetime.now().isoformat(),
            source_site="essentialcardano.io",
            content_category=content_type,
            firecrawl_success=False,
            error_message="All retry attempts failed",
            retry_count=self.max_retries
        )

    def _make_api_request(self, url: str, content_type: str) -> Optional[ExtractedContent]:
        """Make single API request to Firecrawl"""
        payload = {
            "url": url,
            "formats": ["markdown", "html"],
            "includeTags": ["title", "meta"],
            "onlyMainContent": True,
            "waitFor": 3000  # Wait 3 seconds for dynamic content
        }

        print(f"📡 Requesting: {url}")
        start_time = time.time()

        response = requests.post(
            f"{self.base_url}/scrape",
            headers=self.headers,
            json=payload,
            timeout=self.timeout
        )

        elapsed = time.time() - start_time
        print(f"⏱️  Response in {elapsed:.1f}s (Status: {response.status_code})")

        if response.status_code == 408:
            # Handle timeout specifically
            raise Exception("Request timed out in API queue")
        elif response.status_code == 429:
            # Handle rate limiting
            raise Exception("Rate limited by API")
        elif response.status_code != 200:
            raise Exception(f"HTTP {response.status_code}: {response.text[:200]}")

        data = response.json()

        if not data.get("success"):
            raise Exception(f"API error: {data.get('error', 'Unknown error')}")

        # Process successful response
        result = data.get("data", {})
        metadata = {
            "author": result.get("metadata", {}).get("author", ""),
            "description": result.get("metadata", {}).get("description", ""),
            "keywords": result.get("metadata", {}).get("keywords", ""),
            "og_title": result.get("metadata", {}).get("ogTitle", ""),
            "og_description": result.get("metadata", {}).get("ogDescription", ""),
            "canonical_url": result.get("metadata", {}).get("canonical", url),
            "content_type": content_type
        }

        content = ExtractedContent(
            url=url,
            title=result.get("metadata", {}).get("title", ""),
            content=result.get("markdown", ""),
            html=result.get("html", ""),
            metadata=metadata,
            extracted_at=datetime.now().isoformat(),
            source_site="essentialcardano.io",
            content_category=content_type,
            firecrawl_success=True
        )

        print(f"✅ Extracted: {content.title[:50]}...")
        return content

    def save_content(self, content: ExtractedContent) -> bool:
        """Save extracted content to JSON file"""
        try:
            # Create filename from URL
            filename = content.url.replace("https://", "").replace("http://", "")
            filename = filename.replace("/", "_").replace("?", "_").replace("&", "_").replace("#", "_")
            filename = f"{filename}.json"

            # Create subdirectory for content type
            type_dir = self.content_dir / content.content_category
            type_dir.mkdir(exist_ok=True)

            filepath = type_dir / filename

            # Convert to dictionary for JSON serialization
            content_dict = {
                "url": content.url,
                "title": content.title,
                "content": content.content,
                "html": content.html,
                "metadata": content.metadata,
                "extracted_at": content.extracted_at,
                "source_site": content.source_site,
                "content_category": content.content_category,
                "firecrawl_success": content.firecrawl_success,
                "error_message": content.error_message,
                "retry_count": content.retry_count
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content_dict, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"❌ Error saving content for {content.url}: {e}")
            return False

    def run_batch_extraction(self, urls_file: str, batch_size: int = 20, start_batch: int = 0):
        """Run extraction in small batches with proper rate limiting"""
        print("🚀 Starting Optimized Batch Extraction")

        # Load URLs and progress
        urls = self.load_urls(urls_file)
        progress = self.load_progress()
        completed_urls = progress['completed_urls']
        failed_urls = progress['failed_urls']

        # Filter out already processed URLs
        remaining_urls = [u for u in urls if u['url'] not in completed_urls and u['url'] not in failed_urls]

        print(f"📊 Total URLs: {len(urls)}")
        print(f"📊 Already completed: {len(completed_urls)}")
        print(f"📊 Already failed: {len(failed_urls)}")
        print(f"📊 Remaining: {len(remaining_urls)}")

        # Initialize stats
        self.stats['total_urls'] = len(remaining_urls)
        self.stats['started_at'] = datetime.now().isoformat()

        # Process in batches
        for batch_num in range(start_batch, len(remaining_urls), batch_size):
            batch_end = min(batch_num + batch_size, len(remaining_urls))
            batch = remaining_urls[batch_num:batch_end]
            current_batch_number = (batch_num // batch_size) + 1
            total_batches = (len(remaining_urls) + batch_size - 1) // batch_size

            print(f"\n🔄 Processing Batch {current_batch_number}/{total_batches} ({len(batch)} URLs)")
            print(f"📍 URLs {batch_num + 1}-{batch_end} of {len(remaining_urls)}")

            batch_successful = 0
            batch_failed = 0

            for i, url_info in enumerate(batch):
                url = url_info['url']
                content_type = url_info['content_type']

                print(f"\n📄 [{i+1}/{len(batch)}] Processing: {url}")

                # Extract content with retry logic
                content = self.extract_content_with_retry(url, content_type)

                if content and content.firecrawl_success:
                    if self.save_content(content):
                        completed_urls.add(url)
                        batch_successful += 1
                        self.stats['successful'] += 1
                    else:
                        failed_urls.add(url)
                        batch_failed += 1
                        self.stats['failed'] += 1
                else:
                    failed_urls.add(url)
                    batch_failed += 1
                    self.stats['failed'] += 1

                self.stats['processed'] += 1

                # Regular delay between requests
                if i < len(batch) - 1:  # Don't delay after last item in batch
                    delay = self.base_delay + random.uniform(0, 2)  # Add jitter
                    print(f"⏸️  Waiting {delay:.1f}s...")
                    time.sleep(delay)

            # Save progress after each batch
            self.save_progress(completed_urls, failed_urls)
            self.save_stats()

            print(f"\n📊 Batch {current_batch_number} Results:")
            print(f"   ✅ Successful: {batch_successful}")
            print(f"   ❌ Failed: {batch_failed}")
            print(f"   📈 Total Progress: {self.stats['processed']}/{self.stats['total_urls']}")

            # Longer delay between batches
            if batch_end < len(remaining_urls):
                batch_delay = 15 + random.uniform(0, 10)  # 15-25 second delay between batches
                print(f"🛌 Batch break: {batch_delay:.1f}s...")
                time.sleep(batch_delay)

        # Final summary
        self._print_final_summary()

    def _print_final_summary(self):
        """Print final extraction summary"""
        success_rate = (self.stats['successful'] / self.stats['total_urls']) * 100 if self.stats['total_urls'] > 0 else 0

        print(f"\n🎉 EXTRACTION COMPLETE!")
        print(f"=" * 50)
        print(f"Total URLs processed: {self.stats['processed']}")
        print(f"Successfully extracted: {self.stats['successful']} ({success_rate:.1f}%)")
        print(f"Failed: {self.stats['failed']}")
        print(f"Timeouts: {self.stats['timeouts']}")
        print(f"Rate limited: {self.stats['rate_limited']}")
        print(f"Content saved to: {self.content_dir}")

def main():
    """Main execution function"""
    api_key = os.getenv("FIRECRAWL_API_KEY")

    if not api_key:
        print("❌ FIRECRAWL_API_KEY environment variable not set")
        return

    extractor = OptimizedExtractor(api_key)

    # Check if URLs file exists
    urls_file = "comprehensive_extraction/essential_cardano_urls.json"
    if not Path(urls_file).exists():
        print(f"❌ URLs file not found: {urls_file}")
        print("Please run sitemap_parser.py first")
        return

    # Start with small batches to test rate limiting
    print("🎯 Starting with small batch size to test API limits...")
    extractor.run_batch_extraction(urls_file, batch_size=10, start_batch=0)

if __name__ == "__main__":
    main()