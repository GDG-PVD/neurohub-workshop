"""
Integration tests for the workshop agent.
Tests the agent with various prompts and configurations.
"""

import pytest
import asyncio
from unittest.mock import Mock, patch
import sys
import os

# Add the workshop agent directory to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'agents', 'workshop_agent'))

from agent import get_agent
from config import AGENT_NAME


class TestWorkshopAgentIntegration:
    """Integration tests for the workshop agent."""
    
    def test_agent_creation(self):
        """Test that the agent can be created successfully."""
        with patch('agent.MCP_AVAILABLE', False):
            agent = get_agent()
            assert agent is not None
            assert agent.name == AGENT_NAME
    
    def test_agent_configuration(self):
        """Test that agent configuration is properly loaded."""
        with patch('agent.MCP_AVAILABLE', False):
            agent = get_agent()
            
            # Check that instructions include configured elements
            instructions = agent.instruction
            assert "neurotechnology" in instructions.lower()
            assert "experiment" in instructions.lower()
            assert "signal" in instructions.lower()
    
    def test_agent_without_mcp(self):
        """Test that agent works without MCP tools."""
        with patch('agent.MCP_AVAILABLE', False):
            agent = get_agent()
            
            # Agent should have no tools when MCP is not available
            assert not hasattr(agent, 'tools') or agent.tools == []
    
    @pytest.mark.asyncio
    async def test_agent_response_format(self):
        """Test that the agent can handle basic interactions."""
        # This would require mocking the Runner and session services
        # For now, we just verify the agent structure is correct
        with patch('agent.MCP_AVAILABLE', False):
            agent = get_agent()
            
            # Verify agent has required attributes
            assert hasattr(agent, 'name')
            assert hasattr(agent, 'model')
            assert hasattr(agent, 'instruction')
    
    def test_configuration_customization(self):
        """Test that configuration changes affect agent behavior."""
        # Mock different configuration values
        test_name = "test_assistant"
        test_areas = ["test_area_1", "test_area_2"]
        
        with patch('config.AGENT_NAME', test_name):
            with patch('config.FOCUS_AREAS', test_areas):
                with patch('agent.MCP_AVAILABLE', False):
                    agent = get_agent()
                    
                    assert agent.name == test_name
                    # Instructions should include focus areas
                    for area in test_areas:
                        assert area in agent.instruction


if __name__ == "__main__":
    pytest.main([__file__, "-v"])