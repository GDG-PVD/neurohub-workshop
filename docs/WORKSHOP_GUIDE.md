# NeuroHub Workshop Guide
## BGU-Brown Summer School: Build with AI

Welcome to the NeuroHub workshop! In this hands-on session, you'll learn to build a multi-agent AI system for neurotechnology research using Google's cutting-edge AI infrastructure.

> **📚 Full Codelab**: For detailed step-by-step instructions that follow the complete workshop flow, see the [NeuroHub Codelab](NEUROHUB_CODELAB.md). This guide provides a quick reference version.

## What You'll Build

You'll create NeuroHub, an AI-powered platform that helps researchers:
- Design neuroscience experiments
- Analyze biosignal data (EEG, EMG, ECG)
- Generate research documentation
- Coordinate complex research workflows

### Development Approach

This workshop uses a **hybrid development model**:
- **Modules 1-6**: Rapid development in Cloud Shell with instant feedback
- **Module 6 (Final)**: Deploy to Firebase for a production-ready, shareable application

This approach lets you focus on learning AI concepts without deployment complexity, then experience the satisfaction of sharing your creation with the world!

## Prerequisites

Before starting, ensure you have:
- [ ] Google Cloud account with billing enabled
- [ ] Basic Python knowledge
- [ ] Web browser (Chrome recommended)
- [ ] Terminal/command line familiarity

## Workshop Schedule

### Part 1: Foundation (45 min)
- Set up Google Cloud environment
- Deploy the base NeuroHub application
- Explore the neuroscience research database

### Part 2: Your First AI Agent (45 min)
- Build a documentation agent using Google ADK
- Test agent responses locally
- Understand agent lifecycle and memory

### Part 3: Connecting Tools (30 min)
- Set up Model Context Protocol (MCP) server
- Enable agents to create experiments
- Test tool integration

### Part 4: Multi-Agent Workflows (45 min)
- Build signal processing agent with sub-agents
- Implement iterative analysis patterns
- Handle complex agent states

### Part 5: Agent Communication (30 min)
- Enable Agent-to-Agent (A2A) protocol
- Deploy agents as microservices
- Test with A2A Inspector

### Part 6: Orchestration (45 min)
- Build research orchestrator agent
- Coordinate multiple specialized agents
- Create end-to-end workflows

### Part 7: Production Deployment (30 min)
- Deploy backend services to Google Cloud Run
- Deploy frontend to Firebase Hosting
- Get a shareable public URL
- Showcase your multi-agent AI system to the world!

## Getting Started

### Step 1: Access Cloud Shell

