# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

NeuroHub is a multi-agent AI platform for neurotechnology research, built for the BGU-Brown Summer School "Build with AI" workshop. This project demonstrates how to build production-ready multi-agent systems using Google's AI infrastructure (ADK, A2A protocol, and MCP).

Adapted from Christina Lin's InstaVibe codelab, NeuroHub transforms social event planning concepts into neurotechnology research workflows.

## Workshop Quick Start

### Step 1: Initial Setup
```bash
# Clone the repository
git clone https://github.com/GDG-PVD/neurohub-workshop.git
cd neurohub-workshop

# Initialize Google Cloud project (creates ~/project_id.txt)
bash init.sh

# Set environment variables (MUST source, not execute)
source set_env.sh

# Enable required Google Cloud APIs
gcloud services enable run.googleapis.com cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com artifactregistry.googleapis.com spanner.googleapis.com \
  apikeys.googleapis.com iam.googleapis.com compute.googleapis.com \
  aiplatform.googleapis.com cloudresourcemanager.googleapis.com maps-backend.googleapis.com
```

### Step 2: Database Setup
```bash
# Install UV and create virtual environment
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt

# Create Spanner instance and database
gcloud spanner instances create neurohub-graph-instance \
  --config=regional-us-central1 --processing-units=100

gcloud spanner databases create neurohub-db \
  --instance=neurohub-graph-instance

# Load initial data
cd neurohub && python setup.py
```

### Step 3: Run the Application
```bash
# Terminal 1: Start the Flask web app
cd neurohub && python app.py

# Terminal 2: Start MCP server (in a new terminal)
cd tools/neurohub && python mcp_server.py

# Terminal 3: Start an agent (e.g., documentation agent)
cd agents/documentation && python a2a_server.py
```

## Workshop Progression Guide

### Module 1: Understanding the Base Application
- Explore the Flask web interface at http://localhost:8080
- Review the database schema and property graph model
- Test basic CRUD operations via the UI

### Module 2: Building Your First Agent (ADK)
- Start with the documentation agent
- Learn ADK concepts: BaseAgent, LlmAgent, LoopAgent
- Test locally using ADK Dev UI

### Module 3: Adding Tools with MCP
- Understand Model Context Protocol
- Connect agents to the MCP server
- Enable agents to create experiments and analyses

### Module 4: Multi-Agent Workflows
- Build the signal processor agent with sub-agents
- Implement loop patterns for iterative analysis
- Handle agent state and memory

### Module 5: Agent Communication (A2A)
- Wrap agents with A2A servers
- Define agent cards and capabilities
- Test with A2A Inspector

### Module 6: Orchestration
- Build the research orchestrator agent
- Coordinate multiple specialized agents
- Handle complex research workflows

### Module 7: Production Deployment
- Build Docker containers
- Deploy to Cloud Run
- Integrate with Vertex AI Agent Engine

## Key Commands Reference

### Development Commands
```bash
# Install dependencies
uv pip install -r requirements.txt
uv pip install agents/a2a_common-0.1.0-py3-none-any.whl

# Run the main application
cd neurohub && python app.py

# Run an agent server
cd agents/[agent-name] && python a2a_server.py

# Test an agent
cd agents/documentation && python instavibe_test_client.py

# Run MCP server
cd tools/neurohub && python mcp_server.py
```

### Docker & Deployment
```bash
# Build agent container
docker build -t [agent-name] -f agents/[agent-name]/Dockerfile .

# Deploy to Cloud Run
gcloud builds submit --config agents/cloudbuild.yaml \
  --substitutions=_AGENT_NAME=[agent-name],_IMAGE_PATH=gcr.io/${PROJECT_ID}/[agent-name]:latest

# Create artifact registry (one-time setup)
gcloud artifacts repositories create neurohub-workshop \
  --repository-format=docker --location=us-central1
```

### Database Operations
```bash
# Setup database with sample data
cd neurohub && python setup.py

# Reset database (drops all tables)
# Execute SQL from neurohub/reset_neurohub.sql in Spanner console
# Note: neurohub/reset.sql contains old InstaVibe schema - use reset_neurohub.sql instead

# Test graph queries in Spanner Studio
Graph NeuroResearchGraph
MATCH (r:Researcher)-[:Leads]->(e:Experiment)
RETURN r.name, e.name
```

