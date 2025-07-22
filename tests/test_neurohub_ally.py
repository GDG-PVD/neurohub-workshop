"""
Tests for NeuroHub Ally AI Assistant functionality.
"""

import pytest
import json
from unittest.mock import patch, MagicMock, AsyncMock
import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from neurohub.app import app
from neurohub.actual_ai_integration import A2AClient, stream_ai_response


class TestNeuroHubAllyRoutes:
    """Test NeuroHub Ally web routes."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_neurohub_ally_page(self, client):
        """Test that NeuroHub Ally page loads."""
        response = client.get('/neurohub-ally')
        assert response.status_code == 200
        assert b'NeuroHub Ally' in response.data
        assert b'AI-powered research assistant' in response.data
    
    def test_neurohub_ally_submit_no_query(self, client):
        """Test form submission without query."""
        response = client.post('/api/neurohub-ally/submit', 
                             data={'research_query': ''})
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
        assert 'required' in data['error']
    
    def test_neurohub_ally_submit_with_query(self, client):
        """Test form submission with valid query."""
        response = client.post('/api/neurohub-ally/submit',
                             data={
                                 'research_query': 'Help me design an EEG experiment',
                                 'context': 'eeg',
                                 'experiment_type': 'cognitive'
                             })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['success'] is True
        assert 'response' in data
        assert 'EEG' in data['response']
    
    @patch('neurohub.neurohub_routes.stream_ai_response_sync')
    def test_neurohub_ally_stream(self, mock_stream, client):
        """Test streaming endpoint."""
        # Mock the streaming response
        mock_stream.return_value = [
            'data: {"type": "status", "message": "Connecting..."}\n\n',
            'data: {"type": "response", "agent": "test", "content": "Test response"}\n\n'
        ]
        
        response = client.post('/api/neurohub-ally/stream',
                             json={
                                 'query': 'Test query',
                                 'context': 'test',
                                 'experiment_type': 'test'
                             })
        
        assert response.status_code == 200
        assert response.mimetype == 'text/event-stream'


class TestA2AIntegration:
    """Test A2A agent integration."""
    
    @pytest.mark.asyncio
    async def test_discover_agents_no_agents(self):
        """Test agent discovery when no agents are running."""
        async with A2AClient() as client:
            # Mock the session to return 404 for all agents
            mock_response = AsyncMock()
            mock_response.status = 404
            client.session.get = AsyncMock(return_value=mock_response)
            
            agents = await client.discover_agents()
            assert agents == []
    
    @pytest.mark.asyncio
    async def test_discover_agents_with_agent(self):
        """Test agent discovery with one agent available."""
        async with A2AClient() as client:
            # Mock response for successful agent discovery
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                "agent_id": "test-agent",
                "capabilities": ["test"]
            })
            
            # Create async context manager for the mock
            async def mock_get(url):
                class AsyncContextManager:
                    async def __aenter__(self):
                        return mock_response
                    async def __aexit__(self, exc_type, exc_val, exc_tb):
                        pass
                return AsyncContextManager()
            
            client.session.get = mock_get
            
            agents = await client.discover_agents()
            assert len(agents) > 0
    
    @pytest.mark.asyncio
    async def test_send_to_agent_success(self):
        """Test sending message to agent successfully."""
        async with A2AClient() as client:
            # Mock successful response
            mock_response = AsyncMock()
            mock_response.status = 200
            mock_response.json = AsyncMock(return_value={
                "response": "Test successful response"
            })
            
            # Create async context manager
            async def mock_post(url, **kwargs):
                class AsyncContextManager:
                    async def __aenter__(self):
                        return mock_response
                    async def __aexit__(self, exc_type, exc_val, exc_tb):
                        pass
                return AsyncContextManager()
            
            client.session.post = mock_post
            
            result = await client.send_to_agent("documentation", "Test message")
            assert "response" in result
            assert result["response"] == "Test successful response"
    
    @pytest.mark.asyncio
    async def test_query_routing(self):
        """Test that queries are routed to appropriate agents."""
        # Test documentation routing
        async for chunk in stream_ai_response("Write a report for my experiment"):
            data = json.loads(chunk)
            if data.get("type") == "status":
                assert "documentation" in data["message"].lower() or "no ai agents" in data["message"].lower()
                break
        
        # Test signal processor routing
        async for chunk in stream_ai_response("Analyze my EEG signal quality"):
            data = json.loads(chunk)
            if data.get("type") == "status":
                assert "signal" in data["message"].lower() or "no ai agents" in data["message"].lower()
                break


class TestErrorHandling:
    """Test error handling in NeuroHub Ally."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client
    
    def test_malformed_json_request(self, client):
        """Test handling of malformed JSON in stream endpoint."""
        response = client.post('/api/neurohub-ally/stream',
                             data='not json',
                             content_type='application/json')
        # Should handle gracefully, though exact behavior depends on Flask config
        assert response.status_code in [400, 500]
    
    @pytest.mark.asyncio
    async def test_agent_timeout_handling(self):
        """Test handling of agent timeout."""
        async with A2AClient() as client:
            # Set very short timeout
            client.timeout = 0.001
            
            result = await client.send_to_agent("documentation", "Test")
            assert "error" in result


if __name__ == "__main__":
    pytest.main([__file__, "-v"])