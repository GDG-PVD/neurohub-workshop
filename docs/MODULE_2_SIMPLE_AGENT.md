# Module 2: Building Your First Agent - Simplified Version

Due to the truncation issues with heredocs, here's a simpler approach using shorter commands.

## Step 1: Create Directory and Navigate

```bash
cd ~/neurohub-workshop
mkdir -p agents/simple_agent
cd agents/simple_agent
```

## Step 2: Create a Simple Agent Without MCP

First, let's create a basic agent that works without MCP tools to test the setup:

```bash
# Create simple_agent.py
echo '"""Simple Research Assistant Agent."""' > simple_agent.py
echo '' >> simple_agent.py
echo 'from google.adk.agents import Agent' >> simple_agent.py
echo '' >> simple_agent.py
echo 'research_assistant_agent = Agent(' >> simple_agent.py
echo '    name="simple_research_assistant",' >> simple_agent.py
echo '    model="gemini-2.0-flash",' >> simple_agent.py
echo '    description="A simple research assistant for NeuroHub",' >> simple_agent.py
echo '    instruction="You are a research assistant. Help with neuroscience research tasks."' >> simple_agent.py
echo ')' >> simple_agent.py
```

## Step 3: Create Test Script

```bash
# Create test script
echo 'import asyncio' > test_simple.py
echo 'from google.adk.runners import Runner' >> test_simple.py
echo 'from google.adk.sessions import InMemorySessionService' >> test_simple.py
echo 'from google.adk.artifacts import InMemoryArtifactService' >> test_simple.py
echo 'from simple_agent import research_assistant_agent' >> test_simple.py
echo '' >> test_simple.py
echo 'async def test():' >> test_simple.py
echo '    session_service = InMemorySessionService()' >> test_simple.py
echo '    artifact_service = InMemoryArtifactService()' >> test_simple.py
echo '    session = await session_service.create_session()' >> test_simple.py
echo '    runner = Runner(' >> test_simple.py
echo '        agent=research_assistant_agent,' >> test_simple.py
echo '        session_service=session_service,' >> test_simple.py
echo '        artifact_service=artifact_service' >> test_simple.py
echo '    )' >> test_simple.py
echo '    result = await runner.run(' >> test_simple.py
echo '        session_id=session.session_id,' >> test_simple.py
echo '        prompt="Hello! What can you help with?"' >> test_simple.py
echo '    )' >> test_simple.py
echo '    print(result.response)' >> test_simple.py
echo '' >> test_simple.py
echo 'asyncio.run(test())' >> test_simple.py
```

## Step 4: Create Requirements

```bash
# Create requirements.txt
echo 'google-cloud-aiplatform[adk,agent_engines]==1.91.0' > requirements.txt
echo 'google-adk==0.4.0' >> requirements.txt
echo 'aiohttp==3.9.5' >> requirements.txt
```

## Step 5: Install and Test

```bash
# Install dependencies
uv pip install -r requirements.txt

# Run the simple test
python test_simple.py
```

## Step 6: Working with the Documentation Agent

Instead of creating a new agent, let's use the existing documentation agent:

```bash
# Navigate to documentation agent
cd ~/neurohub-workshop/agents/documentation

# Check if the test client works
python neurohub_test_client.py
```

If you get import errors, try installing the MCP package:

```bash
uv pip install mcp
```

## Alternative: Use the Working Documentation Agent

The documentation agent already exists and is properly configured. Here's how to test it:

```bash
# Make sure you're in the right directory
cd ~/neurohub-workshop/agents/documentation

# Run the test client that's already there
python neurohub_test_client.py
```

## Troubleshooting

If you still get import errors:

1. Check your google-adk version:
   ```bash
   uv pip show google-adk
   ```

2. Try installing the exact versions from the main requirements:
   ```bash
   cd ~/neurohub-workshop
   uv pip install -r requirements.txt
   ```

3. For the MCP import issue, try this alternative import:
   ```python
   from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
   ```

## Next Steps

Once you have the simple agent working:
1. Test it with different prompts
2. Add more sophisticated instructions
3. Try connecting it to MCP tools when the import issues are resolved
4. Move on to testing the A2A server wrapper