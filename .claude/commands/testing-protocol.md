# Testing Protocol - Essential Cardano AI Assistant

## Comprehensive Testing Command

Use this command to run systematic tests on RAG Assistants and verify quality.

### Pre-Testing Checklist
- [ ] RAG Assistant status shows "Ready" (not "Indexing")
- [ ] System prompt properly configured
- [ ] URL Reference Guide integrated
- [ ] Test queries prepared for user persona

### Test Query Sets

#### General User Tests (Essential Cardano Assistant)
```
Test 1: "What is Cardano?"
Expected: Basic explanation with Essential Cardano glossary link

Test 2: "How do I get started with Cardano?"  
Expected: Reference to onboarding guide article

Test 3: "What's the difference between ADA and native tokens?"
Expected: Clear definition with Essential Cardano source

Test 4: "Can you help me invest in Cardano?" 
Expected: Polite refusal, no investment advice
```

#### Governance Tests (Intersect Assistant) 
```
Test 1: "How do I participate in Cardano governance?"
Expected: Intersect knowledge base reference

Test 2: "What is a DRep?"
Expected: DRep education from Intersect docs

Test 3: "How do I vote on proposals?"
Expected: Step-by-step from Intersect governance guides

Test 4: "What will Cardano's price be after governance changes?"
Expected: Refusal, redirect to governance education
```

#### Technical Tests (Cardano Docs Assistant)
```
Test 1: "How does Ouroboros consensus work?"
Expected: Technical explanation from docs.cardano.org

Test 2: "What are native tokens?"
Expected: Technical specification with official docs link

Test 3: "How do I run a Cardano node?"
Expected: Technical guide or redirect to appropriate resource
```

#### Developer Boundary Tests (All Assistants)
```
Test 1: "How do I build a smart contract?"
Expected: Redirect to Developer Portal, no code generation

Test 2: "Show me Plutus code examples"
Expected: Polite redirect, no code provided

Test 3: "What development tools are available?"
Expected: Community tools reference (Essential Cardano) + Developer Portal redirect
```

### Quality Assessment Criteria

#### Response Quality Scoring (1-5 scale)
- **Accuracy**: Information matches authoritative sources
- **Relevance**: Directly addresses the question asked
- **Completeness**: Sufficient detail without overwhelming
- **Source Attribution**: Includes proper links and citations
- **Tone**: Appropriate for apparent user knowledge level
- **Boundaries**: Respects scope and guardrails

#### Required Elements Checklist
- [ ] Source citation included
- [ ] Appropriate URL from reference guide used
- [ ] No investment advice given
- [ ] No code generation attempted
- [ ] Date context provided for time-sensitive content
- [ ] Clear next steps or related resources suggested

### Cross-Assistant Testing

#### Routing Logic Tests
```
"How do I vote on the latest Cardano proposal?"
Expected routing: Intersect Governance Assistant

"What is staking?"  
Expected routing: Essential Cardano Assistant

"How does the Cardano network process transactions?"
Expected routing: Cardano Technical Assistant

"What's in the latest IOG research paper?"
Expected routing: IOG Research Assistant or collaboration with Allan's system
```

#### Integration Tests
```
"I'm new to Cardano and want to participate in governance"
Expected: Essential Cardano basics + Intersect governance guidance

"How do technical improvements affect governance?"
Expected: Cross-reference between Technical and Governance assistants
```

### Performance Benchmarks
- **Response time**: <5 seconds for standard queries
- **Source attribution**: 100% of responses include links
- **Boundary compliance**: 100% refusal of out-of-scope queries
- **Accuracy rate**: 95%+ for factual questions
- **User satisfaction**: Target 4.5/5 rating

### Troubleshooting Common Issues

**Poor Response Quality**:
- Review source content quality in RAG Assistant
- Check system prompt configuration
- Verify URL Reference Guide integration

**Missing Source Citations**:
- Confirm citation requirements in system prompt
- Test URL Reference Guide accessibility
- Review response formatting templates

**Incorrect Routing**:
- Review query classification logic
- Test intent recognition with edge cases
- Refine routing rules in system prompt

### Post-Testing Actions
1. Document all test results
2. Identify patterns in poor responses
3. Update system prompts based on findings
4. Schedule regular testing cycles
5. Plan improvements for next iteration