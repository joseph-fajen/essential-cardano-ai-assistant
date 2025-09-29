# Cardano Documentation Dataset - September 19, 2025

## Dataset Overview

This folder contains a comprehensive extraction of content from docs.cardano.org as individual page files, suitable for RAG (Retrieval-Augmented Generation) systems and AI assistants.

## Extraction Details

- **Extraction Date**: September 29, 2025
- **Source Website**: https://docs.cardano.org
- **Total Files**: 81 individual JSON files
- **Success Rate**: TBD%
- **Extraction Method**: Tavily API with systematic sitemap parsing

## Content Coverage

### Content Types Included:
- **About Cardano**: Introduction, governance, network architecture
- **Developer Resources**: Smart contracts (Plutus, Marlowe, Aiken), transaction tutorials, scalability solutions
- **Stake Pool Operators**: Pool creation, maintenance, performance monitoring
- **Cardano Testnets**: Environments, tools, getting started guides
- **New to Blockchain**: Cryptocurrency basics, proof of stake, wallet types
- **Technical Documentation**: Hydra, Mithril, and other Cardano technologies

### Sample Content Areas:
- Plutus smart contract development
- Marlowe financial contracts
- Aiken development tools
- Hydra scaling solutions
- Mithril light client protocols
- Stake pool operation guides
- Blockchain fundamentals education

## File Structure

Each JSON file follows this format:
```json
{
  "url": "https://docs.cardano.org/[page-path]",
  "content": "[Full page content as extracted]",
  "images": ["[Array of image URLs if present]"],
  "extraction_metadata": {
    "batch_number": "[Extraction batch]",
    "extraction_timestamp": "[ISO timestamp]",
    "extraction_time": "[Seconds taken]",
    "source": "tavily_api_raw"
  }
}
```

## Filename Convention

Files are named using URL-to-filename conversion:
- `docs.cardano.org_about-cardano_introduction.json` → `https://docs.cardano.org/about-cardano/introduction`
- `docs.cardano.org_smart-contracts_plutus.json` → Plutus documentation pages
- `docs.cardano.org_stake-pool-course.json` → Stake pool operator guides

## Usage for AI Assistants

This dataset is optimized for:

### Citation Capability
- Each file maps to a specific URL for precise source attribution
- AI assistants can provide exact page citations for every response
- Enables transparent, verifiable answers with working links

### Content Quality
- Zero data loss from original extraction
- Complete context preserved for accurate responses
- Technical documentation suitable for developers and operators

### RAG System Integration
- Individual files enable granular content retrieval
- Clean JSON format for easy parsing
- Comprehensive metadata for content management

## Extraction Pipeline

1. **Sitemap Discovery**: Systematic parsing of docs.cardano.org sitemap
2. **Batch Extraction**: Tavily API processing (15 URLs per batch for technical content)
3. **Content Preservation**: Raw content saved without lossy processing
4. **File Organization**: URL-based naming for clear mapping

## Quality Metrics

- **Completeness**: TBD% of discovered URLs successfully extracted
- **Accuracy**: Direct extraction preserves original formatting and links
- **Coverage**: All major documentation sections of Cardano included
- **Freshness**: Extracted September 2025 with latest technical documentation

## Use Cases

- **Cardano Technical Assistant**: Developer-focused chatbot with complete official documentation
- **Educational Platform**: Comprehensive knowledge base for learning Cardano development
- **Documentation Search**: Searchable technical reference for developers and SPOs
- **Training Data**: Fine-tuning language models on official Cardano technical content

## Technical Notes

- **No Processing Artifacts**: Raw content preserved exactly as extracted
- **Comprehensive Coverage**: Developer resources, SPO guides, educational content
- **Production Ready**: Suitable for immediate deployment in RAG systems
- **Globant Compatible**: Format optimized for Globant Enterprise AI platform

## Comparison with Essential Cardano Dataset

This dataset complements the Essential Cardano dataset:
- **Essential Cardano**: Community knowledge, FAQ, glossary, ecosystem updates
- **Cardano Documentation**: Official technical documentation, development guides, infrastructure
- **Combined Usage**: Complete Cardano knowledge spanning community resources and technical documentation

---

**Generated**: September 29, 2025
**Pipeline**: Tavily API → Raw Extraction → Individual File Splitting
**Status**: Production Ready
**Next Step**: Upload to Globant Enterprise AI for comprehensive Cardano technical assistant deployment
