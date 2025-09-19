#!/usr/bin/env python3
"""
IOG Blog Tavily Extractor
Full pipeline for extracting all IOG blog content using Tavily API
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List
from pathlib import Path
from dotenv import load_dotenv
from tavily import TavilyClient

# Load environment variables
load_dotenv()

class IOGBlogTavilyExtractor:
    """Complete Tavily-based extraction pipeline for IOG blog content"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.tavily_client = TavilyClient(api_key=api_key)

        # Output directories
        self.output_dir = Path("iog_blog_comprehensive")
        self.raw_dir = self.output_dir / "raw_extractions"
        self.progress_dir = self.output_dir / "progress"

        # Create directories
        for directory in [self.raw_dir, self.progress_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        # Progress tracking
        self.progress_file = self.progress_dir / "extraction_progress.json"
        self.stats_file = self.progress_dir / "extraction_stats.json"

        # Tavily batch settings (optimized for blog content)
        self.batch_size = 20  # Moderate batches for blog posts
        self.request_delay = 3  # Seconds between requests
        self.max_retries = 3

        # Statistics
        self.stats = {
            'total_urls': 0,
            'batches_processed': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
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
            return {'completed_batches': [], 'completed_urls': set()}

        with open(self.progress_file, 'r', encoding='utf-8') as f:
            progress = json.load(f)

        return {
            'completed_batches': progress.get('completed_batches', []),
            'completed_urls': set(progress.get('completed_urls', []))
        }

    def save_progress(self, completed_batches: List[int], completed_urls: set):
        """Save extraction progress"""
        progress = {
            'completed_batches': completed_batches,
            'completed_urls': list(completed_urls),
            'last_saved': datetime.now().isoformat()
        }

        with open(self.progress_file, 'w', encoding='utf-8') as f:
            json.dump(progress, f, indent=2, ensure_ascii=False)

    def save_stats(self):
        """Save extraction statistics"""
        self.stats['last_update'] = datetime.now().isoformat()
        with open(self.stats_file, 'w', encoding='utf-8') as f:
            json.dump(self.stats, f, indent=2, ensure_ascii=False)

    def extract_batch(self, urls: List[str], batch_number: int) -> Dict:
        """Extract a batch of URLs using Tavily"""
        for attempt in range(self.max_retries):
            try:
                print(f"📡 Extracting batch {batch_number} ({len(urls)} URLs) - Attempt {attempt + 1}")

                start_time = time.time()

                # Use Tavily's batch extraction
                response = self.tavily_client.extract(
                    urls=urls,
                    include_images=False,
                    extract_depth="basic"  # Use basic for speed and cost
                )

                elapsed = time.time() - start_time
                print(f"⏱️  Batch completed in {elapsed:.2f} seconds")

                # Save raw response
                raw_file = self.raw_dir / f"iog_blog_batch_{batch_number:03d}.json"
                with open(raw_file, 'w', encoding='utf-8') as f:
                    json.dump({
                        'batch_number': batch_number,
                        'urls': urls,
                        'extraction_time': elapsed,
                        'timestamp': datetime.now().isoformat(),
                        'response': response
                    }, f, indent=2, ensure_ascii=False)

                return response

            except Exception as e:
                print(f"❌ Batch {batch_number} attempt {attempt + 1} failed: {e}")
                if attempt < self.max_retries - 1:
                    delay = (attempt + 1) * 5  # Exponential backoff
                    print(f"⏸️  Retrying in {delay} seconds...")
                    time.sleep(delay)

        print(f"💥 Batch {batch_number} failed after {self.max_retries} attempts")
        return None

    def run_comprehensive_extraction(self, urls_file: str = "comprehensive_extraction/iog_blog_urls.json"):
        """Run complete extraction of all IOG blog URLs"""
        print("🚀 Starting IOG Blog Tavily Extraction")
        print(f"=" * 60)

        # Load URLs and progress
        all_urls = self.load_urls(urls_file)
        progress = self.load_progress()

        # Filter URLs by type for better organization
        url_groups = {}
        for url_info in all_urls:
            content_type = url_info['content_type']
            if content_type not in url_groups:
                url_groups[content_type] = []
            url_groups[content_type].append(url_info['url'])

        print(f"📊 URL DISTRIBUTION:")
        for content_type, urls in url_groups.items():
            print(f"   {content_type}: {len(urls)} URLs")

        # Initialize stats
        total_urls = len(all_urls)
        self.stats['total_urls'] = total_urls
        self.stats['started_at'] = datetime.now().isoformat()

        print(f"\n📊 EXTRACTION PLAN:")
        print(f"   Total URLs: {total_urls}")
        print(f"   Batch size: {self.batch_size}")
        print(f"   Estimated batches: {(total_urls + self.batch_size - 1) // self.batch_size}")
        print(f"   Estimated cost: ${(total_urls/5) * 0.0016:.2f}")

        # Process in batches
        batch_number = 0
        completed_batches = progress['completed_batches']
        completed_urls = progress['completed_urls']

        # Group URLs into batches
        for i in range(0, total_urls, self.batch_size):
            batch_number += 1

            # Skip if batch already completed
            if batch_number in completed_batches:
                print(f"⏭️  Skipping completed batch {batch_number}")
                continue

            batch_urls = [all_urls[j]['url'] for j in range(i, min(i + self.batch_size, total_urls))]

            print(f"\n🔄 Processing Batch {batch_number}/{(total_urls + self.batch_size - 1) // self.batch_size}")
            print(f"   URLs: {i + 1}-{min(i + self.batch_size, total_urls)} of {total_urls}")

            # Extract batch
            response = self.extract_batch(batch_urls, batch_number)

            if response:
                # Update statistics
                successful_in_batch = len([r for r in response.get('results', []) if r.get('raw_content')])
                failed_in_batch = len(batch_urls) - successful_in_batch

                self.stats['successful_extractions'] += successful_in_batch
                self.stats['failed_extractions'] += failed_in_batch
                self.stats['batches_processed'] += 1

                # Update progress
                completed_batches.append(batch_number)
                completed_urls.update(batch_urls)

                print(f"   ✅ Successful: {successful_in_batch}")
                print(f"   ❌ Failed: {failed_in_batch}")

            else:
                print(f"   💥 Batch failed completely")
                self.stats['failed_extractions'] += len(batch_urls)

            # Save progress after each batch
            self.save_progress(completed_batches, completed_urls)
            self.save_stats()

            # Delay between batches
            if batch_number < ((total_urls + self.batch_size - 1) // self.batch_size):
                print(f"⏸️  Batch delay: {self.request_delay} seconds...")
                time.sleep(self.request_delay)

        # Final summary
        self._print_final_summary()

    def _print_final_summary(self):
        """Print final extraction summary"""
        success_rate = (self.stats['successful_extractions'] / self.stats['total_urls']) * 100 if self.stats['total_urls'] > 0 else 0
        total_time = datetime.now() - datetime.fromisoformat(self.stats['started_at'])

        print(f"\n🎉 IOG BLOG TAVILY EXTRACTION COMPLETE!")
        print(f"=" * 60)
        print(f"📊 FINAL STATISTICS:")
        print(f"   Total URLs: {self.stats['total_urls']}")
        print(f"   Batches processed: {self.stats['batches_processed']}")
        print(f"   Successfully extracted: {self.stats['successful_extractions']} ({success_rate:.1f}%)")
        print(f"   Failed extractions: {self.stats['failed_extractions']}")
        print(f"   Total time: {total_time}")
        print(f"   Average time per URL: {total_time.total_seconds() / self.stats['total_urls']:.2f} seconds")

        print(f"\n📁 OUTPUT DIRECTORIES:")
        print(f"   Raw extractions: {self.raw_dir}")
        print(f"   Progress tracking: {self.progress_dir}")

        # Count raw extraction files
        raw_files = list(self.raw_dir.glob("iog_blog_batch_*.json"))
        print(f"\n🎯 READY FOR BATCH SPLITTING:")
        print(f"   Raw batch files created: {len(raw_files)}")
        print(f"   Next step: Run iog_blog_batch_splitter.py")

def main():
    """Main execution function"""
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        print("❌ TAVILY_API_KEY environment variable not set")
        return

    # Check if URLs file exists
    urls_file = "comprehensive_extraction/iog_blog_urls.json"
    if not Path(urls_file).exists():
        print(f"❌ URLs file not found: {urls_file}")
        print("Please run iog_blog_sitemap_parser.py first")
        return

    extractor = IOGBlogTavilyExtractor(api_key)
    extractor.run_comprehensive_extraction(urls_file)

if __name__ == "__main__":
    main()