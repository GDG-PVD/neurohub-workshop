"""
NeuroHub AI Integration Module
Connects the web application to A2A agents for AI-powered research assistance.
"""

import json
import asyncio
from typing import Dict, List, Optional, AsyncGenerator
import aiohttp
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# A2A Agent endpoints
AGENT_ENDPOINTS = {
    "documentation": "http://localhost:8002",
    "signal_processor": "http://localhost:8003", 
    "experiment_designer": "http://localhost:8004",
    "orchestrator": "http://localhost:8005"
}

class A2AClient:
    """Client for communicating with A2A agents."""
    
    def __init__(self):
        self.session = None
        self.timeout = aiohttp.ClientTimeout(total=30)
        
    async def __aenter__(self):
        self.session = aiohttp.ClientSession(timeout=self.timeout)
        return self
        
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            await self.session.close()
            
    async def discover_agents(self) -> List[Dict]:
        """Discover available A2A agents."""
        available_agents = []
        
        for agent_name, endpoint in AGENT_ENDPOINTS.items():
            try:
                async with self.session.get(f"{endpoint}/.well-known/agent.json") as response:
                    if response.status == 200:
                        agent_info = await response.json()
                        agent_info["name"] = agent_name
                        agent_info["endpoint"] = endpoint
                        available_agents.append(agent_info)
                        logger.info(f"Discovered agent: {agent_name} at {endpoint}")
            except Exception as e:
                logger.warning(f"Agent {agent_name} at {endpoint} not available: {e}")
                
        return available_agents
        
    async def send_to_agent(self, agent_name: str, message: str, context: Dict = None) -> Dict:
        """Send a message to a specific agent."""
        endpoint = AGENT_ENDPOINTS.get(agent_name)
        if not endpoint:
            raise ValueError(f"Unknown agent: {agent_name}")
            
        payload = {
            "message": message,
            "context": context or {}
        }
        
        try:
            async with self.session.post(
                f"{endpoint}/process",
                json=payload,
                headers={"Content-Type": "application/json"}
            ) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    error_text = await response.text()
                    logger.error(f"Agent {agent_name} error: {error_text}")
                    return {"error": f"Agent returned status {response.status}"}
        except Exception as e:
            logger.error(f"Error communicating with agent {agent_name}: {e}")
            return {"error": str(e)}

async def stream_ai_response(query: str, context: str = None, experiment_type: str = None) -> AsyncGenerator[str, None]:
    """
    Stream AI responses for the NeuroHub Ally interface.
    Intelligently routes queries to appropriate agents.
    """
    async with A2AClient() as client:
        # Discover available agents
        available_agents = await client.discover_agents()
        
        if not available_agents:
            yield json.dumps({
                "type": "error",
                "message": "No AI agents are currently available. Please ensure agents are running."
            })
            return
            
        # Determine which agent to use based on query content
        agent_to_use = "orchestrator"  # Default to orchestrator
        
        query_lower = query.lower()
        if any(keyword in query_lower for keyword in ["document", "report", "write", "summarize"]):
            agent_to_use = "documentation"
        elif any(keyword in query_lower for keyword in ["signal", "eeg", "emg", "ecg", "analyze", "quality"]):
            agent_to_use = "signal_processor"
        elif any(keyword in query_lower for keyword in ["experiment", "protocol", "design", "study"]):
            agent_to_use = "experiment_designer"
            
        # Check if the selected agent is available
        agent_available = any(agent["name"] == agent_to_use for agent in available_agents)
        if not agent_available and available_agents:
            # Fall back to first available agent
            agent_to_use = available_agents[0]["name"]
            
        logger.info(f"Routing query to {agent_to_use} agent")
        
        # Send initial status
        yield json.dumps({
            "type": "status",
            "message": f"Connecting to {agent_to_use} agent..."
        })
        
        # Prepare context for the agent
        agent_context = {
            "research_area": context,
            "experiment_type": experiment_type,
            "available_agents": [agent["name"] for agent in available_agents]
        }
        
        # Send query to agent
        response = await client.send_to_agent(agent_to_use, query, agent_context)
        
        if "error" in response:
            yield json.dumps({
                "type": "error", 
                "message": response["error"]
            })
        else:
            # Stream the response
            yield json.dumps({
                "type": "response",
                "agent": agent_to_use,
                "content": response.get("response", "No response from agent")
            })

async def process_research_query(query: str, context: Dict = None) -> Dict:
    """
    Process a research query using the orchestrator agent.
    This is used for non-streaming responses.
    """
    async with A2AClient() as client:
        # Always route complex queries to orchestrator
        response = await client.send_to_agent("orchestrator", query, context)
        return response

# Synchronous wrapper for Flask integration
def stream_ai_response_sync(query: str, context: str = None, experiment_type: str = None):
    """Synchronous wrapper for streaming AI responses."""
    import nest_asyncio
    nest_asyncio.apply()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    async def get_chunks():
        chunks = []
        async for chunk in stream_ai_response(query, context, experiment_type):
            chunks.append(f"data: {chunk}\n\n")
        return chunks
    
    try:
        chunks = loop.run_until_complete(get_chunks())
        for chunk in chunks:
            yield chunk
    finally:
        loop.close()