# ADR-008: MCP Server Implementation Without ADK Tools

Date: 2025-07-22

## Status

Accepted

## Context

The NeuroHub MCP server initially attempted to use Google ADK's `Tool` class for defining MCP tools. However, this resulted in an ImportError because the `Tool` class is not properly exposed in the current version of the ADK package (`google-adk==0.4.0`).

The error encountered was:
```
ImportError: cannot import name 'Tool' from 'google.adk.tools'
```

This blocking issue prevented the MCP server from starting, which is critical for agent-platform communication as documented in [ADR-003](ADR-003-mcp-over-direct-api.md).

## Decision

We will implement the MCP server using native MCP types without dependency on ADK's Tool class. This involves:

1. Defining tool schemas directly as dictionaries
2. Mapping tool names to their implementation functions
3. Using MCP's native `types.Tool` for tool definitions
4. Removing the ADK tools import dependency

## Consequences

### Positive

- **Immediate functionality**: MCP server can start and run without ADK import errors
- **Reduced coupling**: Less dependency on ADK internals that may change
- **Clearer implementation**: Direct mapping between MCP protocol and our tools
- **Better maintainability**: Tool definitions are self-contained
- **Workshop stability**: Students won't encounter blocking import errors

### Negative

- **Code duplication**: Tool schemas must be manually maintained
- **Loss of ADK integration**: Cannot leverage ADK's tool validation features
- **Manual type checking**: Must ensure schema correctness without ADK helpers

### Neutral

- **Performance**: No significant performance impact
- **Functionality**: All MCP features remain available

## Implementation Details

### Before (ADK-dependent):
```python
from google.adk.tools import Tool, ToolResponse

experiment_tool = Tool(
    name="create_experiment",
    description="...",
    parameter_schema={...},
    function=create_experiment
)
```

### After (Native MCP):
```python
tool_schemas = {
    "create_experiment": {
        "name": "create_experiment",
        "description": "...",
        "inputSchema": {...}
    }
}

tool_functions = {
    "create_experiment": create_experiment
}
```

## Related Decisions

- [ADR-003: MCP for Agent-Platform Communication](ADR-003-mcp-over-direct-api.md) - Establishes MCP as the communication protocol
- [ADR-004: A2A Protocol](ADR-004-a2a-protocol.md) - Agents use MCP tools via A2A
- [ADR-007: NeuroHub Ally Integration](007-neurohub-ally-integration.md) - Depends on MCP server availability

## Notes

- The MCP server runs on port 8001 by default (configurable via `MCP_PORT`)
- This implementation follows the MCP specification directly
- Future ADK versions may expose the Tool class properly, allowing migration back
- Tests ensure all tools are properly exposed and callable