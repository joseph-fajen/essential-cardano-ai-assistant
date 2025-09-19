#!/usr/bin/env python3
"""
Cardano Documentation Sitemap Parser
Systematically extracts all URLs from the Cardano documentation sitemap for comprehensive content extraction
"""

import requests
import xml.etree.ElementTree as ET
import json
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Set
from urllib.parse import urlparse
import re

class CardanoDocsSitemapParser:
    """Parser for Cardano documentation sitemap to get comprehensive URL list"""

    def __init__(self):
        self.sitemap_url = "https://docs.cardano.org/sitemap.xml"
        self.output_dir = Path("comprehensive_extraction")
        self.output_dir.mkdir(exist_ok=True)

        # Content type patterns based on URL structure for docs.cardano.org
        self.content_patterns = {
            "about_cardano": r"/about-cardano",
            "developer_resources": r"/(smart-contracts|native-tokens|transaction-tutorials|scalability|release-notes)",
            "stake_pool_operators": r"/stake-pool-course",
            "testnets": r"/cardano-testnets",
            "new_to_blockchain": r"/new-to-blockchain",
            "governance": r"/governance",
            "technical": r"/(plutus|marlowe|aiken|hydra|mithril)",
            "other": r".*"  # catchall
        }

    def fetch_sitemap(self) -> str:
        """Fetch the sitemap XML content"""
        try:
            print(f"Fetching sitemap from {self.sitemap_url}")
            response = requests.get(self.sitemap_url, timeout=30)
            response.raise_for_status()
            print(f"✅ Successfully fetched sitemap ({len(response.content)} bytes)")
            return response.content
        except Exception as e:
            print(f"❌ Error fetching sitemap: {e}")
            raise

    def parse_sitemap_xml(self, xml_content: str) -> List[Dict]:
        """Parse XML sitemap and extract URL information"""
        try:
            root = ET.fromstring(xml_content)

            # Handle namespace
            namespace = {'sitemap': 'http://www.sitemaps.org/schemas/sitemap/0.9'}

            urls = []
            for url_element in root.findall('sitemap:url', namespace):
                loc = url_element.find('sitemap:loc', namespace)
                lastmod = url_element.find('sitemap:lastmod', namespace)
                changefreq = url_element.find('sitemap:changefreq', namespace)
                priority = url_element.find('sitemap:priority', namespace)

                if loc is not None:
                    url_info = {
                        'url': loc.text,
                        'lastmod': lastmod.text if lastmod is not None else None,
                        'changefreq': changefreq.text if changefreq is not None else None,
                        'priority': priority.text if priority is not None else None,
                        'content_type': self._categorize_url(loc.text)
                    }
                    urls.append(url_info)

            print(f"✅ Parsed {len(urls)} URLs from sitemap")
            return urls

        except Exception as e:
            print(f"❌ Error parsing sitemap XML: {e}")
            raise

    def _categorize_url(self, url: str) -> str:
        """Categorize URL based on path patterns"""
        path = urlparse(url).path.lower()

        for category, pattern in self.content_patterns.items():
            if category != "other" and re.search(pattern, path):
                return category

        return "other"

    def analyze_urls(self, urls: List[Dict]) -> Dict:
        """Analyze URL distribution and provide statistics"""
        stats = {
            'total_urls': len(urls),
            'by_content_type': {},
            'by_priority': {},
            'by_changefreq': {},
            'sample_urls': {}
        }

        # Count by content type
        for url_info in urls:
            content_type = url_info['content_type']
            stats['by_content_type'][content_type] = stats['by_content_type'].get(content_type, 0) + 1

            # Store sample URLs for each content type
            if content_type not in stats['sample_urls']:
                stats['sample_urls'][content_type] = []
            if len(stats['sample_urls'][content_type]) < 3:
                stats['sample_urls'][content_type].append(url_info['url'])

        # Count by priority
        for url_info in urls:
            priority = url_info.get('priority', 'unknown')
            stats['by_priority'][priority] = stats['by_priority'].get(priority, 0) + 1

        # Count by change frequency
        for url_info in urls:
            changefreq = url_info.get('changefreq', 'unknown')
            stats['by_changefreq'][changefreq] = stats['by_changefreq'].get(changefreq, 0) + 1

        return stats

    def filter_urls_for_extraction(self, urls: List[Dict]) -> List[Dict]:
        """Filter URLs to exclude non-content pages"""
        excluded_patterns = [
            r'/api',
            r'/admin',
            r'\.xml$',
            r'\.json$',
            r'/search',
            r'/404',
            r'/#'  # Hash anchors
        ]

        filtered_urls = []
        excluded_count = 0

        for url_info in urls:
            url = url_info['url']

            # Check if URL should be excluded
            should_exclude = False
            for pattern in excluded_patterns:
                if re.search(pattern, url, re.IGNORECASE):
                    should_exclude = True
                    break

            if not should_exclude:
                filtered_urls.append(url_info)
            else:
                excluded_count += 1

        print(f"✅ Filtered URLs: {len(filtered_urls)} included, {excluded_count} excluded")
        return filtered_urls

    def save_urls(self, urls: List[Dict], filename: str = "cardano_docs_urls.json"):
        """Save URLs to JSON file for extraction processing"""
        filepath = self.output_dir / filename

        # Prepare data for saving
        save_data = {
            'extracted_at': datetime.now().isoformat(),
            'sitemap_url': self.sitemap_url,
            'total_urls': len(urls),
            'urls': urls
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(save_data, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved {len(urls)} URLs to {filepath}")
        return filepath

    def create_extraction_batches(self, urls: List[Dict], batch_size: int = 15) -> List[List[Dict]]:
        """Create batches for systematic extraction (smaller batches for technical docs)"""
        batches = []
        for i in range(0, len(urls), batch_size):
            batch = urls[i:i + batch_size]
            batches.append(batch)

        print(f"✅ Created {len(batches)} batches of up to {batch_size} URLs each")
        return batches

    def print_analysis(self, stats: Dict):
        """Print detailed analysis of sitemap URLs"""
        print("\n" + "="*50)
        print("CARDANO DOCUMENTATION SITEMAP ANALYSIS")
        print("="*50)

        print(f"\n📊 TOTAL URLS: {stats['total_urls']}")

        print(f"\n📁 BY CONTENT TYPE:")
        for content_type, count in sorted(stats['by_content_type'].items(), key=lambda x: x[1], reverse=True):
            percentage = (count / stats['total_urls']) * 100
            print(f"  {content_type:20} {count:4d} ({percentage:5.1f}%)")

        print(f"\n⭐ BY PRIORITY:")
        for priority, count in sorted(stats['by_priority'].items()):
            percentage = (count / stats['total_urls']) * 100
            print(f"  {priority:10} {count:4d} ({percentage:5.1f}%)")

        print(f"\n🔄 BY CHANGE FREQUENCY:")
        for changefreq, count in sorted(stats['by_changefreq'].items()):
            percentage = (count / stats['total_urls']) * 100
            print(f"  {changefreq:10} {count:4d} ({percentage:5.1f}%)")

        print(f"\n📝 SAMPLE URLS BY TYPE:")
        for content_type, sample_urls in stats['sample_urls'].items():
            if sample_urls:
                print(f"  {content_type}:")
                for url in sample_urls:
                    print(f"    - {url}")

    def run_comprehensive_analysis(self):
        """Run complete sitemap analysis and prepare for extraction"""
        print("🚀 Starting Cardano Documentation Sitemap Analysis")

        # Fetch and parse sitemap
        xml_content = self.fetch_sitemap()
        all_urls = self.parse_sitemap_xml(xml_content)

        # Analyze all URLs
        all_stats = self.analyze_urls(all_urls)
        self.print_analysis(all_stats)

        # Filter for content extraction
        print(f"\n🔍 Filtering URLs for content extraction...")
        filtered_urls = self.filter_urls_for_extraction(all_urls)

        # Analyze filtered URLs
        filtered_stats = self.analyze_urls(filtered_urls)
        print(f"\n📋 FILTERED ANALYSIS (for extraction):")
        print(f"Total URLs for extraction: {filtered_stats['total_urls']}")
        for content_type, count in sorted(filtered_stats['by_content_type'].items(), key=lambda x: x[1], reverse=True):
            print(f"  {content_type}: {count}")

        # Save URLs for extraction
        urls_file = self.save_urls(filtered_urls)

        # Create extraction batches (smaller for technical docs)
        batches = self.create_extraction_batches(filtered_urls, batch_size=15)

        # Save batch information
        batch_info = {
            'total_batches': len(batches),
            'batch_size': 15,
            'total_urls': len(filtered_urls),
            'batches': [
                {
                    'batch_number': i + 1,
                    'start_index': i * 15,
                    'end_index': min((i + 1) * 15, len(filtered_urls)),
                    'url_count': len(batch),
                    'sample_urls': [url['url'] for url in batch[:3]]
                }
                for i, batch in enumerate(batches)
            ]
        }

        batch_file = self.output_dir / "cardano_docs_extraction_batches.json"
        with open(batch_file, 'w', encoding='utf-8') as f:
            json.dump(batch_info, f, indent=2, ensure_ascii=False)

        print(f"✅ Saved batch information to {batch_file}")

        print(f"\n🎯 READY FOR EXTRACTION:")
        print(f"  URLs file: {urls_file}")
        print(f"  Batch file: {batch_file}")
        print(f"  Total URLs: {len(filtered_urls)}")
        print(f"  Batches: {len(batches)} (batch size: 15 for technical content)")

        return {
            'urls_file': urls_file,
            'batch_file': batch_file,
            'total_urls': len(filtered_urls),
            'batches': len(batches),
            'filtered_urls': filtered_urls
        }

def main():
    """Main execution function"""
    parser = CardanoDocsSitemapParser()
    result = parser.run_comprehensive_analysis()

    print(f"\n✅ Cardano Documentation sitemap analysis complete!")
    print(f"Next step: Use Tavily extraction script with {result['total_urls']} URLs")

if __name__ == "__main__":
    main()