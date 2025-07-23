#!/usr/bin/env python3
"""
Simple MCP Server for NeuroHub using individual tool decorators.
"""

import os
import json
import logging
from datetime import datetime
from mcp.server.fastmcp import FastMCP

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

# Define tools using the @app.tool decorator
@app.tool()
async def create_experiment_tool(
    name: str,
    description: str,
    principal_investigator: str,
    hypothesis: str,
    start_date: str,
    protocol: dict = None,
    equipment_ids: list = None
) -> str:
    """Create a new neurotechnology experiment in the database."""
    result = create_experiment(
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
async def create_analysis_report_tool(
    signal_id: str,
    researcher_id: str,
    analysis_type: str,
    findings: str,
    confidence_score: float = None,
    methodology: dict = None
) -> str:
    """Create an analysis report for signal data."""
    result = create_analysis_report(
        signal_id=signal_id,
        researcher_id=researcher_id,
        analysis_type=analysis_type,
        findings=findings,
        confidence_score=confidence_score,
        methodology=methodology
    )
    return json.dumps(result)

@app.tool()
async def create_session_log_tool(
    experiment_id: str,
    researcher_id: str,
    duration_minutes: int,
    notes: str = None,
    participants: int = None,
    environmental_conditions: dict = None
) -> str:
    """Create a session log for an experimental session."""
    result = create_session_log(
        experiment_id=experiment_id,
        researcher_id=researcher_id,
        duration_minutes=duration_minutes,
        notes=notes,
        participants=participants,
        environmental_conditions=environmental_conditions
    )
    return json.dumps(result)

@app.tool()
async def export_findings_tool(
    experiment_id: str,
    output_format: str = "markdown",
    include_raw_data: bool = False
) -> str:
    """Export research findings in publication format."""
    result = export_findings(
        experiment_id=experiment_id,
        output_format=output_format,
        include_raw_data=include_raw_data
    )
    return json.dumps(result)

@app.tool()
async def register_device_tool(
    name: str,
    device_type: str,
    manufacturer: str,
    specifications: dict
) -> str:
    """Register a new research device/equipment."""
    result = register_device(
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
    
    logger.info(f"Starting NeuroHub MCP Server (Simple) on {host}:{port}")
    
    # Run the server
    uvicorn.run(
        app,
        host=host,
        port=port,
        log_level="info"
    )