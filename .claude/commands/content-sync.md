# Content Sync Protocol - Essential Cardano AI Assistant

## Knowledge Base Update Command

Use this command to manage content updates across all RAG Assistants.

### Update Schedule Overview

#### Real-time Updates (Automated)
- **IOG Blog Posts**: RSS feed integration when available
- **Governance Proposals**: Intersect API updates (if available)
- **Emergency Updates**: Critical corrections or announcements

#### Weekly Updates  
- **Essential Cardano Repository**: Sync with GitHub changes
- **Cardano Documentation**: Official docs updates
- **Community Resources**: New tools and resources

#### Monthly Reviews
- **Research Papers**: New IOG research publications
- **Deprecated Content**: Remove outdated information  
- **Quality Audit**: Review response accuracy and user feedback

### Content Source Management

#### Essential Cardano AI Assistant
**Repository**: https://github.com/input-output-hk/essential-cardano-content
**Update process**:
1. Monitor repository for changes
2. Review new/modified content for quality
3. Update RAG Assistant with approved changes
4. Test key queries to verify improvements

**Content filters**:
- ✅ Include: Glossary updates, FAQ additions, community resources
- ❌ Exclude: Draft content, internal planning documents

#### Intersect Governance Assistant  
**Source**: https://docs.intersectmbo.org/
**Update process**:
1. Manual review of governance changes
2. Priority on constitutional updates and process changes
3. Coordinate with Neil Burgess for access to updates
4. Test governance-specific queries

**Content priorities**:
- 🔥 High: Constitutional changes, voting procedures
- 📋 Medium: DRep education updates, tool changes
- 📝 Low: Historical governance information

#### Cardano Technical Assistant
**Source**: https://docs.cardano.org/  
**Update process**:
1. Monitor official documentation repository
2. Sync technical specifications and feature updates
3. Verify no development code examples included
4. Test technical accuracy

**Content management**:
- ✅ Include: Network operations, technical specifications, feature explanations
- ❌ Exclude: Implementation code, development tutorials (redirect to Developer Portal)

#### IOG Research Assistant
**Sources**: IOG blog, research papers
**Update process**:
1. Weekly scan for new blog posts
2. Add publication date metadata
3. Coordinate with Allan's research AI for paper integration
4. Archive content older than 24 months

**Date management**:
- Recent content (0-6 months): High priority, current status
- Older content (6-24 months): Available with date context
- Archived content (24+ months): Remove or clearly mark as historical

### Quality Control Process

#### Pre-Update Checklist
- [ ] Content is publicly available
- [ ] No sensitive or confidential information
- [ ] Source attribution is clear
- [ ] Publication date is available for time-sensitive content
- [ ] Content aligns with target user personas

#### Post-Update Verification
- [ ] RAG Assistant indexing completed successfully
- [ ] Test queries return improved responses
- [ ] Source citations include new content appropriately
- [ ] No degradation in existing query quality
- [ ] Response times remain acceptable

### Update Coordination

#### Team Communication
**Before major updates**:
- Notify team of planned content changes
- Coordinate with Allan's research AI team for overlapping content
- Schedule maintenance windows for large updates

**After updates**:
- Report completion status
- Share any issues encountered
- Document improvements or degradations observed

#### Version Control
- Maintain backup of previous RAG Assistant state
- Document all changes with timestamps
- Track performance metrics before/after updates
- Plan rollback procedures for problematic updates

### Monitoring & Metrics

#### Content Freshness Tracking
- Last update date for each knowledge source
- Number of new/modified documents per update
- User queries that would benefit from newer content

#### Performance Impact Assessment  
- Response quality changes after updates
- Query response time variations
- User satisfaction scores pre/post update
- Source attribution accuracy

#### Issue Tracking
- Failed content ingestions
- Quality degradations after updates
- User-reported inaccuracies
- Missing or broken links

### Emergency Update Protocol

#### Critical Issues (Immediate action required)
- Factual errors in governance information
- Broken links to essential resources
- Privacy or security information exposure
- Major policy changes affecting user guidance

#### Emergency Response Steps
1. **Assess impact**: Determine scope of issue
2. **Quick fix**: Remove/correct problematic content
3. **Test verification**: Ensure fix resolves issue
4. **Team notification**: Alert stakeholders of emergency update
5. **Follow-up review**: Plan permanent solution

### Integration with Development Workflow

#### Staging Environment
- Test all content updates in staging before production
- Verify integration with system prompts and URL references
- Run full testing protocol before deployment

#### Production Deployment
- Schedule updates during low-usage periods
- Monitor system performance during updates
- Have rollback plan ready for immediate issues

#### Post-Deployment Monitoring
- Watch for unusual query patterns
- Monitor error rates and response quality
- Gather user feedback on new content effectiveness