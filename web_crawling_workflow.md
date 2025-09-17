# Web Crawling Content Extraction Workflow

## Overview
This document outlines the workflow for migrating from GitHub source files to web-crawled live content to solve broken link issues in the Essential Cardano AI Assistant.

## Problem Analysis
**Root Cause**: GitHub source files contain incomplete URLs that are missing unique identifiers added by content management systems during publication.

**Examples**:
- Source file path: `/faq/what-is-staking-and-delegation-on-cardano`
- Live URL: `/faq/what-is-staking-and-delegation-on-cardano-716f9c75`
- Missing component: `-716f9c75` (unique identifier)

## Target Sites for Crawling

### 1. Essential Cardano (Priority 1)
- **Base URL**: https://www.essentialcardano.io
- **Key Sections**:
  - `/faq/*` - Frequently asked questions
  - `/glossary/*` - Term definitions  
  - `/article/*` - Educational articles
  - `/guides/*` - How-to guides
- **Content Structure**: Structured with author, date, tags, and contributor metadata
- **URL Pattern**: `/{section}/{title}-{unique-id}`

### 2. Cardano Documentation (Priority 2)
- **Base URL**: https://docs.cardano.org
- **Key Sections**:
  - `/learn/*` - Learning materials
  - `/build/*` - Technical documentation
  - `/operate/*` - Node operation guides
  - `/governance/*` - Governance information
- **Content Structure**: Technical documentation with code examples
- **URL Pattern**: Standard technical documentation structure

### 3. Developer Portal (Priority 3)
- **Base URL**: https://developers.cardano.org
- **Key Sections**:
  - `/docs/*` - API documentation
  - `/tools/*` - Development tools
  - `/tutorials/*` - Coding tutorials
  - `/get-started/*` - Onboarding guides
- **Content Structure**: Code-focused with examples and tutorials
- **URL Pattern**: Standard developer documentation structure

## Globant Enterprise Web Crawling Implementation

### Tools Selection
**Recommended**: Basic tools (no configuration required)
- `com.globant.geai.web_search` - For discovering pages
- `com.globant.geai.web_scraper_httpx` - For content extraction

**Alternative**: Firecrawl tools (configuration required)
- `com.globant.geai.firecrawl.web_search` - Enhanced search
- `com.globant.geai.firecrawl.web_scraper` - Advanced extraction with multiple formats

### Crawling Strategy

#### Phase 1: Content Discovery
1. **Site Mapping**: Use web_search to discover all major sections
2. **URL Collection**: Systematically collect URLs from sitemaps and navigation
3. **Categorization**: Group URLs by content type (FAQ, Glossary, Articles, Guides)

#### Phase 2: Content Extraction
1. **Systematic Crawling**: Use web_scraper_httpx for each discovered URL
2. **Content Structuring**: Preserve metadata (author, date, tags)
3. **Quality Control**: Verify URL accuracy and content completeness

#### Phase 3: Content Processing
1. **Deduplication**: Remove duplicate content across sites
2. **Format Standardization**: Convert to consistent markdown format
3. **Link Validation**: Ensure all internal links are properly preserved

## Content Agent Configuration

### Agent Prompt Template
```
You are a content extraction agent for the Essential Cardano AI Assistant project.

Your role:
1. Search for Cardano-related content on specified websites
2. Extract complete content with preserved URL structure
3. Maintain author attribution and metadata
4. Ensure link accuracy for live site integration

Guidelines:
- Always preserve the complete URL including unique identifiers
- Extract author, date, and tag information when available
- Maintain the original content structure and formatting
- Focus on educational and community-oriented content
- Avoid extracting outdated or deprecated information

Target sites: essentialcardano.io, docs.cardano.org, developers.cardano.org
```

### Extraction Workflow Steps
1. **Initialize Agent** with web search and scraper tools
2. **Configure Search Parameters** for each target site
3. **Execute Systematic Crawling** section by section
4. **Process and Validate Content** before upload
5. **Upload to Unified RAG Assistant** knowledge base

## Quality Assurance

### Validation Checkpoints
- [ ] URL accuracy verification against live sites
- [ ] Content completeness compared to source materials
- [ ] Metadata preservation (author, date, tags)
- [ ] Link functionality testing
- [ ] Duplicate content identification

### Success Metrics
- **Link Accuracy**: 100% of extracted URLs should work when clicked
- **Content Coverage**: Match or exceed current GitHub source content
- **Metadata Preservation**: Author, date, and tag information retained
- **Processing Efficiency**: Complete crawling within reasonable timeframe

## Migration Strategy

### From Current Setup
**Current**: 3 RAG Assistants + Router Flow + GitHub sources
**Target**: 1 RAG Assistant + Web-crawled content

### Migration Steps
1. **Parallel Development**: Build new single assistant alongside current setup
2. **Content Migration**: Upload web-crawled content to new assistant
3. **Testing Phase**: Validate against current assistant performance
4. **Router Update**: Point router to new single assistant
5. **Cleanup**: Archive old assistants after successful migration

## Implementation Timeline

### Week 1: Setup and Discovery
- Configure content extraction agent
- Perform initial site mapping and URL discovery
- Test crawling workflow with sample pages

### Week 2: Content Extraction
- Systematic crawling of all target sites
- Content processing and quality validation
- Prepare content for RAG assistant upload

### Week 3: RAG Assistant Creation
- Create new unified RAG assistant
- Upload processed content
- Configure system prompt for unified knowledge base

### Week 4: Testing and Migration
- Comprehensive testing against current setup
- Router flow migration
- Performance validation and optimization

## Technical Considerations

### Rate Limiting
- Implement appropriate delays between requests
- Respect robots.txt and site policies
- Monitor for any access restrictions

### Content Updates
- Establish regular crawling schedule for content freshness
- Implement change detection for efficient updates
- Maintain version control for content changes

### Error Handling
- Robust error handling for failed page loads
- Retry mechanisms for temporary failures
- Logging and monitoring for troubleshooting

## Expected Outcomes

### Immediate Benefits
- **Elimination of broken links**: All URLs will be live and functional
- **Simplified architecture**: Single RAG assistant reduces complexity
- **Accurate source attribution**: Proper URLs for all citations

### Long-term Advantages
- **Easier maintenance**: Single knowledge base to manage
- **Content freshness**: Regular web crawling ensures up-to-date information
- **Scalability**: Easy to add new sites and content types
- **Consistency**: Unified approach to all Cardano documentation

## Next Steps
1. Configure content extraction agent in Globant Enterprise
2. Begin systematic crawling of Essential Cardano site
3. Process and validate extracted content
4. Create unified RAG assistant with web-crawled knowledge base