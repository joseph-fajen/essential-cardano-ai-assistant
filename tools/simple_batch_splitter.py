#!/usr/bin/env python3
"""
Simple Batch Splitter for Tavily Raw Extractions

Takes the raw batch files and splits them into individual files per URL,
preserving all content for accurate page-by-page citations.

No processing, no content modification - just clean file splitting.
"""

import json
import os
from pathlib import Path
from urllib.parse import urlparse
import re

def url_to_filename(url):
    """Convert URL to a safe filename while preserving page identification"""
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
    """Split a single batch file into individual URL files"""
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

        # Create individual file with minimal structure
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

def main():
    # Set up paths
    raw_extractions_dir = Path("tavily_comprehensive/raw_extractions")
    output_dir = Path("tavily_comprehensive/individual_pages")

    # Create output directory
    output_dir.mkdir(exist_ok=True)

    # Get all batch files
    batch_files = sorted(raw_extractions_dir.glob("batch_*.json"))

    if not batch_files:
        print("No batch files found in tavily_comprehensive/raw_extractions/")
        return

    print(f"Found {len(batch_files)} batch files to process")

    total_processed = 0

    for batch_file in batch_files:
        print(f"\nProcessing {batch_file.name}...")
        try:
            count = split_batch_file(batch_file, output_dir)
            total_processed += count
            print(f"Processed {count} individual pages from {batch_file.name}")
        except Exception as e:
            print(f"Error processing {batch_file.name}: {e}")

    print(f"\n✅ Total individual page files created: {total_processed}")
    print(f"📁 Output directory: {output_dir}")
    print(f"🎯 Ready for Globant upload with perfect page-by-page citations!")

if __name__ == "__main__":
    main()