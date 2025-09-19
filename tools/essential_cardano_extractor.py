#!/usr/bin/env python3
"""
Essential Cardano Content Extractor
Local implementation using Firecrawl API for systematic content extraction
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

class FirecrawlContentExtractor:
    """Local implementation of Essential Cardano Content Extractor using Firecrawl API"""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.base_url = "https://api.firecrawl.dev/v0"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        # Target sites and priority sections from agent configuration
        self.target_sites = {
            "essentialcardano.io": {
                "priority_sections": ["/faq", "/glossary", "/article", "/guides"],
                "category": "community_knowledge"
            },
            "docs.cardano.org": {
                "priority_sections": ["/learn", "/build", "/operate", "/governance"],
                "category": "technical_documentation"
            },
            "developers.cardano.org": {
                "priority_sections": ["/docs", "/tools", "/tutorials", "/get-started"],
                "category": "developer_resources"
            }
        }

        # Output directory for extracted content
        self.output_dir = Path("extracted_content")
        self.output_dir.mkdir(exist_ok=True)

    def search_content(self, site: str, query: str, limit: int = 10) -> List[str]:
        """Search for content URLs on a specific site"""
        search_url = f"{self.base_url}/search"

        payload = {
            "query": f"site:{site} {query}",
            "limit": limit
        }

        try:
            response = requests.post(search_url, headers=self.headers, json=payload)
            response.raise_for_status()

            data = response.json()
            urls = []

            if data.get("success") and "data" in data:
                for result in data["data"]:
                    if "url" in result:
                        urls.append(result["url"])

            print(f"Found {len(urls)} URLs for {site} with query '{query}'")
            return urls

        except Exception as e:
            print(f"Error searching {site}: {e}")
            return []

    def extract_content(self, url: str, format_type: str = "markdown") -> Optional[ExtractedContent]:
        """Extract content from a specific URL using Firecrawl"""
        scrape_url = f"{self.base_url}/scrape"

        payload = {
            "url": url,
            "formats": [format_type, "html"],
            "includeTags": ["title", "meta"],
            "onlyMainContent": True
        }

        try:
            response = requests.post(scrape_url, headers=self.headers, json=payload)
            response.raise_for_status()

            data = response.json()

            if not data.get("success"):
                print(f"Failed to extract content from {url}: {data.get('error', 'Unknown error')}")
                return None

            result = data.get("data", {})

            # Extract metadata
            metadata = {
                "author": result.get("metadata", {}).get("author", ""),
                "description": result.get("metadata", {}).get("description", ""),
                "keywords": result.get("metadata", {}).get("keywords", ""),
                "og_title": result.get("metadata", {}).get("ogTitle", ""),
                "og_description": result.get("metadata", {}).get("ogDescription", ""),
                "canonical_url": result.get("metadata", {}).get("canonical", url)
            }

            # Determine source site and category
            source_site = self._get_source_site(url)
            content_category = self.target_sites.get(source_site, {}).get("category", "unknown")

            content = ExtractedContent(
                url=url,
                title=result.get("metadata", {}).get("title", ""),
                content=result.get("markdown", "") if format_type == "markdown" else result.get("content", ""),
                html=result.get("html", ""),
                metadata=metadata,
                extracted_at=datetime.now().isoformat(),
                source_site=source_site,
                content_category=content_category
            )

            print(f"Successfully extracted content from {url}")
            return content

        except Exception as e:
            print(f"Error extracting content from {url}: {e}")
            return None

    def _get_source_site(self, url: str) -> str:
        """Determine source site from URL"""
        for site in self.target_sites.keys():
            if site in url:
                return site
        return "unknown"

    def save_content(self, content: ExtractedContent):
        """Save extracted content to JSON file"""
        # Create filename from URL
        filename = content.url.replace("https://", "").replace("http://", "")
        filename = filename.replace("/", "_").replace("?", "_").replace("&", "_")
        filename = f"{filename}.json"

        # Create subdirectory for source site
        site_dir = self.output_dir / content.source_site
        site_dir.mkdir(exist_ok=True)

        filepath = site_dir / filename

        # Convert to dictionary for JSON serialization
        content_dict = {
            "url": content.url,
            "title": content.title,
            "content": content.content,
            "html": content.html,
            "metadata": content.metadata,
            "extracted_at": content.extracted_at,
            "source_site": content.source_site,
            "content_category": content.content_category
        }

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content_dict, f, indent=2, ensure_ascii=False)

        print(f"Saved content to {filepath}")

    def extract_site_content(self, site: str, section_queries: List[str] = None, max_pages: int = 50):
        """Extract content from a specific site"""
        print(f"\n--- Extracting content from {site} ---")

        if section_queries is None:
            section_queries = self.target_sites.get(site, {}).get("priority_sections", [])

        all_urls = set()

        # Search for content in priority sections
        for section in section_queries:
            search_query = f"{section} OR path:{section}"
            urls = self.search_content(site, search_query, limit=max_pages)
            all_urls.update(urls)

        # Also search for general content
        general_queries = ["cardano", "blockchain", "introduction", "guide", "tutorial"]
        for query in general_queries:
            urls = self.search_content(site, query, limit=10)
            all_urls.update(urls)

        print(f"Total unique URLs found for {site}: {len(all_urls)}")

        # Extract content from each URL
        successful_extractions = 0
        for i, url in enumerate(list(all_urls)[:max_pages]):
            print(f"Processing {i+1}/{min(len(all_urls), max_pages)}: {url}")

            content = self.extract_content(url, format_type="markdown")
            if content:
                self.save_content(content)
                successful_extractions += 1

            # Rate limiting - be respectful to the API
            time.sleep(1)

        print(f"Successfully extracted {successful_extractions} pages from {site}")

    def extract_all_sites(self, max_pages_per_site: int = 20):
        """Extract content from all target sites"""
        print("Starting Essential Cardano Content Extraction")
        print(f"Target sites: {list(self.target_sites.keys())}")
        print(f"Max pages per site: {max_pages_per_site}")
        print(f"Output directory: {self.output_dir}")

        for site in self.target_sites.keys():
            try:
                self.extract_site_content(site, max_pages=max_pages_per_site)
            except Exception as e:
                print(f"Error processing {site}: {e}")
                continue

        print("\n--- Extraction Complete ---")
        print(f"Check extracted content in: {self.output_dir}")

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
    extractor = FirecrawlContentExtractor(api_key)

    # Start with Essential Cardano as proof of concept
    print("Starting with Essential Cardano extraction...")
    extractor.extract_site_content("essentialcardano.io", max_pages=5)

if __name__ == "__main__":
    main()