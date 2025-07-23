"""
A2A Server for the Workshop Agent
This allows your agent to be discovered and used by other agents or the web app.
"""

from common.server import A2AServer
from common.types import AgentCard, AgentCapabilities, AgentSkill
from agent import workshop_agent
from config import AGENT_NAME, DESCRIPTION, FOCUS_AREAS

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Server configuration
host = os.environ.get("A2A_HOST", "localhost")
port = int(os.environ.get("A2A_PORT", 10010))  # Different port from other agents
PUBLIC_URL = os.environ.get("PUBLIC_URL")

# Create agent card
agent_card = AgentCard(
    agent_id=f"workshop_{AGENT_NAME}",
    name=AGENT_NAME,
    description=DESCRIPTION,
    capabilities=AgentCapabilities(
        skills=[
            AgentSkill(
                skill_id="neurotechnology_qa",
                name="Neurotechnology Q&A",
                description=f"Answer questions about {', '.join(FOCUS_AREAS[:2])}, and more",
                input_schema={
                    "type": "object",
                    "properties": {
                        "question": {
                            "type": "string",
                            "description": "Your neurotechnology question"
                        }
                    },
                    "required": ["question"]
                },
                output_schema={
                    "type": "object",
                    "properties": {
                        "answer": {
                            "type": "string",
                            "description": "The answer to your question"
                        }
                    }
                }
            )
        ]
    ),
    url=PUBLIC_URL
)

# Simple wrapper to handle A2A requests
async def handle_request(request):
    """Handle incoming A2A requests."""
    try:
        # For now, just pass through to the agent
        # In a real implementation, you'd parse the request and route appropriately
        logger.info(f"Received request: {request}")
        
        # Here you would integrate with the Runner to process the request
        # This is a simplified version
        return {
            "status": "success",
            "message": f"Workshop agent '{AGENT_NAME}' received your request"
        }
    except Exception as e:
        logger.error(f"Error handling request: {e}")
        return {
            "status": "error",
            "message": str(e)
        }

if __name__ == "__main__":
    print(f"Starting A2A server for '{AGENT_NAME}' on {host}:{port}")
    print(f"Agent focus areas: {', '.join(FOCUS_AREAS)}")
    
    # Note: The actual A2A server implementation would go here
    # For now, this is a placeholder that shows the structure
    print("\nNote: Full A2A server implementation needed")
    print("For now, your agent works with the test scripts!")
    print("\nTo make your agent available to other services:")
    print("1. Implement the A2A server using the common.server.A2AServer class")
    print("2. Start this server to expose your agent on the network")
    print("3. Other agents can then discover and communicate with your agent")