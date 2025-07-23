# Workshop Agent Troubleshooting Guide

## Quick Diagnosis

If you're having trouble running the workshop agent, try these tests in order:

### 1. Simple Diagnostic Test
```bash
python simple_test.py
```
This tests basic imports and agent creation without the Runner framework.

### 2. Quick Test
```bash
python quick_test.py
```
This runs a single interaction with the agent using the full ADK Runner.

### 3. Interactive Test
```bash
python interactive_test.py
```
This starts an interactive chat session with the agent.

## Common Issues and Solutions

### "MCP tools not available"
**Symptom**: Warning message about MCP tools not being available

**Solution**: This is OK! The agent will still work for answering questions. MCP tools are only needed for database operations.

### "ModuleNotFoundError: No module named 'google.adk'"
**Symptom**: Import errors for ADK modules

**Solutions**:
1. Make sure you activated the virtual environment:
   ```bash
   cd ~/neurohub-workshop
   source .venv/bin/activate
   ```

2. Reinstall dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

### "Runner.__init__() missing required argument"
**Symptom**: TypeError when creating Runner

**Solution**: Pull the latest code - this has been fixed:
```bash
git pull origin main
```

### Authentication Errors
**Symptom**: Errors related to Google Cloud authentication

**Solutions**:
1. Re-run environment setup:
   ```bash
   source ~/neurohub-workshop/set_env.sh
   ```

2. Check your project is set:
   ```bash
   echo $GOOGLE_CLOUD_PROJECT
   ```

3. Verify authentication:
   ```bash
   gcloud auth application-default login
   ```

## Understanding the Agent Architecture

The workshop agent uses Google's ADK (Agent Development Kit):

1. **Agent**: The core intelligence (uses Gemini model)
2. **Runner**: Manages conversations and sessions
3. **Session Service**: Tracks conversation state
4. **MCP Tools**: Optional - connects to database operations

## Test Script Differences

- **simple_test.py**: Just tests agent creation (no conversation)
- **quick_test.py**: Runs one question/answer
- **interactive_test.py**: Full chat interface

## Still Having Issues?

1. Check the main workshop guide: `docs/NEUROHUB_WORKSHOP.md`
2. Ensure the MCP server is running if you need database tools
3. Try running without tools first (the agent will still answer questions)

## Environment Variables

Make sure these are set (check with `echo $VARIABLE_NAME`):
- `GOOGLE_CLOUD_PROJECT`
- `GOOGLE_GENAI_USE_VERTEXAI` (should be TRUE)
- `GOOGLE_CLOUD_LOCATION` (should be us-central1)