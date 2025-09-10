# Essential Cardano AI Assistant Project

A sophisticated AI assistant chatbot for the Essential Cardano community, built on the Globant Enterprise platform. This assistant serves as a knowledgeable guide for the Cardano ecosystem, helping users navigate from basic concepts to advanced topics across governance, technical documentation, and community resources.

## Project Overview

### Mission
Create an educational, community-focused AI assistant that provides accurate, well-sourced information about Cardano blockchain, its ecosystem, governance, and related topics while maintaining strict quality and safety standards.

### Target Audiences
- **General Users**: New to blockchain, need basic explanations and onboarding guidance
- **Tech-Savvy Users**: Familiar with blockchain, interested in governance participation and advanced features  
- **Developers**: Need technical documentation (redirected to appropriate resources)
- **Stake Pool Operators**: Infrastructure operators requiring technical and governance information

## Current Status

### ✅ Completed
- [x] Comprehensive system prompt development (`system_prompt.md`)
- [x] URL reference guide for accurate source citations (`url_reference_guide.md`)
- [x] Multi-source knowledge base architecture strategy (`knowledge_base_architecture.md`)
- [x] Globant Enterprise platform implementation strategy (`globant_platform_strategy.md`)
- [x] Content ingestion and management workflows (`content_ingestion_workflow.md`)
- [x] Essential Cardano content upload (~1,000 files) to Globant Enterprise
- [x] Comprehensive workflow commands (`.claude/commands/`)

### 🚧 In Progress
- [ ] Essential Cardano RAG Assistant indexing completion (Globant Enterprise)
- [ ] Initial testing and quality validation

### 📋 Next Priorities
- [ ] Test Essential Cardano AI Assistant once indexing completes
- [ ] Create Intersect Governance Assistant (second RAG Assistant)
- [ ] Upload Intersect knowledge base content
- [ ] Implement multi-agent routing logic
- [ ] Create additional specialized RAG Assistants (Technical, Research)

## Platform & Architecture

### Globant Enterprise Setup
- **Platform**: Globant Enterprise AI (console.saia.ai)
- **Project**: Content Team (IOG)
- **Approach**: Multiple specialized RAG Assistants for different knowledge domains
- **Current**: "Essential Cardano AI Assistant" with ~1,000 files uploaded

### Multi-Agent Architecture Strategy
```
User Query → Intent Classification → Route to Appropriate RAG Assistant → Generate Response → Cite Sources
```

**Planned RAG Assistants**:
1. **Essential Cardano AI Assistant** (current) - Community knowledge, basics, onboarding
2. **Intersect Governance Assistant** (next) - All governance, voting, DRep education
3. **Cardano Technical Assistant** (planned) - docs.cardano.org technical content  
4. **IOG Research Assistant** (planned) - Blog posts, research papers

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
- **Joseph Fajen** - Project lead, platform implementation
- **Olga Hryniuk** - Content strategy, Essential Cardano domain expertise
- **Neil Burgess** - Intersect knowledge base access coordination
- **Allan Martínez** - Research AI collaboration (~250 IOG research papers)
- **Lars Brünjes** - System prompt development consultation

### External Collaborations
- **Allan's Research AI Project** - Integration opportunity for research paper queries
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

**Last Updated**: 2025-09-10  
**Project Lead**: Joseph Fajen  
**Platform**: Globant Enterprise AI  
**Repository**: https://github.com/josephfajen/essential-cardano-ai-assistant