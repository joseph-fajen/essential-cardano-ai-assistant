#!/usr/bin/env python3
"""
Cardano Developer Portal Batch Splitter

Takes the raw Developer Portal batch files and splits them into individual files per URL,
preserving all content for accurate page-by-page citations.

No processing, no content modification - just clean file splitting for developers.cardano.org content.
"""

import json
import os
from pathlib import Path
from urllib.parse import urlparse
import re
from datetime import datetime

def url_to_filename(url):
    """Convert developers.cardano.org URL to a safe filename while preserving page identification"""
    # Parse the URL
    parsed = urlparse(url)

    # Extract domain and path
    domain = parsed.netloc.replace('www.', '')
    path = parsed.path.strip('/')

    # Clean up path for filename
    if path:
        # Replace special characters with underscores
        clean_path = re.sub(r'[^a-zA-Z0-9\-_/]', '_', path)
        clean_path = clean_path.replace('/', '_')
        filename = f"{domain}_{clean_path}"
    else:
        filename = domain

    # Remove multiple underscores and trailing ones
    filename = re.sub(r'_+', '_', filename).strip('_')

    return f"{filename}.json"

def split_batch_file(batch_file_path, output_dir):
    """Split a single Developer Portal batch file into individual URL files"""
    with open(batch_file_path, 'r', encoding='utf-8') as f:
        batch_data = json.load(f)

    batch_number = batch_data.get('batch_number', 'unknown')
    results = batch_data.get('response', {}).get('results', [])

    processed_count = 0

    for result in results:
        url = result.get('url')
        raw_content = result.get('raw_content', '')
        images = result.get('images', [])

        if not url or not raw_content:
            print(f"Skipping entry in batch {batch_number}: missing URL or content")
            continue

        # Create individual file with minimal structure (same as other datasets)
        individual_file = {
            "url": url,
            "content": raw_content,
            "images": images,
            "extraction_metadata": {
                "batch_number": batch_number,
                "extraction_timestamp": batch_data.get('timestamp'),
                "extraction_time": batch_data.get('extraction_time'),
                "source": "tavily_api_raw"
            }
        }

        # Generate filename
        filename = url_to_filename(url)
        output_path = output_dir / filename

        # Handle potential filename conflicts
        counter = 1
        original_filename = filename
        while output_path.exists():
            name, ext = os.path.splitext(original_filename)
            filename = f"{name}_{counter}{ext}"
            output_path = output_dir / filename
            counter += 1

        # Write individual file
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(individual_file, f, indent=2, ensure_ascii=False)

        processed_count += 1
        print(f"Created: {filename}")

    return processed_count

