# Content Ingestion Workflow - Essential Cardano AI Assistant

## Immediate Action Plan (Based on Current Screenshot)

### Current Status
- ✅ "Essential Cardano AI Assistant" with ~1,000 files uploaded
- ⚠️ Status shows "Indexing" - wait for completion before adding more content
- 🎯 **Recommendation**: Do NOT add more content to this RAG Assistant yet

### Step 1: Complete Current Indexing
**Before proceeding**:
- Wait for "Essential Cardano AI Assistant" status to change from "Indexing" to "Ready"
- Test current assistant with basic queries to verify functionality
- Ensure quality of responses with existing Essential Cardano content

### Step 2: Create Second RAG Assistant
**Next immediate action**:
1. Click "CREATE NEW" button (visible in screenshot)
2. Name: "Intersect Governance Assistant"
3. Upload Intersect knowledge base content
4. Configure with governance-specific settings

## Content Source Priorities

### Priority 1: Intersect Governance Content
**Why first**: Critical for governance questions, distinct content type, manageable size

**Content to upload**:
- Intersect knowledge base documents (docs.intersectmbo.org)
- Constitutional documents
- Governance process guides
- DRep education materials

**Expected file count**: 200-500 files (estimate)

### Priority 2: Cardano Technical Documentation
**Why second**: Large, stable content set with clear boundaries

**Content to upload**:
- docs.cardano.org documentation
- Technical specifications
- Network operation guides

**Expected file count**: 500-1,000 files (estimate)

### Priority 3: IOG Recent Content
**Why third**: Requires date-aware processing, most complex to manage

**Content to upload**:
- IOG blog posts (last 24 months)
- Recent announcements
- Research summaries (not full papers - coordinate with Allan)

**Expected file count**: 100-300 files (estimate)

## Quality Control Checklist

### Before Uploading Any New Content Source

**Content Audit**:
- [ ] Remove duplicate files
- [ ] Verify all content is publicly available
- [ ] Check for sensitive or confidential information
- [ ] Ensure content is current (remove outdated material)
- [ ] Add metadata tags if platform supports

**File Preparation**:
- [ ] Convert content to supported formats (text, markdown, PDF)
- [ ] Standardize file naming conventions
- [ ] Include source attribution in file metadata
- [ ] Add publication dates for time-sensitive content

### Post-Upload Verification

**For each new RAG Assistant**:
- [ ] Wait for indexing completion
- [ ] Test with 5-10 sample queries
- [ ] Verify source attribution in responses
- [ ] Check for hallucination or incorrect information
- [ ] Confirm proper boundary respect (no investment advice, etc.)

## Globant Platform Usage Guidelines

### RAG Assistant Naming Convention
```
[Source Type] [Purpose] Assistant
Examples:
- Essential Cardano AI Assistant (current)
- Intersect Governance Assistant
- Cardano Technical Assistant
- IOG Research Assistant
```

### Document Management Best Practices

**File Organization**:
- Group related documents in folders/batches
- Use consistent naming: `source_type_document_name_date.ext`
- Include version numbers for updated documents
- Tag with content type metadata

**Update Strategy**:
- **Essential Cardano**: Monthly sync with repository
- **Intersect**: Manual updates for governance changes
- **Technical Docs**: Bi-weekly sync with official repos
- **IOG Content**: Weekly sync for new blog posts

### Testing Protocol for Each RAG Assistant

**Standard Test Queries**:
1. **Basic Concept**: "What is [fundamental concept]?"
2. **Specific Information**: "How do I [perform specific task]?"
3. **Boundary Test**: "What should I invest in?" (should refuse)
4. **Source Attribution**: Verify links are provided
5. **Cross-Reference**: Test when answer spans multiple sources

**Quality Metrics**:
- Response accuracy: 95%+ for factual questions
- Source attribution: 100% of responses include links
- Boundary respect: 100% refusal of out-of-scope questions
- Response time: <5 seconds for standard queries

## Integration Workflow

### Multi-Assistant Query Routing

**Implementation Steps**:
1. Create all RAG Assistants separately
2. Test each individually for quality
3. Implement routing logic in system prompt
4. Create unified frontend that calls appropriate assistant
5. Add cross-assistant referencing capabilities

**Query Classification Examples**:
```
"How do I vote on governance proposals?" → Intersect Governance Assistant
"What is native token?" → Essential Cardano AI Assistant  
"How does Ouroboros consensus work?" → Cardano Technical Assistant
"What's new in latest Cardano update?" → IOG Research Assistant
"How do I build a dApp?" → Redirect to Developer Portal
```

## Troubleshooting Common Issues

### If Indexing Fails
- Check file formats are supported
- Verify file sizes within limits
- Remove corrupted or empty files
- Contact Globant support if persistent

### If Responses Are Poor Quality
- Review source content quality
- Check for conflicting information between sources
- Refine system prompt instructions
- Consider removing low-quality documents

### If Source Attribution Is Missing
- Verify URL Reference Guide is properly integrated
- Check system prompt instructions for citation requirements
- Test with specific queries that should trigger links
- Update prompt with better citation examples

## Next Steps Summary

1. ⏳ **Wait** for current indexing to complete
2. 🧪 **Test** Essential Cardano AI Assistant thoroughly
3. 🆕 **Create** Intersect Governance Assistant
4. 📤 **Upload** Intersect content to new assistant
5. 🔄 **Repeat** process for technical documentation
6. 🔗 **Implement** routing between assistants
7. 🚀 **Deploy** unified frontend experience

This approach gives you granular control while building toward the sophisticated multi-agent system outlined in your strategy.