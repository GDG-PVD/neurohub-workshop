# Module 2: Building Your First Agent with ADK - Detailed Step-by-Step Guide

## Overview

In this module, you'll build your first AI agent using Google's Agent Development Kit (ADK). We'll create a simple research assistant agent that can help with neurotechnology documentation tasks.

### What You'll Learn
- Understanding ADK core concepts (BaseAgent, LlmAgent, LoopAgent)
- Creating and configuring an ADK agent
- Integrating with MCP tools
- Testing agents locally
- Debugging and troubleshooting

### Prerequisites
- Completed Module 1 (base application running)
- MCP server running on port 8001
- Virtual environment activated with all dependencies

## Step 1: Understanding ADK Concepts

### Core ADK Classes

1. **BaseAgent**: Foundation class for all agents
   - Provides basic agent functionality
   - No built-in LLM capabilities
   - Used for simple, deterministic agents

2. **Agent**: Standard ADK agent with LLM
   - Built on BaseAgent
   - Includes LLM integration
   - Can use tools via MCP
   - Single-turn conversations

3. **LlmAgent**: Advanced LLM agent
   - Multi-turn conversations
   - Memory management
   - Complex reasoning

4. **LoopAgent**: Iterative processing agent
   - Handles workflows with loops
   - Can retry and refine outputs
   - Good for complex analysis

For this module, we'll use the standard `Agent` class.

## Step 2: Creating Your First Agent

### 2.1 Create Agent Directory Structure

```bash
# Create a new agent directory
mkdir -p agents/research_assistant
cd agents/research_assistant

# Create required files
touch agent.py
touch test_agent.py
touch requirements.txt
touch README.md
```

### 2.2 Define Agent Requirements

Create `requirements.txt`:
```txt
google-cloud-aiplatform[adk,agent_engines]==1.91.0
google-adk==0.4.0
mcp[cli]==1.7.1
aiohttp==3.9.5
```

### 2.3 Create the Agent Code

Create `agent.py` with the following content:

```python
"""Research Assistant Agent - A simple ADK agent for NeuroHub."""

import os
from google.adk.agents import Agent
from google.adk.mcp import MCPToolset, SseServerParams

# Step 1: Define the agent's model
# We use Gemini Flash for fast responses
MODEL = "gemini-2.0-flash"

# Step 2: Define the agent's instructions
# This tells the agent what it should do and how to behave
AGENT_INSTRUCTIONS = """
You are a research assistant agent for NeuroHub, a neurotechnology research platform.

Your primary responsibilities:
1. Help researchers document their experiments
2. Create analysis reports for signal data
3. Generate session logs for research activities
4. Export findings in various formats

Guidelines:
- Be precise and scientific in your documentation
- Use proper neuroscience terminology
- Include relevant metadata (timestamps, device info, parameters)
- Validate data before creating reports
- Follow research ethics and privacy standards

When using tools:
- create_experiment: Use for new research protocols
- create_analysis_report: Use for documenting analysis results
- create_session_log: Use for recording research sessions
- export_findings: Use to generate output files
"""

# Step 3: Get MCP server URL from environment
# Default to localhost for development
MCP_SERVER_URL = os.getenv("MCP_SERVER_URL", "http://localhost:8001")

# Step 4: Create the agent function
def get_agent():
    """Create and configure the research assistant agent."""
    
    # Create MCP toolset for connecting to tools
    mcp_toolset = MCPToolset(
        server_params=SseServerParams(
            url=f"{MCP_SERVER_URL}/sse"
        )
    )
    
    # Create the agent with configuration
    agent = Agent(
        name="research_assistant",
        description="Research assistant for NeuroHub documentation and analysis",
        instructions=AGENT_INSTRUCTIONS,
        model=MODEL,
        toolsets=[mcp_toolset]  # Connect MCP tools
    )
    
    return agent

# Step 5: Export the agent for use by ADK
# This is required for ADK to find your agent
research_assistant_agent = get_agent()
```

### 2.4 Understanding the Code

Let's break down each part:

1. **Imports**:
   - `Agent`: The main ADK agent class
   - `MCPToolset`: Connects to MCP server for tools
   - `SseServerParams`: Configuration for Server-Sent Events

2. **Model Selection**:
   - `gemini-2.0-flash`: Fast, efficient model
   - Good for documentation tasks
   - Lower cost than Pro models

