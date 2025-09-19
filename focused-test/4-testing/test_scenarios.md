# Test Scenarios for Essential Cardano AI Assistant

## Objective
Test the deployed RAG Assistant to verify it can provide accurate responses with working source URLs from our extracted content.

## Test Categories

### 1. Content Accuracy Tests
**Scenario**: Ask questions about content we know we extracted
- "What is staking on Cardano?"
- "How do I choose a stake pool?"
- "What is Cardano governance?"

**Success Criteria**:
- ✅ Accurate information matching extracted content
- ✅ Proper source attribution ("According to Essential Cardano FAQ...")
- ✅ No hallucinated information

### 2. URL Citation Tests
**Scenario**: Request specific sources or "where can I learn more"
- "Where can I read more about staking?"
- "Show me the official documentation about governance"
- "Give me the FAQ link for delegation"

**Success Criteria**:
- ✅ Provides working URLs from our extracted content
- ✅ URLs lead to the correct pages
- ✅ URLs include proper unique identifiers (e.g., `-716f9c75`)

### 3. Source Attribution Tests
**Scenario**: Questions requiring source differentiation
- "What's the difference between Essential Cardano and Cardano Docs explanations?"
- "Is this from the FAQ or glossary?"

**Success Criteria**:
- ✅ Correctly identifies source (essentialcardano.io vs docs.cardano.org)
- ✅ Can differentiate between FAQ, glossary, documentation
- ✅ Maintains attribution consistency

### 4. Limitation Tests
**Scenario**: Ask about content we didn't extract
- "How do I develop smart contracts?" (developer content we may not have)
- "What's the latest Cardano news?" (time-sensitive content)

**Success Criteria**:
- ✅ Acknowledges knowledge limitations
- ✅ Redirects to appropriate sources
- ✅ Doesn't fabricate information

## Test Results Template

```
Question: [Test question]
Response: [Assistant response]
URLs Provided: [List any URLs in response]
URL Status: [✅ Working / ❌ Broken / ⚠️ Redirects]
Content Accuracy: [✅ Accurate / ❌ Inaccurate / ⚠️ Partial]
Source Attribution: [✅ Correct / ❌ Missing / ⚠️ Vague]
Overall: [PASS/FAIL]
Notes: [Additional observations]
```

## Success Metrics

- **URL Accuracy**: 90%+ of provided URLs should work correctly
- **Content Accuracy**: 95%+ of factual claims should be correct
- **Source Attribution**: 100% of responses should include proper attribution
- **No Hallucination**: 0% fabricated information about content we didn't extract