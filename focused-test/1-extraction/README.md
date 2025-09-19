# Step 1: Content Extraction

Extract targeted content from Essential Cardano websites using the Firecrawl API.

## Target Pages

Focus on 5-10 high-value pages that users commonly ask about:

### Essential Cardano (essentialcardano.io)
- FAQ: What is staking and delegation?
- FAQ: How do I choose a stake pool?
- Glossary: Key terms
- Governance overview

### Cardano Docs (docs.cardano.org)
- Introduction to Cardano
- Staking guide
- Governance overview

### Developer Portal (developers.cardano.org)
- Getting started guide
- Wallet integration

## Scripts

- `extract_test_content.py` - Focused extraction script for test pages
- Uses `../tools/` scripts as foundation

## Output

- `raw_extractions/` - Raw JSON files from Firecrawl API
- Each file contains: URL, metadata, content, links, extraction timestamp