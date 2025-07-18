# NeuroHub Workshop Setup Checklist

Use this checklist to ensure you've completed all setup steps correctly.

## Pre-Workshop Requirements

- [ ] Google Cloud account created
- [ ] Billing enabled on Google Cloud account
- [ ] Chrome browser installed (recommended)
- [ ] Stable internet connection

## Part 1: Cloud Shell Setup

- [ ] Opened Google Cloud Console
- [ ] Activated Cloud Shell
- [ ] Opened Cloud Shell Editor
- [ ] Logged into Cloud Code plugin
- [ ] Selected correct Google Cloud Project

## Part 2: Repository Setup

- [ ] Cloned neurohub-workshop repository
- [ ] Changed to neurohub-workshop directory
- [ ] Made scripts executable (`chmod +x`)
- [ ] Ran `bash init.sh`
- [ ] Entered Project ID when prompted
- [ ] File `~/project_id.txt` created

## Part 3: Environment Configuration

- [ ] Ran `source set_env.sh` (used `source`, not `./`)
- [ ] Verified environment variables are set:
  ```bash
  echo $GOOGLE_CLOUD_PROJECT
  echo $SPANNER_INSTANCE_ID
  echo $SPANNER_DATABASE_ID
  ```

## Part 4: Enable Google Cloud APIs

- [ ] Ran the `gcloud services enable` command
- [ ] Waited for completion (2-3 minutes)
- [ ] No error messages displayed

## Part 5: Set IAM Permissions

- [ ] Granted all required IAM roles to service account
- [ ] Verified in IAM Console that roles are assigned

## Part 6: Create Maps API Key

- [ ] Created API key in Google Cloud Console
- [ ] Named it exactly: "Maps Platform API Key"
- [ ] Restricted to Maps JavaScript API
- [ ] Saved API key value
- [ ] File `~/mapkey.txt` created

## Part 7: Create Artifact Registry

- [ ] Created repository named "neurohub-workshop"
- [ ] Set format as Docker
- [ ] Set location as us-central1

## Part 8: Database Setup

### Spanner Instance
- [ ] Created instance: `neurohub-graph-instance`
- [ ] Set configuration: regional-us-central1
- [ ] Set processing units: 100
- [ ] Instance creation completed

### Database Creation
- [ ] Created database: `neurohub-db`
- [ ] Database uses GOOGLE_STANDARD_SQL dialect

### Python Environment
- [ ] Installed UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] Sourced cargo env: `source $HOME/.cargo/env`
- [ ] Created virtual environment: `uv venv`
- [ ] Activated environment: `source .venv/bin/activate`
- [ ] Installed requirements: `uv pip install -r requirements.txt`
- [ ] No installation errors

### Load Sample Data
- [ ] Changed to neurohub directory
- [ ] Ran `python setup.py`
- [ ] Script completed without errors
- [ ] Tables and graph created

### Verify Database
- [ ] Opened Spanner Console
- [ ] Found neurohub-graph-instance
- [ ] Found neurohub-db
- [ ] Opened Spanner Studio
- [ ] Test query returned results

## Part 9: Test Base Application

- [ ] Started Flask app (Terminal 1)
- [ ] Started MCP server (Terminal 2)
- [ ] No error messages in either terminal
- [ ] Accessed http://localhost:8080
- [ ] Home page loads correctly
- [ ] Can view researcher profiles
- [ ] Can view experiment details

## Part 10: Agent Setup

- [ ] Installed a2a_common wheel:
  ```bash
  uv pip install agents/a2a_common-0.1.0-py3-none-any.whl
  ```
- [ ] Tested documentation agent:
  ```bash
  cd agents/documentation
  python instavibe_test_client.py
  ```
- [ ] Agent responded correctly

## Verification Commands

Run these to verify your setup:

```bash
# Check project
gcloud config get-value project

# Check Python environment
which python
python --version

# Check environment variables
env | grep GOOGLE
env | grep SPANNER

# Check services are enabled
gcloud services list --enabled | grep -E "(spanner|run|aiplatform)"

# Check Spanner instance
gcloud spanner instances list

# Check artifact registry
gcloud artifacts repositories list
```

## Ready to Start?

If all items are checked, you're ready for the workshop! 🎉

If you're missing any checkmarks:
1. Go back to that section in the setup guide
2. Complete the missing steps
3. Ask for help if needed

## Common Issues

**Missing ~/project_id.txt or ~/mapkey.txt:**
- These files should be in your home directory, not the project directory
- Run `ls ~/*.txt` to check

**Environment variables not set:**
- Make sure you used `source set_env.sh` not `./set_env.sh`
- Run the command again if needed

**Import errors when running Python scripts:**
- Ensure virtual environment is activated
- Check prompt shows `(.venv)`
- Re-run `uv pip install -r requirements.txt`

---
✅ Complete this checklist before starting the workshop modules!