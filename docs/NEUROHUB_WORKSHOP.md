# NeuroHub Workshop: Build Multi-Agent AI Systems
## BGU-Brown Summer School: Build with AI

Welcome to the NeuroHub workshop! In this comprehensive guide, you'll learn to build a production-ready multi-agent AI system for neurotechnology research using Google Cloud's cutting-edge AI infrastructure.

---

## Table of Contents
1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Initial Setup](#initial-setup)
4. [Module 1: Understanding the Application](#module-1-understanding-the-application)
5. [Module 2: Your First AI Agent](#module-2-your-first-ai-agent)
6. [Module 3: Connecting Tools with MCP](#module-3-connecting-tools-with-mcp)
7. [Module 4: Multi-Agent Workflows](#module-4-multi-agent-workflows)
8. [Module 5: Agent Communication (A2A)](#module-5-agent-communication-a2a)
9. [Module 6: Deploy to Production](#module-6-deploy-to-production)
10. [Teardown](#teardown)
11. [Quick Reference](#quick-reference)

---

## Overview

### What You'll Build
**NeuroHub**: An AI-powered platform that helps neuroscience researchers:
- 🧠 Design neuroscience experiments
- 📊 Analyze biosignal data (EEG, EMG, ECG)
- 📝 Generate research documentation
- 🔄 Coordinate complex research workflows

### Technologies You'll Learn
- **Google ADK**: Build intelligent agents with memory and reasoning
- **Model Context Protocol (MCP)**: Connect agents to tools and databases
- **Agent-to-Agent (A2A)**: Enable agent communication
- **Google Cloud**: Spanner, Cloud Run, Firebase Hosting

### Development Approach
- **Modules 1-5**: Rapid development in Cloud Shell with instant feedback
- **Module 6**: Deploy to Firebase for a shareable, production-ready application

---

## Prerequisites

Before starting, ensure you have:
- ✅ Google Cloud account with billing enabled
- ✅ Basic Python knowledge
- ✅ Web browser (Chrome recommended)
- ✅ 15 minutes for setup + 2-3 hours for the workshop

---

## Initial Setup

### Step 1: Access Google Cloud Shell

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click **Activate Cloud Shell** button (>_ icon) in the top toolbar
3. Wait for Cloud Shell to initialize
4. Click **Open Editor** if you prefer the IDE view

> 💡 **Tip**: You can resize Cloud Shell by dragging the divider

### Step 2: Clone the Repository

```bash
git clone https://github.com/GDG-PVD/neurohub-workshop.git
cd neurohub-workshop
```

### Step 3: Initialize Your Project

```bash
# Make scripts executable
chmod +x init.sh set_env.sh

# Initialize project (creates ~/project_id.txt)
./init.sh
```

When prompted, enter your Google Cloud project ID and press Enter.

### Step 4: Enable Required APIs

```bash
# This takes 2-3 minutes
gcloud services enable run.googleapis.com cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com artifactregistry.googleapis.com spanner.googleapis.com \
  apikeys.googleapis.com iam.googleapis.com compute.googleapis.com \
  aiplatform.googleapis.com cloudresourcemanager.googleapis.com maps-backend.googleapis.com
```

### Step 5: Set Environment Variables

```bash
# IMPORTANT: Must use 'source', not './' or 'bash'
source set_env.sh
```

### Step 6: Configure IAM Permissions

```bash
PROJECT_ID=$(cat ~/project_id.txt)
PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format="value(projectNumber)")

# Add Spanner permissions
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/spanner.databaseUser"

# Add AI Platform permissions  
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$PROJECT_NUMBER-compute@developer.gserviceaccount.com" \
  --role="roles/aiplatform.user"
```

### Step 7: Create Maps API Key

```bash
gcloud services api-keys create maps-key-workshop \
  --display-name="Maps Platform API Key" \
  --restrictions="" \
  --project=$PROJECT_ID

# Save the key
gcloud services api-keys get-key-string \
  $(gcloud services api-keys list --filter="displayName='Maps Platform API Key'" \
    --format="value(uid)" --limit=1) \
  --project=$PROJECT_ID > ~/mapkey.txt
```

### Step 8: Create Spanner Database

```bash
# Create instance (takes ~1 minute)
gcloud spanner instances create neurohub-graph-instance \
  --config=regional-us-central1 \
  --processing-units=100 \
  --description="NeuroHub Research Database"

# Create database
gcloud spanner databases create neurohub-db \
  --instance=neurohub-graph-instance
```

### Step 9: Set Up Python Environment

```bash
# Install UV (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Create virtual environment
cd ~/neurohub-workshop
uv venv
source .venv/bin/activate

# Install dependencies (30-60 seconds with UV!)
uv pip install -r requirements.txt
```

### Step 10: Load Sample Data

```bash
cd neurohub
python setup.py
cd ..
```

### Verify Setup

Run this query in [Spanner Studio](https://console.cloud.google.com/spanner):

```sql
SELECT 
    r.name AS researcher_name,
    e.name AS experiment_name
FROM 
    Researcher r
JOIN 
    Experiment e ON r.researcher_id = e.principal_investigator_id
LIMIT 5;
```

You should see researcher-experiment pairs.

> 🎉 **Congratulations!** Your environment is ready. Let's build some AI agents!

---

## Module 1: Understanding the Application

**Duration**: 20 minutes  
**Goal**: Explore the NeuroHub platform and understand its architecture

### Start the Application

Open **3 terminal tabs** in Cloud Shell (click the + icon):

**Tab 1 - Web Application:**
```bash
cd ~/neurohub-workshop
source set_env.sh
source .venv/bin/activate
cd neurohub && python app.py
```

**Tab 2 - MCP Server:**
```bash
cd ~/neurohub-workshop
source set_env.sh
source .venv/bin/activate
cd tools/neurohub && python mcp_server.py
```

### Access the Application

1. Click **Web Preview** (🌐) in Cloud Shell toolbar
2. Select **Preview on port 8080**
3. Explore the application:
   - Browse researcher profiles
   - View experiment details
   - Check the NeuroHub Ally (AI assistant)

### Test NeuroHub Ally

1. Click **NeuroHub Ally** in the navigation
2. Try this prompt: "What experiments are studying motor control?"
3. Notice: It can't help yet - we need to build agents!

### Understand the Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Web App       │────▶│   MCP Server    │────▶│    Spanner      │
│  (Flask/SSE)    │     │   (Tools)       │     │   Database      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
         │                       ▲
         └───────────────────────┴────────────────┐
                                                  │
                          ┌─────────────────┐     │
                          │   AI Agents     │─────┘
                          │  (ADK + A2A)    │
                          └─────────────────┘
```

> **🚧 Troubleshooting**: 
> - If port 8080 is busy: `lsof -ti:8080 | xargs kill -9`
> - If imports fail: Make sure you activated the virtual environment

---

## Module 2: Your First AI Agent

**Duration**: 30 minutes  
**Goal**: Build a documentation agent using Google ADK

### Understanding ADK Concepts

Google ADK provides three types of agents:
- **BaseAgent**: Simple request-response
- **LlmAgent**: Adds LLM reasoning
- **LoopAgent**: Iterative processing with state

### Build the Documentation Agent

**Tab 3 - New Terminal:**
```bash
cd ~/neurohub-workshop/agents/documentation
```

Look at the agent structure:
```python
# agent.py - Core agent logic
class DocumentationAgent(BaseAgent):
    def process_request(self, request):
        # Your agent logic here
```

### Test Your Agent Locally

```bash
# Run the test client
python instavibe_test_client.py
```

Try these prompts:
1. "Generate a report for the Motor Imagery BCI experiment"
2. "Summarize findings from EMG analysis"

### Wrap with A2A Protocol

The agent is already wrapped for network communication:
```python
# documentation_agent.py
agent = A2AAgent(
    agent_id="documentation-agent",
    agent=DocumentationAgent(),
    port=8002
)
```

### Start the Agent Server

```bash
python a2a_server.py
```

Your agent is now running on port 8002!

### Connect to NeuroHub Ally

The web app automatically discovers A2A agents. Refresh the page and try NeuroHub Ally again - it should now be able to generate documentation!

> **🚧 Troubleshooting**:
> - "Module not found": `uv pip install agents/a2a_common-0.1.0-py3-none-any.whl`
> - "Port already in use": Change port in a2a_server.py

---

## Module 3: Connecting Tools with MCP

**Duration**: 20 minutes  
**Goal**: Enable agents to create experiments and save data

### Understanding MCP

Model Context Protocol (MCP) provides:
- Standardized tool definitions
- Type-safe parameters
- Automatic validation
- Tool discovery

### Available Tools

Check `tools/neurohub/mcp_server.py`:
- `create_experiment`: Register new experiments
- `create_analysis_report`: Document findings
- `create_session_log`: Record sessions
- `export_findings`: Generate outputs

### Enable MCP in Your Agent

The connection is already configured:
```python
# In agent initialization
self.mcp_client = MCPClient(server_url="http://localhost:8001")
tools = self.mcp_client.list_tools()
```

### Test Tool Usage

In NeuroHub Ally, try:
"Create a new EEG experiment for studying sleep patterns with 20 participants"

The agent should:
1. Use the documentation agent to design the experiment
2. Call `create_experiment` to save it
3. Return the experiment ID

### Verify in Database

Check Spanner Studio:
```sql
SELECT * FROM Experiment 
ORDER BY create_time DESC 
LIMIT 1;
```

> **🚧 Troubleshooting**:
> - "MCP connection failed": Ensure MCP server is running in Tab 2
> - "Tool not found": Check tool name matches exactly

---

## Module 4: Multi-Agent Workflows

**Duration**: 30 minutes  
**Goal**: Build complex workflows with specialized agents

### The Signal Processor Agent

This agent demonstrates:
- Sub-agent orchestration
- Iterative analysis with LoopAgent
- State management

**Tab 4 - New Terminal:**
```bash
cd ~/neurohub-workshop/agents/signal_processor
python a2a_server.py
```

### Agent Hierarchy

```
SignalProcessorAgent (LoopAgent)
├── PreprocessingAgent (BaseAgent)
├── AnalysisAgent (LlmAgent)
└── QualityCheckAgent (BaseAgent)
```

### Test Complex Workflow

In NeuroHub Ally:
"Analyze the EEG data from the Motor Imagery experiment. Check signal quality and identify motor cortex activation patterns."

Watch the agent:
1. Retrieve signal data
2. Preprocess (filtering, artifact removal)
3. Analyze patterns
4. Quality check
5. Generate report

### Understanding Loop Patterns

```python
class SignalProcessorAgent(LoopAgent):
    def should_continue(self, state):
        return state.quality_score < 0.8 and state.iterations < 3
```

> **🚧 Troubleshooting**:
> - "Agent timeout": Increase timeout in agent config
> - "Memory error": Check state size, implement cleanup

---

## Module 5: Agent Communication (A2A)

**Duration**: 20 minutes  
**Goal**: Enable direct agent-to-agent communication

### Start All Agents

Make sure all agents are running:
- Documentation Agent (port 8002)
- Signal Processor (port 8003)
- Experiment Designer (port 8004)
- Research Orchestrator (port 8005)

### Test the Orchestrator

**Tab 5 - New Terminal:**
```bash
cd ~/neurohub-workshop/agents/research_orchestrator
python a2a_server.py
```

In NeuroHub Ally:
"Design and run a complete study on attention during meditation. Create the experiment, collect EEG data, analyze it, and generate a report."

### Watch the Orchestration

The orchestrator will:
1. Call experiment designer → Create protocol
2. Call signal processor → Analyze data
3. Call documentation → Generate report
4. Coordinate the entire workflow

### A2A Inspector

Check agent communication:
```bash
curl http://localhost:8005/.well-known/agent.json | jq
```

> **🚧 Troubleshooting**:
> - "Agent not found": Check agent is running and port is correct
> - "Connection refused": Verify firewall rules allow localhost connections

---

## Module 6: Deploy to Production

**Duration**: 20 minutes  
**Goal**: Deploy your complete system to Firebase

### Why Deploy?

- Get a permanent, shareable URL
- Experience production deployment
- Show off your work!

### Pre-deployment Checklist

✅ All agents working locally  
✅ NeuroHub Ally responding correctly  
✅ Database has sample data  

### Run Deployment Script

```bash
cd ~/neurohub-workshop
./deploy_to_firebase.sh
```

This script:
1. Builds and deploys backend to Cloud Run
2. Configures Firebase Hosting
3. Sets up routing and environment variables
4. Provides your public URL!

### What Gets Deployed

- **Frontend**: Static files on Firebase CDN
- **Backend**: Flask app on Cloud Run (auto-scaling)
- **Agents**: Containerized on Cloud Run
- **Database**: Existing Spanner instance

### Test Your Production App

1. Visit the Firebase URL (shown in output)
2. Test all functionality
3. Share with others!

> **🚧 Troubleshooting**:
> - "Permission denied": `chmod +x deploy_to_firebase.sh`
> - "Firebase CLI not found": `npm install -g firebase-tools`
> - Build fails: Check Dockerfile syntax

---

## Teardown

### Quick Teardown (Keep Project)

Remove resources but keep your project:

```bash
# Delete Spanner instance
gcloud spanner instances delete neurohub-graph-instance --quiet

# Delete Cloud Run services
gcloud run services delete neurohub-app --region=us-central1 --quiet

# Delete Firebase hosting
firebase hosting:disable
```

### Complete Teardown (Delete Project)

**⚠️ Warning**: This deletes EVERYTHING and stops all billing:

```bash
PROJECT_ID=$(cat ~/project_id.txt)
gcloud projects delete $PROJECT_ID
```

### Partial Teardown Options

Keep some resources for later:
```bash
# Keep database, delete compute
gcloud run services list --format="value(name)" | xargs -I {} gcloud run services delete {} --quiet

# Keep project, pause Spanner
gcloud spanner instances update neurohub-graph-instance --processing-units=100
```

---

## Quick Reference

### Common Commands

```bash
# Environment setup
source set_env.sh
source .venv/bin/activate

# Start services
cd neurohub && python app.py              # Web app
cd tools/neurohub && python mcp_server.py # MCP server
cd agents/[name] && python a2a_server.py  # Agents

# Testing
python instavibe_test_client.py           # Test agent locally
```

### Port Reference

| Service | Port | Access |
|---------|------|--------|
| Flask App | 8080 | Web Preview → Preview on port 8080 |
| MCP Server | 8001 | Internal (localhost) |
| Documentation | 8002 | Internal (localhost) |
| Signal Processor | 8003 | Internal (localhost) |
| Experiment Designer | 8004 | Internal (localhost) |
| Orchestrator | 8005 | Internal (localhost) |

### Useful SQL Queries

```sql
-- Test connection
SELECT name FROM Researcher LIMIT 5;

-- Find experiments
SELECT r.name, e.name 
FROM Researcher r
JOIN Experiment e ON r.researcher_id = e.principal_investigator_id;

-- Recent analyses
SELECT * FROM Analysis 
ORDER BY create_time DESC 
LIMIT 10;
```

### Environment Variables

```bash
GOOGLE_CLOUD_PROJECT      # Your project ID
SPANNER_INSTANCE_ID       # neurohub-graph-instance
SPANNER_DATABASE_ID       # neurohub-db
GOOGLE_MAPS_API_KEY       # From ~/mapkey.txt
MCP_SERVER_URL           # http://localhost:8001
```

---

## Congratulations! 🎉

You've successfully built a production-ready multi-agent AI system! 

### What You've Accomplished

✅ Built multiple AI agents with Google ADK  
✅ Connected agents to tools with MCP  
✅ Enabled agent communication with A2A  
✅ Deployed to production on Google Cloud  
✅ Created a shareable, scalable application  

### Next Steps

- Experiment with agent prompts and behaviors
- Add new tools to the MCP server  
- Create your own specialized agents
- Share your NeuroHub URL!

### Resources

- [Google ADK Documentation](https://github.com/google/adk)
- [MCP Specification](https://modelcontextprotocol.io/)
- [A2A Protocol](https://github.com/weimeilin79/a2a-python)

---

**Thank you for participating in the NeuroHub workshop!**