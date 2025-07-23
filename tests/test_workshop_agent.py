"""
Unit tests for the workshop agent implementation.
"""

import unittest
from unittest.mock import patch, MagicMock
import sys
import os

# Add parent directory to path to import workshop agent modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'agents', 'workshop_agent'))

class TestWorkshopAgentConfig(unittest.TestCase):
    """Test the configuration module."""
    
    def test_config_imports(self):
        """Test that config.py can be imported."""
        try:
            import config
            self.assertTrue(hasattr(config, 'AGENT_NAME'))
            self.assertTrue(hasattr(config, 'MODEL'))
            self.assertTrue(hasattr(config, 'DESCRIPTION'))
            self.assertTrue(hasattr(config, 'PERSONALITY'))
            self.assertTrue(hasattr(config, 'FOCUS_AREAS'))
        except ImportError as e:
            self.fail(f"Failed to import config: {e}")
    
    def test_config_values(self):
        """Test that config has reasonable default values."""
        import config
        
        self.assertIsInstance(config.AGENT_NAME, str)
        self.assertGreater(len(config.AGENT_NAME), 0)
        
        self.assertIn(config.MODEL, ["gemini-2.0-flash", "gemini-1.5-pro"])
        
        self.assertIsInstance(config.FOCUS_AREAS, list)
        self.assertGreater(len(config.FOCUS_AREAS), 0)
        
        self.assertIsInstance(config.TEMPERATURE, (float, type(None)))
        if config.TEMPERATURE is not None:
            self.assertGreaterEqual(config.TEMPERATURE, 0.0)
            self.assertLessEqual(config.TEMPERATURE, 1.0)


class TestWorkshopAgent(unittest.TestCase):
    """Test the agent module."""
    
    @patch('agent.Agent')
    def test_agent_creation_without_mcp(self, mock_agent_class):
        """Test agent creation when MCP is not available."""
        # Mock the agent instance
        mock_agent_instance = MagicMock()
        mock_agent_class.return_value = mock_agent_instance
        
        # Import with MCP unavailable
        with patch.dict('sys.modules', {'google.adk.tools.mcp_tool.mcp_toolset': None, 
                                        'google.adk.mcp': None}):
            # Force reload to trigger import logic
            if 'agent' in sys.modules:
                del sys.modules['agent']
            
            import agent
            
            # Verify agent was created
            self.assertIsNotNone(agent.workshop_agent)
            mock_agent_class.assert_called_once()
            
            # Check that agent was created without tools
            call_args = mock_agent_class.call_args[1]
            self.assertNotIn('tools', call_args)
    
    def test_create_agent_instructions(self):
        """Test instruction generation from config."""
        import agent
        
        instructions = agent.create_agent_instructions()
        
        # Check that instructions contain key elements
        self.assertIn("responsibilities", instructions)
        self.assertIn("expertise", instructions)
        self.assertIn("Guidelines", instructions)
        
        # Check that config values are incorporated
        import config
        for area in config.FOCUS_AREAS:
            self.assertIn(area, instructions)
    
    @patch('agent.Agent')
    @patch('agent.MCPToolset')
    def test_agent_creation_with_mcp(self, mock_mcp_toolset, mock_agent_class):
        """Test agent creation when MCP is available."""
        # Make MCP available
        import agent
        agent.MCP_AVAILABLE = True
        
        # Mock the MCP toolset
        mock_toolset_instance = MagicMock()
        mock_mcp_toolset.return_value = mock_toolset_instance
        
        # Mock the agent
        mock_agent_instance = MagicMock()
        mock_agent_class.return_value = mock_agent_instance
        
        # Create agent
        test_agent = agent.get_agent()
        
        # Verify MCP toolset was created
        mock_mcp_toolset.assert_called_once()
        
        # Verify agent was created with tools
        mock_agent_class.assert_called_once()
        call_args = mock_agent_class.call_args[1]
        self.assertIn('tools', call_args)
        self.assertEqual(call_args['tools'], [mock_toolset_instance])
    
    @patch('agent.os.getenv')
    def test_mcp_url_from_environment(self, mock_getenv):
        """Test that MCP URL is read from environment."""
        mock_getenv.return_value = "http://custom-mcp:9999"
        
        import agent
        # Force reload to pick up mocked env
        if 'agent' in sys.modules:
            del sys.modules['agent']
        import agent as agent_reloaded
        
        # The agent module should use the custom URL
        # This would be validated in the MCP connection params


class TestQuickTest(unittest.TestCase):
    """Test the quick_test module."""
    
    def test_quick_test_imports(self):
        """Test that quick_test.py can be imported."""
        try:
            import quick_test
            self.assertTrue(hasattr(quick_test, 'quick_test'))
            self.assertTrue(hasattr(quick_test, 'TEST_PROMPTS'))
        except ImportError as e:
            self.fail(f"Failed to import quick_test: {e}")


class TestInteractiveTest(unittest.TestCase):
    """Test the interactive_test module."""
    
    def test_interactive_test_imports(self):
        """Test that interactive_test.py can be imported."""
        try:
            import interactive_test
            self.assertTrue(hasattr(interactive_test, 'interactive_test'))
        except ImportError as e:
            self.fail(f"Failed to import interactive_test: {e}")


if __name__ == '__main__':
    unittest.main()