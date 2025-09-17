# Migration Strategy: From 3 RAG Assistants to Unified Web-Crawled Assistant

## Current State Analysis

### Existing Architecture
- **Essential Cardano AI Assistant**: ~1,000 files from GitHub sources
- **Cardano Docs AI Assistant**: 79 MDX→TXT files  
- **Developer Portal AI Assistant**: Technical documentation files
- **Essential Cardano Router Flow**: Keyword-based routing between assistants

### Identified Issues
- **Broken links**: GitHub source files lack unique identifiers present in live URLs
- **Maintenance complexity**: Managing 3 separate knowledge bases
- **Content duplication**: Overlapping content across assistants
- **Routing complexity**: Keyword-based routing may miss nuanced queries

## Target Architecture

### Unified Single Assistant
- **Name**: Essential Cardano AI Assistant (Unified)
- **Knowledge Base**: Web-crawled content from live sites
- **Sources**: essentialcardano.io, docs.cardano.org, developers.cardano.org
- **Benefits**: Accurate URLs, simplified maintenance, unified search

### Router Flow Simplification
- **From**: 3-way routing with keyword matching
- **To**: Single assistant endpoint or intelligent pre-processing
- **Result**: Simplified architecture with consistent user experience

## Migration Plan

### Phase 1: Preparation (Week 1)

#### 1.1 Content Extraction Agent Setup
**Location**: Globant Enterprise Console
**Tools**: `com.globant.geai.web_search` + `com.globant.geai.web_scraper_httpx`

**Agent Configuration**:
```
Name: Essential Cardano Content Extractor
Description: Systematically crawls and extracts content from Cardano documentation sites
Tools: web_search, web_scraper_httpx

Prompt: You are a content extraction agent for the Essential Cardano AI Assistant project. Your role is to systematically crawl Cardano-related websites and extract complete content while preserving URL structure and metadata.

Instructions:
1. Search for content on specified Cardano websites
2. Extract complete content with preserved URLs including unique identifiers
3. Maintain author attribution and metadata when available
4. Focus on educational and community content
5. Ensure all extracted URLs are complete and functional

Target sites:
- essentialcardano.io (priority: /faq, /glossary, /article, /guides)
- docs.cardano.org (priority: /learn, /build, /operate, /governance)  
- developers.cardano.org (priority: /docs, /tools, /tutorials)
```

#### 1.2 Site Mapping and URL Discovery
1. **Essential Cardano Site Map**
   - Discover all FAQ entries with unique IDs
   - Map glossary terms with complete URLs
   - Identify article and guide URLs
   - Document URL pattern: `/{section}/{title}-{unique-id}`

2. **Cardano Documentation Map**
   - Catalog learning materials structure
   - Map technical documentation sections
   - Identify governance content areas
   - Document standard documentation URLs

3. **Developer Portal Map**
   - Survey API documentation structure
   - Identify tool and tutorial sections
   - Map getting started resources
   - Document development guide URLs

#### 1.3 Test Crawling Protocol
1. **Sample Page Testing**
   - Extract 10 FAQ pages from Essential Cardano
   - Verify URL accuracy and content completeness
   - Test metadata preservation (author, date, tags)
   - Validate content formatting and structure

2. **Quality Validation**
   - Confirm all extracted URLs work when clicked
   - Verify content matches source material
   - Check for proper author and date attribution
   - Ensure no broken internal links

### Phase 2: Content Extraction (Week 2)

#### 2.1 Systematic Content Crawling

**Essential Cardano Priority Sections**:
- `/faq/*` - All frequently asked questions
- `/glossary/*` - Complete terminology definitions
- `/article/*` - Educational articles and guides
- `/guides/*` - Step-by-step instructional content

**Cardano Documentation Priority Sections**:
- `/learn/*` - Foundational learning materials
- `/build/*` - Technical implementation guides
- `/operate/*` - Node operation and infrastructure
- `/governance/*` - Governance processes and information

**Developer Portal Priority Sections**:
- `/docs/*` - Core API and technical documentation
- `/get-started/*` - Developer onboarding resources
- `/tools/*` - Development tools and utilities
- `/tutorials/*` - Step-by-step development guides

#### 2.2 Content Processing Pipeline
1. **Extraction**: Use web_scraper_httpx for each discovered URL
2. **Validation**: Verify content completeness and URL accuracy
3. **Formatting**: Convert to consistent markdown structure
4. **Deduplication**: Remove overlapping content across sources
5. **Quality Control**: Manual review of sample extractions

#### 2.3 Content Organization
```
Extracted Content Structure:
├── essential-cardano/
│   ├── faq/
│   ├── glossary/
│   ├── articles/
│   └── guides/
├── cardano-docs/
│   ├── learn/
│   ├── build/
│   ├── operate/
│   └── governance/
└── developer-portal/
    ├── docs/
    ├── tools/
    ├── tutorials/
    └── get-started/
```

### Phase 3: Unified Assistant Creation (Week 3)

#### 3.1 New RAG Assistant Configuration
**Location**: Globant Enterprise Console
**Name**: Essential Cardano AI Assistant (Unified)

