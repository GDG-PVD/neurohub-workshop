# NeuroHub Workshop - Complete Setup Guide for Google Cloud

This guide provides detailed, step-by-step instructions for setting up NeuroHub on Google Cloud Platform (GCP) from scratch. It's designed for workshop participants with minimal cloud experience.

## 🎯 What You'll Accomplish

By the end of this setup, you'll have:
- ✅ A fully configured Google Cloud project
- ✅ Spanner database with neurotechnology research data
- ✅ Python environment with all dependencies
- ✅ All necessary permissions and APIs enabled
- ✅ Map visualization configured
- ✅ Ready to deploy AI agents to Cloud Run

## 📋 Prerequisites

Before starting, ensure you have:
- [ ] Google account (Gmail or Google Workspace)
- [ ] Credit card for Google Cloud billing (free tier available)
- [ ] Web browser (Chrome recommended)
- [ ] Basic command-line familiarity

## 🚀 Part 1: Google Cloud Account Setup

### Step 1.1: Create Google Cloud Account

1. **Navigate to Google Cloud Console**
   - Open https://console.cloud.google.com in a new browser tab
   - Sign in with your Google account
   - Accept Terms of Service if prompted

2. **Claim Your Free Credits** (if eligible)
   - New users get $300 in free credits
   - Click the promotional banner if it appears
   - Follow the setup wizard

### Step 1.2: Create a New Project

1. **Open Project Selector**
   - Look at the top navigation bar
   - Click the dropdown next to "Google Cloud" (may show "Select a project")
   
2. **Create New Project**
   - Click **NEW PROJECT** button
   - Fill in the details:
     ```
     Project name: neurohub-workshop-[yourname]
     Organization: (leave as default)
     Location: (leave as default)
     ```
   - Click **CREATE**
   - Wait for the notification: "Created project neurohub-workshop-[yourname]"

3. **Note Your Project ID**
   - The Project ID appears under the project name
   - It looks like: `neurohub-workshop-abc123`
   - **Copy this ID** - you'll need it soon!

### Step 1.3: Enable Billing

1. **Navigate to Billing**
   - Click the hamburger menu ☰ (top-left)
   - Select **Billing**
   
