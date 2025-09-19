# Router Flow Technical Specifications

## Overview
Technical documentation for the intelligent routing system that directs user queries to appropriate specialized RAG Assistants on the Essential Cardano AI platform.

## Architecture Summary

### Core Components
```
User Query (essentialcardano.io) 
    ↓
JavaScript Widget (Globant Enterprise)
    ↓  
Router Flow (Intent Classification)
    ↓
Specialized RAG Assistant Selection
    ↓
Response Generation + Source Citations
    ↓
Return to User Interface
```

## Router Flow Logic

### Phase 1: Two-Assistant Routing

#### Essential Cardano AI Assistant
**Trigger Conditions:**
- **Keywords**: "staking", "voting", "governance", "beginner", "what is", "how to start", "newcomer"
- **Intent Patterns**: 
  - Questions about basic concepts
  - Community engagement queries
  - Onboarding and getting started
  - General Cardano ecosystem questions
- **Confidence Threshold**: > 70%

**Example Queries:**
- "What is staking in Cardano?"
- "How do I vote in Cardano governance?"
- "I'm new to Cardano, where do I start?"
- "What is the Essential Cardano Guide?"

#### Cardano Docs AI Assistant  
**Trigger Conditions:**
- **Keywords**: "node", "SPO", "stake pool", "operator", "fees", "technical", "configuration", "testnet", "developer"
- **Intent Patterns**:
  - Technical implementation questions
  - Stake pool operation queries
  - Node configuration and maintenance
  - Testing environment questions
- **Confidence Threshold**: > 70%

**Example Queries:**
- "How do I set up a Cardano node?"
- "What are the requirements to run a stake pool?"
- "How do transaction fees work technically?"
- "How to configure a testnet environment?"

### Fallback Logic
- **Default Route**: Essential Cardano AI Assistant (community focus)
- **Low Confidence**: Present both options to user
- **Ambiguous Queries**: Route to Essential Cardano with explanation

## Implementation in Globant Enterprise

### Flow Structure
```
1. User Input Node
   ↓
2. Intent Analysis Node
   - Natural language processing
   - Keyword extraction
   - Context analysis
   ↓
3. Conditional Routing Node  
   - Score each assistant (0-100)
   - Apply confidence thresholds
   - Select highest scoring route
   ↓
4. Assistant Invocation Node
   - Call selected RAG Assistant
   - Pass original query + context
   ↓  
5. Response Processing Node
   - Format response
   - Add source citations
   - Apply branding
   ↓
6. Output Node
   - Return to widget interface
```

### Conditional Logic Configuration

#### Primary Routing Rules
```javascript
// Pseudocode for routing logic
if (queryContains(["node", "SPO", "stake pool", "operator", "fees", "technical"]) || 
    intentClassification == "technical_implementation") {
    route = "cardano_docs_assistant";
    confidence = calculateConfidence(keywords, context);
} else if (queryContains(["staking", "voting", "governance", "beginner", "what is"]) ||
           intentClassification == "community_onboarding") {
    route = "essential_cardano_assistant"; 
    confidence = calculateConfidence(keywords, context);
} else {
    route = "essential_cardano_assistant"; // Default fallback
    confidence = 0.5; // Medium confidence
}
```

#### Confidence Scoring Algorithm
```
Base Score: 0-100 points
+ Keyword Matches: +10 points per primary keyword
+ Intent Classification: +20 points for high-confidence intent
+ Context Relevance: +15 points for domain-specific context
+ User History: +5 points for consistent domain queries

Final Score = min(100, Base Score + Bonuses)
```

## Website Widget Integration

### JavaScript Implementation
```html
<!-- Essential Cardano Website Integration -->
<script>
// Globant Enterprise Generated Widget Code
(function() {
    // Dynamic SDK loading
    var script = document.createElement('script');
    script.src = 'https://workspace.saia.ai/static/js/web-sdk.js';
    script.async = true;
    
    script.onload = function() {
        // Initialize router flow widget
        var chatWidget = document.createElement('fluentlab-app');
        
        // Configuration
        chatWidget.setAttribute('applicationkey', 'ESSENTIAL_CARDANO_ROUTER_KEY');
        chatWidget.setAttribute('title', 'Essential Cardano AI Assistant');
        chatWidget.setAttribute('launcher', 'true');
        chatWidget.setAttribute('branding', 'essential-cardano');
        
        // Custom styling
        chatWidget.style.setProperty('--fluentlab-primary-color', '#1b4fa0');
        chatWidget.style.setProperty('--fluentlab-header-bg', '#1b4fa0');
        
        document.body.appendChild(chatWidget);
    };
    
    document.head.appendChild(script);
})();
</script>
```

