# NeuroHub Ally Architecture

## Overview

The NeuroHub Ally is an AI assistant interface in the web application that connects to multiple specialized AI agents. Here's how the components work together:

## System Components

### 1. Web Application (Port 8080)
- **Flask web server** with the NeuroHub Ally interface
- Sends user queries to AI agents via HTTP/A2A protocol
- Displays responses in the web UI

### 2. AI Integration Layer
- **File**: `neurohub/actual_ai_integration.py`
- Routes queries to appropriate agents based on content
- Manages agent discovery and communication
- Falls back to mock responses if no agents available

### 3. A2A Agent Servers
Each agent runs as a separate server:
- **Documentation Agent** (Port 8002): Creates reports and documentation
- **Signal Processor** (Port 8003): Analyzes biosignal data
- **Experiment Designer** (Port 8004): Designs research protocols
- **Research Orchestrator** (Port 8005): Coordinates complex workflows

### 4. MCP Server (Port 8001)
- Provides database tools to agents
- Enables agents to create experiments, save analyses, etc.

## How It Works

### When NO Agents Are Running (Default for Modules 1-2)
```
User → Web App → Mock Response → User
```
- The web app returns pre-written example responses
- Perfect for understanding the UI and application flow
- No AI functionality required

### When Agents ARE Running (Modules 5-6)
```
User → Web App → AI Integration → A2A Agent → Response → User
                                      ↓
                                  MCP Server
                                      ↓
                                   Database
```

## Query Routing Logic

The AI integration layer intelligently routes queries:

1. **Documentation queries** → Documentation Agent
   - Keywords: "document", "report", "write", "summarize"

2. **Signal analysis queries** → Signal Processor
   - Keywords: "signal", "eeg", "emg", "ecg", "analyze"

3. **Experiment design queries** → Experiment Designer
   - Keywords: "experiment", "protocol", "design", "study"

4. **Complex/general queries** → Research Orchestrator
   - Default for queries that don't match specific patterns

## Module Progression

### Module 1: Web App Only
- Explore the UI
- See mock responses
- Understand the application structure

### Module 2: Build Your First Agent
- Create the workshop agent
- Test it standalone (not connected to web app yet)

### Module 3: Connect to MCP
- Enable database operations
- Still running agents standalone

### Module 4: Multi-Agent Workflows
- Build specialized agents
- Test agent capabilities

### Module 5: A2A Communication
- Start agents as A2A servers
- Web app can now discover and use agents
- NeuroHub Ally becomes fully functional

### Module 6: Production Deployment
- Deploy everything to cloud
- Fully integrated system

## Testing the Integration

### Check if agents are discoverable:
```bash
# Test if documentation agent is running
curl http://localhost:8002/.well-known/agent.json

# Test all agent endpoints
for port in 8002 8003 8004 8005; do
  echo "Checking port $port..."
  curl -s http://localhost:$port/.well-known/agent.json | jq .name || echo "Not running"
done
```

### Send a test query:
```bash
curl -X POST http://localhost:8002/process \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello, agent!", "context": {}}'
```

## Important Notes

1. **Agents are optional** for Modules 1-4
2. **Mock responses** allow you to explore the full UI without AI
3. **A2A servers** require the common module and MCP (may not be available in all environments)
4. **The workshop agent** (Module 2) doesn't have A2A by default - it's added in Module 5

## Troubleshooting

### "No AI agents are currently available"
This means:
- The web app is trying to connect to agents
- No A2A servers are running on the expected ports
- This is normal for Modules 1-4!

### "Mock response" appears
This means:
- The web app is using fallback responses
- This is the expected behavior when agents aren't running
- Perfect for learning the application structure

### To make NeuroHub Ally fully functional:
1. Complete Module 5 (A2A Communication)
2. Start all agent A2A servers
3. Ensure MCP server is running
4. The web app will automatically discover and use the agents