3. **Instructions**:
   - Define agent's role and responsibilities
   - Provide guidelines for behavior
   - Explain available tools
   - Set quality standards

4. **MCP Integration**:
   - Connects to MCP server via SSE
   - Automatically discovers available tools
   - Handles tool execution

5. **Agent Creation**:
   - Name: Unique identifier
   - Description: What the agent does
   - Instructions: Detailed behavior guide
   - Model: LLM to use
   - Toolsets: Connected tools

## Step 3: Testing Your Agent Locally

### 3.1 Create Test Script

Create `test_agent.py`:

```python
"""Test script for the research assistant agent."""

import asyncio
import json
from datetime import datetime
from google.adk.agents import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.artifacts import InMemoryArtifactService
from agent import research_assistant_agent

async def test_agent():
    """Test the research assistant agent with various tasks."""
    
    # Step 1: Create services for testing
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    
    # Step 2: Create a test session
    session = await session_service.create_session()
    print(f"Created session: {session.session_id}")
    
    # Step 3: Create agent runner
    runner = Runner(
        agent=research_assistant_agent,
        session_service=session_service,
        artifact_service=artifact_service
    )
    
    # Step 4: Test different agent capabilities
    test_prompts = [
        # Test 1: Basic greeting
        "Hello! Can you introduce yourself and explain what you can help with?",
        
        # Test 2: Create an experiment
        "Help me create a new EEG experiment for studying visual perception. "
        "The experiment should use a 32-channel EEG system and include "
        "visual stimuli presentation.",
        
        # Test 3: Create analysis report
        "Create an analysis report for an EEG session that showed "
        "increased alpha wave activity during meditation.",
        
        # Test 4: Export findings
        "Export the findings from our visual perception experiment "
        "in a format suitable for publication."
    ]
    
    # Run each test
    for i, prompt in enumerate(test_prompts, 1):
        print(f"\n{'='*60}")
        print(f"Test {i}: {prompt[:50]}...")
        print(f"{'='*60}")
        
        try:
            # Send prompt to agent
            result = await runner.run(
                session_id=session.session_id,
                prompt=prompt
            )
            
            # Print response
            print(f"\nAgent Response:")
            print(result.response)
            
            # Check if tools were used
            if hasattr(result, 'tool_calls') and result.tool_calls:
                print(f"\nTools Used:")
                for tool_call in result.tool_calls:
                    print(f"- {tool_call.tool_name}: {tool_call.parameters}")
            
        except Exception as e:
            print(f"Error: {str(e)}")
            print(f"Type: {type(e).__name__}")
    
    print(f"\n{'='*60}")
    print("Testing complete!")

# Run the test
if __name__ == "__main__":
    # Make sure MCP server is running
    print("Starting agent test...")
    print("Make sure MCP server is running on http://localhost:8001")
    print()
    
    asyncio.run(test_agent())
```

### 3.2 Run the Test

```bash
# Make sure you're in the agent directory
cd agents/research_assistant

# Activate virtual environment (if not already)
source ../../.venv/bin/activate

# Install dependencies
uv pip install -r requirements.txt

# Run the test
python test_agent.py
```

## Step 4: Debugging Common Issues

### 4.1 MCP Connection Issues

**Problem**: Agent can't connect to MCP server
```
Error: Connection refused to http://localhost:8001/sse
```

**Solution**:
1. Check MCP server is running:
   ```bash
   # In a separate terminal
   cd tools/neurohub
   python mcp_server.py
   ```

2. Verify port is correct:
   ```bash
   # Check if port 8001 is listening
   lsof -i :8001
   ```

3. Test MCP server directly:
   ```bash
   curl http://localhost:8001/sse
   ```

### 4.2 Import Errors

**Problem**: Module not found errors
```
ModuleNotFoundError: No module named 'google.adk'
```

**Solution**:
1. Check virtual environment is activated:
   ```bash
   which python
   # Should show .venv/bin/python
   ```

2. Reinstall dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Verify ADK installation:
   ```bash
   uv pip show google-adk
   ```

### 4.3 Agent Not Finding Tools

**Problem**: Agent says tools are not available
```
"I don't have access to the create_experiment tool"
```

