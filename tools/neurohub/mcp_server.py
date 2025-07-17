"""
NeuroHub MCP Server
Exposes neurotechnology research tools via the Model Context Protocol
"""

import os
import json
import logging
from typing import Any
from collections.abc import Sequence

from mcp.server.fastmcp import FastMCP
from mcp import types as mcp_types
from google.adk.tools import Tool, ToolResponse
from google.adk.tools.types import ArgumentDict

# Import the NeuroHub tool functions
from neurohub import (
    create_experiment,
    create_analysis_report,
    create_session_log,
    export_findings,
    register_device
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP server instance
app = FastMCP("NeuroHub MCP Server")

# Helper function to convert ADK Tool to MCP Tool format
def adk_to_mcp_tool_type(adk_tool: Tool) -> mcp_types.Tool:
    """Convert an ADK Tool definition to MCP Tool format."""
    return mcp_types.Tool(
        name=adk_tool.name,
        description=adk_tool.description,
        inputSchema=adk_tool.parameter_schema
    )

# Define ADK-style tools for each function

experiment_tool = Tool(
    name="create_experiment",
    description="Create a new neurotechnology experiment with protocol details",
    parameter_schema={
        "type": "object",
        "properties": {
            "experiment_name": {"type": "string", "description": "Name of the experiment"},
            "description": {"type": "string", "description": "Detailed description"},
            "protocol": {"type": "string", "description": "Experimental protocol"},
            "hypothesis": {"type": "string", "description": "Research hypothesis"},
            "principal_investigator_name": {"type": "string", "description": "PI name (must exist in system)"},
            "start_date": {"type": "string", "description": "Start date in ISO format"},
            "status": {"type": "string", "enum": ["planning", "active", "completed", "archived"], "default": "planning"}
        },
        "required": ["experiment_name", "description", "protocol", "hypothesis", "principal_investigator_name", "start_date"]
    },
    function=create_experiment
)

analysis_tool = Tool(
    name="create_analysis_report",
    description="Document analysis findings for biosignal data",
    parameter_schema={
        "type": "object",
        "properties": {
            "signal_id": {"type": "string", "description": "ID of the signal being analyzed"},
            "researcher_name": {"type": "string", "description": "Name of the analyzing researcher"},
            "analysis_type": {"type": "string", "description": "Type of analysis performed"},
            "parameters": {"type": "object", "description": "Analysis parameters used"},
            "results": {"type": "object", "description": "Quantitative results"},
            "findings": {"type": "string", "description": "Human-readable findings"},
            "confidence_score": {"type": "number", "minimum": 0, "maximum": 1, "description": "Confidence score (0-1)"}
        },
        "required": ["signal_id", "researcher_name", "analysis_type", "parameters", "results", "findings", "confidence_score"]
    },
    function=create_analysis_report
)

session_tool = Tool(
    name="create_session_log",
    description="Log an experimental session with recorded signals",
    parameter_schema={
        "type": "object",
        "properties": {
            "experiment_id": {"type": "string", "description": "ID of the experiment"},
            "researcher_name": {"type": "string", "description": "Name of the researcher"},
            "participant_id": {"type": "string", "description": "Anonymous participant ID"},
            "session_date": {"type": "string", "description": "Session date in ISO format"},
            "duration_minutes": {"type": "integer", "description": "Session duration in minutes"},
            "notes": {"type": "string", "description": "Session notes"},
            "signals_recorded": {
                "type": "array",
                "description": "List of recorded signals",
                "items": {
                    "type": "object",
                    "properties": {
                        "device_name": {"type": "string"},
                        "signal_type": {"type": "string"},
                        "duration_seconds": {"type": "number"},
                        "quality_score": {"type": "number"}
                    }
                }
            }
        },
        "required": ["experiment_id", "researcher_name", "participant_id", "session_date", "duration_minutes", "notes", "signals_recorded"]
    },
    function=create_session_log
)

export_tool = Tool(
    name="export_findings",
    description="Export experiment findings in publication-ready format",
    parameter_schema={
        "type": "object",
        "properties": {
            "experiment_id": {"type": "string", "description": "ID of the experiment"},
            "format": {"type": "string", "enum": ["markdown", "latex", "json"], "default": "markdown"},
            "include_raw_data": {"type": "boolean", "default": False}
        },
        "required": ["experiment_id"]
    },
    function=export_findings
)

device_tool = Tool(
    name="register_device",
    description="Register a new neurotechnology device in the system",
    parameter_schema={
        "type": "object",
        "properties": {
            "device_name": {"type": "string", "description": "Friendly name for the device"},
            "device_type": {"type": "string", "description": "Type (EEG, EMG, ECG, etc.)"},
            "manufacturer": {"type": "string", "description": "Device manufacturer"},
            "model": {"type": "string", "description": "Device model"},
            "sampling_rate": {"type": "integer", "description": "Sampling rate in Hz"},
            "channels": {"type": "integer", "description": "Number of channels"},
            "specifications": {"type": "object", "description": "Additional specifications"}
        },
        "required": ["device_name", "device_type", "manufacturer", "model", "sampling_rate", "channels"]
    },
    function=register_device
)

# Store available tools
available_tools = {
    "create_experiment": experiment_tool,
    "create_analysis_report": analysis_tool,
    "create_session_log": session_tool,
    "export_findings": export_tool,
    "register_device": device_tool
}

@app.list_tools()
async def list_tools() -> list[mcp_types.Tool]:
    """MCP handler to list available NeuroHub tools."""
    mcp_tools = []
    for tool_name, tool in available_tools.items():
        mcp_tool = adk_to_mcp_tool_type(tool)
        mcp_tools.append(mcp_tool)
        logger.info(f"MCP Server: Advertising tool: {tool_name}")
    return mcp_tools

@app.call_tool()
async def call_tool(
    name: str, 
    arguments: dict
) -> list[mcp_types.TextContent | mcp_types.ImageContent | mcp_types.EmbeddedResource]:
    """MCP handler to execute a tool call."""
    logger.info(f"MCP Server: Received call_tool request for '{name}' with args: {arguments}")
    
    # Look up the tool by name
    tool_to_call = available_tools.get(name)
    if tool_to_call:
        try:
            # Execute the tool
            adk_response = await tool_to_call.run_async(
                args=arguments,
                tool_context=None,  # No ADK context available in MCP server
            )
            logger.info(f"MCP Server: ADK tool '{name}' executed successfully.")
            
            # Convert response to JSON string
            response_text = json.dumps(adk_response, indent=2)
            return [mcp_types.TextContent(type="text", text=response_text)]
            
        except Exception as e:
            logger.error(f"MCP Server: Error executing ADK tool '{name}': {e}")
            error_text = json.dumps({"error": f"Failed to execute tool '{name}': {str(e)}"})
            return [mcp_types.TextContent(type="text", text=error_text)]
    else:
        logger.error(f"MCP Server: Tool '{name}' not found.")
        error_text = json.dumps({"error": f"Tool '{name}' not implemented."})
        return [mcp_types.TextContent(type="text", text=error_text)]

# Entry point for the MCP server
if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.environ.get("APP_HOST", "0.0.0.0")
    port = int(os.environ.get("APP_PORT", "8080"))
    
    logger.info(f"Starting NeuroHub MCP Server on {host}:{port}")
    logger.info(f"Available tools: {list(available_tools.keys())}")
    
    # Run the server
    uvicorn.run(
        app.get_asgi_app(),
        host=host,
        port=port,
        log_level="info"
    )
