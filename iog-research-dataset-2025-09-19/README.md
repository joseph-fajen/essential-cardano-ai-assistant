# IOG Research Dataset - September 19, 2025

## Dataset Overview

This folder contains a comprehensive extraction of research content from iohk.io as individual page files, suitable for RAG (Retrieval-Augmented Generation) systems and AI assistants. This dataset focuses on IOG's research publications, academic papers, and technical research rather than blog content.

## Extraction Details

- **Extraction Date**: September 19, 2025
- **Source Website**: https://iohk.io/en/research
- **Total Files**: 624 individual JSON files
- **Success Rate**: 100% for research content (624 successful extractions from research URLs)
- **Extraction Method**: Tavily API with systematic sitemap parsing
- **Content Focus**: Research publications and academic papers (blog posts excluded due to bot protection)

## Content Coverage

### Content Types Included:
- **Research Publications**: Peer-reviewed academic papers and research documents
- **Technical Research**: Cryptographic protocols and consensus mechanisms
- **Whitepapers**: Foundational documents for Cardano protocols
- **Research Library**: Complete IOG research archive and publications
- **Technical Specifications**: Formal protocol definitions and technical standards

### Sample Content Areas:
- Ouroboros consensus protocol family (Praos, Genesis, Leios)
- Zero-knowledge proofs and cryptographic primitives
- Blockchain scalability and layer 2 solutions
- Formal verification and protocol analysis
- Extended UTXO model and smart contract platforms
- Cryptographic innovations and security proofs
- Peer-to-peer networking and distributed systems

### Temporal Coverage:
- **Date Range**: 2016-2025 (9+ years of research)
- **Historical Context**: Complete evolution of IOG's research contributions to blockchain science
- **Recent Research**: Latest developments in cryptographic protocols and consensus mechanisms

## File Structure

Each JSON file follows this format:
```json
{
  "url": "https://iohk.io/en/research/library/papers/[paper-title]",
  "content": "[Full research paper content as extracted]",
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

Files are named using URL-to-filename conversion preserving research structure:
- `iohk.io_en_research_library_papers_ouroboros-leios-design-goals-and-concepts.json` → Research paper on Ouroboros Leios
- `iohk.io_en_research_library_papers_extended-utxo-model.json` → Extended UTXO research paper
- `iohk.io_en_research_[category]_[paper-title].json` → Research publications organized by category

## Usage for AI Assistants

This dataset is optimized for:

### Citation Capability
- Each file maps to a specific URL for precise source attribution
- AI assistants can provide exact research paper citations with publication metadata
- Enables transparent, verifiable answers with working links to original research

### Content Quality
- Zero data loss from original extraction
- Complete context preserved for accurate responses
- Peer-reviewed research content suitable for academic and expert-level queries

### RAG System Integration
- Individual files enable granular content retrieval
- Clean JSON format for easy parsing
- Comprehensive metadata for content management

## Extraction Pipeline

1. **Sitemap Discovery**: Systematic parsing of iohk.io sitemap for research content
2. **Content Filtering**: Focus on research papers and academic publications (excluding blog posts due to bot protection)
3. **Batch Extraction**: Tavily API processing (20 URLs per batch for research content)
4. **Content Preservation**: Raw content saved without lossy processing
5. **File Organization**: Research-aware naming preserving publication structure

## Quality Metrics

- **Completeness**: 100% of research URLs successfully extracted (624 research papers)
- **Accuracy**: Direct extraction preserves original formatting and links
- **Coverage**: Complete IOG research archive spanning 2016-2025
- **Freshness**: Extracted September 2025 with latest research publications

## Use Cases

- **Academic Research Assistant**: Technical chatbot with complete IOG research knowledge
- **Protocol Development**: Understanding formal specifications and technical foundations
- **Research Documentation Search**: Searchable archive of peer-reviewed research and whitepapers
- **Training Data**: Fine-tuning language models on cryptographic and blockchain research content

## Technical Notes

- **No Processing Artifacts**: Raw content preserved exactly as extracted
- **Comprehensive Archive**: Complete IOG research library with publication structure preserved
- **Production Ready**: Suitable for immediate deployment in RAG systems
- **Globant Compatible**: Format optimized for Globant Enterprise AI platform

## Comparison with Other Cardano Datasets

This dataset complements other Cardano knowledge sources:
- **Essential Cardano**: Community knowledge, FAQ, ecosystem updates
- **Cardano Documentation**: Official technical specifications and infrastructure
- **Developer Portal**: Practical development guides and tutorials
- **IOG Research**: Academic papers, research publications, formal specifications
- **Combined Usage**: Complete Cardano knowledge spanning community resources to cutting-edge research

## Historical Significance

This dataset captures the complete intellectual history of Input Output Global's contributions to:
- Blockchain consensus mechanisms (Ouroboros family)
- Smart contract platforms and virtual machines
- Cryptographic innovations and zero-knowledge proofs
- Governance systems and democratic blockchain evolution
- Scalability solutions and layer 2 protocols

---

**Generated**: September 19, 2025
**Pipeline**: Tavily API → Raw Extraction → Individual File Splitting
**Status**: Production Ready
**Next Step**: Upload to Globant Enterprise AI for comprehensive IOG research assistant deployment
