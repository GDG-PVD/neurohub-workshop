"""
Pre-built Workshop Agent - Ready to run!
Students can customize this agent by modifying config.py
"""

import os
import sys
import logging
from google.adk.agents import Agent

# Import configuration
from config import *

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Try to import MCP tools - gracefully handle if not available
try:
    if ENABLE_TOOLS:
        from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
        MCP_AVAILABLE = True
    else:
        MCP_AVAILABLE = False
except ImportError:
    try:
        # Try alternative import path
        from google.adk.mcp import MCPToolset, SseServerParams
        MCP_AVAILABLE = True
    except ImportError:
        logger.warning("MCP tools not available - agent will run without tools")
        MCP_AVAILABLE = False

def create_agent_instructions():
    """Build the complete agent instructions from config."""
    
    # Build focus areas string
    focus_areas_str = "\n".join([f"- {area}" for area in FOCUS_AREAS])
    
    instructions = f"""
{PERSONALITY}

Your primary responsibilities:
1. Help researchers design and document experiments
2. Provide guidance on signal analysis and processing
3. Assist with research methodology and best practices
4. Generate reports and summaries of findings

Your areas of expertise include:
{focus_areas_str}

Guidelines for interaction:
{CUSTOM_INSTRUCTIONS}

When helping with experiments:
- Ask clarifying questions to understand research goals
- Suggest appropriate methodologies and controls
- Provide specific technical recommendations
- Consider ethical implications and safety

Available tools (when connected to MCP server):
- create_experiment: Register new experiments in the database
- create_analysis_report: Document analysis findings
- create_session_log: Record experimental sessions
- export_findings: Generate publication-ready summaries
"""
    
    return instructions

def get_agent():
    """Create and configure the workshop agent."""
    
    logger.info(f"Creating agent '{AGENT_NAME}'...")
    
    # Build agent configuration
    agent_config = {
        "name": AGENT_NAME,
        "model": MODEL,
        "description": DESCRIPTION,
        "instruction": create_agent_instructions(),
    }
    
    # Add model parameters if specified
    model_params = {}
    if TEMPERATURE is not None:
        model_params["temperature"] = TEMPERATURE
    if MAX_TOKENS is not None:
        model_params["max_tokens"] = MAX_TOKENS
    
    if model_params:
        agent_config["model_params"] = model_params
    
    # Add MCP tools if available
    if MCP_AVAILABLE and ENABLE_TOOLS:
        try:
            mcp_url = os.getenv("MCP_SERVER_URL", MCP_SERVER_URL)
            logger.info(f"Connecting to MCP server at {mcp_url}...")
            
            mcp_toolset = MCPToolset(
                connection_params=SseServerParams(
                    url=f"{mcp_url}/sse"
                )
            )
            agent_config["tools"] = [mcp_toolset]
            logger.info("MCP tools connected successfully")
        except Exception as e:
            logger.warning(f"Could not connect to MCP server: {e}")
            logger.info("Agent will run without tools")
    else:
        logger.info("Running in no-tools mode")
    
    # Create the agent
    agent = Agent(**agent_config)
    
    logger.info(f"Agent '{AGENT_NAME}' created successfully")
    logger.info(f"Model: {MODEL}")
    logger.info(f"Focus areas: {', '.join(FOCUS_AREAS[:2])}...")
    
    return agent

# Create the agent instance
workshop_agent = get_agent()