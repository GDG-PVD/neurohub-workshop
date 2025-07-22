"""
Tests for the NeuroHub MCP Server
"""

import pytest
import json
from unittest.mock import Mock, patch, AsyncMock
from mcp import types as mcp_types

# Import the MCP server module
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'tools', 'neurohub'))
from mcp_server import app, tool_schemas, tool_functions


class TestMCPServer:
    """Test suite for the NeuroHub MCP Server."""
    
    @pytest.mark.asyncio
    async def test_list_tools(self):
        """Test that all tools are correctly listed."""
        tools = await app.list_tools()
        
        # Verify we have the correct number of tools
        assert len(tools) == 5
        
        # Verify tool names
        tool_names = [tool.name for tool in tools]
        expected_names = [
            "create_experiment",
            "create_analysis_report", 
            "create_session_log",
            "export_findings",
            "register_device"
        ]
        for name in expected_names:
            assert name in tool_names
        
        # Verify each tool has required fields
        for tool in tools:
            assert isinstance(tool, mcp_types.Tool)
            assert tool.name
            assert tool.description
            assert tool.inputSchema
    
    @pytest.mark.asyncio
    async def test_create_experiment_tool_call(self):
        """Test calling the create_experiment tool."""
        # Mock the create_experiment function
        with patch('mcp_server.create_experiment') as mock_create:
            mock_create.return_value = {
                "experiment_id": "exp123",
                "status": "success"
            }
            
            # Call the tool
            args = {
                "experiment_name": "Test Experiment",
                "description": "A test experiment",
                "protocol": "Test protocol",
                "hypothesis": "Test hypothesis",
                "principal_investigator_name": "Dr. Test",
                "start_date": "2025-01-01T00:00:00Z",
                "status": "planning"
            }
            
            result = await app.call_tool("create_experiment", args)
            
            # Verify the result
            assert len(result) == 1
            assert isinstance(result[0], mcp_types.TextContent)
            response = json.loads(result[0].text)
            assert response["experiment_id"] == "exp123"
            assert response["status"] == "success"
            
            # Verify the function was called with correct args
            mock_create.assert_called_once_with(**args)
    
    @pytest.mark.asyncio
    async def test_tool_not_found(self):
        """Test calling a non-existent tool."""
        result = await app.call_tool("non_existent_tool", {})
        
        assert len(result) == 1
        assert isinstance(result[0], mcp_types.TextContent)
        response = json.loads(result[0].text)
        assert "error" in response
        assert "not implemented" in response["error"]
    
    @pytest.mark.asyncio
    async def test_tool_error_handling(self):
        """Test error handling when a tool raises an exception."""
        with patch('mcp_server.create_experiment') as mock_create:
            mock_create.side_effect = Exception("Database connection failed")
            
            args = {
                "experiment_name": "Test",
                "description": "Test",
                "protocol": "Test",
                "hypothesis": "Test",
                "principal_investigator_name": "Test",
                "start_date": "2025-01-01T00:00:00Z"
            }
            
            result = await app.call_tool("create_experiment", args)
            
            assert len(result) == 1
            assert isinstance(result[0], mcp_types.TextContent)
            response = json.loads(result[0].text)
            assert "error" in response
            assert "Failed to execute tool" in response["error"]
            assert "Database connection failed" in response["error"]
    
    def test_tool_schemas_completeness(self):
        """Test that all tool schemas are properly defined."""
        # Verify we have schemas for all functions
        assert len(tool_schemas) == len(tool_functions)
        
        # Verify each schema has required fields
        for name, schema in tool_schemas.items():
            assert schema["name"] == name
            assert "description" in schema
            assert "inputSchema" in schema
            assert schema["inputSchema"]["type"] == "object"
            assert "properties" in schema["inputSchema"]
            assert "required" in schema["inputSchema"]
    
    def test_tool_functions_mapping(self):
        """Test that tool functions are correctly mapped."""
        # Verify all functions are callable
        for name, func in tool_functions.items():
            assert callable(func)
            assert name in tool_schemas
    
    @pytest.mark.asyncio
    async def test_create_analysis_report_tool(self):
        """Test the create_analysis_report tool."""
        with patch('mcp_server.create_analysis_report') as mock_create:
            mock_create.return_value = {
                "analysis_id": "analysis123",
                "status": "completed"
            }
            
            args = {
                "signal_id": "sig123",
                "researcher_name": "Dr. Analyzer",
                "analysis_type": "spectral",
                "parameters": {"window": "hanning"},
                "results": {"peak_freq": 10.5},
                "findings": "Normal alpha activity",
                "confidence_score": 0.95
            }
            
            result = await app.call_tool("create_analysis_report", args)
            
            assert len(result) == 1
            response = json.loads(result[0].text)
            assert response["analysis_id"] == "analysis123"
            mock_create.assert_called_once_with(**args)
    
    @pytest.mark.asyncio
    async def test_register_device_tool(self):
        """Test the register_device tool."""
        with patch('mcp_server.register_device') as mock_register:
            mock_register.return_value = {
                "device_id": "dev123",
                "status": "registered"
            }
            
            args = {
                "device_name": "EEG Amplifier",
                "device_type": "EEG",
                "manufacturer": "NeuroTech",
                "model": "NT-1000",
                "sampling_rate": 1000,
                "channels": 32,
                "specifications": {"impedance": "10k"}
            }
            
            result = await app.call_tool("register_device", args)
            
            assert len(result) == 1
            response = json.loads(result[0].text)
            assert response["device_id"] == "dev123"
            mock_register.assert_called_once_with(**args)
    
    @pytest.mark.asyncio
    async def test_null_response_handling(self):
        """Test handling of None responses from tools."""
        with patch('mcp_server.export_findings') as mock_export:
            mock_export.return_value = None
            
            result = await app.call_tool("export_findings", {"experiment_id": "exp123"})
            
            assert len(result) == 1
            response = json.loads(result[0].text)
            assert response["status"] == "completed"
            assert "successfully" in response["message"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])