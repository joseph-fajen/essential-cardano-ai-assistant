#!/usr/bin/env python3
"""
Process extracted content for Globant upload
Clean, organize, and format content for optimal RAG performance
"""

import json
import re
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class ContentProcessor:
    """Process raw extractions for Globant RAG Assistant"""

    def __init__(self):
        self.input_dir = Path(__file__).parent.parent / "1-extraction" / "raw_extractions"
        self.output_dir = Path(__file__).parent / "processed_content"
        self.output_dir.mkdir(exist_ok=True)

    def clean_markdown_content(self, content: str) -> str:
        """Clean and optimize markdown content for RAG"""
        if not content:
            return ""

        # Remove navigation elements
        content = re.sub(r'\[Skip to main content\].*?\n', '', content)
        content = re.sub(r'Search\.\.\.', '', content)

        # Clean up excessive whitespace
        content = re.sub(r'\n{3,}', '\n\n', content)
        content = content.strip()

        # Remove footer content (privacy policies, etc.)
        footer_patterns = [
            r'This work is licensed under.*$',
            r'© IOHK.*$',
            r'Cardano is an open-source project\..*$',
            r'Subscribe to our newsletter.*$'
        ]

        for pattern in footer_patterns:
            content = re.sub(pattern, '', content, flags=re.MULTILINE | re.DOTALL)

        return content.strip()

    def extract_key_sections(self, content: str) -> Dict[str, str]:
        """Extract key sections from content"""
        sections = {}

        # Try to find main heading
        title_match = re.search(r'^# (.+)$', content, re.MULTILINE)
        if title_match:
            sections['title'] = title_match.group(1)

        # Extract introduction paragraph
        lines = content.split('\n')
        intro_started = False
        intro_lines = []

        for line in lines:
            if line.startswith('# ') or line.startswith('## '):
                if intro_started:
                    break
                if line.startswith('# '):
                    intro_started = True
                continue

            if intro_started and line.strip():
                if line.startswith('#'):
                    break
                intro_lines.append(line)

        if intro_lines:
            sections['introduction'] = '\n'.join(intro_lines).strip()

        return sections

    def process_single_file(self, filepath: Path) -> Dict:
        """Process a single extracted content file"""
        print(f"📝 Processing: {filepath.name}")

        with open(filepath, 'r', encoding='utf-8') as f:
            raw_data = json.load(f)

        # Clean the content
        clean_content = self.clean_markdown_content(raw_data.get('content', {}).get('markdown', ''))
        sections = self.extract_key_sections(clean_content)

        # Create processed content structure
        processed = {
            "source_info": {
                "original_url": raw_data.get('url_info', {}).get('final_url', ''),
                "site_category": raw_data.get('test_info', {}).get('category', ''),
                "extraction_date": raw_data.get('test_info', {}).get('extracted_at', ''),
                "processing_date": datetime.now().isoformat()
            },
            "metadata": {
                "title": raw_data.get('metadata', {}).get('title', ''),
                "description": raw_data.get('metadata', {}).get('description', ''),
                "canonical_url": raw_data.get('url_info', {}).get('final_url', ''),
                "content_type": self.determine_content_type(raw_data),
                "content_quality": raw_data.get('extraction_quality', {}).get('content_score', 'unknown')
            },
            "content": {
                "title": sections.get('title', raw_data.get('metadata', {}).get('title', '')),
                "introduction": sections.get('introduction', ''),
                "full_content": clean_content,
                "word_count": len(clean_content.split()),
                "char_count": len(clean_content)
            },
            "links": {
                "internal_links": raw_data.get('links', {}).get('internal_links', []),
                "external_links": raw_data.get('links', {}).get('external_links', [])[:10],  # Limit external links
                "source_url": raw_data.get('url_info', {}).get('final_url', '')
            },
            "rag_optimization": {
                "chunk_size": "optimal" if len(clean_content) < 4000 else "large",
                "contains_faq": "faq" in raw_data.get('url_info', {}).get('final_url', '').lower(),
                "contains_glossary": "glossary" in raw_data.get('url_info', {}).get('final_url', '').lower(),
                "priority": self.determine_priority(raw_data)
            }
        }

        return processed

    def determine_content_type(self, raw_data: Dict) -> str:
        """Determine the type of content"""
        url = raw_data.get('url_info', {}).get('final_url', '').lower()

        if 'faq' in url:
            return 'faq'
        elif 'glossary' in url:
            return 'glossary'
        elif 'introduction' in url or 'what-is' in url:
            return 'introduction'
        elif 'get-started' in url or 'getting-started' in url:
            return 'getting_started'
        elif 'integrate' in url:
            return 'integration_guide'
        else:
            return 'documentation'

    def determine_priority(self, raw_data: Dict) -> str:
        """Determine content priority for RAG"""
        url = raw_data.get('url_info', {}).get('final_url', '').lower()
        content_length = raw_data.get('content', {}).get('text_length', 0)

        # High priority: FAQ, glossary, introductions
        if any(term in url for term in ['faq', 'glossary', 'introduction', 'what-is']):
            return 'high'

        # Medium priority: Getting started guides
        if any(term in url for term in ['get-started', 'getting-started']):
            return 'medium'

        # Priority based on content length and quality
        if content_length > 2000:
            return 'medium'
        elif content_length > 500:
            return 'low'
        else:
            return 'very_low'

    def create_globant_upload_format(self, processed_files: List[Dict]) -> Dict:
        """Create optimized format for Globant upload"""
        upload_data = {
            "knowledge_base_info": {
                "name": "Essential Cardano Focused Test",
                "description": "Curated content from Essential Cardano, Cardano Docs, and Developer Portal for testing URL accuracy and content quality",
                "created_at": datetime.now().isoformat(),
                "content_sources": list(set(item['source_info']['site_category'] for item in processed_files)),
                "total_documents": len(processed_files)
            },
            "documents": []
        }

        for item in processed_files:
            # Create document optimized for RAG
            document = {
                "id": f"cardano_{item['source_info']['site_category']}_{datetime.now().strftime('%Y%m%d')}_{len(upload_data['documents'])}",
                "title": item['content']['title'],
                "content": item['content']['full_content'],
                "metadata": {
                    "source_url": item['source_info']['original_url'],
                    "source_site": item['source_info']['site_category'],
                    "content_type": item['metadata']['content_type'],
                    "priority": item['rag_optimization']['priority'],
                    "word_count": item['content']['word_count'],
                    "extraction_date": item['source_info']['extraction_date']
                },
                "tags": [
                    item['metadata']['content_type'],
                    item['source_info']['site_category'].replace('.', '_'),
                    item['rag_optimization']['priority'] + '_priority'
                ]
            }

            upload_data["documents"].append(document)

        return upload_data

    def process_all_extractions(self):
        """Process all extracted content files"""
        print("🔄 Starting Content Processing")
        print("=" * 50)

        extraction_files = list(self.input_dir.glob("*.json"))
        if not extraction_files:
            print("❌ No extraction files found!")
            return False

        # Exclude summary files
        content_files = [f for f in extraction_files if not f.name.startswith('extraction_summary')]

        print(f"📁 Found {len(content_files)} content files to process")

        processed_files = []

        for filepath in content_files:
            try:
                processed = self.process_single_file(filepath)
                processed_files.append(processed)

                # Save individual processed file
                output_name = filepath.stem + "_processed.json"
                output_path = self.output_dir / output_name

                with open(output_path, 'w', encoding='utf-8') as f:
                    json.dump(processed, f, indent=2, ensure_ascii=False)

                print(f"✅ Saved: {output_name}")

            except Exception as e:
                print(f"❌ Error processing {filepath.name}: {e}")

        # Create Globant upload format
        if processed_files:
            upload_data = self.create_globant_upload_format(processed_files)

            upload_path = self.output_dir.parent / "3-upload" / "globant_ready" / "focused_test_knowledge_base.json"
            upload_path.parent.mkdir(parents=True, exist_ok=True)

            with open(upload_path, 'w', encoding='utf-8') as f:
                json.dump(upload_data, f, indent=2, ensure_ascii=False)

            print(f"\n🎯 Globant Upload Ready!")
            print(f"📄 Processed {len(processed_files)} documents")
            print(f"📁 Upload file: {upload_path}")

        return True

def main():
    """Main execution function"""
    processor = ContentProcessor()
    success = processor.process_all_extractions()

    if success:
        print("\n✅ Processing Complete!")
        print("🎯 Next Steps:")
        print("1. Review processed content in processed_content/")
        print("2. Upload focused_test_knowledge_base.json to Globant Enterprise")
        print("3. Create RAG Assistant with uploaded content")
        print("4. Run test scenarios in step 4-testing/")
    else:
        print("\n❌ Processing failed!")

if __name__ == "__main__":
    main()