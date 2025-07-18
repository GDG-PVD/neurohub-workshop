# NeuroHub MCP Tool Server

## Overview

The MCP (Model Context Protocol) server provides standardized tools for agents to interact with the NeuroHub platform. It acts as a bridge between AI agents and the core platform functionality.

**Status:** Production  
**Port:** 8001  
**Protocol:** MCP over SSE

## Available Tools

### 1. `create_experiment`
Creates a new neuroscience experiment in the database.

**Parameters:**
- `title` (str): Experiment title
- `researcher_id` (str): ID of the lead researcher
- `hypothesis` (str): Research hypothesis
- `methodology` (str): Experimental methodology

**Returns:** Experiment ID (string)

### 2. `create_analysis_report`
Documents signal analysis results.

**Parameters:**
- `experiment_id` (str): Associated experiment
- `signal_data_id` (str): Analyzed signal reference
- `findings` (str): Analysis findings
- `metrics` (dict): Quantitative results

**Returns:** Analysis report ID (string)

### 3. `create_session_log`
Records an experimental session.

**Parameters:**
- `experiment_id` (str): Parent experiment
- `date` (str): Session date (ISO format)
- `duration_minutes` (int): Session duration
- `notes` (str): Session observations

**Returns:** Session ID (string)

### 4. `export_findings`
Exports research findings in various formats.

**Parameters:**
- `experiment_id` (str): Source experiment
- `format` (str): Export format (pdf, markdown, latex)
- `include_data` (bool): Include raw data

**Returns:** Export file path (string)

### 5. `register_device`
Registers new measurement equipment.

**Parameters:**
- `device_type` (str): Device category (EEG, EMG, etc.)
- `manufacturer` (str): Device manufacturer
- `model` (str): Model name
- `specifications` (dict): Technical specs

**Returns:** Device ID (string)

## Installation

```bash
cd tools/neurohub
uv pip install -r requirements.txt
```

## Running the Server

### Local Development

```bash
python mcp_server.py
```

The server will start on `http://localhost:8001`

### Docker Deployment

```bash
docker build -t neurohub-mcp -f Dockerfile .
docker run -p 8001:8001 neurohub-mcp
```

## Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MCP_PORT` | Server port | 8001 |
| `NEUROHUB_BASE_URL` | Platform API URL | http://localhost:8080 |
| `LOG_LEVEL` | Logging level | INFO |
| `CORS_ORIGINS` | Allowed origins | * |

## Testing Tools

### Using curl

```bash
# List available tools
curl http://localhost:8001/tools

# Call a tool
curl -X POST http://localhost:8001/tools/create_experiment \
  -H "Content-Type: application/json" \
  -d '{
    "title": "EEG Alpha Wave Study",
    "researcher_id": "R001",
    "hypothesis": "Meditation increases alpha waves",
    "methodology": "20min guided meditation with continuous EEG"
  }'
```

### Using MCP Client

```python
from mcp import Client

async with Client("http://localhost:8001") as client:
    result = await client.call_tool(
        "create_experiment",
        title="BCI Control Study",
        researcher_id="R002",
        hypothesis="Motor imagery improves with training",
        methodology="Daily BCI sessions for 2 weeks"
    )
    print(f"Created experiment: {result}")
```

## Tool Development

### Adding New Tools

1. Define tool in `mcp_server.py`:
```python
@mcp_server.tool()
async def new_tool_name(param1: str, param2: int) -> dict:
    """Tool description for agents."""
    # Implementation
    return {"result": "success"}
```

2. Add validation and error handling
3. Update this README
4. Test with agents

### Best Practices

- Keep tool functions focused and single-purpose
- Use clear, descriptive parameter names
- Validate all inputs
- Return consistent response formats
- Log important operations

## Error Handling

Tools return errors in standard format:
```json
{
  "error": {
    "type": "ValidationError",
    "message": "Invalid researcher ID",
    "details": {"researcher_id": "R999"}
  }
}
```

## Integration with Agents

Agents access tools via MCP client:

```python
from google.genai.lib import ToolProvider
from mcp import Client

# In agent initialization
mcp_client = Client("http://localhost:8001")
tools = await mcp_client.list_tools()

# In agent execution
result = await mcp_client.call_tool("create_experiment", **params)
```

## Monitoring

- Health check: `GET /health`
- Metrics: `GET /metrics`
- Tool usage logs in `./logs/mcp_access.log`

## Troubleshooting

### Connection refused
- Check server is running
- Verify port 8001 is available
- Check firewall settings

### Tool not found
- Ensure tool is registered with `@mcp_server.tool()`
- Check tool name spelling
- Restart server after adding tools

### Database errors
- Verify NeuroHub platform is running
- Check database credentials
- Ensure network connectivity

## Related Documentation

- [MCP Protocol Specification](https://modelcontextprotocol.io)
- [ADR-003: MCP for Agent Communication](../../docs/adr/ADR-003-mcp-over-direct-api.md)
- [Agent Integration Guide](../../docs/agent-integration.md)