### Custom Styling Requirements
```css
/* Essential Cardano Branding */
:root {
    --fluentlab-primary-color: #1b4fa0;
    --fluentlab-secondary-color: #ffffff;
    --fluentlab-header-bg: #1b4fa0;
    --fluentlab-header-text: #ffffff;
    --fluentlab-border-radius: 8px;
    --fluentlab-font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
}

/* Widget positioning */
fluentlab-app {
    position: fixed;
    bottom: 20px;
    right: 20px;
    z-index: 1000;
}

/* Responsive behavior */
@media (max-width: 768px) {
    fluentlab-app {
        bottom: 10px;
        right: 10px;
        left: 10px;
        width: calc(100% - 20px);
    }
}
```

## Performance Specifications

### Response Time Targets
- **Query Analysis**: < 500ms
- **Assistant Routing**: < 200ms  
- **RAG Response Generation**: < 2.5s
- **Total Response Time**: < 3.5s

### Accuracy Targets
- **Routing Accuracy**: > 90% correct assistant selection
- **Response Relevance**: > 85% user satisfaction
- **Source Attribution**: 100% responses include proper citations

### Scalability Requirements
- **Concurrent Users**: Support 100+ simultaneous conversations
- **Query Volume**: Handle 1,000+ queries per day
- **Response Consistency**: Maintain performance under load

## Monitoring and Analytics

### Key Metrics to Track
```
Router Performance:
- Routing accuracy percentage
- Confidence score distribution
- Fallback usage frequency
- Query classification success rate

User Experience:
- Average response time
- User satisfaction ratings
- Conversation completion rates
- Most common query types

Assistant Usage:
- Query distribution between assistants
- Response quality by assistant
- Knowledge gap identification
- Content effectiveness metrics
```

### Error Handling
```
Error Scenarios:
1. Assistant Unavailable
   - Fallback to alternative assistant
   - Display service status message
   
2. Low Confidence Routing
   - Present multiple options to user
   - Allow manual assistant selection
   
3. Query Processing Failure
   - Graceful error message
   - Suggest query reformulation
   
4. Network/Connectivity Issues  
   - Retry mechanism (3 attempts)
   - Offline mode message
```

## Future Enhancements (Phase 2-4)

### Multi-Assistant Expansion
```
Phase 2: Three-Way Routing
+ Intersect Governance Assistant
- Governance keywords: "constitution", "DRep", "voting", "proposal"

Phase 3: Four-Way Routing  
+ Developer Portal Assistant
- Developer keywords: "code", "API", "tutorial", "SDK", "integration"

Phase 4: Five-Way Routing
+ IOG Research Assistant
- Research keywords: "research", "paper", "announcement", "blog", "update"
```

### Advanced Routing Features
- **Context Awareness**: Remember conversation history
- **User Profiling**: Adapt routing based on user expertise level
- **Cross-Assistant Referencing**: Route follow-up questions intelligently  
- **A/B Testing**: Optimize routing algorithms based on outcomes

### Integration Enhancements
- **Voice Input**: Support speech-to-text queries
- **Multilingual**: Support additional languages beyond English
- **Rich Responses**: Include images, charts, and interactive elements
- **Mobile App**: Native mobile application integration

## Security and Privacy

### Data Handling
- **Query Logging**: Anonymized for analytics only
- **Personal Information**: No storage of personally identifiable data
- **Session Management**: Temporary session IDs, auto-expire
- **GDPR Compliance**: European privacy regulation compliance

### Access Control
- **Rate Limiting**: Prevent abuse and ensure fair usage
- **Content Filtering**: Block inappropriate or malicious queries
- **Authentication**: Optional user accounts for enhanced experience
- **Audit Trail**: Log routing decisions for quality assurance

---

**Document Version**: 1.0  
**Last Updated**: September 11, 2025  
**Implementation Target**: Phase 1 - Next 2-3 weeks  
**Platform**: Globant Enterprise AI (console.saia.ai)