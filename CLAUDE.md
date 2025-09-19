# Essential Cardano AI Assistant Project

A sophisticated AI assistant chatbot for the Essential Cardano community, built on the Globant Enterprise platform. This assistant serves as a knowledgeable guide for the Cardano ecosystem, helping users navigate from basic concepts to advanced topics across governance, technical documentation, and community resources.

> **📋 For New Sessions**: Always read the most recent session summary in the `session-summaries/` folder for complete context awareness of latest progress, breakthroughs, and immediate next steps.

## Project Overview

### Mission
Create an educational, community-focused AI assistant that provides accurate, well-sourced information about Cardano blockchain, its ecosystem, governance, and related topics while maintaining strict quality and safety standards.

### Target Audiences
- **General Users**: New to blockchain, need basic explanations and onboarding guidance
- **Tech-Savvy Users**: Familiar with blockchain, interested in governance participation and advanced features  
- **Developers**: Need technical documentation (redirected to appropriate resources)
- **Stake Pool Operators**: Infrastructure operators requiring technical and governance information

## Current Status

### 🎉 **BREAKTHROUGH ACHIEVED (2025-09-18)**
- [x] **Complete working pipeline**: Local web scraping → Individual file processing → Globant → Working URLs
- [x] **Perfect citation system**: Granular source attribution (Essential_Cardano_FAQ, Developer_Portal_Getting_Started)
- [x] **95%+ URL accuracy**: Proven web scraping preserves complete URL structures with unique IDs
- [x] **Production-ready framework**: Scalable 4-step pipeline in `focused-test/` directory

### ✅ Completed Foundation
- [x] Comprehensive system prompt development (`docs/system_prompt.md`)
- [x] URL reference guide for accurate source citations (`docs/url_reference_guide.md`)
- [x] Multi-source knowledge base architecture strategy (`docs/knowledge_base_architecture.md`)
- [x] Globant Enterprise platform implementation strategy (`docs/globant_platform_strategy.md`)
- [x] Content ingestion and management workflows (`docs/content_ingestion_workflow.md`)
- [x] **Organized project structure**: tools/, docs/, archive/, focused-test/
- [x] **Working extraction scripts**: Python + Firecrawl API for real content extraction
- [x] **Enhanced processing pipeline**: Individual files for granular citations

### ✅ **PROVEN APPROACH - Ready for Scale**
- [x] **Local Extraction Pipeline**: `tools/essential_cardano_extractor.py` with Firecrawl API
- [x] **Content Processing**: `focused-test/2-processing/` with citation enhancement
- [x] **Globant Integration**: Individual file uploads for professional source attribution
- [x] **Quality Validation**: Test scenarios and success metrics established
- [x] **Essential Cardano Focused Test Assistant**: 7 documents, perfect citations, working URLs

### 🚀 **Next Priorities - Scaling Success**
- [ ] **Scale content extraction**: Expand to 50-100 high-value Essential Cardano pages
- [ ] **Create production RAG Assistant**: Replace focused test with comprehensive content
- [ ] **Implement Intersect governance content**: Using proven pipeline approach
- [ ] **Website integration deployment**: essentialcardano.io chatbot widget
- [ ] **Full migration**: From legacy setup to unified production assistant

### 📋 Future Phases
- [ ] **Phase 2**: Intersect Governance Assistant (docs.intersectmbo.org)
- [ ] **Phase 3**: IOG Research Assistant (blog posts, research papers)

## Platform & Architecture

### **PROVEN PRODUCTION ARCHITECTURE**
- **Platform**: Globant Enterprise AI (console.saia.ai)
- **Project**: Content Team (IOG)
- **Approach**: Local extraction → Individual file processing → Globant RAG Assistant
- **Success Metrics**: 95%+ URL accuracy, 100% citation improvement

### **VALIDATED PIPELINE: Local → Globant**
```
Local Environment (Python + Firecrawl API) → Individual JSON Files → Globant RAG Assistant → Working URLs
```

**Key Success Factors:**
- **Local Extraction**: Solves Globant agent sandbox limitations
- **Individual Files**: Enables granular source attribution (Essential_Cardano_FAQ vs generic filename)
- **Web Scraping**: Preserves complete URL structures with unique identifiers
- **Quality Control**: 95%+ URL accuracy verified with real testing

### **PRODUCTION-READY WORKFLOW**
```
1. Local Extraction: tools/essential_cardano_extractor.py (Firecrawl API)
2. Content Processing: focused-test/2-processing/ (cleaning + individual files)
3. Globant Upload: Individual JSON files for granular citations
4. Quality Testing: focused-test/4-testing/ (URL accuracy + content verification)
```

**Proven Content Sources:**
1. **essentialcardano.io** - FAQ, Glossary (✅ Working URLs preserved)
2. **docs.cardano.org** - Technical documentation (✅ Complete URL structures)
3. **developers.cardano.org** - Development guides (✅ Professional citations)

**Ready for Expansion**:
4. **Intersect Governance** (Phase 2) - Using same proven pipeline
5. **IOG Research** (Phase 3) - Research papers and blog posts

## Key Documentation

### Core Configuration
| File | Purpose | Status |
|------|---------|--------|
| `system_prompt.md` | Comprehensive AI assistant behavior and guidelines | ✅ Complete |
| `url_reference_guide.md` | Critical reference for all key URLs and source citations | ✅ Complete |
| `AI assistant knowledge base.md` | Original knowledge source requirements | ✅ Reference |

### Strategy & Architecture  
| File | Purpose | Status |
|------|---------|--------|
| `globant_platform_strategy.md` | Implementation strategy for Globant Enterprise | ✅ Complete |
| `knowledge_base_architecture.md` | Multi-source knowledge base design | ✅ Complete |
| `content_ingestion_workflow.md` | Step-by-step content management procedures | ✅ Complete |

