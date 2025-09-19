#!/usr/bin/env python3
"""
MDX to TXT Converter for Globant Enterprise Platform

Converts MDX files to TXT format while preserving content structure and metadata.
Handles YAML frontmatter conversion and maintains directory hierarchy.
"""

import os
import re
import yaml
from pathlib import Path
from typing import Dict, Any, Optional

def parse_frontmatter(content: str) -> tuple[Optional[Dict[str, Any]], str]:
    """
    Parse YAML frontmatter from MDX content.
    
    Returns:
        tuple: (frontmatter_dict, content_without_frontmatter)
    """
    # Check if content starts with frontmatter delimiter
    if not content.startswith('---\n'):
        return None, content
    
    # Find the closing delimiter
    parts = content.split('---\n', 2)
    if len(parts) < 3:
        return None, content
    
    try:
        # Parse YAML frontmatter
        frontmatter = yaml.safe_load(parts[1])
        # Return frontmatter and remaining content
        return frontmatter, parts[2]
    except yaml.YAMLError:
        # If YAML parsing fails, return original content
        return None, content

def format_frontmatter_as_text(frontmatter: Dict[str, Any]) -> str:
    """
    Convert YAML frontmatter to readable text headers.
    """
    if not frontmatter:
        return ""
    
    lines = ["# Document Metadata", ""]
    
    for key, value in frontmatter.items():
        # Format key names nicely
        formatted_key = key.replace('_', ' ').replace('-', ' ').title()
        
        if isinstance(value, str):
            lines.append(f"**{formatted_key}:** {value}")
        elif isinstance(value, (int, float)):
            lines.append(f"**{formatted_key}:** {value}")
        elif isinstance(value, list):
            lines.append(f"**{formatted_key}:** {', '.join(str(item) for item in value)}")
        else:
            lines.append(f"**{formatted_key}:** {str(value)}")
    
    lines.extend(["", "---", ""])
    return "\n".join(lines)

def convert_mdx_to_txt(mdx_file_path: Path, output_dir: Path) -> bool:
    """
    Convert a single MDX file to TXT format.
    
    Args:
        mdx_file_path: Path to the source MDX file
        output_dir: Base output directory
        
    Returns:
        bool: True if conversion successful, False otherwise
    """
    try:
        # Read the MDX file
        with open(mdx_file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Parse frontmatter
        frontmatter, markdown_content = parse_frontmatter(content)
        
        # Convert frontmatter to text
        frontmatter_text = format_frontmatter_as_text(frontmatter)
        
        # Combine frontmatter and content
        txt_content = frontmatter_text + markdown_content
        
        # Create output file path (preserve directory structure, change extension)
        # Find the 'docs' directory in the path and create relative path from there
        docs_index = None
        for i, part in enumerate(mdx_file_path.parts):
            if part == 'docs':
                docs_index = i
                break
        
        if docs_index is not None:
            # Create relative path starting after 'docs'
            relative_parts = mdx_file_path.parts[docs_index + 1:]
            relative_path = Path(*relative_parts) if relative_parts else Path(mdx_file_path.name)
        else:
            # Fallback: use filename only if 'docs' not found
            relative_path = Path(mdx_file_path.name)
            
        output_file_path = output_dir / relative_path.with_suffix('.txt')
        
        # Create output directory if it doesn't exist
        output_file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Write the TXT file
        with open(output_file_path, 'w', encoding='utf-8') as f:
            f.write(txt_content)
        
        print(f"✓ Converted: {mdx_file_path.name} → {output_file_path}")
        return True
        
    except Exception as e:
        print(f"✗ Error converting {mdx_file_path}: {str(e)}")
        return False

def batch_convert_mdx_files(source_dir: Path, output_dir: Path) -> Dict[str, int]:
    """
    Batch convert all MDX files in source directory to TXT format.
    
    Args:
        source_dir: Source directory containing MDX files
        output_dir: Output directory for converted TXT files
        
    Returns:
        dict: Statistics about the conversion process
    """
    stats = {"converted": 0, "failed": 0, "total": 0}
    
    # Find all MDX files
    mdx_files = list(source_dir.rglob("*.mdx"))
    stats["total"] = len(mdx_files)
    
    print(f"Found {stats['total']} MDX files to convert...")
    print(f"Source directory: {source_dir}")
    print(f"Output directory: {output_dir}")
    print("-" * 60)
    
    # Convert each file
    for mdx_file in mdx_files:
        if convert_mdx_to_txt(mdx_file, output_dir):
            stats["converted"] += 1
        else:
            stats["failed"] += 1
    
    print("-" * 60)
    print(f"Conversion complete!")
    print(f"Total files: {stats['total']}")
    print(f"Successfully converted: {stats['converted']}")
    print(f"Failed: {stats['failed']}")
    
    return stats

def main():
    """Main function to run the conversion process."""
    import argparse
    
    # Set up command line arguments
    parser = argparse.ArgumentParser(description='Convert MDX files to TXT format for Globant Enterprise')
    parser.add_argument('--source', '-s', 
                       default="/Users/josephfajen/git/cardano-documentation/docs",
                       help='Source directory containing MDX files (default: entire docs directory)')
    parser.add_argument('--output', '-o',
                       default="/Users/josephfajen/git/cardano-documentation/docs-converted",
                       help='Output directory for converted TXT files (default: docs-converted in source repo)')
    
    args = parser.parse_args()
    
    # Define paths
    source_dir = Path(args.source)
    output_dir = Path(args.output)
    
    # Verify source directory exists
    if not source_dir.exists():
        print(f"Error: Source directory does not exist: {source_dir}")
        return
    
    # Create output directory
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Run batch conversion
    stats = batch_convert_mdx_files(source_dir, output_dir)
    
    # Print final summary
    if stats["failed"] == 0:
        print(f"\n🎉 All {stats['converted']} files converted successfully!")
    else:
        print(f"\n⚠️  {stats['converted']} files converted, {stats['failed']} failed.")
    
    print(f"\nConverted files are available in: {output_dir}")

if __name__ == "__main__":
    main()