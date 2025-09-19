#!/usr/bin/env python3
"""
Tavily Comprehensive Extractor
Full pipeline for extracting all Essential Cardano content using Tavily with content processing
"""

import os
import json
import time
from datetime import datetime
from typing import Dict, List
from pathlib import Path
from dotenv import load_dotenv
from tavily import TavilyClient
from tavily_content_processor import TavilyContentProcessor

# Load environment variables
load_dotenv()

class TavilyComprehensiveExtractor:
    """Complete Tavily-based extraction pipeline with processing"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.tavily_client = TavilyClient(api_key=api_key)
        self.processor = TavilyContentProcessor()

        # Output directories
        self.output_dir = Path("tavily_comprehensive")
        self.raw_dir = self.output_dir / "raw_extractions"
        self.processed_dir = self.output_dir / "processed_content"
        self.globant_dir = self.output_dir / "globant_ready"
        self.progress_dir = self.output_dir / "progress"

        # Create directories
        for directory in [self.raw_dir, self.processed_dir, self.globant_dir, self.progress_dir]:
            directory.mkdir(parents=True, exist_ok=True)

        # Progress tracking
        self.progress_file = self.progress_dir / "extraction_progress.json"
        self.stats_file = self.progress_dir / "extraction_stats.json"

        # Tavily batch settings (optimized for their API)
        self.batch_size = 20  # Max URLs per request
        self.request_delay = 3  # Seconds between requests
        self.max_retries = 3

        # Statistics
        self.stats = {
            'total_urls': 0,
            'batches_processed': 0,
            'successful_extractions': 0,
            'failed_extractions': 0,
            'processed_content_items': 0,
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
                raw_file = self.raw_dir / f"batch_{batch_number:03d}.json"
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

    def process_batch_results(self, response: Dict, batch_number: int) -> List:
        """Process Tavily response and create clean content"""
        if not response:
            return []

        # Process with our content processor
        processed_contents = self.processor.process_tavily_results(response)

        # Save processed results
        processed_file = self.processed_dir / f"batch_{batch_number:03d}_processed.json"
        with open(processed_file, 'w', encoding='utf-8') as f:
            json.dump([{
                'url': content.url,
                'title': content.title,
                'main_content': content.main_content,
                'content_type': content.content_type,
                'sections': content.sections,
                'metadata': content.metadata,
                'quality_score': content.quality_score
            } for content in processed_contents], f, indent=2, ensure_ascii=False)

        # Create individual Globant-ready files
        for content in processed_contents:
            self.create_globant_file(content, batch_number)

        return processed_contents

    def create_globant_file(self, content, batch_number: int):
        """Create individual file ready for Globant upload"""
        # Create filename from URL
        filename = content.url.replace("https://", "").replace("http://", "")
        filename = filename.replace("/", "_").replace("?", "_").replace("&", "_")
        filename = f"{content.content_type}_{filename}.json"

        filepath = self.globant_dir / filename

        # Globant-optimized content structure
        globant_content = {
            'url': content.url,
            'title': content.title,
            'content': content.main_content,
            'content_type': content.content_type,
            'metadata': {
                **content.metadata,
                'quality_score': content.quality_score,
                'sections_count': len(content.sections),
                'extraction_method': 'tavily_api',
                'processed_with': 'tavily_content_processor',
                'source_site': 'essentialcardano.io',
                'batch_number': batch_number,
                'extracted_at': datetime.now().isoformat()
            }
        }

        # Add sections as additional content for better RAG performance
        if content.sections:
            additional_content = []
            for section in content.sections:
                if section.get('type') == 'faq_item':
                    additional_content.append(f"Q: {section.get('question', '')}")
                    additional_content.append(f"A: {section.get('answer', '')}")
                elif section.get('type') == 'glossary_term':
                    additional_content.append(f"Term: {section.get('term', '')}")
                elif section.get('type') == 'article_reference':
                    additional_content.append(f"Article: {section.get('title', '')}")

            if additional_content:
                globant_content['content'] += "\n\n" + "\n".join(additional_content)

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(globant_content, f, indent=2, ensure_ascii=False)

    def run_comprehensive_extraction(self, urls_file: str = "comprehensive_extraction/essential_cardano_urls.json"):
        """Run complete extraction of all URLs"""
        print("🚀 Starting Tavily Comprehensive Extraction")
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
                # Process results
                processed_contents = self.process_batch_results(response, batch_number)

                # Update statistics
                successful_in_batch = len([r for r in response.get('results', []) if r.get('raw_content')])
                failed_in_batch = len(batch_urls) - successful_in_batch

                self.stats['successful_extractions'] += successful_in_batch
                self.stats['failed_extractions'] += failed_in_batch
                self.stats['processed_content_items'] += len(processed_contents)
                self.stats['batches_processed'] += 1

                # Update progress
                completed_batches.append(batch_number)
                completed_urls.update(batch_urls)

                print(f"   ✅ Successful: {successful_in_batch}")
                print(f"   ❌ Failed: {failed_in_batch}")
                print(f"   📄 Processed: {len(processed_contents)}")

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

        print(f"\n🎉 TAVILY COMPREHENSIVE EXTRACTION COMPLETE!")
        print(f"=" * 60)
        print(f"📊 FINAL STATISTICS:")
        print(f"   Total URLs: {self.stats['total_urls']}")
        print(f"   Batches processed: {self.stats['batches_processed']}")
        print(f"   Successfully extracted: {self.stats['successful_extractions']} ({success_rate:.1f}%)")
        print(f"   Failed extractions: {self.stats['failed_extractions']}")
        print(f"   Processed content items: {self.stats['processed_content_items']}")
        print(f"   Total time: {total_time}")
        print(f"   Average time per URL: {total_time.total_seconds() / self.stats['total_urls']:.2f} seconds")

        print(f"\n📁 OUTPUT DIRECTORIES:")
        print(f"   Raw extractions: {self.raw_dir}")
        print(f"   Processed content: {self.processed_dir}")
        print(f"   Globant-ready files: {self.globant_dir}")
        print(f"   Progress tracking: {self.progress_dir}")

        # Count Globant-ready files
        globant_files = list(self.globant_dir.glob("*.json"))
        print(f"\n🎯 READY FOR GLOBANT UPLOAD:")
        print(f"   Individual files created: {len(globant_files)}")
        print(f"   Upload directory: {self.globant_dir}")

def main():
    """Main execution function"""
    api_key = os.getenv("TAVILY_API_KEY")

    if not api_key:
        print("❌ TAVILY_API_KEY environment variable not set")
        return

    # Check if URLs file exists
    urls_file = "comprehensive_extraction/essential_cardano_urls.json"
    if not Path(urls_file).exists():
        print(f"❌ URLs file not found: {urls_file}")
        print("Please run sitemap_parser.py first")
        return

    extractor = TavilyComprehensiveExtractor(api_key)
    extractor.run_comprehensive_extraction(urls_file)

if __name__ == "__main__":
    main()