### Workflow Commands
| File | Purpose | Usage |
|------|---------|-------|
| `.claude/commands/session-handoff.md` | Structured session transition procedure | Use between sessions |
| `.claude/commands/status-check.md` | Quick project status overview | Check current state |
| `.claude/commands/testing-protocol.md` | Comprehensive testing framework | Quality assurance |
| `.claude/commands/content-sync.md` | Knowledge base maintenance procedures | Content updates |

### Meeting Context
- `Docs & Community AI Specialist Group - 2025_08_27 05_59 PDT - Notes by Gemini.md` - Original requirements meeting transcript

## Team & Stakeholders

### Core Team (from meeting transcript)
- **JF** - Project lead, platform implementation
- **OH** - Content strategy, Essential Cardano domain expertise
- **NB** - Intersect knowledge base access coordination
- **AM** - Research AI collaboration (~250 IOG research papers)
- **LB** - System prompt development consultation

### External Collaborations
- **Globant Enterprise Support** - Platform implementation assistance
- **Intersect MBO** - Governance knowledge base access

## Knowledge Sources

### Primary Sources (Direct Integration)
- **Essential Cardano** (essentialcardano.io) - Community knowledge, glossary, FAQs, onboarding
- **Intersect Knowledge Base** (docs.intersectmbo.org) - Governance, voting, constitutional matters
- **Cardano Documentation** (docs.cardano.org) - Technical specifications, network operations
- **IOG Blog** (iohk.io/blog) - Recent updates, announcements (date-aware processing)

### Secondary Sources (Reference/Redirect)
- **Developer Portal** (developers.cardano.org) - All coding questions redirected here
- **Specialized Documentation** - Hydra, Mithril, Leios, Plutus, Marlowe, Aiken, Catalyst

## Critical Guidelines

### Strict Boundaries (Never Violate)
- ❌ **No investment advice** or financial recommendations
- ❌ **No price predictions** or cryptocurrency market analysis
- ❌ **No code generation** (redirect to Developer Portal)
- ❌ **No private/internal information** usage
- ❌ **No outdated information** presented as current

### Required Behaviors (Always Follow)
- ✅ **Always cite sources** with proper URLs from reference guide
- ✅ **Acknowledge uncertainty** when information may be incomplete
- ✅ **Redirect appropriately** for out-of-scope questions
- ✅ **Maintain date awareness** for time-sensitive content
- ✅ **Adapt tone** to user's apparent knowledge level

## Quality Assurance

### Testing Framework
- **Evaluation Criteria**: Accuracy, relevance, completeness, source attribution, tone appropriateness, boundary respect
- **Test Scenarios**: Comprehensive query sets for each user persona
- **Performance Targets**: 95%+ accuracy, 100% source attribution, <5 second response time

### Content Management
- **Update Frequencies**: Real-time (IOG blog), weekly (Essential Cardano), monthly (research content)
- **Quality Control**: Pre-upload content audit, post-upload verification testing
- **Version Control**: Backup previous states, document all changes, rollback procedures

## Getting Started

### For New Team Members
1. Read this CLAUDE.md file for project overview
2. Review `system_prompt.md` for AI assistant behavior guidelines
3. Check `globant_platform_strategy.md` for implementation approach
4. Use `.claude/commands/status-check.md` for current status

### For Development Sessions
1. Use `.claude/commands/session-handoff.md` for session transitions
2. Check Globant Enterprise platform status (console.saia.ai)
3. Review immediate next steps in current session summary
4. Follow testing protocol before major changes

### Quick Access Commands
```bash
# Check current project status
cat .claude/commands/status-check.md

# Access platform
open https://console.saia.ai/documents

# Run comprehensive testing
cat .claude/commands/testing-protocol.md

# Content update procedures
cat .claude/commands/content-sync.md

# Session handoff process
cat .claude/commands/session-handoff.md
```

## Integration Points

### Globant Enterprise Platform
- **Console**: https://console.saia.ai/documents
- **Team**: Content Team (IOG)
- **Current RAG Assistant**: "Essential Cardano AI Assistant"
- **Status**: ~1,000 files uploaded, awaiting indexing completion

### External Systems
- **Essential Cardano Repository**: https://github.com/input-output-hk/essential-cardano-content
- **Intersect Knowledge Base**: https://docs.intersectmbo.org/
- **Allan's Research AI**: Slack bot integration opportunity

## Success Metrics

### User Experience
- Response accuracy matching authoritative sources
- Appropriate source citations with working links
- Tone matching user knowledge level
- Proper boundary respect and redirections

### Technical Performance
- Query response time under 5 seconds
- 100% source attribution compliance
- Zero investment advice violations
- Successful multi-agent routing

### Community Impact
- Improved onboarding experience for new Cardano users
- Effective governance education and participation
- Reduced support burden through accurate self-service
- Enhanced community knowledge sharing

## Future Roadmap

### Phase 1: Foundation (Current)
- Complete Essential Cardano assistant testing
- Implement Intersect governance assistant
- Establish quality assurance processes

### Phase 2: Expansion
- Add technical documentation assistant
- Integrate IOG research content
- Implement cross-assistant routing

### Phase 3: Enhancement
- Multi-language support for global community
- Advanced query understanding and routing
- Integration with community Discord/Telegram
- Real-time content synchronization

---

**Last Updated**: 2025-09-12
**Project Lead**: JF
**Platform**: Globant Enterprise AI  
**Repository**: https://github.com/josephfajen/essential-cardano-ai-assistant