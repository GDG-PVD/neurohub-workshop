# NeuroHub Workshop - Comprehensive Troubleshooting Guide

This guide covers common issues encountered during the NeuroHub workshop and provides detailed solutions. Issues are organized by workshop phase for easy reference.

## 🔍 Quick Diagnostic Commands

Before troubleshooting, run these commands to gather system information:

```bash
# Create diagnostic script
cat > diagnose.sh << 'EOF'
#!/bin/bash
echo "=== NeuroHub Workshop Diagnostics ==="
echo "Date: $(date)"
echo "User: $(whoami)"
echo "PWD: $(pwd)"
echo "Project: $(gcloud config get-value project 2>/dev/null || echo 'NOT SET')"
echo "Python: $(which python || echo 'NOT FOUND')"
echo "Virtual Env: ${VIRTUAL_ENV:-'NOT ACTIVATED'}"
echo "UV: $(which uv || echo 'NOT INSTALLED')"
echo
echo "Environment Variables:"
echo "  GOOGLE_CLOUD_PROJECT: ${GOOGLE_CLOUD_PROJECT:-'NOT SET'}"
echo "  SPANNER_INSTANCE_ID: ${SPANNER_INSTANCE_ID:-'NOT SET'}"
echo "  SERVICE_ACCOUNT_NAME: ${SERVICE_ACCOUNT_NAME:-'NOT SET'}"
echo
echo "Key Files:"
echo "  ~/project_id.txt: $([ -f ~/project_id.txt ] && echo 'EXISTS' || echo 'MISSING')"
echo "  ~/mapkey.txt: $([ -f ~/mapkey.txt ] && echo 'EXISTS' || echo 'MISSING')"
echo "  .env: $([ -f .env ] && echo 'EXISTS' || echo 'MISSING')"
echo "==================================="
EOF

chmod +x diagnose.sh
./diagnose.sh
```

## 📋 Table of Contents

