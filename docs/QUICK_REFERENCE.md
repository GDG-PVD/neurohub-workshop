# NeuroHub Workshop - Quick Reference Card

## Essential Commands

### 🚀 Initial Setup
```bash
bash init.sh                    # Initialize project (run once)
source set_env.sh              # Load environment (run in each terminal)
source .venv/bin/activate      # Activate UV virtual environment
```

### 📦 Package Installation
```bash
# Install UV (one-time setup)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Create virtual environment and install packages
uv venv
uv pip install -r requirements.txt
uv pip install agents/a2a_common-0.1.0-py3-none-any.whl
```

### 🗄️ Database Commands
```bash
# Create Spanner instance
gcloud spanner instances create neurohub-graph-instance \
  --config=regional-us-central1 --processing-units=100

# Create database
gcloud spanner databases create neurohub-db \
  --instance=neurohub-graph-instance

# Load sample data
cd neurohub && python setup.py
```

### 🏃 Running Services

**Terminal 1 - Web App:**
```bash
cd neurohub && python app.py
```

**Terminal 2 - MCP Server:**
```bash
cd tools/neurohub && python mcp_server.py
```

**Terminal 3 - Agent:**
```bash
cd agents/[agent-name] && python a2a_server.py
```

### 🧪 Testing Agents
```bash
cd agents/documentation
python instavibe_test_client.py
```

### 🐳 Docker Commands
```bash
# Build container
docker build -t [agent-name] -f agents/[agent-name]/Dockerfile .

# Deploy to Cloud Run
gcloud builds submit --config agents/cloudbuild.yaml \
  --substitutions=_AGENT_NAME=[agent-name]
```

### 🔍 Useful Queries

**Test Database Connection:**
```sql
SELECT name 
FROM Researcher 
LIMIT 5;
```

**Find Experiments:**
```sql
Graph NeuroResearchGraph
MATCH (r:Researcher)-[:Leads]->(e:Experiment)
RETURN r.name, e.name
```

## 📍 Default Ports

| Service | Port | Access in Cloud Shell |
|---------|------|----------------------|
| Flask App | 8080 | Web Preview → Preview on port 8080 |
| MCP Server | 8001 | Internal service (localhost:8001) |
| Documentation Agent | 8002 | Internal service (localhost:8002) |
| Signal Processor | 8003 | Internal service (localhost:8003) |
| Experiment Designer | 8004 | Internal service (localhost:8004) |
| Orchestrator | 8005 | Internal service (localhost:8005) |

**Note**: Only the Flask app (port 8080) needs web preview. Other services communicate internally via localhost.

## 🎯 Agent Names

- `documentation` - Generates research reports
- `signal_processor` - Analyzes biosignals
- `experiment_designer` - Creates protocols
- `research_orchestrator` - Coordinates agents

## 🔧 Environment Variables

```bash
GOOGLE_CLOUD_PROJECT      # Your project ID
SPANNER_INSTANCE_ID       # neurohub-graph-instance
SPANNER_DATABASE_ID       # neurohub-db
GOOGLE_CLOUD_LOCATION     # us-central1
```

## ⚡ Quick Fixes

**Permission denied:**
```bash
chmod +x init.sh set_env.sh
```

**Activate virtual environment:**
```bash
source .venv/bin/activate  # UV uses .venv by default
```

**Check environment:**
```bash
echo $GOOGLE_CLOUD_PROJECT
gcloud config get-value project
```

**View logs:**
```bash
gcloud run logs read --service=[agent-name]
```

## 📱 Web Preview in Cloud Shell

1. Click **Web Preview** button (eye icon)
2. Select **Preview on port 8080**
3. Or manually change port in preview URL

## 🆘 Help Commands

```bash
gcloud --help
gcloud spanner --help
gcloud run --help
docker --help
```

---
Keep this card handy during the workshop!