# ADR-003: Use MCP for Agent-Platform Communication

**Date:** 2024-07-15

**Status:** Accepted

**Deciders:** Workshop instructors, Technical architects

**Tags:** architecture, integration, agent-communication

## Context

NeuroHub agents need to interact with the platform to:
- Create experiments and analyses
- Store results in the database
- Export findings
- Register devices

We need a standardized way for agents to access these platform capabilities without tight coupling.

## Decision

Use Model Context Protocol (MCP) to expose platform functionality as tools that agents can discover and use.

## Considered Options

1. **MCP (Model Context Protocol)**: Standardized tool protocol
   - Pros:
     - Industry standard for LLM tool integration
     - Automatic tool discovery
     - Type-safe interfaces
     - Transport agnostic (SSE, WebSocket, etc.)
     - Good AI assistant integration
   - Cons:
     - Additional server component
     - Learning curve for protocol

2. **Direct REST API calls**: Agents call platform APIs directly
   - Pros:
     - Simple HTTP requests
     - No additional protocol
     - Direct control
   - Cons:
     - Tight coupling
     - No standardized discovery
     - Each agent needs API client code
     - Harder to mock/test

3. **Shared database access**: Agents write directly to database
   - Pros:
     - Most direct approach
     - No intermediate layer
   - Cons:
     - Tight coupling to schema
     - No business logic enforcement
     - Security concerns
     - Hard to audit/control

## Consequences

### Positive
- Clean separation between agents and platform
- Agents can discover available tools dynamically
- Easy to add new tools without changing agents
- Standardized error handling and types
- Better testability with mock MCP servers

### Negative
- Additional component to maintain (MCP server)
- Network overhead for tool calls
- Agents depend on MCP server availability

### Neutral
- Establishes pattern for future integrations
- Requires MCP client in agents

## Implementation Notes

MCP server exposes tools like:

```python
@mcp_server.tool()
async def create_experiment(
    title: str,
    researcher_id: str,
    hypothesis: str,
    methodology: str
) -> str:
    """Creates a new neuroscience experiment."""
    # Validates input
    # Calls database layer
    # Returns experiment ID
```

Agents use tools via MCP client:

```python
result = await mcp_client.call_tool(
    "create_experiment",
    title="EEG Study",
    researcher_id="R001",
    hypothesis="...",
    methodology="..."
)
```

## References

- [Model Context Protocol Specification](https://modelcontextprotocol.io)
- [MCP Python SDK](https://github.com/modelcontextprotocol/python-sdk)
- [ADR-004: A2A Protocol](ADR-004-a2a-protocol.md)

## Notes

This decision enables loose coupling between agents and platform, following microservices best practices while maintaining simplicity for workshop participants.