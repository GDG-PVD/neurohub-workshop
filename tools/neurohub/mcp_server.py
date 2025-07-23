"""
NeuroHub MCP Server
Exposes neurotechnology research tools via the Model Context Protocol
"""

import os
import json
import logging

from mcp.server.fastmcp import FastMCP
from mcp import types as mcp_types

# NeuroHub tool functions will be imported within each tool decorator

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastMCP server instance
app = FastMCP("NeuroHub MCP Server")


# Define tools using the @app.tool decorator
@app.tool()
async def create_experiment(
    name: str,
    description: str,
    principal_investigator: str,
    hypothesis: str,
    start_date: str,
    protocol: dict = None,
    equipment_ids: list = None
) -> str:
    """Create a new neurotechnology experiment in the database."""
    from neurohub import create_experiment as create_exp_func
    result = create_exp_func(
        name=name,
        description=description,
        principal_investigator=principal_investigator,
        hypothesis=hypothesis,
        start_date=start_date,
        protocol=protocol,
        equipment_ids=equipment_ids
    )
    return json.dumps(result)

@app.tool()
async def create_analysis_report(
    signal_id: str,
    researcher_id: str,
    analysis_type: str,
    findings: str,
    confidence_score: float = None,
    methodology: dict = None
) -> str:
    """Create an analysis report for signal data."""
    from neurohub import create_analysis_report as create_report_func
    result = create_report_func(
        signal_id=signal_id,
        researcher_id=researcher_id,
        analysis_type=analysis_type,
        findings=findings,
        confidence_score=confidence_score,
        methodology=methodology
    )
    return json.dumps(result)

@app.tool()
async def create_session_log(
    experiment_id: str,
    researcher_id: str,
    duration_minutes: int,
    notes: str = None,
    participants: int = None,
    environmental_conditions: dict = None
) -> str:
    """Create a session log for an experimental session."""
    from neurohub import create_session_log as create_log_func
    result = create_log_func(
        experiment_id=experiment_id,
        researcher_id=researcher_id,
        duration_minutes=duration_minutes,
        notes=notes,
        participants=participants,
        environmental_conditions=environmental_conditions
    )
    return json.dumps(result)

@app.tool()
async def export_findings(
    experiment_id: str,
    output_format: str = "markdown",
    include_raw_data: bool = False
) -> str:
    """Export research findings in publication format."""
    from neurohub import export_findings as export_func
    result = export_func(
        experiment_id=experiment_id,
        output_format=output_format,
        include_raw_data=include_raw_data
    )
    return json.dumps(result)

@app.tool()
async def register_device(
    name: str,
    device_type: str,
    manufacturer: str,
    specifications: dict
) -> str:
    """Register a new research device/equipment."""
    from neurohub import register_device as register_func
    result = register_func(
        name=name,
        device_type=device_type,
        manufacturer=manufacturer,
        specifications=specifications
    )
    return json.dumps(result)

# Entry point for the MCP server
if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    host = os.environ.get("MCP_HOST", "0.0.0.0")
    port = int(os.environ.get("MCP_PORT", "8001"))
    
    logger.info(f"Starting NeuroHub MCP Server on {host}:{port}")
    logger.info("Tools will be automatically discovered by FastMCP")
    
    # Run the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )
