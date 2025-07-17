# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

NeuroHub is a multi-agent AI platform for neurotechnology research and development, built on Google Cloud's AI infrastructure. It combines a Flask web application with specialized AI agents that communicate via Google's Agent Development Kit (ADK), Agent-to-Agent (A2A) protocol, and Model Context Protocol (MCP).

This workshop project demonstrates how to build production-ready multi-agent systems for scientific research applications, adapted from Christina Lin's InstaVibe codelab.

## Common Development Commands

### Python Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask application
cd neurohub && python app.py

# Run an agent server
cd agents/[agent-name] && python a2a_server.py

# Test an agent
cd agents/documentation && python instavibe_test_client.py
```

### Database Setup

```bash
# Set up the database schema and test data
cd neurohub && python setup.py

# Reset the database (drops all tables)
# Execute the SQL in neurohub/reset.sql via Spanner console
```

### Docker Operations

```bash
# Build an agent container
docker build -t [agent-name] -f agents/[agent-name]/Dockerfile .

# Build the main app container
docker build -t neurohub -f neurohub/Dockerfile .

# Deploy via Google Cloud Build
gcloud builds submit --config agents/cloudbuild.yaml --substitutions=_AGENT_NAME=[agent-name]
```

### Environment Setup

```bash
# Initialize Google Cloud project (creates project_id.txt)
source init.sh

# Set environment variables (must be sourced)
source set_env.sh

# Environment variables needed:
# - GOOGLE_CLOUD_PROJECT (from project_id.txt)
# - SPANNER_INSTANCE_ID (default: neurohub-graph-instance)
# - SPANNER_DATABASE_ID (default: neurohub-db)
# - GOOGLE_MAPS_API_KEY (from mapkey.txt)
# - FLASK_SECRET_KEY (for session management)
```

## High-Level Architecture

### System Components

1. **Core Application (`/neurohub/`)**
   - Flask web server with SSE support for real-time features
   - Google Cloud Spanner database with property graph model
   - Web UI for viewing researchers, experiments, and signal data
   - REST API endpoints for creating experiments and analysis reports
   - "NeuroHub Ally" AI-powered research assistant

2. **AI Agents (`/agents/`)**
   - **Signal Processor Agent**: Analyzes biosignal data (EEG, EMG, ECG) and identifies patterns
   - **Experiment Designer Agent**: Creates research protocols based on scientific literature
   - **Documentation Agent**: Generates research reports and exports findings
   - **Research Orchestrator Agent**: Coordinates multi-agent workflows for complex research tasks

3. **Tools (`/tools/neurohub/`)**
   - MCP server exposing neurotechnology-specific functions:
     - `create_experiment`: Register new research experiments
     - `create_analysis_report`: Document signal analysis findings
     - `create_session_log`: Record experimental session data
     - `export_findings`: Generate formatted research outputs
     - `register_device`: Add new measurement devices to the system
   - Accessible by agents via SSE transport protocol

4. **Common Library (`a2a_common`)**
   - Shared utilities for task management, typing, and server implementations
   - Packaged as a wheel file and imported by all agents

### Database Schema

The application uses Google Cloud Spanner with a property graph model for research relationships:

**Nodes:**
- `Researcher`: Scientists with name, email, institution, expertise
- `Experiment`: Research studies with protocols, hypotheses, status
- `Device`: Measurement equipment (EEG headsets, EMG sensors, etc.)
- `SignalData`: Recorded biosignals with quality metrics
- `Session`: Individual data collection sessions
- `Analysis`: Signal processing results and findings
- `Publication`: Research papers documenting experiments

**Edges (Relationships):**
- `Collaboration`: Researcher ↔ Researcher research partnerships
- `Leads`: Researcher → Experiment (principal investigator)
- `Conducts`: Researcher → Session
- `PartOf`: Session → Experiment
- `RecordedIn`: SignalData → Session
- `RecordedWith`: SignalData → Device
- `Analyzes`: Analysis → SignalData
- `PerformedBy`: Researcher → Analysis
- `Uses`: Experiment → Device
- `Documents`: Publication → Experiment

### Agent Development Pattern

Each agent follows this structure:
```
agents/[agent-name]/
├── agent.py              # Main agent definition
├── [agent-name]_agent.py # Agent wrapper extending AgentWithTaskManager
├── a2a_server.py         # A2A server for agent communication
├── requirements.txt      # Agent-specific dependencies
└── Dockerfile           # Container configuration
```

Agents are built using Google ADK and extend base classes like `LlmAgent`, `LoopAgent`, or `BaseAgent`. They use async/await patterns and integrate with MCP servers for tool access.

### API Endpoints

**Web Routes:**
- `GET /` - Home page with experiments and research data
- `GET /researcher/<researcher_id>` - Researcher profile and publications
- `GET /experiment/<experiment_id>` - Experiment details with protocol
- `GET /neurohub-ally` - AI research planning assistant

**REST APIs:**
- `POST /api/experiments` - Create a new experiment
- `POST /api/analyses` - Submit analysis results
- `POST /api/sessions` - Log experimental sessions

**SSE Endpoints:**
- `GET /neurohub-ally/stream-protocol` - Stream AI-generated research protocols
- `GET /neurohub-ally/stream-analysis-status` - Stream analysis progress updates

### Key Environment Variables

```bash
# Google Cloud
GOOGLE_CLOUD_PROJECT      # Your GCP project ID
SPANNER_INSTANCE_ID       # Default: neurohub-graph-instance
SPANNER_DATABASE_ID       # Default: neurohub-db
GOOGLE_CLOUD_LOCATION     # Default: us-central1

# Application
FLASK_SECRET_KEY          # Session encryption key
APP_HOST                  # Default: 0.0.0.0
APP_PORT                  # Default: 8080

# APIs
GOOGLE_MAPS_API_KEY       # For location visualization
GOOGLE_MAPS_MAP_ID        # Map styling ID
GOOGLE_GENAI_USE_VERTEXAI # Set to TRUE for Vertex AI

# MCP Configuration
MCP_SERVER_URL            # MCP server endpoint
```

### Development Patterns

1. **Async Operations**: All agents use async/await with `nest_asyncio` for nested loops
2. **Error Handling**: Comprehensive error pages and flash messages
3. **Resource Management**: Use `AsyncExitStack` for proper cleanup
4. **Configuration**: Load from `.env` files using `python-dotenv`
5. **Placeholder Comments**: Mark incomplete sections with `#REPLACE FOR` or `#REPLACE ME`
6. **Type Hints**: Use typing annotations throughout the codebase
7. **Graph Queries**: Use GQL for complex relationship queries, SQL for simple operations

### Testing Approach

- Test agents using test client scripts (e.g., `instavibe_test_client.py`)
- Use the ADK `Runner` class for agent execution
- No traditional unit tests; testing is integration-focused
- Test queries can be modified in client scripts to test different scenarios

### Deployment

- Docker containers for each service
- Google Cloud Run for hosting
- Cloud Build for CI/CD (`gcloud builds submit`)
- Port 8080 exposed for all services
- Multi-stage Docker builds with dependency caching

### Important Notes

1. **Database Connection**: The app expects a Spanner instance named `neurohub-graph-instance` with database `neurohub-db`. Update these in environment variables if different.
2. **Authentication**: Ensure proper Google Cloud authentication before running (`gcloud auth login`)
3. **Property Graph**: The database uses Spanner's property graph feature for relationship queries
4. **Agent Communication**: Agents communicate via A2A protocol on separate ports
5. **MCP Tools**: Tools are exposed via MCP server and accessed by agents through SSE transport