**Solution**:
1. Check MCP server logs for tool registration
2. Verify tool names in MCP server match agent expectations
3. Test tool discovery:
   ```python
   # Add to test script
   print("Available tools:", agent.toolsets[0].tools)
   ```

### 4.4 Authentication Errors

**Problem**: Gemini API authentication fails
```
Error: 403 Forbidden - API key not valid
```

**Solution**:
1. Check environment variables:
   ```bash
   echo $GOOGLE_CLOUD_PROJECT
   echo $GOOGLE_GENAI_USE_VERTEXAI
   ```

2. Re-source environment:
   ```bash
   source ../../set_env.sh
   ```

3. Verify project setup:
   ```bash
   gcloud config get-value project
   ```

## Step 5: Enhancing Your Agent

### 5.1 Add Specialized Behaviors

Modify the instructions to add domain expertise:

```python
AGENT_INSTRUCTIONS = """
You are a research assistant agent for NeuroHub, a neurotechnology research platform.

Your primary responsibilities:
1. Help researchers document their experiments
2. Create analysis reports for signal data
3. Generate session logs for research activities
4. Export findings in various formats

Specialized Knowledge:
- EEG: 10-20 system, frequency bands (delta, theta, alpha, beta, gamma)
- EMG: Motor unit analysis, fatigue detection
- ECG: Heart rate variability, arrhythmia detection
- Signal Processing: FFT, wavelet analysis, artifact removal

Guidelines:
- Be precise and scientific in your documentation
- Use proper neuroscience terminology
- Include relevant metadata (timestamps, device info, parameters)
- Validate data before creating reports
- Follow research ethics and privacy standards
- Suggest appropriate analysis methods based on signal type

When using tools:
- create_experiment: Use for new research protocols
- create_analysis_report: Use for documenting analysis results
- create_session_log: Use for recording research sessions
- export_findings: Use to generate output files
"""
```

### 5.2 Add Error Handling

Enhance the agent creation with error handling:

```python
def get_agent():
    """Create and configure the research assistant agent."""
    try:
        # Create MCP toolset
        mcp_toolset = MCPToolset(
            server_params=SseServerParams(
                url=f"{MCP_SERVER_URL}/sse"
            )
        )
        
        # Create agent
        agent = Agent(
            name="research_assistant",
            description="Research assistant for NeuroHub documentation",
            instructions=AGENT_INSTRUCTIONS,
            model=MODEL,
            toolsets=[mcp_toolset]
        )
        
        print(f"Agent created successfully with MCP at {MCP_SERVER_URL}")
        return agent
        
    except Exception as e:
        print(f"Error creating agent: {str(e)}")
        # Create agent without tools as fallback
        return Agent(
            name="research_assistant",
            description="Research assistant for NeuroHub documentation",
            instructions=AGENT_INSTRUCTIONS,
            model=MODEL,
            toolsets=[]  # No tools, but agent still works
        )
```

### 5.3 Add Logging

Add logging for debugging:

```python
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def get_agent():
    """Create and configure the research assistant agent."""
    logger.info("Creating research assistant agent")
    logger.info(f"MCP Server URL: {MCP_SERVER_URL}")
    
    try:
        mcp_toolset = MCPToolset(
            server_params=SseServerParams(
                url=f"{MCP_SERVER_URL}/sse"
            )
        )
        logger.info("MCP toolset created successfully")
        
        agent = Agent(
            name="research_assistant",
            description="Research assistant for NeuroHub documentation",
            instructions=AGENT_INSTRUCTIONS,
            model=MODEL,
            toolsets=[mcp_toolset]
        )
        logger.info("Agent created successfully")
        
        return agent
        
    except Exception as e:
        logger.error(f"Error creating agent: {str(e)}")
        raise
```

## Step 6: Integration Testing

### 6.1 Test with Real MCP Tools

Create an integration test that uses actual tools:

```python
async def integration_test():
    """Test agent with real MCP tool interactions."""
    
    # Create services
    session_service = InMemorySessionService()
    artifact_service = InMemoryArtifactService()
    session = await session_service.create_session()
    
    # Create runner
    runner = Runner(
        agent=research_assistant_agent,
        session_service=session_service,
        artifact_service=artifact_service
    )
    
    # Test creating a real experiment
    prompt = """
    Create an experiment with these details:
    - Title: "Alpha Wave Response to Meditation"
    - Researcher: Dr. Sarah Chen
    - Device: 32-channel EEG system
    - Parameters: 
      - Sampling rate: 1000 Hz
      - Duration: 30 minutes
      - Conditions: baseline, meditation, post-meditation
    """
    
    result = await runner.run(
        session_id=session.session_id,
        prompt=prompt
    )
    
    print("Integration Test Result:")
    print(result.response)
    
    # Check if experiment was created in database
    # (You would add actual database verification here)
```