1. [Initial Setup Issues](#initial-setup-issues)
2. [Environment Configuration Issues](#environment-configuration-issues)
3. [API and Permission Issues](#api-and-permission-issues)
4. [Database Issues](#database-issues)
5. [Python Environment Issues](#python-environment-issues)
6. [Application Runtime Issues](#application-runtime-issues)
7. [Agent Development Issues](#agent-development-issues)
8. [Docker and Deployment Issues](#docker-and-deployment-issues)
9. [Cloud Run Issues](#cloud-run-issues)
10. [Network and Connectivity Issues](#network-and-connectivity-issues)

---

## 🚀 Initial Setup Issues

### Issue: "Permission denied" when running scripts

**Symptoms:**
```
bash: ./init.sh: Permission denied
```

**Solution:**
```bash
# Make all scripts executable
chmod +x *.sh

# Verify permissions
ls -la *.sh
```

### Issue: Cloud Shell session expired

**Symptoms:**
- "Your Cloud Shell session has expired"
- Lost terminal history
- Environment variables reset

**Solution:**
```bash
# Re-navigate to project directory
cd ~/neurohub-workshop

# Re-source environment
source set_env.sh

# Re-activate Python environment
source .venv/bin/activate
```

### Issue: "Project not set" errors

**Symptoms:**
```
ERROR: (gcloud.spanner.instances.create) The required property [project] is not currently set.
```

**Solutions:**

1. **Check if project_id.txt exists:**
```bash
# Check file
cat ~/project_id.txt

# If missing, create it
echo "YOUR-PROJECT-ID" > ~/project_id.txt
```

2. **Set gcloud project:**
```bash
gcloud config set project $(cat ~/project_id.txt)
```

3. **Source environment variables:**
```bash
source set_env.sh  # MUST use 'source', not './'
```

---

## 🔧 Environment Configuration Issues

### Issue: Environment variables not set

**Symptoms:**
- Commands fail with "variable not set"
- `echo $GOOGLE_CLOUD_PROJECT` returns empty

**Solution:**
```bash
# Always use source command
source set_env.sh

# Verify all variables
env | grep -E "(GOOGLE_CLOUD|SPANNER|SERVICE_ACCOUNT)"

# If still missing, set manually
export GOOGLE_CLOUD_PROJECT=$(cat ~/project_id.txt)
export SPANNER_INSTANCE_ID="neurohub-graph-instance"
export SPANNER_DATABASE_ID="neurohub-db"
export PROJECT_NUMBER=$(gcloud projects describe $GOOGLE_CLOUD_PROJECT --format="value(projectNumber)")
export SERVICE_ACCOUNT_NAME="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"
```

### Issue: Wrong project selected

**Symptoms:**
- Resources created in wrong project
- "Resource not found" errors

**Solution:**
```bash
# List all projects
gcloud projects list

# Switch to correct project
gcloud config set project YOUR-CORRECT-PROJECT-ID

# Update project_id.txt
echo "YOUR-CORRECT-PROJECT-ID" > ~/project_id.txt

# Re-source environment
source set_env.sh
```

---

## 🔐 API and Permission Issues

### Issue: API not enabled errors

**Symptoms:**
```
API [spanner.googleapis.com] not enabled on project
```

**Solution:**
```bash
# Enable missing API
gcloud services enable spanner.googleapis.com

# Enable all required APIs at once
gcloud services enable \
  run.googleapis.com \
  cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com \
  artifactregistry.googleapis.com \
  spanner.googleapis.com \
  apikeys.googleapis.com \
  iam.googleapis.com \
  compute.googleapis.com \
  aiplatform.googleapis.com \
  cloudresourcemanager.googleapis.com \
  maps-backend.googleapis.com

# Verify APIs are enabled
gcloud services list --enabled | grep -E "(spanner|run|aiplatform)"
```

### Issue: IAM permission denied

**Symptoms:**
```
Error 403: The caller does not have permission
```

**Solutions:**

1. **Check current user permissions:**
```bash
# Get current user
gcloud auth list

# Check project IAM policy
gcloud projects get-iam-policy $(cat ~/project_id.txt)
```

2. **Grant missing permissions:**
```bash
# For your user account
gcloud projects add-iam-policy-binding $(cat ~/project_id.txt) \
  --member="user:YOUR-EMAIL@gmail.com" \
  --role="roles/owner"

# For service account
./grant_permissions.sh  # Run the script from setup
```

### Issue: Billing not enabled

**Symptoms:**
```
Billing must be enabled for activation of service
```

**Solution:**
1. Go to https://console.cloud.google.com/billing
2. Link a billing account to your project
3. Retry the failed operation

---

## 💾 Database Issues

### Issue: Spanner instance creation fails

**Symptoms:**
```
Error creating instance: googleapi: Error 409: Instance already exists
```

**Solutions:**

1. **Check if instance exists:**
```bash
gcloud spanner instances list
```

2. **Delete and recreate:**
```bash
# Delete existing
gcloud spanner instances delete neurohub-graph-instance --quiet

# Recreate
gcloud spanner instances create neurohub-graph-instance \
  --config=regional-us-central1 \
  --processing-units=100 \
  --edition=STANDARD
```

### Issue: Database connection errors

**Symptoms:**
```
google.api_core.exceptions.NotFound: 404 Database not found
```

**Solutions:**

1. **Verify database exists:**
```bash
gcloud spanner databases list --instance=neurohub-graph-instance
```

2. **Create if missing:**
```bash
gcloud spanner databases create neurohub-db \
  --instance=neurohub-graph-instance
```

3. **Check environment variables:**
```bash
echo $SPANNER_INSTANCE_ID  # Should be: neurohub-graph-instance
echo $SPANNER_DATABASE_ID  # Should be: neurohub-db
```

### Issue: Graph queries fail

**Symptoms:**
- "Invalid graph query" errors
- Empty results from MATCH queries

**Solutions:**

1. **Verify graph is created:**
```sql
-- In Spanner Studio
SHOW PROPERTY GRAPHS;
```

2. **Recreate graph if needed:**
```bash
cd ~/neurohub-workshop/neurohub
python setup.py
```

---

## 🐍 Python Environment Issues

### Issue: UV not found

**Symptoms:**
```
bash: uv: command not found
```

**Solution:**
```bash
# Reinstall UV
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Add to PATH permanently
echo 'source $HOME/.cargo/env' >> ~/.bashrc
```

### Issue: Virtual environment not activated

**Symptoms:**
- `which python` shows system Python
- Package imports fail

**Solution:**
```bash
# Navigate to project
cd ~/neurohub-workshop

# Activate virtual environment
source .venv/bin/activate  # Note: .venv, not env

# Verify activation
which python  # Should show .venv/bin/python
```

### Issue: Package installation fails

**Symptoms:**
```
ERROR: Could not find a version that satisfies the requirement
```

**Solutions:**

1. **Use UV instead of pip:**
```bash
uv pip install -r requirements.txt
```

2. **Clear UV cache:**
```bash
uv cache clean
uv pip install -r requirements.txt --force-reinstall
```

3. **Check Python version:**
```bash
python --version  # Should be 3.11 or higher
```

### Issue: Module import errors

**Symptoms:**
```
ModuleNotFoundError: No module named 'google.cloud.spanner'
```

**Solution:**
```bash
# Ensure virtual environment is activated
source .venv/bin/activate

# Reinstall requirements
uv pip install -r requirements.txt

# Install agent common library
uv pip install agents/a2a_common-0.1.0-py3-none-any.whl
```

---

## 🌐 Application Runtime Issues

### Issue: Port 8080 already in use

**Symptoms:**
```
[Errno 48] Address already in use
```

**Solutions:**

1. **Find and kill process:**
```bash
# Find process using port
lsof -i :8080

# Kill the process
kill -9 <PID>
```

2. **Use different port:**
```bash
# Set different port
export APP_PORT=8081

# Run app
cd neurohub && python app.py
```

### Issue: Flask app crashes immediately

**Symptoms:**
- App starts then exits
- "KeyError" in logs

**Solution:**
```bash
# Check all required environment variables
source ~/neurohub-workshop/set_env.sh

# Create .env file if missing
cd ~/neurohub-workshop/neurohub
cat > .env << EOF
GOOGLE_CLOUD_PROJECT=$(cat ~/project_id.txt)
SPANNER_INSTANCE_ID=neurohub-graph-instance
SPANNER_DATABASE_ID=neurohub-db
GOOGLE_MAPS_API_KEY=$(cat ~/mapkey.txt)
FLASK_SECRET_KEY=your-secret-key-here
EOF

# Restart app
python app.py
```

### Issue: MCP server connection fails

**Symptoms:**
```
Failed to connect to MCP server at localhost:8001
```

**Solutions:**

1. **Start MCP server:**
```bash
# In new terminal
cd ~/neurohub-workshop
source .venv/bin/activate
source set_env.sh
cd tools/neurohub
python mcp_server.py
```

2. **Check MCP server logs:**
```bash
# Look for errors in MCP terminal
# Common: missing environment variables
```

---

## 🤖 Agent Development Issues

### Issue: Agent fails to start

**Symptoms:**
```
AttributeError: 'NoneType' object has no attribute 'create_agent'
```

**Solution:**
```bash
# Install agent dependencies
cd ~/neurohub-workshop
uv pip install agents/a2a_common-0.1.0-py3-none-any.whl

# Set required environment variables
export GOOGLE_GENAI_API_KEY="your-api-key"  # If using Gemini
export GOOGLE_GENAI_USE_VERTEXAI=TRUE       # For Vertex AI
```

### Issue: A2A server connection errors

**Symptoms:**
```
Connection refused: localhost:8002
```

**Solutions:**

1. **Check if A2A server is running:**
```bash
ps aux | grep a2a_server
```

2. **Start A2A server:**
```bash
cd agents/documentation
python a2a_server.py
```

3. **Check port conflicts:**
```bash
# Each agent needs unique port
# documentation: 8002
# signal_processor: 8003
# experiment_designer: 8004
# research_orchestrator: 8005
```

### Issue: Agent can't access tools

**Symptoms:**
- "Tool not found" errors
- Agent can't create experiments

**Solution:**
```bash
# Ensure MCP server is running
cd tools/neurohub && python mcp_server.py

# Check MCP_SERVER_URL environment variable
export MCP_SERVER_URL="http://localhost:8001"
```

---

## 🐳 Docker and Deployment Issues

### Issue: Docker build fails

**Symptoms:**
```
error: failed to solve: failed to read dockerfile
```

**Solutions:**

1. **Build from repository root:**
```bash
# MUST be in repository root
cd ~/neurohub-workshop

# Build with correct path
docker build -t documentation -f agents/documentation/Dockerfile .
```

2. **Check Docker daemon:**
```bash
# Verify Docker is available in Cloud Shell
docker version
```

### Issue: Artifact Registry not found

**Symptoms:**
```
Failed to push image: Repository does not exist
```

**Solution:**
```bash
# Create repository
gcloud artifacts repositories create neurohub-workshop \
  --repository-format=docker \
  --location=us-central1

# Configure Docker auth
gcloud auth configure-docker us-central1-docker.pkg.dev
```

### Issue: Cloud Build fails

**Symptoms:**
- Build succeeds but deployment fails
- "Invalid image" errors

**Solutions:**

1. **Check cloudbuild.yaml:**
```bash
# Verify substitutions
cat agents/cloudbuild.yaml
```

2. **Run with correct substitutions:**
```bash
gcloud builds submit --config agents/cloudbuild.yaml \
  --substitutions=_AGENT_NAME=documentation,_LOCATION=us-central1
```

---

## ☁️ Cloud Run Issues

### Issue: Service deployment fails

**Symptoms:**
```
Deployment failed: User does not have permission
```

**Solution:**
```bash
# Grant Cloud Run permissions
gcloud projects add-iam-policy-binding $(cat ~/project_id.txt) \
  --member="serviceAccount:${SERVICE_ACCOUNT_NAME}" \
  --role="roles/run.admin"

# Enable Cloud Run API
gcloud services enable run.googleapis.com
```

### Issue: Service returns 503 errors

**Symptoms:**
- Service deploys but returns errors
- "Service Unavailable"

**Solutions:**

1. **Check service logs:**
```bash
gcloud run logs read --service=neurohub --region=us-central1
```

2. **Common fixes:**
```bash
# Increase memory
gcloud run services update neurohub \
  --memory=1Gi \
  --region=us-central1

# Set environment variables
gcloud run services update neurohub \
  --set-env-vars="GOOGLE_CLOUD_PROJECT=$(cat ~/project_id.txt)" \
  --region=us-central1
```

---

## 🌐 Network and Connectivity Issues

### Issue: Web Preview not working

**Symptoms:**
- "Unable to connect" in preview
- Blank page

**Solutions:**

1. **Check if app is running:**
```bash
ps aux | grep "python app.py"
```

2. **Try different preview method:**
   - Click "Web Preview" button
   - Select "Change port"
   - Enter 8080
   - Click "Change and Preview"

3. **Use manual URL:**
```bash
# Get preview URL
echo "https://8080-${CLOUDSHELL_WEB_HOST}"
```

### Issue: Maps not displaying

**Symptoms:**
- Gray box where map should be
- Console errors about API key

**Solutions:**

1. **Verify API key:**
```bash
cat ~/mapkey.txt
```

2. **Check key restrictions:**
   - Go to https://console.cloud.google.com/apis/credentials
   - Edit key settings
   - Ensure Maps JavaScript API is enabled

3. **Update environment:**
```bash
export GOOGLE_MAPS_API_KEY=$(cat ~/mapkey.txt)
source set_env.sh
```

---

## 🔄 Quick Recovery Scripts

### Full Environment Reset

```bash
cat > reset_environment.sh << 'EOF'
#!/bin/bash
echo "Resetting NeuroHub environment..."

# Kill all Python processes
pkill -f python

# Reset directory
cd ~/neurohub-workshop

# Source environment
source set_env.sh

# Activate Python environment
source .venv/bin/activate

# Verify setup
echo "Environment reset complete!"
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Python: $(which python)"
EOF

chmod +x reset_environment.sh
./reset_environment.sh
```

### Service Restart Script

```bash
cat > restart_services.sh << 'EOF'
#!/bin/bash
# Kill existing services
pkill -f "python app.py"
pkill -f "python mcp_server.py"
pkill -f "python a2a_server.py"

# Start services in background
cd ~/neurohub-workshop/neurohub && python app.py &
cd ~/neurohub-workshop/tools/neurohub && python mcp_server.py &
cd ~/neurohub-workshop/agents/documentation && python a2a_server.py &

echo "Services restarted!"
EOF

chmod +x restart_services.sh
```

---

## 📞 Getting Help

If you're still stuck:

1. **Run diagnostics:**
   ```bash
   ./diagnose.sh > diagnostics.txt
   ```

2. **Check logs:**
   - Application logs: Look at terminal output
   - Cloud logs: `gcloud logging read`

3. **Ask for help:**
   - Share your `diagnostics.txt` with instructors
   - Include the exact error message
   - Describe what you were trying to do

---
*NeuroHub Workshop Troubleshooting Guide v1.0 | Don't hesitate to ask for help!*