**System Prompt**: Use `unified_system_prompt.md`
**Knowledge Base**: All web-crawled content from Phase 2
**Settings**: 
- Response length: Balanced
- Accuracy: High priority
- Source attribution: Required

#### 3.2 Knowledge Base Upload
1. **Content Preparation**
   - Organize extracted content by source and section
   - Verify all URLs include proper unique identifiers
   - Ensure consistent markdown formatting
   - Validate metadata preservation

2. **Upload Process**
   - Upload Essential Cardano content first (largest content set)
   - Add Cardano Documentation content
   - Include Developer Portal content
   - Monitor upload progress and indexing status

3. **Verification Testing**
   - Test knowledge base search functionality
   - Verify content accessibility across all sources
   - Confirm URL accuracy in responses
   - Validate source attribution features

### Phase 4: Testing and Migration (Week 4)

#### 4.1 Comprehensive Testing Protocol

**Link Accuracy Testing**:
- Test all FAQ links include proper unique identifiers
- Verify glossary URLs work correctly
- Confirm technical documentation links are functional
- Validate developer portal resource links

**Content Quality Testing**:
- Compare responses against current 3-assistant setup
- Test knowledge coverage across all domains
- Verify appropriate content prioritization
- Confirm source attribution accuracy

**User Experience Testing**:
- Test with sample queries from each user persona
- Verify appropriate response complexity for audience
- Confirm proper routing to relevant content
- Test boundary compliance (investment advice, etc.)

#### 4.2 Router Flow Migration

**Option A: Direct Replacement**
- Update existing Router Flow to point to unified assistant
- Maintain same entry point for users
- Simplify routing logic to single destination

**Option B: Parallel Deployment**
- Create new Router Flow for unified assistant
- Run parallel testing with current setup
- Gradual migration with performance comparison

**Option C: Pre-processing Enhancement**
- Add intelligent query analysis before routing
- Use unified assistant for all query types
- Implement query context enhancement

#### 4.3 Performance Validation
1. **Response Time Testing**
   - Compare response times vs. current setup
   - Ensure <5 second response target maintained
   - Monitor knowledge base search performance

2. **Accuracy Assessment**
   - Test 100+ sample queries across domains
   - Verify 95%+ accuracy target maintained
   - Confirm 100% source attribution compliance

3. **User Acceptance Testing**
   - Internal team testing with diverse query types
   - Stakeholder review and feedback collection
   - Final approval before production deployment

### Phase 5: Production Deployment

#### 5.1 Deployment Steps
1. **Final Validation**
   - Complete testing protocol execution
   - Stakeholder approval confirmation
   - Performance metrics validation

2. **Router Flow Update**
   - Switch Router Flow to unified assistant
   - Monitor initial user interactions
   - Verify seamless transition

3. **Legacy Assistant Management**
   - Archive current 3 assistants as backup
   - Document migration completion
   - Plan content update procedures

#### 5.2 Post-Migration Monitoring
1. **Performance Tracking**
   - Monitor response times and accuracy
   - Track user satisfaction indicators
   - Identify any deployment issues

2. **Content Maintenance Planning**
   - Establish regular web crawling schedule
   - Plan content update procedures
   - Set up change detection monitoring

## Risk Management

### Potential Risks and Mitigation

**Risk: Content Extraction Issues**
- Mitigation: Thorough testing with sample pages
- Backup: Maintain current assistants during transition

**Risk: URL Structure Changes**
- Mitigation: Regular monitoring and update procedures  
- Backup: Implement change detection alerts

**Risk: Performance Degradation**
- Mitigation: Parallel testing and optimization
- Backup: Rollback plan to current architecture

**Risk: Content Quality Issues**
- Mitigation: Comprehensive quality validation
- Backup: Manual content review process

## Success Metrics

### Primary Objectives
- **Link Accuracy**: 100% of URLs functional and correctly formatted
- **Content Coverage**: Match or exceed current knowledge base scope
- **Response Quality**: Maintain 95%+ accuracy with proper attribution
- **Performance**: Response times under 5 seconds

### Secondary Objectives
- **Maintenance Simplification**: Reduce ongoing management overhead
- **Architecture Clarity**: Simplified system for future expansion
- **Content Freshness**: Improved ability to maintain current information
- **User Experience**: Seamless transition without functionality loss

## Timeline Summary

| Week | Phase | Key Deliverables |
|------|-------|-----------------|
| 1 | Preparation | Content extraction agent setup, site mapping, test protocol |
| 2 | Extraction | Complete content crawling, processing, quality validation |
| 3 | Creation | Unified assistant setup, knowledge base upload, initial testing |
| 4 | Testing | Comprehensive validation, router migration, performance verification |

## Next Steps

1. **Configure content extraction agent** in Globant Enterprise
2. **Begin Essential Cardano site mapping** and URL discovery
3. **Execute test crawling protocol** with sample pages
4. **Validate URL accuracy** and content preservation
5. **Proceed with systematic content extraction** across all target sites

This migration strategy provides a structured approach to resolving the broken link issues while simplifying the overall architecture for better maintainability and user experience.