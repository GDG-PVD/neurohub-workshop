# ADR-007: NeuroHub Ally AI Assistant Integration

## Status
Accepted

## Context
The NeuroHub platform needed an AI assistant interface to connect workshop participants with the multi-agent system they build during the workshop. This assistant serves as the primary interaction point between users and the AI agents (documentation, signal processor, experiment designer, and orchestrator).

## Decision
We implemented NeuroHub Ally as a web-based chat interface that:
1. Provides a user-friendly form for research queries
2. Connects to A2A agents via HTTP when available
3. Falls back to mock responses when agents are offline
4. Uses Server-Sent Events (SSE) for streaming responses
5. Intelligently routes queries to appropriate specialized agents

## Consequences

### Positive
- Seamless workshop experience - works with or without agents running
- Clear visual feedback about agent availability and status
- Supports real-time streaming for responsive interaction
- Extensible architecture for adding new agents
- Follows existing architectural patterns (ADR-004 Multi-Agent Architecture)

### Negative
- Requires all agents to be running locally for full functionality
- Additional complexity in handling both streaming and non-streaming responses
- Potential latency when discovering available agents

## Implementation Details

### Architecture Components
1. **Frontend** (`neurohub_ally.html`):
   - Bootstrap-based UI matching NeuroHub design
   - JavaScript SSE client for streaming responses
   - Fallback handling for non-streaming endpoints

2. **Backend Integration** (`actual_ai_integration.py`):
   - A2AClient class for agent discovery and communication
   - Intelligent query routing based on content analysis
   - Async/await pattern with synchronous wrapper for Flask

3. **API Endpoints** (`neurohub_routes.py`):
   - `/neurohub-ally` - Main UI page
   - `/api/neurohub-ally/submit` - Form submission (fallback)
   - `/api/neurohub-ally/stream` - SSE streaming endpoint

### Agent Discovery
The system attempts to connect to agents at these endpoints:
- Documentation: `http://localhost:8002`
- Signal Processor: `http://localhost:8003`
- Experiment Designer: `http://localhost:8004`
- Orchestrator: `http://localhost:8005`

### Query Routing Logic
- Keywords like "document", "report" → Documentation agent
- Keywords like "signal", "EEG", "analyze" → Signal Processor
- Keywords like "experiment", "protocol" → Experiment Designer
- Complex queries → Orchestrator (default)

## Related ADRs
- ADR-003: Technology Stack Selection (Flask, SSE support)
- ADR-004: Multi-Agent Architecture Design (A2A protocol)
- ADR-005: Development Environment Strategy (local-first approach)
- ADR-010: Bilingual Support (UI language considerations for agent responses)

## References
- [Server-Sent Events Specification](https://html.spec.whatwg.org/multipage/server-sent-events.html)
- [A2A Protocol Documentation](https://github.com/weimeilin79/a2a-python)
- [Flask Streaming Documentation](https://flask.palletsprojects.com/en/2.3.x/patterns/streaming/)