### 6.2 Performance Testing

Test agent response times:

```python
import time

async def performance_test():
    """Test agent performance and response times."""
    
    prompts = [
        "What types of experiments can I create?",
        "Explain EEG frequency bands",
        "Create a simple EMG experiment",
        "Generate a session log for today"
    ]
    
    times = []
    
    for prompt in prompts:
        start = time.time()
        
        result = await runner.run(
            session_id=session.session_id,
            prompt=prompt
        )
        
        elapsed = time.time() - start
        times.append(elapsed)
        
        print(f"Prompt: {prompt[:30]}...")
        print(f"Response time: {elapsed:.2f}s")
        print()
    
    avg_time = sum(times) / len(times)
    print(f"Average response time: {avg_time:.2f}s")
```

## Step 7: Best Practices

### 7.1 Agent Design Principles

1. **Single Responsibility**: Each agent should focus on one domain
2. **Clear Instructions**: Be specific about capabilities and limitations
3. **Error Handling**: Gracefully handle missing tools or services
4. **Logging**: Add comprehensive logging for debugging
5. **Testing**: Include unit and integration tests

### 7.2 Code Organization

```
agents/research_assistant/
├── agent.py              # Main agent definition
├── test_agent.py         # Local test script
├── integration_test.py   # Integration tests
├── requirements.txt      # Dependencies
├── README.md            # Documentation
└── config/
    └── prompts.py       # Reusable prompts
```

### 7.3 Documentation

Create a README.md for your agent:

```markdown
# Research Assistant Agent

## Overview
An ADK agent that helps researchers document neurotechnology experiments and analyses.

## Capabilities
- Create experiments with detailed protocols
- Generate analysis reports for signal data
- Record research session logs
- Export findings in various formats

## Requirements
- Python 3.11+
- MCP server running on port 8001
- Google Cloud project configured

## Usage
```python
from agent import research_assistant_agent

# Agent is ready to use with ADK Runner
```

## Testing
```bash
python test_agent.py
```

## Configuration
- Model: gemini-2.0-flash
- MCP Server: Set MCP_SERVER_URL environment variable
```

## Step 8: Troubleshooting Guide

### Common Issues and Solutions

#### 1. Agent Doesn't Respond
- Check if model name is correct
- Verify API authentication
- Look for errors in agent creation

#### 2. Tools Not Working
- Ensure MCP server is running
- Check tool names match exactly
- Verify network connectivity

#### 3. Slow Responses
- Consider using gemini-flash model
- Check network latency
- Review instruction complexity

#### 4. Memory Issues
- Use session management properly
- Clear old sessions periodically
- Monitor resource usage

### Debug Checklist

- [ ] Virtual environment activated?
- [ ] All dependencies installed?
- [ ] MCP server running?
- [ ] Environment variables set?
- [ ] Google Cloud authenticated?
- [ ] Correct model specified?
- [ ] Network connectivity OK?
- [ ] Logs showing errors?

## Next Steps

Congratulations! You've built your first ADK agent. In the next modules, you'll learn:

- Module 3: Enhancing agents with MCP tools
- Module 4: Building multi-agent workflows
- Module 5: Agent communication with A2A
- Module 6: Advanced orchestration patterns

### Exercises

1. **Modify Instructions**: Add a new specialized behavior to your agent
2. **Add a Tool**: Create a new test for a different MCP tool
3. **Error Handling**: Add try-catch blocks for better error messages
4. **Performance**: Measure and optimize response times
5. **Documentation**: Create detailed API documentation for your agent

### Resources

- [Google ADK Documentation](https://github.com/google/adk)
- [ADK Examples](https://github.com/google/adk/tree/main/examples)
- [MCP Protocol Spec](https://modelcontextprotocol.io/)
- [Gemini Models Guide](https://ai.google.dev/models/gemini)