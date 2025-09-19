#!/usr/bin/env python3
"""
Comprehensive Essential Cardano Content Extractor
Uses sitemap-based systematic extraction for complete content coverage
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
import signal
import sys

# Load environment variables from .env file
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

class ComprehensiveExtractor:
    """Comprehensive extractor using sitemap-based URL list"""

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

        # Progress tracking
        self.progress_file = self.progress_dir / "extraction_progress.json"
        self.stats_file = self.progress_dir / "extraction_stats.json"
        self.failed_urls_file = self.progress_dir / "failed_urls.json"

        # Rate limiting
        self.request_delay = 2  # seconds between requests
        self.batch_delay = 10   # seconds between batches

        # Statistics
        self.stats = {
            'total_urls': 0,
            'processed': 0,
            'successful': 0,
            'failed': 0,
            'skipped': 0,
            'started_at': None,
            'last_update': None,
            'estimated_completion': None,
            'failed_urls': []
        }

        # Signal handling for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)

    def _signal_handler(self, signum, frame):
        """Handle graceful shutdown"""
        print(f"\n🛑 Received signal {signum}. Saving progress and shutting down...")
        self._save_progress()
        self._save_stats()
        sys.exit(0)

    def load_urls(self, urls_file: str) -> List[Dict]:
        """Load URLs from sitemap parser output"""
        urls_path = Path(urls_file)
        if not urls_path.exists():
            raise FileNotFoundError(f"URLs file not found: {urls_file}")

        with open(urls_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        urls = data.get('urls', [])
        print(f"✅ Loaded {len(urls)} URLs from {urls_file}")
        return urls

    def load_progress(self) -> Dict:
        """Load previous extraction progress if available"""
        if not self.progress_file.exists():
            return {'completed_urls': set(), 'failed_urls': set()}

        with open(self.progress_file, 'r', encoding='utf-8') as f:
            progress = json.load(f)

        return {
            'completed_urls': set(progress.get('completed_urls', [])),
            'failed_urls': set(progress.get('failed_urls', []))
        }

    def _save_progress(self):
        """Save extraction progress"""
        progress = {
            'completed_urls': list(self.completed_urls),
            'failed_urls': list(self.failed_urls),
            'last_saved': datetime.now().isoformat()
        }

        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

    def _save_stats(self):
        """Save extraction statistics"""
        self.stats['last_update'] = datetime.now().isoformat()

        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)

        # Save failed URLs separately for analysis
        if self.stats['failed_urls']:
            with open(self.failed_urls_file, 'w', encoding='utf-8') as f:
                json.dump(self.stats['failed_urls'], f, indent=2, ensure_ascii=False)

    def extract_content(self, url: str, content_type: str) -> Optional[ExtractedContent]:
        """Extract content from a specific URL using Firecrawl"""
        scrape_url = f"{self.base_url}/scrape"

        payload = {
            "url": url,
            "formats": ["markdown", "html"],
            "includeTags": ["title", "meta"],
            "onlyMainContent": True,
            "waitFor": 2000  # Wait 2 seconds for dynamic content
        }

        try:
            response = requests.post(scrape_url, headers=self.headers, json=payload, timeout=60)
            response.raise_for_status()

            data = response.json()

            if not data.get("success"):
                error_msg = data.get('error', 'Unknown error')
                print(f"❌ Failed to extract {url}: {error_msg}")
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
                    error_message=error_msg
                )

            result = data.get("data", {})

            # Extract metadata
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

            return content

        except Exception as e:
            error_msg = str(e)
            print(f"❌ Error extracting {url}: {error_msg}")
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
                error_message=error_msg
            )

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
                "error_message": content.error_message
            }

            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(content_dict, f, indent=2, ensure_ascii=False)

            return True

        except Exception as e:
            print(f"❌ Error saving content for {content.url}: {e}")
            return False

    def _estimate_completion_time(self):
        """Estimate completion time based on current progress"""
        if self.stats['processed'] == 0:
            return None

        elapsed = (datetime.now() - datetime.fromisoformat(self.stats['started_at'])).total_seconds()
        rate = self.stats['processed'] / elapsed  # URLs per second
        remaining = self.stats['total_urls'] - self.stats['processed']
        estimated_seconds = remaining / rate if rate > 0 else 0

        completion_time = datetime.now().timestamp() + estimated_seconds
        return datetime.fromtimestamp(completion_time).isoformat()

    def print_progress(self, current_batch: int, total_batches: int, url: str):
        """Print detailed progress information"""
        progress_pct = (self.stats['processed'] / self.stats['total_urls']) * 100
        success_rate = (self.stats['successful'] / self.stats['processed']) * 100 if self.stats['processed'] > 0 else 0

        print(f"\n📊 PROGRESS UPDATE")
        print(f"Batch: {current_batch}/{total_batches}")
        print(f"URLs: {self.stats['processed']}/{self.stats['total_urls']} ({progress_pct:.1f}%)")
        print(f"Success: {self.stats['successful']} ({success_rate:.1f}%)")
        print(f"Failed: {self.stats['failed']}")
        print(f"Current: {url}")

        # Estimate completion time
        estimated = self._estimate_completion_time()
        if estimated:
            print(f"ETA: {estimated[:19]}")

    def run_comprehensive_extraction(self, urls_file: str = "comprehensive_extraction/essential_cardano_urls.json"):
        """Run comprehensive extraction of all URLs"""
        print("🚀 Starting Comprehensive Essential Cardano Extraction")

        # Load URLs and progress
        urls = self.load_urls(urls_file)
        progress = self.load_progress()

        self.completed_urls = progress['completed_urls']
        self.failed_urls = progress['failed_urls']

        # Initialize stats
        self.stats['total_urls'] = len(urls)
        self.stats['started_at'] = datetime.now().isoformat()
        self.stats['processed'] = len(self.completed_urls) + len(self.failed_urls)
        self.stats['successful'] = len(self.completed_urls)
        self.stats['failed'] = len(self.failed_urls)

        print(f"Total URLs: {len(urls)}")
        print(f"Already processed: {self.stats['processed']}")
        print(f"Remaining: {len(urls) - self.stats['processed']}")

        # Process URLs in batches
        batch_size = 50
        current_batch = 0
        total_batches = (len(urls) + batch_size - 1) // batch_size

        for i in range(0, len(urls), batch_size):
            current_batch += 1
            batch = urls[i:i + batch_size]

            print(f"\n🔄 Processing Batch {current_batch}/{total_batches}")

            for url_info in batch:
                url = url_info['url']
                content_type = url_info['content_type']

                # Skip if already processed
                if url in self.completed_urls or url in self.failed_urls:
                    self.stats['skipped'] += 1
                    continue

                # Print progress
                self.print_progress(current_batch, total_batches, url)

                # Extract content
                content = self.extract_content(url, content_type)

                if content and content.firecrawl_success:
                    # Save successful extraction
                    if self.save_content(content):
                        self.completed_urls.add(url)
                        self.stats['successful'] += 1
                        print(f"✅ Extracted: {url}")
                    else:
                        self.failed_urls.add(url)
                        self.stats['failed'] += 1
                        self.stats['failed_urls'].append({
                            'url': url,
                            'error': 'Failed to save content',
                            'timestamp': datetime.now().isoformat()
                        })
                else:
                    # Handle failed extraction
                    self.failed_urls.add(url)
                    self.stats['failed'] += 1
                    error_msg = content.error_message if content else "Unknown error"
                    self.stats['failed_urls'].append({
                        'url': url,
                        'error': error_msg,
                        'timestamp': datetime.now().isoformat()
                    })
                    print(f"❌ Failed: {url} - {error_msg}")

                self.stats['processed'] += 1

                # Rate limiting
                time.sleep(self.request_delay)

            # Save progress after each batch
            self._save_progress()
            self._save_stats()

            # Batch delay
            if current_batch < total_batches:
                print(f"⏸️  Batch delay: {self.batch_delay} seconds...")
                time.sleep(self.batch_delay)

        # Final summary
        self._print_final_summary()

    def _print_final_summary(self):
        """Print final extraction summary"""
        total_time = datetime.now() - datetime.fromisoformat(self.stats['started_at'])
        success_rate = (self.stats['successful'] / self.stats['total_urls']) * 100

        print(f"\n🎉 EXTRACTION COMPLETE!")
        print(f"=" * 50)
        print(f"Total URLs: {self.stats['total_urls']}")
        print(f"Successfully extracted: {self.stats['successful']} ({success_rate:.1f}%)")
        print(f"Failed: {self.stats['failed']}")
        print(f"Skipped: {self.stats['skipped']}")
        print(f"Total time: {total_time}")
        print(f"Average time per URL: {total_time.total_seconds() / self.stats['total_urls']:.1f} seconds")
        print(f"\n📁 Content saved to: {self.content_dir}")
        print(f"📊 Progress saved to: {self.progress_dir}")

        if self.stats['failed'] > 0:
            print(f"\n⚠️  {self.stats['failed']} URLs failed - check {self.failed_urls_file}")

def main():
    """Main execution function"""
    # Get Firecrawl API key from environment variable
    api_key = os.getenv("FIRECRAWL_API_KEY")

    if not api_key:
        print("Error: FIRECRAWL_API_KEY environment variable not set")
        print("Please set your Firecrawl API key:")
        print("export FIRECRAWL_API_KEY='your_api_key_here'")
        return

    # Initialize extractor
    extractor = ComprehensiveExtractor(api_key)

    # Check if URLs file exists
    urls_file = "comprehensive_extraction/essential_cardano_urls.json"
    if not Path(urls_file).exists():
        print(f"❌ URLs file not found: {urls_file}")
        print("Please run sitemap_parser.py first to generate the URLs file")
        return

    # Start comprehensive extraction
    extractor.run_comprehensive_extraction(urls_file)

if __name__ == "__main__":
    main()