2. **Link Billing Account**
   - Click **LINK A BILLING ACCOUNT**
   - If you don't have one, click **CREATE BILLING ACCOUNT**
   - Add payment information (you won't be charged during the workshop)
   - Select your billing account
   - Click **SET ACCOUNT**

## 🖥️ Part 2: Cloud Shell Setup

### Step 2.1: Activate Cloud Shell

1. **Find Cloud Shell Button**
   - Look at the top-right corner of the console
   - Find the terminal icon `>_` (Activate Cloud Shell)
   - Click it

2. **Wait for Provisioning**
   - A panel opens at the bottom
   - Wait for "Provisioning Cloud Shell..." to complete
   - You'll see a command prompt: `username@cloudshell:~ (project-id)$`

### Step 2.2: Open Cloud Shell Editor

1. **Open Editor**
   - In the Cloud Shell toolbar (dark bar at top)
   - Click **Open Editor** button 📁✏️
   - The editor opens in full screen

2. **Understand the Layout**
   - **Left**: File explorer
   - **Center**: Code editor
   - **Bottom**: Terminal

### Step 2.3: Configure Cloud Code

1. **Check Status Bar**
   - Look at the bottom of the editor
   - Find "Cloud Code - Sign in" or "Cloud Code - no project"

2. **Sign In to Cloud Code**
   - Click the status message
   - Select **Sign in**
   - Authorize in the new tab
   - Return to editor

3. **Select Your Project**
   - Click status bar again
   - Select **Select a Google Cloud Project**
   - Choose your `neurohub-workshop-[yourname]` project

## 📥 Part 3: Repository Setup

### Step 3.1: Clone the Workshop Repository

1. **Open Terminal**
   - In Cloud Shell Editor: **Terminal** → **New Terminal**
   - Or use the existing terminal at the bottom

2. **Clone Repository**
   ```bash
   git clone https://github.com/GDG-PVD/neurohub-workshop.git
   cd neurohub-workshop
   ```

3. **Make Scripts Executable**
   ```bash
   chmod +x init.sh set_env.sh
   ```

### Step 3.2: Initialize Project Configuration

1. **Run Initialization**
   ```bash
   ./init.sh
   ```

2. **Enter Your Project ID**
   - When prompted: `Please enter your Google Cloud Project ID:`
   - Paste your Project ID (from Part 1.2)
   - Press Enter

3. **Verify Success**
   - You should see: `Project ID saved to ~/project_id.txt`

## 🔧 Part 4: Enable Google Cloud APIs

### Step 4.1: Configure gcloud CLI

```bash
gcloud config set project $(cat ~/project_id.txt) --quiet
```

### Step 4.2: Enable All Required APIs

Run this single command (it's long but necessary):

```bash
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
  maps-backend.googleapis.com \
  --project=$(cat ~/project_id.txt)
```

**⏱️ This takes 2-3 minutes.** You'll see progress messages.

### Step 4.3: Verify API Enablement

```bash
gcloud services list --enabled --project=$(cat ~/project_id.txt) | grep -E "(spanner|run|aiplatform)"
```

You should see the enabled services listed.

## 🔐 Part 5: Configure Environment & Permissions

### Step 5.1: Set Environment Variables

**CRITICAL**: Use `source`, not `./` or `bash`!

```bash
source set_env.sh
```

### Step 5.2: Verify Environment

```bash
echo "Project: $GOOGLE_CLOUD_PROJECT"
echo "Spanner Instance: $SPANNER_INSTANCE_ID"
echo "Service Account: $SERVICE_ACCOUNT_NAME"
```

All should show values, not be empty.

### Step 5.3: Grant IAM Permissions

Run this complete script to grant all permissions:

```bash
# Create a script file
cat > grant_permissions.sh << 'EOF'
#!/bin/bash
set -e

echo "Granting IAM permissions to service account..."

# Define roles array
ROLES=(
  "roles/spanner.admin"
  "roles/spanner.databaseUser"
  "roles/artifactregistry.admin"
  "roles/cloudbuild.builds.editor"
  "roles/run.admin"
  "roles/iam.serviceAccountUser"
  "roles/aiplatform.user"
  "roles/logging.logWriter"
  "roles/logging.viewer"
)

# Grant each role
for role in "${ROLES[@]}"; do
  echo "Granting $role..."
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
    --role="$role" \
    --quiet
done

echo "All permissions granted successfully!"
EOF

# Make executable and run
chmod +x grant_permissions.sh
./grant_permissions.sh
```

## 🗺️ Part 6: Configure Maps API

### Step 6.1: Create API Key via Console

1. **Navigate to APIs & Services**
   - Go to: https://console.cloud.google.com/apis/credentials
   - Ensure your project is selected

2. **Create New API Key**
   - Click **+ CREATE CREDENTIALS** → **API key**
   - Copy the displayed key immediately!
   - Click **CLOSE**

### Step 6.2: Configure API Key

1. **Edit the Key**
   - Find your new key in the list
   - Click the three dots ⋮ → **Edit API key**

2. **Set Key Properties**
   - **Name**: `Maps Platform API Key` (exactly this!)
   - **Application restrictions**: None
   - **API restrictions**: 
     - Select "Restrict key"
     - Add: Maps JavaScript API
   - Click **SAVE**

### Step 6.3: Store API Key

Back in Cloud Shell:
```bash
# Replace YOUR_API_KEY with your actual key
echo "YOUR_API_KEY" > ~/mapkey.txt
```

## 📊 Part 7: Database Setup

### Step 7.1: Create Spanner Instance

```bash
gcloud spanner instances create neurohub-graph-instance \
  --config=regional-us-central1 \
  --description="GraphDB Instance for NeuroHub Workshop" \
  --processing-units=100 \
  --edition=STANDARD \
  --project=$(cat ~/project_id.txt)
```

**⏱️ This takes 1-2 minutes.**

### Step 7.2: Create Database

```bash
gcloud spanner databases create neurohub-db \
  --instance=neurohub-graph-instance \
  --database-dialect=GOOGLE_STANDARD_SQL \
  --project=$(cat ~/project_id.txt)
```

### Step 7.3: Verify Database Creation

1. **Check via CLI**
   ```bash
   gcloud spanner databases list \
     --instance=neurohub-graph-instance \
     --project=$(cat ~/project_id.txt)
   ```

2. **Check via Console**
   - Go to: https://console.cloud.google.com/spanner
   - Click `neurohub-graph-instance`
   - Verify `neurohub-db` exists

## 🐍 Part 8: Python Environment Setup

### Step 8.1: Install UV Package Manager

```bash
# Install UV (fast Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env

# Verify installation
uv --version
```

### Step 8.2: Create Virtual Environment

```bash
# Ensure you're in the project directory
cd ~/neurohub-workshop

# Create virtual environment
uv venv

# Activate it
source .venv/bin/activate
```

Your prompt should now show `(.venv)`.

### Step 8.3: Install Dependencies

```bash
# Install all Python packages (super fast with UV!)
uv pip install -r requirements.txt

# Install the common agent library
uv pip install agents/a2a_common-0.1.0-py3-none-any.whl
```

## 🗄️ Part 9: Load Sample Data

### Step 9.1: Run Database Setup

```bash
cd neurohub
python setup.py
cd ..
```

You should see output like:
```
Creating tables...
Tables created successfully!
Loading sample data...
Sample data loaded successfully!
```

### Step 9.2: Verify Data Loading

1. **Via Spanner Studio**
   - Go to: https://console.cloud.google.com/spanner
   - Navigate to: neurohub-graph-instance → neurohub-db
   - Click **Spanner Studio**
   - Run this query:
     ```sql
     Graph NeuroResearchGraph
     MATCH (r:Researcher)-[:Leads]->(e:Experiment)
     RETURN r.name, e.title
     LIMIT 5
     ```
   - Click **RUN**
   - Verify you see researcher-experiment pairs

## 🐳 Part 10: Container Registry Setup

### Step 10.1: Create Artifact Registry

```bash
gcloud artifacts repositories create neurohub-workshop \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for NeuroHub workshop" \
  --project=$(cat ~/project_id.txt)
```

### Step 10.2: Configure Docker Authentication

```bash
gcloud auth configure-docker us-central1-docker.pkg.dev \
  --project=$(cat ~/project_id.txt)
```

## ✅ Part 11: Final Verification

### Step 11.1: Run Verification Script

Create and run a verification script:

```bash
cat > verify_setup.sh << 'EOF'
#!/bin/bash
echo "=== NeuroHub Workshop Setup Verification ==="
echo

# Check environment variables
echo "1. Environment Variables:"
echo "   Project ID: ${GOOGLE_CLOUD_PROJECT:-NOT SET}"
echo "   Spanner Instance: ${SPANNER_INSTANCE_ID:-NOT SET}"
echo "   Service Account: ${SERVICE_ACCOUNT_NAME:-NOT SET}"
echo

# Check Python environment
echo "2. Python Environment:"
echo "   Python: $(which python)"
echo "   Virtual Env: ${VIRTUAL_ENV:-NOT ACTIVATED}"
echo

# Check key files
echo "3. Configuration Files:"
echo "   Project ID file: $([ -f ~/project_id.txt ] && echo "✓ Found" || echo "✗ Missing")"
echo "   Map key file: $([ -f ~/mapkey.txt ] && echo "✓ Found" || echo "✗ Missing")"
echo

# Check APIs
echo "4. Enabled APIs:"
gcloud services list --enabled --project=$(cat ~/project_id.txt) 2>/dev/null | \
  grep -E "(spanner|run|aiplatform)" | \
  awk '{print "   ✓", $1}'
echo

# Check Spanner
echo "5. Spanner Database:"
gcloud spanner databases list \
  --instance=neurohub-graph-instance \
  --project=$(cat ~/project_id.txt) 2>/dev/null | \
  grep neurohub-db && echo "   ✓ Database exists" || echo "   ✗ Database missing"
echo

echo "=== Verification Complete ==="
EOF

chmod +x verify_setup.sh
./verify_setup.sh
```

### Step 11.2: Test Application Locally

1. **Terminal 1: Start Flask App**
   ```bash
   cd neurohub
   python app.py
   ```

2. **Terminal 2: Preview Application**
   - Click **Web Preview** → **Preview on port 8080**
   - You should see the NeuroHub interface!

## 🎉 Setup Complete!

You're now ready to start the workshop modules! Your environment includes:
- ✅ Google Cloud project configured
- ✅ All APIs enabled
- ✅ Spanner database with sample data
- ✅ Python environment ready
- ✅ Container registry for deployments
- ✅ Maps API for visualizations

## 🆘 Quick Troubleshooting

### "Permission denied" errors
```bash
chmod +x *.sh
```

### "Project not set" errors
```bash
source set_env.sh  # Remember: source, not ./
```

### Virtual environment not activated
```bash
source .venv/bin/activate
```

### Database connection errors
- Verify environment variables are set
- Check Spanner instance name matches exactly
- Ensure you're in the virtual environment

### Port already in use
```bash
lsof -i :8080  # Find what's using port 8080
kill -9 <PID>  # Kill the process
```

## 📚 Next Steps

1. Keep this terminal/browser setup open
2. Proceed to the [Workshop Guide](WORKSHOP_GUIDE.md)
3. Start with Module 1: Understanding the Base Application

---
*NeuroHub Workshop Setup Guide v2.0 | Questions? Ask your instructor!*