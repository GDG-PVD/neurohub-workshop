# [Agent Name] Agent

## Purpose

[Clear description of what this agent does and why it's needed in the NeuroHub system]

**Agent Type:** [LlmAgent | LoopAgent | BaseAgent]  
**A2A Port:** [Default port number]  
**Status:** [Development | Testing | Production]

## Capabilities

This agent can:
- [Capability 1]
- [Capability 2]
- [Capability 3]

## Architecture

### Agent Components

```
[agent-name]/
├── agent.py              # Core ADK agent logic
├── [agent-name]_agent.py # Agent wrapper class
├── a2a_server.py         # A2A protocol server
├── requirements.txt      # Agent dependencies
├── Dockerfile           # Container configuration
└── README.md           # This file
```

### Integration Points

- **MCP Tools Used:** [List any MCP tools this agent uses]
- **Sub-agents:** [If LoopAgent, list sub-agents]
- **External Services:** [Any external APIs or services]

## Running the Agent

### Local Development

```bash
# Install dependencies
cd agents/[agent-name]
uv pip install -r requirements.txt
uv pip install ../a2a_common-0.1.0-py3-none-any.whl

# Run the A2A server
python a2a_server.py
```

The agent will be available at `http://localhost:[PORT]`

### Testing

```bash
# Run the test client
python test_client.py

# Or test with A2A Inspector
# 1. Open A2A Inspector
# 2. Connect to http://localhost:[PORT]
# 3. Send test queries
```

### Docker Deployment

```bash
# Build from project root
docker build -t [agent-name] -f agents/[agent-name]/Dockerfile .

# Run container
docker run -p [PORT]:[PORT] [agent-name]
```

## Agent Card

The agent exposes its capabilities via A2A protocol:

```json
{
  "name": "[Agent Name]",
  "description": "[What the agent does]",
  "version": "1.0.0",
  "capabilities": {
    "input_types": ["text", "structured_data"],
    "output_types": ["text", "json"],
    "tools": ["tool1", "tool2"]
  }
}
```

## Usage Examples

### Basic Query

```python
# Example of querying this agent
query = {
    "task": "[Describe task]",
    "parameters": {
        "param1": "value1"
    }
}
```

### Expected Response

```json
{
  "status": "success",
  "result": {
    "field1": "value",
    "field2": 123
  }
}
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `A2A_PORT` | Port for A2A server | [PORT] |
| `MCP_SERVER_URL` | MCP server endpoint | http://localhost:8001 |
| `LOG_LEVEL` | Logging verbosity | INFO |

### Agent Instructions

The agent uses these core instructions:
```
[Key instruction summary or excerpt]
```

See `agent.py` for full instructions.

## Error Handling

| Error Type | Description | Recovery |
|------------|-------------|----------|
| `ConnectionError` | Can't reach MCP server | Check MCP_SERVER_URL |
| `ValidationError` | Invalid input format | Check input schema |
| `TimeoutError` | Processing timeout | Retry with smaller data |

## Performance Notes

- Average response time: [X seconds]
- Memory usage: [Typical RAM usage]
- Concurrent requests: [Supported or not]

## Development Guide

### Extending the Agent

1. **Adding new capabilities**: Update instructions in `agent.py`
2. **Adding tools**: Register with MCP server and update agent
3. **Modifying output format**: Update response schema

### Best Practices

- Keep instructions focused and clear
- Validate inputs before processing
- Log important operations for debugging
- Handle errors gracefully

## Related Documentation

- [ADR-XXX: Decision about this agent](../adr/ADR-XXX.md)
- [Orchestrator Integration](../agents/research_orchestrator/README.md)
- [MCP Tools Documentation](../tools/neurohub/README.md)

## Changelog

### v1.0.0 - [Date]
- Initial implementation
- Basic [capability] support

## Troubleshooting

### Agent not responding
1. Check if A2A server is running
2. Verify port is not in use
3. Check logs for errors

### MCP connection failed
1. Ensure MCP server is running
2. Check MCP_SERVER_URL environment variable
3. Verify network connectivity