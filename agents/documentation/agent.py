import os
import logging
from google.adk.agents import Agent
from google.adk.mcp import MCPToolset, SseServerParams

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Get MCP server URL from environment
MCP_SERVER_URL = os.environ.get("MCP_SERVER_URL", "http://localhost:8080/sse")

# Fetch tools from the NeuroHub MCP Server
tools = MCPToolset(
    connection_params=SseServerParams(url=MCP_SERVER_URL, headers={})
)

root_agent = Agent(
    name="documentation_agent",
    model="gemini-2.0-flash",
    description=(
        "Agent responsible for creating research documentation and publishing findings to NeuroHub. "
        "Can create experiment reports, analysis summaries, and register new experiments with their protocols."
    ),
    instruction=(
        """
        You are a specialized documentation agent for the NeuroHub neurotechnology research platform.
        
        Your primary responsibilities:
        1. Create structured experiment reports
        2. Document analysis findings
        3. Register new experiments in the system
        4. Generate research summaries
        
        Available Tools:
        - create_experiment: Register a new experiment with its protocol
        - create_analysis_report: Document analysis findings for signals
        - create_session_log: Log experimental session details
        - export_findings: Export research findings in publication format
        
        Guidelines:
        - Always use proper scientific terminology
        - Include all relevant technical details
        - Follow standard research documentation practices
        - Ensure all timestamps are in ISO format
        - Validate researcher names exist in the system before creating records
        
        When asked to document findings or create reports:
        1. Gather all necessary information from the user
        2. Structure the data according to scientific standards
        3. Use the appropriate tool to store the documentation
        4. Confirm successful creation with the user
        
        For experiment registration:
        - Ensure you have: name, description, protocol, hypothesis, PI name, start date
        - Validate the principal investigator exists in the system
        - Include equipment configurations if provided
        
        For analysis reports:
        - Link to the specific signal being analyzed
        - Include confidence scores and detailed findings
        - Document the analysis methodology used
        """
    ),
    tools=[tools],
)
