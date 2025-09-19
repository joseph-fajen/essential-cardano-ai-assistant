#!/usr/bin/env python3
"""
Focused Test Content Extraction
Extract 5-10 high-value pages for Essential Cardano AI Assistant testing
"""

import os
import sys
import json
import time
import requests
from datetime import datetime
from pathlib import Path

# Add tools directory to path to import our existing modules
sys.path.append(str(Path(__file__).parent.parent.parent / "tools"))

from dotenv import load_dotenv

# Load environment variables
load_dotenv(Path(__file__).parent.parent.parent / ".env")

class FocusedTestExtractor:
    """Extract specific high-value pages for testing"""

    def __init__(self):
        self.api_key = os.getenv("FIRECRAWL_API_KEY")
        if not self.api_key:
            raise ValueError("FIRECRAWL_API_KEY not found in environment")

        self.base_url = "https://api.firecrawl.dev/v0"
        self.headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        # Output directory
        self.output_dir = Path(__file__).parent / "raw_extractions"
        self.output_dir.mkdir(exist_ok=True)

        # High-value target URLs for testing
        self.target_urls = {
            # Essential Cardano - FAQ (commonly asked questions)
            "essentialcardano.io": [
                "https://www.essentialcardano.io/faq",
                "https://www.essentialcardano.io/glossary",
            ],

            # Cardano Docs - Core information
            "docs.cardano.org": [
                "https://docs.cardano.org/about-cardano/introduction",
                "https://docs.cardano.org/new-to-cardano/what-is-a-blockchain",
                "https://docs.cardano.org/learn/what-is-cardano",
            ],

            # Developer Portal - Getting started
            "developers.cardano.org": [
                "https://developers.cardano.org/docs/get-started/",
                "https://developers.cardano.org/docs/integrate-cardano/",
            ]
        }

    def extract_url(self, url: str, category: str) -> dict:
        """Extract content from a single URL"""
        print(f"🔍 Extracting: {url}")

        payload = {
            "url": url,
            "formats": ["markdown", "html"],
            "includeTags": ["title", "meta"],
            "onlyMainContent": True,
            "timeout": 30000
        }

        try:
            response = requests.post(
                f"{self.base_url}/scrape",
                headers=self.headers,
                json=payload,
                timeout=45
            )

            if response.status_code != 200:
                print(f"❌ HTTP {response.status_code}: {response.text[:200]}")
                return None

            data = response.json()

            if not data.get("success"):
                print(f"❌ Extraction failed: {data.get('error', 'Unknown error')}")
                return None

            result = data.get("data", {})

            # Organize extracted content
            extracted_content = {
                "test_info": {
                    "category": category,
                    "target_url": url,
                    "extracted_at": datetime.now().isoformat(),
                    "test_purpose": "Focused test for URL accuracy and content quality"
                },
                "url_info": {
                    "requested_url": url,
                    "final_url": result.get("metadata", {}).get("canonical", url),
                    "status": "success"
                },
                "metadata": {
                    "title": result.get("metadata", {}).get("title", ""),
                    "description": result.get("metadata", {}).get("description", ""),
                    "author": result.get("metadata", {}).get("author", ""),
                    "keywords": result.get("metadata", {}).get("keywords", ""),
                    "og_title": result.get("metadata", {}).get("ogTitle", ""),
                    "og_description": result.get("metadata", {}).get("ogDescription", "")
                },
                "content": {
                    "markdown": result.get("markdown", ""),
                    "html": result.get("html", ""),
                    "text_length": len(result.get("markdown", "")),
                    "html_length": len(result.get("html", ""))
                },
                "links": {
                    "internal_links": [],
                    "external_links": [],
                    "total_links": len(result.get("linksOnPage", []))
                },
                "extraction_quality": {
                    "has_title": bool(result.get("metadata", {}).get("title")),
                    "has_content": len(result.get("markdown", "")) > 100,
                    "has_links": len(result.get("linksOnPage", [])) > 0,
                    "content_score": "high" if len(result.get("markdown", "")) > 1000 else "medium" if len(result.get("markdown", "")) > 500 else "low"
                }
            }

            # Categorize links
            all_links = result.get("linksOnPage", [])
            for link in all_links:
                if any(domain in link for domain in ["essentialcardano.io", "docs.cardano.org", "developers.cardano.org"]):
                    extracted_content["links"]["internal_links"].append(link)
                else:
                    extracted_content["links"]["external_links"].append(link)

            print(f"✅ Success: {extracted_content['content']['text_length']} chars, {len(all_links)} links")
            return extracted_content

        except Exception as e:
            print(f"❌ Error extracting {url}: {e}")
            return None

    def save_extraction(self, content: dict, url: str, category: str):
        """Save extracted content to JSON file"""
        # Create safe filename
        safe_url = url.replace("https://", "").replace("http://", "")
        safe_url = safe_url.replace("/", "_").replace("?", "_").replace("&", "_").replace("#", "_")

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{category}_{safe_url}_{timestamp}.json"

        filepath = self.output_dir / filename

        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(content, f, indent=2, ensure_ascii=False)

        print(f"💾 Saved: {filepath.name}")
        return filepath

    def extract_all_test_content(self):
        """Extract all target URLs for the focused test"""
        print("🧪 Starting Focused Test Content Extraction")
        print("=" * 60)
        print(f"Output directory: {self.output_dir}")
        print(f"Total target URLs: {sum(len(urls) for urls in self.target_urls.values())}")
        print()

        results = {
            "extraction_summary": {
                "started_at": datetime.now().isoformat(),
                "total_targets": sum(len(urls) for urls in self.target_urls.values()),
                "successful_extractions": 0,
                "failed_extractions": 0,
                "extracted_files": []
            },
            "results_by_site": {}
        }

        for category, urls in self.target_urls.items():
            print(f"📂 Processing {category}")
            site_results = []

            for url in urls:
                content = self.extract_url(url, category)

                if content:
                    filepath = self.save_extraction(content, url, category)
                    results["extraction_summary"]["successful_extractions"] += 1
                    results["extraction_summary"]["extracted_files"].append(str(filepath.name))

                    site_results.append({
                        "url": url,
                        "status": "success",
                        "file": filepath.name,
                        "content_length": content["content"]["text_length"],
                        "quality_score": content["extraction_quality"]["content_score"]
                    })
                else:
                    results["extraction_summary"]["failed_extractions"] += 1
                    site_results.append({
                        "url": url,
                        "status": "failed",
                        "file": None
                    })

                # Rate limiting
                time.sleep(2)

            results["results_by_site"][category] = site_results
            print()

        # Save extraction summary
        results["extraction_summary"]["completed_at"] = datetime.now().isoformat()
        summary_file = self.output_dir / f"extraction_summary_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"

        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

        # Print final summary
        print("🎉 Extraction Complete!")
        print(f"✅ Successful: {results['extraction_summary']['successful_extractions']}")
        print(f"❌ Failed: {results['extraction_summary']['failed_extractions']}")
        print(f"📁 Files saved in: {self.output_dir}")
        print(f"📊 Summary: {summary_file.name}")

        return results

def main():
    """Main execution function"""
    try:
        extractor = FocusedTestExtractor()
        results = extractor.extract_all_test_content()

        print("\n🎯 Next Steps:")
        print("1. Review extracted content in raw_extractions/")
        print("2. Proceed to step 2-processing/ to clean and organize content")
        print("3. Upload processed content to Globant Enterprise")
        print("4. Test AI Assistant responses in step 4-testing/")

        return True

    except Exception as e:
        print(f"❌ Extraction failed: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)