# Cardano Developer Portal Dataset - September 19, 2025

## Dataset Overview

This folder contains a comprehensive extraction of content from developers.cardano.org as individual page files, suitable for RAG (Retrieval-Augmented Generation) systems and AI assistants.

## Extraction Details

- **Extraction Date**: September 19, 2025
- **Source Website**: https://developers.cardano.org
- **Total Files**: 225 individual JSON files
- **Success Rate**: 93.0% (225 successful extractions from 242 discovered URLs)
- **Extraction Method**: Tavily API with systematic sitemap parsing

## Content Coverage

### Content Types Included:
- **Blog Posts**: Monthly developer updates, technical insights (2021-2025)
- **Get Started**: Beginner guides for Cardano development
- **Smart Contracts**: Aiken, Plutarch, Marlowe development guides
- **Governance**: Participation and voting mechanisms
- **Native Tokens**: Token creation and management
- **Integrate Cardano**: Wallet integrations and API usage
- **Stake Pool Operations**: Technical setup and maintenance guides
- **Transaction Metadata**: Advanced transaction features

### Sample Content Areas:
- Smart contract development tutorials
- Blockchain fundamentals for developers
- CLI tools and operations
- Security best practices
- Development environment setup
- API integrations and SDKs
- Community tools and showcase projects

## File Structure

Each JSON file follows this format:
```json
{
  "url": "https://developers.cardano.org/[page-path]",
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
- `developers.cardano.org_docs_get-started.json` → `https://developers.cardano.org/docs/get-started`
- `developers.cardano.org_blog_monthly-update.json` → Monthly update blog posts
- `developers.cardano.org_docs_smart-contracts_aiken.json` → Aiken development guides

## Usage for AI Assistants

This dataset is optimized for:

### Citation Capability
- Each file maps to a specific URL for precise source attribution
- AI assistants can provide exact page citations for every response
- Enables transparent, verifiable answers with working links

### Content Quality
- Zero data loss from original extraction
- Complete context preserved for accurate responses
- Developer-focused content suitable for technical queries

### RAG System Integration
- Individual files enable granular content retrieval
- Clean JSON format for easy parsing
- Comprehensive metadata for content management

## Extraction Pipeline

1. **Sitemap Discovery**: Systematic parsing of developers.cardano.org sitemap
2. **Batch Extraction**: Tavily API processing (20 URLs per batch for mixed content)
3. **Content Preservation**: Raw content saved without lossy processing
4. **File Organization**: URL-based naming for clear mapping

## Quality Metrics

- **Completeness**: 93.0% of discovered URLs successfully extracted
- **Accuracy**: Direct extraction preserves original formatting and links
- **Coverage**: All major developer portal sections included
- **Freshness**: Extracted September 2025 with latest development guides and blog updates

## Use Cases

- **Cardano Developer Assistant**: Code-focused chatbot with complete developer portal knowledge
- **Educational Platform**: Comprehensive learning resource for Cardano development
- **Technical Documentation Search**: Searchable developer reference and tutorials
- **Training Data**: Fine-tuning language models on Cardano development content

## Technical Notes

- **No Processing Artifacts**: Raw content preserved exactly as extracted
- **Comprehensive Coverage**: Blog posts, tutorials, guides, and technical documentation
- **Production Ready**: Suitable for immediate deployment in RAG systems
- **Globant Compatible**: Format optimized for Globant Enterprise AI platform

## Comparison with Other Cardano Datasets

This dataset complements other Cardano knowledge sources:
- **Essential Cardano**: Community knowledge, FAQ, ecosystem updates
- **Cardano Documentation**: Official technical specifications and infrastructure
- **Developer Portal**: Practical development guides, tutorials, and community tools
- **Combined Usage**: Complete Cardano development ecosystem spanning theory to practice

---

**Generated**: September 19, 2025
**Pipeline**: Tavily API → Raw Extraction → Individual File Splitting
**Status**: Production Ready
**Next Step**: Upload to Globant Enterprise AI for comprehensive Cardano developer assistant deployment
