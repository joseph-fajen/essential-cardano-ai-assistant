#!/usr/bin/env python3
"""
Enhanced Processing: Create Individual Files for Better Citations
Split content into separate files for granular source attribution in Globant
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class IndividualFileProcessor:
    """Create individual files for each document to improve citations"""

    def __init__(self):
        self.input_dir = Path(__file__).parent.parent / "1-extraction" / "raw_extractions"
        self.output_dir = Path(__file__).parent / "individual_files"
        self.upload_dir = Path(__file__).parent.parent / "3-upload" / "globant_ready"

        # Create output directories
        self.output_dir.mkdir(exist_ok=True)
        self.upload_dir.mkdir(exist_ok=True)

    def clean_content_for_citation(self, content: str) -> str:
        """Clean content while preserving readability for citations"""
        if not content:
            return ""

        # Remove navigation but keep main content structure
        content = re.sub(r'\[Skip to main content\].*?\n', '', content)
        content = re.sub(r'Search\.\.\.', '', content)

        # Remove excessive navigation lists but keep important links
        content = re.sub(r'^\- \[.*?\]\(.*?\)$', '', content, flags=re.MULTILINE)

        # Clean up whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip()

        # Remove footer content
        footer_patterns = [
            r'This work is licensed under.*$',
            r'© IOHK.*$',
            r'Cardano is an open-source project\..*$',
            r'Follow us.*?Reddit.*?\n',
            r'Join the community.*?Academy.*?\n'
        ]

        for pattern in footer_patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)

        return content.strip()

    def create_citation_friendly_name(self, raw_data: Dict) -> str:
        """Create human-readable name for better citations"""
        url = raw_data.get('url_info', {}).get('final_url', '').lower()
        title = raw_data.get('metadata', {}).get('title', '')

        # Create descriptive names based on content
        if 'essentialcardano.io/faq' in url:
            return "Essential_Cardano_FAQ"
        elif 'essentialcardano.io/glossary' in url:
            return "Essential_Cardano_Glossary"
        elif 'docs.cardano.org/about-cardano/introduction' in url:
            return "Cardano_Docs_Introduction"
        elif 'docs.cardano.org/new-to-cardano/what-is-a-blockchain' in url:
            return "Cardano_Docs_What_is_Blockchain"
        elif 'docs.cardano.org/learn/what-is-cardano' in url:
            return "Cardano_Docs_What_is_Cardano"
        elif 'developers.cardano.org/docs/get-started' in url:
            return "Developer_Portal_Getting_Started"
        elif 'developers.cardano.org/docs/integrate-cardano' in url:
            return "Developer_Portal_Integration_Guide"
        else:
            # Fallback: create name from title
            safe_title = re.sub(r'[^\w\s-]', '', title)
            safe_title = re.sub(r'\s+', '_', safe_title)
            return safe_title[:50] if safe_title else "Unknown_Document"

    def create_display_title(self, raw_data: Dict, citation_name: str) -> str:
        """Create user-friendly display title"""
        title_map = {
            "Essential_Cardano_FAQ": "Essential Cardano FAQ",
            "Essential_Cardano_Glossary": "Essential Cardano Glossary",
            "Cardano_Docs_Introduction": "Cardano Documentation - Introduction",
            "Cardano_Docs_What_is_Blockchain": "Cardano Documentation - What is a Blockchain",
            "Cardano_Docs_What_is_Cardano": "Cardano Documentation - What is Cardano",
            "Developer_Portal_Getting_Started": "Cardano Developer Portal - Getting Started",
            "Developer_Portal_Integration_Guide": "Cardano Developer Portal - Integration Guide"
        }

        return title_map.get(citation_name, raw_data.get('metadata', {}).get('title', 'Cardano Documentation'))

    def process_single_file_to_individual(self, filepath: Path) -> Dict:
        """Process single extraction file into individual citation-friendly document"""
        print(f"📝 Processing: {filepath.name}")

        with open(filepath, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # Create citation-friendly identifiers
        citation_name = self.create_citation_friendly_name(raw_data)
        display_title = self.create_display_title(raw_data, citation_name)

        # Clean content
        clean_content = self.clean_content_for_citation(raw_data.get('content', {}).get('markdown', ''))

        # Create individual document structure
        document = {
            "document_info": {
                "id": citation_name.lower(),
                "citation_name": citation_name,
                "display_title": display_title,
                "content_type": self.determine_content_type(raw_data),
                "created_at": datetime.now().isoformat()
            },
            "source": {
                "original_url": raw_data.get('url_info', {}).get('final_url', ''),
                "site": raw_data.get('test_info', {}).get('category', ''),
                "extraction_date": raw_data.get('test_info', {}).get('extracted_at', '')
            },
            "metadata": {
                "title": display_title,
                "description": raw_data.get('metadata', {}).get('description', ''),
                "canonical_url": raw_data.get('url_info', {}).get('final_url', ''),
                "word_count": len(clean_content.split()),
                "content_quality": self.assess_content_quality(clean_content)
            },
            "content": clean_content,
            "tags": [
                citation_name.lower(),
                raw_data.get('test_info', {}).get('category', '').replace('.', '_'),
                self.determine_content_type(raw_data),
                "essential_cardano_focused_test"
            ]
        }

        return document

    def determine_content_type(self, raw_data: Dict) -> str:
        """Determine content type for tagging"""
        url = raw_data.get('url_info', {}).get('final_url', '').lower()

        if 'faq' in url:
            return 'faq'
        elif 'glossary' in url:
            return 'glossary'
        elif 'introduction' in url:
            return 'introduction'
        elif 'what-is' in url:
            return 'explanation'
        elif 'get-started' in url:
            return 'getting_started'
        elif 'integrate' in url:
            return 'integration_guide'
        else:
            return 'documentation'

    def assess_content_quality(self, content: str) -> str:
        """Assess content quality for prioritization"""
        word_count = len(content.split())

        if word_count > 1500:
            return 'comprehensive'
        elif word_count > 800:
            return 'detailed'
        elif word_count > 300:
            return 'standard'
        else:
            return 'brief'

    def create_individual_files(self):
        """Create individual files for each document"""
        print("🔄 Creating Individual Files for Better Citations")
        print("=" * 60)

        extraction_files = list(self.input_dir.glob("*.json"))
        content_files = [f for f in extraction_files if not f.name.startswith('extraction_summary')]

        print(f"📁 Processing {len(content_files)} documents into individual files")

        individual_files = []
        upload_files_created = []

        for filepath in content_files:
            try:
                # Process into individual document
                document = self.process_single_file_to_individual(filepath)

                # Save individual processed file
                citation_name = document['document_info']['citation_name']
                individual_file = self.output_dir / f"{citation_name}.json"

                with open(individual_file, 'w', encoding='utf-8') as f:
                    json.dump(document, f, indent=2, ensure_ascii=False)

                # Create Globant upload file (single document format)
                upload_file = self.upload_dir / f"{citation_name}.json"

                # Format for Globant upload
                upload_document = {
                    "id": document['document_info']['id'],
                    "title": document['metadata']['title'],
                    "content": document['content'],
                    "metadata": {
                        "source_url": document['source']['original_url'],
                        "source_site": document['source']['site'],
                        "content_type": document['document_info']['content_type'],
                        "word_count": document['metadata']['word_count'],
                        "quality": document['metadata']['content_quality']
                    },
                    "tags": document['tags']
                }

                with open(upload_file, 'w', encoding='utf-8') as f:
                    json.dump(upload_document, f, indent=2, ensure_ascii=False)

                individual_files.append({
                    "citation_name": citation_name,
                    "display_title": document['metadata']['title'],
                    "source_url": document['source']['original_url'],
                    "file_size": individual_file.stat().st_size,
                    "word_count": document['metadata']['word_count']
                })

                upload_files_created.append(upload_file.name)

                print(f"✅ Created: {citation_name}")
                print(f"   📄 Individual: {individual_file.name}")
                print(f"   📤 Upload: {upload_file.name}")

            except Exception as e:
                print(f"❌ Error processing {filepath.name}: {e}")

        # Create summary
        summary = {
            "processing_info": {
                "created_at": datetime.now().isoformat(),
                "total_documents": len(individual_files),
                "approach": "individual_files_for_better_citations"
            },
            "upload_instructions": {
                "method": "upload_each_file_separately",
                "location": str(self.upload_dir),
                "files": upload_files_created,
                "expected_citations": [doc['citation_name'] for doc in individual_files]
            },
            "documents": individual_files
        }

        summary_file = self.output_dir / "individual_files_summary.json"
        with open(summary_file, 'w', encoding='utf-8') as f:
            json.dump(summary, f, indent=2, ensure_ascii=False)

        print(f"\n🎯 Individual Files Created!")
        print(f"📁 Individual files: {self.output_dir}")
        print(f"📤 Upload files: {self.upload_dir}")
        print(f"📊 Summary: {summary_file.name}")

        print(f"\n📋 Upload Instructions:")
        print("1. Upload each file in globant_ready/ separately to Globant")
        print("2. Each file will appear as distinct source in citations")
        print("3. Expected citations:")
        for doc in individual_files:
            print(f"   - {doc['citation_name']}")

        print(f"\n🎯 This should give you granular citations instead of 'focused_test_knowledge_base.json'!")

        return summary

def main():
    """Main execution function"""
    processor = IndividualFileProcessor()
    summary = processor.create_individual_files()

    print("\n✅ Enhanced Processing Complete!")
    print("🎯 Ready to test improved citations with individual file uploads!")

if __name__ == "__main__":
    main()