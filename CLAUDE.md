# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

InstaVibe Bootstrap is a multi-agent AI social network platform built on Google Cloud's AI infrastructure. It combines a Flask web application with multiple specialized AI agents that communicate via Google's Agent Development Kit (ADK) and Model Context Protocol (MCP).

## Common Development Commands

### Python Development

```bash
# Install dependencies
pip install -r requirements.txt

# Run the Flask application
cd instavibe && python app.py

# Run an agent server
cd agents/[agent-name] && python a2a_server.py

# Test an agent
cd agents/[agent-name] && python [agent-name]_test_client.py
```

### Database Setup

```bash
# Set up the database schema and test data
cd instavibe && python setup.py

# Reset the database (drops all tables)
# Execute the SQL in instavibe/reset.sql via Spanner console
```

### Docker Operations

```bash
# Build an agent container
docker build -t [agent-name] -f agents/[agent-name]/Dockerfile .

# Build the main app container
docker build -t instavibe -f instavibe/Dockerfile .

# Deploy via Google Cloud Build
gcloud builds submit --config agents/cloudbuild.yaml --substitutions=_AGENT_NAME=[agent-name]
```

### Environment Setup

```bash
# Initialize Google Cloud project
source init.sh

# Set environment variables
source agents/set_env.sh
```

## High-Level Architecture

### System Components

1. **Core Application (`/instavibe/`)**
   - Flask web server with SSE support for real-time features
   - Google Cloud Spanner database with property graph model
   - Web UI for viewing people, events, and posts
   - REST API endpoints for creating posts and events
   - "Introvert Ally" AI-powered social planning assistant

2. **AI Agents (`/agents/`)**
   - **Planner Agent**: Coordinates multi-agent workflows and task planning
   - **Social Agent**: Handles social media content generation and analysis
   - **Platform MCP Client**: Integrates with MCP servers for tool access
   - **Orchestrate Agent**: Manages agent-to-agent communication

3. **Tools (`/tools/instavibe/`)**
   - MCP server exposing create_event and create_post functions
   - Accessible by agents via SSE transport protocol

4. **Common Library (`a2a_common`)**
   - Shared utilities for task management, typing, and server implementations
   - Packaged as a wheel file and imported by all agents

### Database Schema

The application uses Google Cloud Spanner with a property graph model:

**Nodes:**
- `Person`: Users with name, age
- `Event`: Social events with name, description, date
- `Post`: Social media posts with text, sentiment
- `Location`: Places with coordinates and address

**Edges (Relationships):**
- `Friendship`: Person ↔ Person bidirectional relationships
- `Attendance`: Person → Event (labeled "Attended")
- `Mention`: Post → Person (labeled "Mentioned")
- `EventLocation`: Event → Location (labeled "HasLocation")

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
- `GET /` - Home page with posts and events
- `GET /person/<person_id>` - Person profile
- `GET /event/<event_id>` - Event details with map
- `GET /introvert-ally` - AI social planning assistant

**REST APIs:**
- `POST /api/posts` - Create a new post
- `POST /api/events` - Create an event with locations and attendees

**SSE Endpoints:**
- `GET /introvert-ally/stream-plan` - Stream AI-generated social plans
- `GET /introvert-ally/stream-post-status` - Stream creation status updates

### Key Environment Variables

```bash
# Google Cloud
GOOGLE_CLOUD_PROJECT
SPANNER_INSTANCE_ID
SPANNER_DATABASE_ID

# Application
FLASK_SECRET_KEY
APP_HOST
APP_PORT

# APIs
GOOGLE_MAPS_API_KEY
GOOGLE_MAPS_MAP_ID

# MCP Configuration
MCP_SERVER_URL
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

- Test agents using `*_test_client.py` scripts
- Use the ADK `Runner` class for agent execution
- No traditional unit tests; testing is integration-focused
- Use `planner_eval.evalset.json` for planner agent evaluation

### Deployment

- Docker containers for each service
- Google Cloud Run for hosting
- Cloud Build for CI/CD
- Port 8080 exposed for all services
- Multi-stage Docker builds with dependency caching