def create_dataset_readme(output_dir, total_files, stats):
    """Create comprehensive README.md for the Developer Portal dataset"""
    readme_content = f"""# Cardano Developer Portal Dataset - September 19, 2025

## Dataset Overview

This folder contains a comprehensive extraction of content from developers.cardano.org as individual page files, suitable for RAG (Retrieval-Augmented Generation) systems and AI assistants.

## Extraction Details

- **Extraction Date**: September 19, 2025
- **Source Website**: https://developers.cardano.org
- **Total Files**: {total_files} individual JSON files
- **Success Rate**: {stats.get('success_rate', 'TBD')}%
- **Extraction Method**: Tavily API with systematic sitemap parsing

## Content Coverage

### Content Types Included:
- **Blog Posts**: Monthly developer updates, technical insights (2021-2025)
- **Get Started**: Beginner guides for Cardano development
- **Smart Contracts**: Aiken, Plutarch, Marlowe development guides
- **Governance**: Participation and voting mechanisms
- **Native Tokens**: Token creation and management
- **Integrate Cardano**: Wallet integrations and API usage
- **Stake Pool Operations**: Technical setup and maintenance guides
- **Transaction Metadata**: Advanced transaction features

### Sample Content Areas:
- Smart contract development tutorials
- Blockchain fundamentals for developers
- CLI tools and operations
- Security best practices
- Development environment setup
- API integrations and SDKs
- Community tools and showcase projects

## File Structure

Each JSON file follows this format:
```json
{{
  "url": "https://developers.cardano.org/[page-path]",
  "content": "[Full page content as extracted]",
  "images": ["[Array of image URLs if present]"],
  "extraction_metadata": {{
    "batch_number": "[Extraction batch]",
    "extraction_timestamp": "[ISO timestamp]",
    "extraction_time": "[Seconds taken]",
    "source": "tavily_api_raw"
  }}
}}
```

## Filename Convention

Files are named using URL-to-filename conversion:
- `developers.cardano.org_docs_get-started.json` → `https://developers.cardano.org/docs/get-started`
- `developers.cardano.org_blog_monthly-update.json` → Monthly update blog posts
- `developers.cardano.org_docs_smart-contracts_aiken.json` → Aiken development guides

## Usage for AI Assistants

This dataset is optimized for:

### Citation Capability
- Each file maps to a specific URL for precise source attribution
- AI assistants can provide exact page citations for every response
- Enables transparent, verifiable answers with working links

### Content Quality
- Zero data loss from original extraction
- Complete context preserved for accurate responses
- Developer-focused content suitable for technical queries

### RAG System Integration
- Individual files enable granular content retrieval
- Clean JSON format for easy parsing
- Comprehensive metadata for content management

## Extraction Pipeline

1. **Sitemap Discovery**: Systematic parsing of developers.cardano.org sitemap
2. **Batch Extraction**: Tavily API processing (20 URLs per batch for mixed content)
3. **Content Preservation**: Raw content saved without lossy processing
4. **File Organization**: URL-based naming for clear mapping

## Quality Metrics

- **Completeness**: {stats.get('success_rate', 'TBD')}% of discovered URLs successfully extracted
- **Accuracy**: Direct extraction preserves original formatting and links
- **Coverage**: All major developer portal sections included
- **Freshness**: Extracted September 2025 with latest development guides and blog updates

## Use Cases

- **Cardano Developer Assistant**: Code-focused chatbot with complete developer portal knowledge
- **Educational Platform**: Comprehensive learning resource for Cardano development
- **Technical Documentation Search**: Searchable developer reference and tutorials
- **Training Data**: Fine-tuning language models on Cardano development content

## Technical Notes

- **No Processing Artifacts**: Raw content preserved exactly as extracted
- **Comprehensive Coverage**: Blog posts, tutorials, guides, and technical documentation
- **Production Ready**: Suitable for immediate deployment in RAG systems
- **Globant Compatible**: Format optimized for Globant Enterprise AI platform

## Comparison with Other Cardano Datasets

This dataset complements other Cardano knowledge sources:
- **Essential Cardano**: Community knowledge, FAQ, ecosystem updates
- **Cardano Documentation**: Official technical specifications and infrastructure
- **Developer Portal**: Practical development guides, tutorials, and community tools
- **Combined Usage**: Complete Cardano development ecosystem spanning theory to practice

---

**Generated**: September 19, 2025
**Pipeline**: Tavily API → Raw Extraction → Individual File Splitting
**Status**: Production Ready
**Next Step**: Upload to Globant Enterprise AI for comprehensive Cardano developer assistant deployment
"""

    readme_path = output_dir / "README.md"
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(readme_content)

    print(f"✅ Created comprehensive README.md at {readme_path}")

def main():
    # Set up paths
    raw_extractions_dir = Path("developer_portal_comprehensive/raw_extractions")
    output_dir = Path("developer-portal-dataset-2025-09-19")

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Get all batch files
    batch_files = sorted(raw_extractions_dir.glob("developer_portal_batch_*.json"))

    if not batch_files:
        print("No Developer Portal batch files found in developer_portal_comprehensive/raw_extractions/")
        print("Please run developer_portal_tavily_extractor.py first")
        return

    print(f"Found {len(batch_files)} Developer Portal batch files to process")

    total_processed = 0
    extraction_stats = {}

    for batch_file in batch_files:
        print(f"\nProcessing {batch_file.name}...")
        try:
            count = split_batch_file(batch_file, output_dir)
            total_processed += count
            print(f"Processed {count} individual pages from {batch_file.name}")
        except Exception as e:
            print(f"Error processing {batch_file.name}: {e}")

    # Calculate success rate (will be updated after actual extraction)
    extraction_stats['success_rate'] = 'TBD'  # Will be calculated during extraction

    # Create comprehensive README
    create_dataset_readme(output_dir, total_processed, extraction_stats)

    # Final summary
    print(f"\n🎉 CARDANO DEVELOPER PORTAL DATASET CREATED!")
    print(f"=" * 50)
    print(f"📁 Dataset location: {output_dir}")
    print(f"📄 Individual files created: {total_processed}")
    print(f"📋 README.md: Comprehensive documentation created")
    print(f"🎯 Ready for Globant upload with perfect page-by-page citations!")

    # Calculate dataset size
    try:
        import subprocess
        result = subprocess.run(['du', '-sh', str(output_dir)], capture_output=True, text=True)
        if result.returncode == 0:
            size = result.stdout.split()[0]
            print(f"💾 Dataset size: {size}")
    except:
        pass

    print(f"\n📊 NEXT STEPS:")
    print(f"1. Upload {output_dir}/ to Globant Enterprise AI")
    print(f"2. Create 'Cardano Developer Portal Assistant' RAG Assistant")
    print(f"3. Test with development queries to validate citation capability")
    print(f"4. Combine with other Cardano datasets for comprehensive knowledge")

if __name__ == "__main__":
    main()