#!/usr/bin/env python3
"""
Tavily Content Processor
Experiment with processing Tavily's raw content to create clean, usable content for RAG
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional
from dataclasses import dataclass

@dataclass
class ProcessedContent:
    """Cleaned and structured content from Tavily extraction"""
    url: str
    title: str
    main_content: str
    content_type: str
    sections: List[Dict]
    links: List[Dict]
    metadata: Dict
    quality_score: float

class TavilyContentProcessor:
    """Process and clean Tavily extracted content for RAG optimization"""

    def __init__(self):
        # Navigation and UI elements to remove
        self.noise_patterns = [
            r"Opens in a new window",
            r"Opens an external website",
            r"This website utilizes technologies such as cookies",
            r"Privacy Policy.*?Cookie Policy",
            r"Skip to content",
            r"\[Home\]\(/\)",
            r"\d+ up votes and \d+ down votes\. Total score",
            r"Resources\s*Legal\s*Subscribe to our newsletter",
            r"Refine by:\s*Sort by:",
        ]

        # Content patterns to identify valuable sections
        self.content_patterns = {
            'faq_item': r'## \[([^\]]+)\]\([^)]+\)\s*([^#]+?)(?=##|\Z)',
            'article_title': r'## \[([^\]]+)\]\([^)]+\)',
            'glossary_term': r'## ([A-Za-z][^#\n]+)',
            'development_update': r'## \[Weekly development report[^\]]+\]\([^)]+\)\s*([^#]+?)(?=##|\Z)',
        }

        # Tag extraction patterns
        self.tag_pattern = r'\[([^\]]+)\]\(/search\?tags=([^)]+)\)'

    def process_tavily_results(self, tavily_response: Dict) -> List[ProcessedContent]:
        """Process full Tavily API response"""
        processed_results = []

        for result in tavily_response.get('results', []):
            if result.get('raw_content'):
                processed = self.process_single_content(
                    url=result.get('url', ''),
                    raw_content=result.get('raw_content', ''),
                    title=result.get('title', '')
                )
                if processed:
                    processed_results.append(processed)

        return processed_results

    def process_single_content(self, url: str, raw_content: str, title: str = '') -> Optional[ProcessedContent]:
        """Process single piece of Tavily content"""

        # Determine content type from URL
        content_type = self._determine_content_type(url)

        # Clean the content
        cleaned_content = self._clean_raw_content(raw_content)

        # Extract structured information based on content type
        if content_type == 'faq':
            return self._process_faq_content(url, cleaned_content, title)
        elif content_type == 'glossary':
            return self._process_glossary_content(url, cleaned_content, title)
        elif content_type == 'article':
            return self._process_article_content(url, cleaned_content, title)
        elif content_type == 'development_update':
            return self._process_development_update_content(url, cleaned_content, title)
        else:
            return self._process_generic_content(url, cleaned_content, title, content_type)

    def _determine_content_type(self, url: str) -> str:
        """Determine content type from URL"""
        if '/faq' in url:
            return 'faq'
        elif '/glossary' in url:
            return 'glossary'
        elif '/article' in url:
            return 'article'
        elif '/development-update' in url:
            return 'development_update'
        elif '/video' in url:
            return 'video'
        elif '/infographic' in url:
            return 'infographic'
        elif '/developer' in url:
            return 'developer'
        else:
            return 'other'

    def _clean_raw_content(self, raw_content: str) -> str:
        """Remove noise and UI elements from raw content"""
        cleaned = raw_content

        # Remove noise patterns
        for pattern in self.noise_patterns:
            cleaned = re.sub(pattern, '', cleaned, flags=re.IGNORECASE | re.DOTALL)

        # Remove excessive whitespace
        cleaned = re.sub(r'\n\s*\n\s*\n+', '\n\n', cleaned)
        cleaned = re.sub(r'[ \t]+', ' ', cleaned)

        # Remove navigation menu items (but keep main content links)
        lines = cleaned.split('\n')
        filtered_lines = []

        for line in lines:
            line = line.strip()
            # Skip lines that are just navigation
            if (line.startswith('[') and line.endswith(']') and
                any(nav in line.lower() for nav in ['all', 'articles', 'videos', 'faqs', 'infographics'])):
                continue
            # Skip pagination and filter lines
            if re.match(r'^\d+\s+Results?$', line) or 'Refine by:' in line or 'Sort by:' in line:
                continue
            if line:
                filtered_lines.append(line)

        return '\n'.join(filtered_lines)

    def _process_faq_content(self, url: str, content: str, title: str) -> ProcessedContent:
        """Process FAQ page content"""
        sections = []

        # Extract individual FAQ items
        faq_matches = re.finditer(self.content_patterns['faq_item'], content, re.MULTILINE | re.DOTALL)

        for match in faq_matches:
            question = match.group(1).strip()
            answer = match.group(2).strip()

            # Clean up answer text
            answer = re.sub(r'\s+', ' ', answer)
            answer = re.sub(r'^\s*[^A-Za-z0-9]+\s*', '', answer)  # Remove leading symbols

            if len(answer) > 50:  # Only include substantial answers
                sections.append({
                    'type': 'faq_item',
                    'question': question,
                    'answer': answer,
                    'tags': self._extract_tags(answer)
                })

        # Extract main content (remove individual FAQs for summary)
        main_content = f"Essential Cardano FAQ containing {len(sections)} frequently asked questions covering topics like staking, wallets, governance, and Cardano blockchain fundamentals."

        # Add top questions as preview
        if sections:
            top_questions = [s['question'] for s in sections[:5]]
            main_content += f"\n\nTop questions include: {', '.join(top_questions)}"

        return ProcessedContent(
            url=url,
            title=title or "Essential Cardano FAQ",
            main_content=main_content,
            content_type='faq',
            sections=sections,
            links=self._extract_links(content),
            metadata={'total_faqs': len(sections)},
            quality_score=self._calculate_quality_score(content, sections)
        )

    def _process_glossary_content(self, url: str, content: str, title: str) -> ProcessedContent:
        """Process glossary page content"""
        sections = []

        # Extract glossary terms
        term_matches = re.finditer(self.content_patterns['glossary_term'], content, re.MULTILINE)

        for match in term_matches:
            term = match.group(1).strip()
            if len(term) < 50 and not any(skip in term.lower() for skip in ['resources', 'legal', 'subscribe']):
                sections.append({
                    'type': 'glossary_term',
                    'term': term,
                    'definition': f"Cardano-related term: {term}"
                })

        main_content = f"Essential Cardano Glossary containing definitions for {len(sections)} blockchain and Cardano-specific terms."

        if sections:
            sample_terms = [s['term'] for s in sections[:10]]
            main_content += f"\n\nIncluded terms: {', '.join(sample_terms)}"

        return ProcessedContent(
            url=url,
            title=title or "Essential Cardano Glossary",
            main_content=main_content,
            content_type='glossary',
            sections=sections,
            links=self._extract_links(content),
            metadata={'total_terms': len(sections)},
            quality_score=self._calculate_quality_score(content, sections)
        )

    def _process_article_content(self, url: str, content: str, title: str) -> ProcessedContent:
        """Process article listing page content"""
        sections = []

        # Extract article titles and descriptions
        article_matches = re.finditer(self.content_patterns['article_title'], content, re.MULTILINE)

        for match in article_matches:
            article_title = match.group(1).strip()
            sections.append({
                'type': 'article_reference',
                'title': article_title
            })

        main_content = f"Essential Cardano Articles section containing {len(sections)} educational articles covering blockchain technology, Cardano development, and ecosystem updates."

        if sections:
            recent_articles = [s['title'] for s in sections[:5]]
            main_content += f"\n\nRecent articles include: {', '.join(recent_articles)}"

        return ProcessedContent(
            url=url,
            title=title or "Essential Cardano Articles",
            main_content=main_content,
            content_type='article',
            sections=sections,
            links=self._extract_links(content),
            metadata={'total_articles': len(sections)},
            quality_score=self._calculate_quality_score(content, sections)
        )

    def _process_development_update_content(self, url: str, content: str, title: str) -> ProcessedContent:
        """Process development update listing"""
        sections = []

        # Extract development update titles
        update_matches = re.finditer(self.content_patterns['development_update'], content, re.MULTILINE | re.DOTALL)

        for match in update_matches:
            update_title = match.group(0).split('\n')[0]  # Get first line as title
            update_content = match.group(1).strip()[:500]  # First 500 chars of content

            sections.append({
                'type': 'development_update',
                'title': update_title,
                'summary': update_content
            })

        main_content = f"Cardano Weekly Development Reports providing regular updates on ecosystem progress, featuring {len(sections)} recent reports."

        return ProcessedContent(
            url=url,
            title=title or "Cardano Development Updates",
            main_content=main_content,
            content_type='development_update',
            sections=sections,
            links=self._extract_links(content),
            metadata={'total_updates': len(sections)},
            quality_score=self._calculate_quality_score(content, sections)
        )

    def _process_generic_content(self, url: str, content: str, title: str, content_type: str) -> ProcessedContent:
        """Process other content types"""
        # Extract first meaningful paragraph as main content
        lines = content.split('\n')
        main_content = ""

        for line in lines:
            line = line.strip()
            if len(line) > 100 and not line.startswith('[') and not line.startswith('#'):
                main_content = line[:500]
                break

        if not main_content:
            main_content = f"Essential Cardano {content_type} content from {url}"

        return ProcessedContent(
            url=url,
            title=title or f"Essential Cardano {content_type.title()}",
            main_content=main_content,
            content_type=content_type,
            sections=[],
            links=self._extract_links(content),
            metadata={},
            quality_score=self._calculate_quality_score(content, [])
        )

    def _extract_tags(self, text: str) -> List[str]:
        """Extract tags from content"""
        tags = []
        tag_matches = re.finditer(self.tag_pattern, text)

        for match in tag_matches:
            tag = match.group(1)
            if len(tag) < 30:  # Reasonable tag length
                tags.append(tag)

        return list(set(tags))  # Remove duplicates

    def _extract_links(self, content: str) -> List[Dict]:
        """Extract meaningful links from content"""
        links = []

        # Extract markdown links
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        link_matches = re.finditer(link_pattern, content)

        for match in link_matches:
            link_text = match.group(1)
            link_url = match.group(2)

            # Skip navigation and UI links
            if not any(skip in link_text.lower() for skip in ['home', 'all', 'articles', 'videos']):
                links.append({
                    'text': link_text,
                    'url': link_url
                })

        return links[:20]  # Limit to top 20 links

    def _calculate_quality_score(self, content: str, sections: List[Dict]) -> float:
        """Calculate content quality score (0-1)"""
        score = 0.0

        # Base score for having content
        if len(content) > 100:
            score += 0.3

        # Score for structured sections
        if sections:
            score += min(0.4, len(sections) * 0.05)

        # Score for content length and substance
        if len(content) > 1000:
            score += 0.2

        # Score for having FAQ items or articles
        if any(s.get('type') in ['faq_item', 'article_reference'] for s in sections):
            score += 0.1

        return min(1.0, score)

    def create_globant_ready_files(self, processed_contents: List[ProcessedContent], output_dir: str = "tavily_processed"):
        """Create individual files ready for Globant upload"""
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        for content in processed_contents:
            # Create filename from URL
            filename = content.url.replace("https://", "").replace("http://", "")
            filename = filename.replace("/", "_").replace("?", "_").replace("&", "_")
            filename = f"{filename}.json"

            # Create content for Globant
            globant_content = {
                'url': content.url,
                'title': content.title,
                'content': content.main_content,
                'content_type': content.content_type,
                'sections': content.sections,
                'metadata': {
                    **content.metadata,
                    'quality_score': content.quality_score,
                    'links_count': len(content.links),
                    'sections_count': len(content.sections)
                },
                'processed_with': 'tavily_content_processor',
                'source': 'essentialcardano.io'
            }

            # Save to file
            filepath = output_path / filename
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(globant_content, f, indent=2, ensure_ascii=False)

            print(f"✅ Processed: {content.title} (Quality: {content.quality_score:.2f})")

def main():
    """Test the processor with our Tavily results"""
    processor = TavilyContentProcessor()

    # Load test results
    test_file = Path("tavily_test_results/tavily_basic_test.json")
    if not test_file.exists():
        print("❌ No test results found. Run test_tavily.py first.")
        return

    with open(test_file, 'r', encoding='utf-8') as f:
        test_data = json.load(f)

    print("🔄 Processing Tavily test results...")

    # Process the content
    processed_results = processor.process_tavily_results(test_data['api_response'])

    print(f"\n📊 PROCESSING RESULTS:")
    print(f"   Input URLs: {len(test_data['test_urls'])}")
    print(f"   Processed results: {len(processed_results)}")

    for result in processed_results:
        print(f"\n📄 {result.title}")
        print(f"   Type: {result.content_type}")
        print(f"   Quality: {result.quality_score:.2f}")
        print(f"   Sections: {len(result.sections)}")
        print(f"   Content preview: {result.main_content[:100]}...")

    # Create Globant-ready files
    processor.create_globant_ready_files(processed_results)
    print(f"\n✅ Created Globant-ready files in tavily_processed/")

if __name__ == "__main__":
    main()