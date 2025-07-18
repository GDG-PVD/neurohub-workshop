# NeuroHub Workshop Troubleshooting Guide

This guide helps you resolve common issues during the workshop.

## 🔴 Critical Issues (Workshop Blockers)

### "Permission denied" when running scripts

**Symptom:**
```
bash: ./init.sh: Permission denied
```

**Solution:**
```bash
chmod +x init.sh set_env.sh
```

### Project ID not set

**Symptom:**
```
ERROR: (gcloud.spanner.instances.create) The required property [project] is not currently set.
```

**Solutions:**
1. Run `source set_env.sh` (not `./set_env.sh`)
2. Manually set: `gcloud config set project YOUR-PROJECT-ID`
3. Verify: `echo $GOOGLE_CLOUD_PROJECT`

### Virtual environment not activated

**Symptom:**
```
ModuleNotFoundError: No module named 'google'
```

**Solution:**
```bash
source .venv/bin/activate
# Your prompt should show (.venv)
uv pip install -r requirements.txt
```

## 🟡 Database Issues

### Spanner instance not found

**Symptom:**
```
Instance not found: neurohub-graph-instance
```

**Solutions:**
1. Check instance name:
   ```bash
   gcloud spanner instances list
   ```
2. Create if missing:
   ```bash
   gcloud spanner instances create neurohub-graph-instance \
     --config=regional-us-central1 --processing-units=100
   ```

### Database not found

**Symptom:**
```
Database not found: neurohub-db
```

**Solution:**
```bash
gcloud spanner databases create neurohub-db \
  --instance=neurohub-graph-instance
```

### Tables not found

**Symptom:**
```
Table 'Researcher' not found
```

**Solution:**
```bash
cd neurohub
python setup.py
```

### Graph queries return empty

**Symptom:**
Graph queries work but return no results

**Solution:**
The setup.py script may have failed. Re-run:
```bash
cd neurohub
python setup.py
```

## 🟡 Agent Connection Issues

### MCP server connection refused

**Symptom:**
```
ConnectionRefusedError: [Errno 111] Connection refused
```

**Solutions:**
1. Start MCP server in separate terminal:
   ```bash
   cd tools/neurohub
   python mcp_server.py
   ```
2. Check it's running on port 8001:
   ```bash
   lsof -i :8001
   ```

### Agent not responding

**Symptom:**
Agent starts but doesn't respond to requests

**Solutions:**
1. Check agent is running:
   ```bash
   ps aux | grep a2a_server.py
   ```
2. Check correct port is used
3. Restart agent server
4. Check logs for errors

### Import error for a2a_common

**Symptom:**
```
ModuleNotFoundError: No module named 'a2a_common'
```

**Solution:**
```bash
uv pip install agents/a2a_common-0.1.0-py3-none-any.whl
```

## 🟡 Web Application Issues

### Flask app won't start

**Symptom:**
```
Address already in use
```

**Solutions:**
1. Kill existing process:
   ```bash
   lsof -i :8080
   kill -9 [PID]
   ```
2. Or use different port:
   ```bash
   export APP_PORT=8081
   python app.py
   ```

### Map not displaying

**Symptom:**
Google Maps shows error or doesn't load

**Solutions:**
1. Check API key exists:
   ```bash
   cat ~/mapkey.txt
   ```
2. Verify key name is exactly "Maps Platform API Key"
3. Check Maps JavaScript API is enabled
4. Re-run key retrieval script

### Web preview not working in Cloud Shell

**Solutions:**
1. Use the Web Preview button (eye icon)
2. Select "Preview on port 8080"
3. Or manually change port in URL
4. Ensure app is running first

## 🟡 Docker/Deployment Issues

### Docker build fails

**Symptom:**
```
ERROR: failed to solve: failed to read dockerfile
```

**Solution:**
Build from repository root:
```bash
cd ~/neurohub-workshop  # Go to root
docker build -t [agent] -f agents/[agent]/Dockerfile .
```

### Artifact Registry not found

**Symptom:**
```
Artifact Registry repository does not exist
```

**Solution:**
```bash
gcloud artifacts repositories create neurohub-workshop \
  --repository-format=docker --location=us-central1
```

### Cloud Build fails

**Solutions:**
1. Check you're authenticated:
   ```bash
   gcloud auth list
   ```
2. Enable required APIs:
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   ```
3. Check substitutions are correct

## 🟡 Environment Issues

### Environment variables not set

**Symptom:**
Commands fail with "variable not set" errors

**Solution:**
In EVERY new terminal:
```bash
cd ~/neurohub-workshop
source .venv/bin/activate
source set_env.sh
```

### Wrong Python version

**Symptom:**
Syntax errors or compatibility issues

**Solution:**
```bash
python --version  # Should be 3.8+
# UV handles Python version automatically
uv venv --python 3.11  # Specify version if needed
```

### API not enabled errors

**Symptom:**
```
API [service.googleapis.com] not enabled on project
```

**Solution:**
Re-run the complete API enable command:
```bash
gcloud services enable run.googleapis.com cloudfunctions.googleapis.com \
  cloudbuild.googleapis.com artifactregistry.googleapis.com spanner.googleapis.com \
  apikeys.googleapis.com iam.googleapis.com compute.googleapis.com \
  aiplatform.googleapis.com cloudresourcemanager.googleapis.com maps-backend.googleapis.com
```

## 🔵 Common Warning Messages (Usually Safe to Ignore)

### "InstaVibe" references
Some files still contain "instavibe" in names or configurations. These work fine for the workshop.

### Deprecation warnings
Python package warnings about future versions can be ignored.

### Cloud Shell disconnect
Cloud Shell may disconnect after inactivity. Just reconnect and re-run:
```bash
source .venv/bin/activate
source set_env.sh
```

## 🆘 Getting Help

1. **Check logs:**
   ```bash
   # For web app
   Check terminal output
   
   # For deployed services
   gcloud run logs read --service=[service-name]
   ```

2. **Verify setup:**
   ```bash
   # Run verification commands from setup checklist
   gcloud config get-value project
   env | grep GOOGLE
   ```

3. **Ask for help:**
   - Share the exact error message
   - Mention which module/step you're on
   - Include output of verification commands

## 💡 Pro Tips

1. **Always work from repo root** for Docker builds
2. **Source scripts, don't execute** (set_env.sh)
3. **Keep terminals organized** - label each by service
4. **Check ports aren't in use** before starting services
5. **Restart from scratch** if too many issues:
   ```bash
   cd ~
   rm -rf neurohub-workshop
   # Start over from git clone
   ```

---
Remember: Most issues are environment-related. When in doubt, check your environment variables and virtual environment activation!