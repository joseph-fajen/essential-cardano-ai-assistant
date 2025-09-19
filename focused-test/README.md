# Focused Test: Essential Cardano AI Assistant

This directory contains a complete end-to-end test of the Essential Cardano AI Assistant pipeline, from content extraction to Globant deployment.

## Test Objective

Verify that web-scraped content with proper URLs can be uploaded to Globant Enterprise and produce accurate AI Assistant responses with working source links.

## Pipeline Steps

### 1. Extraction (`1-extraction/`)
- Extract 5-10 pages from Essential Cardano sites
- Preserve URLs with unique identifiers
- Save raw JSON extraction results

### 2. Processing (`2-processing/`)
- Clean and organize extracted content
- Format for optimal RAG Assistant performance
- Prepare structured knowledge base files

### 3. Upload (`3-upload/`)
- Format content for Globant Enterprise upload
- Create unified knowledge base
- Upload to RAG Assistant

### 4. Testing (`4-testing/`)
- Test specific scenarios with the deployed assistant
- Verify URL accuracy and content quality
- Document results and lessons learned

## Success Criteria

- ✅ Assistant provides accurate content from extracted pages
- ✅ Assistant can cite sources correctly
- ✅ Assistant provides working URLs when available
- ✅ End-to-end pipeline is repeatable and scalable

## Target Content

Focus on Essential Cardano FAQ and governance content that users commonly ask about and where source citations are critical.