1. Go to [Google Cloud Console](https://console.cloud.google.com)
2. Click the **Activate Cloud Shell** button (terminal icon) at the top
3. Click **Open Editor** to access the Cloud Shell IDE

### Step 2: Clone the Repository

In the Cloud Shell terminal:
```bash
git clone https://github.com/GDG-PVD/neurohub-workshop.git
cd neurohub-workshop
```

### Step 3: Initial Setup

Run the setup script:
```bash
bash init.sh
```

When prompted, enter your Google Cloud Project ID.

### Step 4: Configure Environment

```bash
source set_env.sh
```

**Important**: Always use `source` (not `./` or `bash`) for this script!

### Step 5: Enable APIs

```bash
gcloud services enable run.googleapis.com cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com artifactregistry.googleapis.com spanner.googleapis.com \
  apikeys.googleapis.com iam.googleapis.com compute.googleapis.com \
  aiplatform.googleapis.com cloudresourcemanager.googleapis.com maps-backend.googleapis.com
```

This may take 2-3 minutes.

## Module 1: Database Setup

### Create Spanner Instance

```bash
gcloud spanner instances create neurohub-graph-instance \
  --config=regional-us-central1 \
  --processing-units=100 \
  --edition=STANDARD
```

### Create Database

```bash
gcloud spanner databases create neurohub-db \
  --instance=neurohub-graph-instance
```

### Set Up Python Environment

```bash
# Install UV (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Create virtual environment with UV
uv venv
source .venv/bin/activate

# Install dependencies with UV (much faster!)
uv pip install -r requirements.txt
```

### Load Sample Data

```bash
cd neurohub
python setup.py
cd ..
```

### Verify Database

1. Go to [Spanner Console](https://console.cloud.google.com/spanner)
2. Click on `neurohub-graph-instance`
3. Click on `neurohub-db`
4. Open **Spanner Studio**
5. Run this test query:

```sql
Graph NeuroResearchGraph
MATCH (r:Researcher)-[:Leads]->(e:Experiment)
RETURN r.name, e.name
```

## Module 2: Run the Base Application

### Terminal 1: Start Flask App

```bash
cd neurohub
python app.py
```

### Terminal 2: Start MCP Server

Open a new terminal tab (+ icon):
```bash
cd neurohub-workshop
source env/bin/activate
source set_env.sh
cd tools/neurohub
python mcp_server.py
```

### Test the Application

1. Click **Web Preview** > **Preview on port 8080**
2. Explore:
   - Researcher profiles
   - Experiment details
   - Signal data visualizations

## Module 3: Build Your First Agent

### Understanding ADK Structure

Each agent has these key files:
- `agent.py` - Core agent logic
- `[name]_agent.py` - Agent wrapper
- `a2a_server.py` - Communication server
- `Dockerfile` - Container configuration

### Install Agent Dependencies

```bash
# Install the common wheel with UV
uv pip install agents/a2a_common-0.1.0-py3-none-any.whl
```

### Test Documentation Agent

```bash
cd agents/documentation
python instavibe_test_client.py
```

### Explore Agent Code

Open `agents/documentation/agent.py` and observe:
- Agent instructions
- Tool definitions
- Response formatting

## Module 4: Deploy Agents

### Build Docker Container

From repository root:
```bash
docker build -t documentation \
  -f agents/documentation/Dockerfile .
```

### Create Artifact Registry

```bash
gcloud artifacts repositories create neurohub-workshop \
  --repository-format=docker \
  --location=us-central1
```

### Deploy to Cloud Run

```bash
gcloud builds submit --config agents/cloudbuild.yaml \
  --substitutions=_AGENT_NAME=documentation
```

## Module 5: Test Full System

### Start All Services

You'll need 4 terminal tabs:

**Tab 1 - Flask App:**
```bash
cd neurohub && python app.py
```

**Tab 2 - MCP Server:**
```bash
cd tools/neurohub && python mcp_server.py
```

**Tab 3 - Documentation Agent:**
```bash
cd agents/documentation && python a2a_server.py
```

**Tab 4 - Orchestrator Agent:**
```bash
cd agents/research_orchestrator && python a2a_server.py
```

### Test NeuroHub Ally

1. Click the **Web Preview** button (🌐) in Cloud Shell toolbar
2. Select **Preview on port 8080**
3. Click **NeuroHub Ally**
4. Try: "Help me design an EEG experiment for studying attention"

## Module 6: Deploy to Firebase (Production)

### Overview

Now that you've built and tested your multi-agent system locally, let's deploy it to Firebase Hosting so you can share it with others!

### Why Firebase?

- **Persistent URL**: Get a permanent link to share your project
- **Production experience**: See your app running in a real cloud environment
- **Portfolio ready**: Great for showcasing your work

### Deployment Steps

1. **Ensure all services are working locally**
   - Test the web app, MCP server, and at least one agent
   - Make sure NeuroHub Ally is responding correctly

2. **Commit your changes** (if any)
   ```bash
   git add -A
   git commit -m "feat: Add my custom agent implementations"
   ```

3. **Run the deployment script**
   ```bash
   cd ~/neurohub-workshop
   ./deploy_to_firebase.sh
   ```

   This script will:
   - Deploy your Flask backend to Cloud Run
   - Set up Firebase Hosting
   - Configure the routing between Firebase and Cloud Run
   - Give you a public URL to share!

4. **Test your deployed application**
   - Visit the Firebase URL shown in the output
   - Test all functionality (may take a minute to fully deploy)
   - Share the URL with others!

### What Gets Deployed?

- **Frontend**: Static files served by Firebase Hosting (fast CDN)
- **Backend**: Flask app running on Cloud Run (auto-scaling)
- **Agents**: Also deployed to Cloud Run (accessible by the backend)
- **Database**: Uses the same Spanner instance (already in cloud)

### Post-Deployment

After deployment, you have:
- A public URL anyone can access
- Auto-scaling based on traffic
- Automatic HTTPS/SSL
- Global CDN for fast loading

### Troubleshooting Deployment

**"Permission denied" error:**
```bash
chmod +x deploy_to_firebase.sh
```

**"Firebase CLI not found":**
```bash
npm install -g firebase-tools
firebase login
```

**"Service account error":**
Make sure you have the necessary IAM roles from the setup phase.

### 🎉 Congratulations!

You've successfully:
1. Built a multi-agent AI system
2. Integrated with Google's AI tools (ADK, A2A, MCP)
3. Deployed to production on Google Cloud

Your NeuroHub instance is now live and shareable!

## Common Commands Cheat Sheet

### Environment Setup
```bash
source set_env.sh              # Load environment variables
source env/bin/activate        # Activate Python environment
```

### Running Services
```bash
cd neurohub && python app.py   # Start web app
cd tools/neurohub && python mcp_server.py  # Start MCP server
cd agents/[name] && python a2a_server.py   # Start agent
```

### Testing
```bash
python instavibe_test_client.py  # Test agent locally
```

### Docker & Deployment
```bash
docker build -t [agent] -f agents/[agent]/Dockerfile .
gcloud builds submit --config agents/cloudbuild.yaml \
  --substitutions=_AGENT_NAME=[agent]
```

## Troubleshooting Tips

### "Permission denied" on scripts
```bash
chmod +x init.sh set_env.sh
```

### "Project not set" errors
Make sure you used `source set_env.sh` (not `./set_env.sh`)

### Agent connection errors
- Check MCP server is running (port 8001)
- Verify all environment variables are set
- Ensure you're in the virtual environment

### Database not found
- Confirm Spanner instance name: `neurohub-graph-instance`
- Confirm database name: `neurohub-db`
- Re-run `python setup.py` if needed

## Next Steps

After completing the workshop:
1. Experiment with modifying agent prompts
2. Add new tools to the MCP server
3. Create your own specialized agent
4. Deploy the complete system to production

## Resources

- [Workshop Slides](https://docs.google.com/presentation/d/xxx)
- [Google ADK Documentation](https://github.com/google/adk)
- [MCP Documentation](https://modelcontextprotocol.io/)
- [Original InstaVibe Codelab](Instavibe%20Codelab.md)

## Questions?

Ask your instructor or teaching assistants - we're here to help!

---
*NeuroHub Workshop v1.0 | BGU-Brown Summer School 2024*