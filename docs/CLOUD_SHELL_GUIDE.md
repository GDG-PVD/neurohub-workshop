# NeuroHub Workshop - Google Cloud Shell Guide

This guide is specifically for running the NeuroHub workshop entirely in Google Cloud Shell.

## Accessing the Web Application

### From Cloud Shell
When running the Flask app in Cloud Shell:

1. Start the Flask app:
   ```bash
   cd ~/neurohub-workshop/neurohub
   python app.py
   ```

2. Access via Web Preview:
   - Click the **Web Preview** button in Cloud Shell toolbar (icon: box with arrow)
   - Select **Preview on port 8080**
   - The app opens in a new tab with a URL like: `https://8080-cs-[random-string].cs-[region].cloudshell.dev`

### Important: Cloud Shell Session Management

Cloud Shell sessions timeout after 20 minutes of inactivity. To prevent this:

1. **Keep-Alive Terminal** (recommended):
   ```bash
   # Run in a separate Cloud Shell tab
   while true; do echo "Keep alive: $(date)"; sleep 300; done
   ```

2. **Persistent Storage**:
   - Your home directory (`~`) persists between sessions
   - The `/tmp` directory does NOT persist
   - Always save important files in your home directory

## Environment Setup for Cloud Shell

1. **Activation Script** (add to ~/.bashrc for persistence):
   ```bash
   echo 'alias neurohub-env="cd ~/neurohub-workshop && source .venv/bin/activate && source set_env.sh"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Quick Environment Setup**:
   ```bash
   neurohub-env  # Activates venv and sets all environment variables
   ```

## Running Services in Cloud Shell

### Terminal Management
Use multiple Cloud Shell terminal tabs:

1. **Tab 1**: Flask Web App
   ```bash
   neurohub-env && cd neurohub && python app.py
   ```

2. **Tab 2**: MCP Server
   ```bash
   neurohub-env && cd tools/neurohub && python mcp_server.py
   ```

3. **Tab 3**: Agent Server
   ```bash
   neurohub-env && cd agents/documentation && python a2a_server.py
   ```

4. **Tab 4**: Keep-Alive + General Commands
   ```bash
   while true; do echo "Keep alive: $(date)"; sleep 300; done
   ```

## Cloud-Native Development Workflow

### 1. Local Testing in Cloud Shell
- Use Web Preview for UI testing
- Services communicate via localhost within Cloud Shell

### 2. Deployment to Cloud Run
Instead of long-running processes in Cloud Shell, deploy to Cloud Run:

```bash
# Deploy Flask app
cd ~/neurohub-workshop/neurohub
gcloud run deploy neurohub-app \
  --source . \
  --region us-central1 \
  --allow-unauthenticated \
  --set-env-vars "GOOGLE_CLOUD_PROJECT=${PROJECT_ID},SPANNER_INSTANCE_ID=${SPANNER_INSTANCE_ID},SPANNER_DATABASE_ID=${SPANNER_DATABASE_ID},GOOGLE_MAPS_API_KEY=${GOOGLE_MAPS_API_KEY}"

# Deploy MCP server
cd ~/neurohub-workshop/tools/neurohub
gcloud run deploy neurohub-mcp-server \
  --source . \
  --region us-central1 \
  --no-allow-unauthenticated

# Deploy agents
cd ~/neurohub-workshop/agents/documentation
gcloud run deploy neurohub-doc-agent \
  --source . \
  --region us-central1 \
  --no-allow-unauthenticated
```

### 3. Service Communication
Once deployed to Cloud Run:
- Services get persistent URLs
- No timeout issues
- Automatic scaling
- Production-ready

## Best Practices for Cloud Shell

1. **Save Your Work Frequently**
   ```bash
   cd ~/neurohub-workshop
   git add -A
   git commit -m "Workshop progress"
   git push  # If you have a remote repo
   ```

2. **Document Your Cloud Resources**
   ```bash
   # Save your Cloud Run URLs
   echo "Flask App: $(gcloud run services describe neurohub-app --region us-central1 --format 'value(status.url)')" >> ~/workshop-urls.txt
   ```

3. **Use Cloud Shell Editor**
   - Click the **Open Editor** button for a VS Code-like experience
   - Better for editing multiple files

4. **Monitor Resources**
   ```bash
   # Check your services
   gcloud run services list --region us-central1
   
   # Check Spanner
   gcloud spanner instances list
   ```

## Troubleshooting

### Session Timeout
If your Cloud Shell session times out:
```bash
# Reactivate environment
neurohub-env

# Check running processes
ps aux | grep python

# Restart services as needed
```

### Port Conflicts
If port 8080 is already in use:
```bash
# Find process using port
lsof -i :8080

# Kill if needed
kill -9 <PID>
```

### Database Connection Issues
```bash
# Verify Spanner connection
cd ~/neurohub-workshop/neurohub
python -c "from db_neurohub import db; print('Connected!' if db else 'Failed!')"
```

## Next Steps

1. Complete local testing in Cloud Shell
2. Deploy all services to Cloud Run
3. Update service URLs in configuration
4. Test end-to-end cloud deployment

Remember: Cloud Shell is for development. Production workloads should run on Cloud Run!