## Architecture Overview

### System Components

1. **Web Application** (`/neurohub/`)
   - Flask server with SSE support
   - REST APIs for experiments and analyses
   - NeuroHub Ally AI assistant
   - Templates: `index.html`, `researcher.html`, `experiment.html`, `neurohub_ally.html`

2. **AI Agents** (`/agents/`)
   - **Signal Processor**: Analyzes biosignals (EEG, EMG, ECG)
   - **Experiment Designer**: Creates research protocols
   - **Documentation**: Generates reports and findings
   - **Research Orchestrator**: Coordinates workflows

3. **MCP Tools** (`/tools/neurohub/`)
   - `create_experiment`: Register new experiments
   - `create_analysis_report`: Document findings
   - `create_session_log`: Record sessions
   - `export_findings`: Generate outputs
   - `register_device`: Add equipment

4. **Database Schema** (Property Graph)
   - **Nodes**: Researcher, Experiment, Device, SignalData, Session, Analysis, Publication
   - **Edges**: Collaboration, Leads, Conducts, Uses, Analyzes, Documents

### Agent Development Pattern
```
agents/[agent-name]/
├── agent.py              # ADK agent logic
├── [agent-name]_agent.py # Agent wrapper
├── a2a_server.py         # A2A server
├── requirements.txt      # Dependencies
└── Dockerfile           # Container config
```

## Environment Variables

```bash
# Core Google Cloud settings
GOOGLE_CLOUD_PROJECT      # Your GCP project ID
SPANNER_INSTANCE_ID       # Default: neurohub-graph-instance
SPANNER_DATABASE_ID       # Default: neurohub-db
GOOGLE_CLOUD_LOCATION     # Default: us-central1

# API Keys and Authentication
GOOGLE_MAPS_API_KEY       # From ~/mapkey.txt
FLASK_SECRET_KEY          # Session encryption
GOOGLE_GENAI_USE_VERTEXAI # Set to TRUE

# Service Configuration
MCP_SERVER_URL           # Default: http://localhost:8001
APP_HOST                 # Default: 0.0.0.0
APP_PORT                 # Default: 8080
```

## Common Issues & Troubleshooting

### Environment Setup Issues
- **"Permission denied" on scripts**: Run `chmod +x init.sh set_env.sh`
- **"Project not set"**: Ensure you ran `source set_env.sh` (not just `./set_env.sh`)
- **API not enabled errors**: Re-run the `gcloud services enable` command

### Database Issues
- **"Instance not found"**: Check SPANNER_INSTANCE_ID matches what you created
- **"Table not found"**: Run `python setup.py` in the neurohub directory
- **Old schema references**: Some files may still reference InstaVibe tables

### Agent Issues
- **"Connection refused"**: Ensure MCP server is running on port 8001
- **"Agent not found"**: Check A2A server is running and port is correct
- **Import errors**: Install the common wheel: `uv pip install agents/a2a_common-0.1.0-py3-none-any.whl`

### Docker/Deployment Issues
- **Build failures**: Ensure you're in the repository root when building
- **"Repository not found"**: Create artifact registry first
- **Authentication errors**: Run `gcloud auth configure-docker`

## Workshop Tips

1. **Start Simple**: Get the base app running before adding agents
2. **Test Incrementally**: Test each agent locally before deploying
3. **Check Logs**: Use `gcloud run logs read` for debugging deployed services
4. **Use Dev Tools**: ADK Dev UI and A2A Inspector are invaluable for testing
5. **Environment Consistency**: Always source `set_env.sh` in new terminals

## Important Notes

1. **File Locations**: Config files (`project_id.txt`, `mapkey.txt`) are in home directory (`~/`)
2. **Name Inconsistencies**: Some files reference "instavibe" - these work but should ideally be updated
3. **Testing**: No unit tests; use integration test clients
4. **Workshop Focus**: Optimized for learning, not production robustness
5. **Placeholder Patterns**: Look for `#REPLACE ME` or `#REPLACE FOR` comments

## Resources

- [Google ADK Documentation](https://github.com/google/adk)
- [A2A Protocol Spec](https://github.com/weimeilin79/a2a-python)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Workshop Slides](docs/workshop-slides.pdf)
- [Original InstaVibe Codelab](docs/Instavibe%20Codelab.md)