# Web Crawling Approach: Architecture Decision Summary

## Executive Summary

Based on feedback from Globant Enterprise and analysis of the current broken link issues, we recommend migrating from the current 3 RAG Assistant architecture to a **unified single RAG Assistant powered by web-crawled content**. This approach will eliminate broken links while simplifying maintenance and improving user experience.

## Problem Analysis

### Root Cause of Broken Links
The current approach uses GitHub source files that generate incomplete URLs missing unique identifiers added by content management systems during publication.

**Examples**:
- **GitHub source**: `/faq/what-is-staking-and-delegation-on-cardano`
- **Live URL**: `/faq/what-is-staking-and-delegation-on-cardano-716f9c75`
- **Missing**: Unique identifier (`-716f9c75`)

### Current Architecture Limitations
- ❌ **Broken links**: Source files don't match live URL structure
- ❌ **Maintenance complexity**: 3 separate knowledge bases to manage
- ❌ **Content duplication**: Overlapping content across assistants
- ❌ **Routing complexity**: Keyword-based routing may miss nuanced queries

## Recommended Solution

### Single Unified RAG Assistant Architecture
- ✅ **Accurate URLs**: Web-crawled content preserves live URL structure
- ✅ **Simplified management**: One knowledge base to maintain
- ✅ **Content freshness**: Regular web crawling ensures current information
- ✅ **Reduced complexity**: Eliminates routing logic and duplicate content

### Globant Enterprise Web Crawling Tools

**Recommended**: Basic Tools (No Configuration Required)
- `com.globant.geai.web_search` - Real-time internet search
- `com.globant.geai.web_scraper_httpx` - URL-based content extraction
- **Advantage**: Ready to use immediately, suitable for systematic crawling

**Alternative**: Firecrawl Tools (Configuration Required)
- `com.globant.geai.firecrawl.web_search` - Enhanced search with snippets
- `com.globant.geai.firecrawl.web_scraper` - Advanced extraction with multiple formats
- **Advantage**: More advanced capabilities, multiple output formats

## Implementation Plan

### Target Sites for Web Crawling
1. **Essential Cardano** (https://www.essentialcardano.io)
   - Sections: FAQ, Glossary, Articles, Guides
   - Content: Community knowledge, onboarding resources
   - URL Pattern: `/{section}/{title}-{unique-id}`

2. **Cardano Documentation** (https://docs.cardano.org)
   - Sections: Learn, Build, Operate, Governance
   - Content: Technical specifications, network operations
   - URL Pattern: Standard documentation structure

3. **Developer Portal** (https://developers.cardano.org)
   - Sections: Docs, Tools, Tutorials, Get Started
   - Content: Development resources, API documentation
   - URL Pattern: Developer-focused documentation

### 4-Week Implementation Timeline

**Week 1: Preparation**
- Configure content extraction agent in Globant Enterprise
- Map site structures and discover URL patterns
- Test crawling with sample pages to verify URL preservation

**Week 2: Content Extraction**
- Systematic web crawling of all target sites
- Content processing and quality validation
- Prepare unified knowledge base for upload

**Week 3: Assistant Creation**
- Create new unified RAG Assistant with enhanced system prompt
- Upload web-crawled content with verified URLs
- Initial testing and validation

**Week 4: Testing and Migration**
- Comprehensive testing across all user personas
- Router Flow migration to point to unified assistant
- Performance validation and production deployment

## Key Benefits

### Immediate Impact
- **Eliminates broken links**: All URLs will be functional and accurate
- **Reduces complexity**: Single assistant instead of three
- **Improves maintenance**: One knowledge base to update
- **Enhances reliability**: Live content ensures current information

### Long-term Advantages
- **Scalability**: Easy to add new content sources
- **Consistency**: Unified approach to all Cardano information
- **Automation**: Regular web crawling keeps content fresh
- **Performance**: Optimized search across single knowledge base

## Technical Verification

### URL Accuracy Testing
Web crawling tests with Essential Cardano confirmed:
- ✅ Complete URLs with unique identifiers preserved
- ✅ Content metadata (author, date, tags) maintained
- ✅ Internal link structure preserved
- ✅ Content formatting suitable for knowledge base upload

### Content Quality Validation
Sample extractions demonstrated:
- ✅ Comprehensive content coverage
- ✅ Proper source attribution
- ✅ Structured information suitable for AI responses
- ✅ Consistent formatting across different content types

## Risk Mitigation

### Potential Challenges and Solutions
- **URL structure changes**: Regular monitoring and update procedures
- **Content extraction quality**: Thorough testing and validation protocols
- **Performance impact**: Parallel testing and optimization
- **Migration complexity**: Phased approach with rollback capability

### Success Metrics
- **Link Accuracy**: 100% functional URLs with proper identifiers
- **Content Coverage**: Match or exceed current knowledge base scope
- **Response Quality**: Maintain 95%+ accuracy with source attribution
- **Performance**: Response times under 5 seconds

## Globant Enterprise Implementation

### Content Extraction Agent Configuration
```
Agent Name: Essential Cardano Content Extractor
Tools: com.globant.geai.web_search, com.globant.geai.web_scraper_httpx
Purpose: Systematic crawling and extraction of Cardano documentation

Workflow:
1. Search for content on target sites
2. Extract complete content with URL preservation
3. Maintain metadata and formatting
4. Prepare for knowledge base upload
```

### Unified RAG Assistant Setup
```
Assistant Name: Essential Cardano AI Assistant (Unified)
System Prompt: Enhanced unified prompt for all content types
Knowledge Base: Web-crawled content from all target sites
Configuration: High accuracy, required source attribution
```

## Stakeholder Communication

### For Globant Enterprise
The unified architecture leverages your web crawling tools effectively while simplifying our overall system design. This reduces the complexity of managing multiple RAG assistants and improves the reliability of URL citations.

### For Essential Cardano Team
This approach ensures that all URLs referenced by the AI assistant will work correctly, improving user experience and maintaining the credibility of the information provided. The unified approach also makes content updates more manageable.

### For Users
The change will be seamless from a user perspective, but they'll benefit from more accurate links and comprehensive responses that can draw from all Cardano documentation sources effectively.

## Next Steps

1. **Configure content extraction agent** in Globant Enterprise Console
2. **Begin systematic web crawling** starting with Essential Cardano
3. **Process and validate extracted content** for knowledge base upload
4. **Create unified RAG Assistant** with comprehensive knowledge base
5. **Test and migrate Router Flow** to new unified architecture

## Conclusion

The web crawling approach addresses the fundamental issue of broken links while providing a more maintainable and scalable architecture. By leveraging Globant Enterprise's web crawling tools, we can ensure accurate URLs, current content, and simplified management while delivering a better user experience.

This architectural change represents a significant improvement in the Essential Cardano AI Assistant's reliability and effectiveness, positioning it for long-term success as the primary educational resource for the Cardano community.

---

**Prepared by**: AI Assistant Analysis  
**Date**: September 2025  
**Status**: Ready for Implementation  
**Priority**: High - Addresses critical broken link issues