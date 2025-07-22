# NeuroHub Workshop - Detailed Setup Guide

This guide provides step-by-step instructions with specific navigation details for setting up your NeuroHub workshop environment.

## Before You Begin

### Prerequisites
- Google account (Gmail or Google Workspace)
- Credit card for Google Cloud billing (you won't be charged during the workshop)
- Chrome browser (recommended for best compatibility)

### Create Google Cloud Account

1. Navigate to https://console.cloud.google.com
2. Sign in with your Google account
3. If prompted, agree to the Terms of Service
4. You'll see the Google Cloud Console dashboard

### Create a New Project

1. Click the project dropdown at the top of the page (might show "Select a project")
2. Click **NEW PROJECT** in the dialog that appears
3. Enter project details:
   - **Project name**: `neurohub-workshop`
   - **Organization**: Leave as is
   - **Location**: Leave as is
4. Click **CREATE**
5. Wait for the notification that says "Created project neurohub-workshop"

### Enable Billing

1. In the left sidebar, navigate to **Billing** (you may need to click the hamburger menu ☰ first)
2. Click **LINK A BILLING ACCOUNT**
3. Select **CREATE BILLING ACCOUNT**
4. Follow the prompts to add your payment information
5. After setup, return to your project

## Part 1: Access Cloud Shell

### Open Cloud Shell

1. Look at the top-right corner of the Google Cloud Console
2. Find the terminal icon (looks like `>_`) - this is the **Activate Cloud Shell** button
3. Click it to open Cloud Shell at the bottom of your browser window
4. You'll see a message "Provisioning Cloud Shell" - wait for it to complete
5. When ready, you'll see a command prompt like: `username@cloudshell:~ (project-id)$`

### Open Cloud Shell Editor

1. In the Cloud Shell toolbar (the dark bar at the top of Cloud Shell), look for the **Open Editor** button
2. It looks like a folder with a pencil icon: 📁✏️
3. Click **Open Editor**
4. The Cloud Shell Editor will open in the full window
5. You'll see:
   - File explorer on the left
   - Editor in the center
   - Terminal at the bottom

### Configure Cloud Code

1. Look at the bottom status bar of the editor
2. Find where it says **Cloud Code - Sign in** or **Cloud Code - no project**
3. Click on it
4. Select **Sign in** if prompted
5. A browser tab will open - authorize Cloud Code
6. Return to the editor
7. Click the status bar again and select **Select a Google Cloud Project**
8. Choose your `neurohub-workshop` project from the list

## Part 2: Find Your Project ID

Your Project ID is different from your Project Name. Here's how to find it:

1. Go back to the Google Cloud Console tab
2. Look at the project dropdown at the top of the page
3. Click on it - you'll see your project listed with:
   - **Name**: neurohub-workshop
   - **ID**: Something like `neurohub-workshop-xyz123`
4. Copy the Project ID - you'll need it soon

Alternative method:
1. From the Console home page, look for the **Project info** card
2. Your Project ID is listed there
3. Click the copy button next to it

## Part 3: Initial Repository Setup

### Open Terminal in Cloud Shell Editor

1. In the Cloud Shell Editor, click **Terminal** in the menu bar
2. Select **New Terminal**
3. A terminal will open at the bottom of the editor

### Verify Authentication

Run this command to check you're authenticated:
```bash
gcloud auth list
```

You should see:
```
Credentialed Accounts
ACTIVE  ACCOUNT
*       your-email@gmail.com
```

### Clone the Repository

```bash
git clone https://github.com/GDG-PVD/neurohub-workshop.git
```

You'll see:
```
Cloning into 'neurohub-workshop'...
remote: Enumerating objects: ...
Receiving objects: 100% ...
```

### Make Scripts Executable

```bash
cd neurohub-workshop
chmod +x init.sh set_env.sh
```

### Run Initialization Script

```bash
./init.sh
```

The script will prompt:
```
Please enter your Google Cloud Project ID:
```

Enter your Project ID (the one you copied earlier) and press Enter.

You should see:
```
Project ID saved to ~/project_id.txt
Initialization complete!
```

## ![Screenshot 2025-07-22 at 3.09.26 PM](/Users/stephenszermer/Library/Application Support/typora-user-images/Screenshot 2025-07-22 at 3.09.26 PM.png)

## Part 4: Enable Google Cloud APIs

### Set Project Configuration

```bash
gcloud config set project $(cat ~/project_id.txt) --quiet
```

### Enable Required APIs

This command enables all the Google Cloud services we'll use:

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
  maps-backend.googleapis.com
```

You'll see progress messages like:
```
Operation "operations/acf.p2-123456789" finished successfully.
```

This takes 2-3 minutes. Wait for it to complete.

## Part 5: Set Environment Variables

### Important: Use 'source' Command

```bash
source set_env.sh
```

**Critical**: You MUST use `source`, not `./` or `bash`. This ensures variables are set in your current shell.

The script will output several environment variables being set.

### Verify Environment

```bash
echo $GOOGLE_CLOUD_PROJECT
echo $SPANNER_INSTANCE_ID
```

Both commands should return values (not empty).

## Part 6: Configure IAM Permissions

### Understanding Service Accounts

Google Cloud uses service accounts for applications to access resources. We need to grant permissions to the default compute service account.

### Grant All Required Permissions

Run this complete command (it's long but necessary):

```bash
# Spanner Admin
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
  --role="roles/spanner.admin"

# Spanner Database User
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
  --role="roles/spanner.databaseUser"

# Artifact Registry Admin
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
  --role="roles/artifactregistry.admin"

# Cloud Build Editor
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
  --role="roles/cloudbuild.builds.editor"

# Cloud Run Admin
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
  --role="roles/run.admin"

# IAM Service Account User
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
  --role="roles/iam.serviceAccountUser"

# Vertex AI User
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
  --role="roles/aiplatform.user"

# Logging Writer
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
  --role="roles/logging.logWriter"

# Logging Viewer
gcloud projects add-iam-policy-binding $PROJECT_ID \
  --member="serviceAccount:$SERVICE_ACCOUNT_NAME" \
  --role="roles/logging.viewer"
```

Each command will output a policy update confirmation.

### Verify IAM Permissions

1. Open a new browser tab
2. Go to https://console.cloud.google.com/iam-admin/iam
3. Make sure your project is selected
4. Look for the service account (ends with `@developer.gserviceaccount.com`)
5. You should see all 9 roles listed

## Part 7: Create Maps API Key

### Navigate to APIs & Services

1. In the Google Cloud Console, click the hamburger menu ☰
2. Navigate to **APIs & Services** > **Credentials**
3. You'll see the Credentials page

### Create New API Key

1. Click the **+ CREATE CREDENTIALS** button at the top
2. Select **API key** from the dropdown
3. A dialog shows "API key created" with your new key
4. **Copy this key value** - you'll need it later
5. Click **CLOSE**

### Configure API Key Restrictions

1. Find your new key in the list (probably named "API key 1")
2. Click the three dots ⋮ on the right
3. Select **Edit API key**
4. In the **Name** field, change it to exactly: `Maps Platform API Key`
   - **Critical**: Use this exact name!
5. Under **Application restrictions**, ensure **None** is selected
6. Under **API restrictions**:
   - Select **Restrict key**
   - Click **Select APIs**
   - In the search box, type `Maps JavaScript API`
   - Check the box next to **Maps JavaScript API**
   - Click **OK**
7. Click **SAVE** at the bottom

### Store API Key

Back in Cloud Shell:
```bash
# You'll be prompted to paste your API key
echo "PASTE_YOUR_API_KEY_HERE" > ~/mapkey.txt
```

Replace `PASTE_YOUR_API_KEY_HERE` with your actual API key.

## Part 8: Create Artifact Registry

### What is Artifact Registry?

Artifact Registry stores Docker container images. We need a repository to store our agent containers.

### Create Repository

```bash
gcloud artifacts repositories create neurohub-workshop \
  --repository-format=docker \
  --location=us-central1 \
  --description="Docker repository for NeuroHub workshop"
```

You should see:
```
Created repository [neurohub-workshop].
```

## Part 9: Database Setup

### Create Spanner Instance

Spanner is Google's globally distributed database. We'll use it to store our research data.

```bash
gcloud spanner instances create neurohub-graph-instance \
  --config=regional-us-central1 \
  --description="GraphDB Instance for NeuroHub" \
  --processing-units=100 \
  --edition=STANDARD
```

This takes 1-2 minutes. You'll see:
```
Creating instance...done.
```

### Create Database

```bash
gcloud spanner databases create neurohub-db \
  --instance=neurohub-graph-instance \
  --database-dialect=GOOGLE_STANDARD_SQL
```

You'll see:
```
Creating database...done.
```

### Grant Database Permissions

```bash
gcloud spanner databases add-iam-policy-binding neurohub-db \
  --instance=neurohub-graph-instance \
  --member="serviceAccount:${SERVICE_ACCOUNT_NAME}" \
  --role="roles/spanner.databaseUser" \
  --project=${PROJECT_ID}
```

## Part 10: Python Environment Setup

### Install UV Package Manager

UV is a fast Python package installer that's much quicker than pip:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.cargo/env
```

### Create Virtual Environment

```bash
cd ~/neurohub-workshop
uv venv
source .venv/bin/activate
```

Your prompt should now show `(.venv)` at the beginning.

### Install Dependencies

```bash
uv pip install -r requirements.txt
```

This installs all Python packages needed for the workshop. With UV, this takes just 30-60 seconds instead of 2-3 minutes!

### Load Sample Data

```bash
cd neurohub
python setup.py
```

You should see output showing tables being created and sample data being loaded.

## Part 11: Verify Database Setup

### Open Spanner Console

1. In a new browser tab, go to https://console.cloud.google.com/spanner
2. Click on **neurohub-graph-instance**
3. Click on **neurohub-db**
4. In the left sidebar, click **Spanner Studio**

### Run Test Query

In the query editor, paste and run:

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

Click **RUN**. You should see results showing researchers and their experiments.

## Part 12: Configure Map Display

### Retrieve API Key Configuration

Back in Cloud Shell:
```bash
source ~/neurohub-workshop/set_env.sh

export KEY_DISPLAY_NAME="Maps Platform API Key"

GOOGLE_MAPS_KEY_ID=$(gcloud services api-keys list \
  --project="${PROJECT_ID}" \
  --filter="displayName='${KEY_DISPLAY_NAME}'" \
  --format="value(uid)" \
  --limit=1)

GOOGLE_MAPS_API_KEY=$(gcloud services api-keys get-key-string "${GOOGLE_MAPS_KEY_ID}" \
  --project="${PROJECT_ID}" \
  --format="value(keyString)")

echo "${GOOGLE_MAPS_API_KEY}" > ~/mapkey.txt
echo "Retrieved GOOGLE_MAPS_API_KEY: ${GOOGLE_MAPS_API_KEY}"
```

The API key should match what you created earlier.

## Ready to Start!

If you've completed all these steps:
- ✅ Cloud Shell is configured
- ✅ Repository is cloned
- ✅ APIs are enabled
- ✅ IAM permissions are set
- ✅ Maps API key is created
- ✅ Database is running with sample data
- ✅ Python environment is ready

You're ready to begin Module 1 of the workshop!

## Next Steps

### 🚀 Start the Workshop

Now that your environment is set up, you have two options:

1. **Follow the Workshop Guide** (Recommended for workshop participants)
   - Open [WORKSHOP_GUIDE.md](WORKSHOP_GUIDE.md)
   - Start with Module 1: Understanding the Application
   - Progress through each module in order

2. **Quick Start** (If you want to see everything running)
   ```bash
   # Terminal 1: Start the web app
   cd ~/neurohub-workshop/neurohub
   python app.py
   
   # Terminal 2: Start MCP server
   cd ~/neurohub-workshop/tools/neurohub
   python mcp_server.py
   
   # Terminal 3: Start an agent
   cd ~/neurohub-workshop/agents/documentation
   python a2a_server.py
   ```
   
   Then click the **Web Preview** button (🌐) in Cloud Shell toolbar and select **Preview on port 8080**!

### 📚 Additional Resources

- **[WORKSHOP_GUIDE.md](WORKSHOP_GUIDE.md)** - Step-by-step workshop modules
- **[QUICK_REFERENCE.md](QUICK_REFERENCE.md)** - Commands and ports reference
- **[WORKSHOP_TROUBLESHOOTING_GUIDE.md](WORKSHOP_TROUBLESHOOTING_GUIDE.md)** - Common issues and solutions
- **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** - Complete documentation overview

### 💡 Tips for Success

1. Keep this terminal window open - you'll need it throughout the workshop
2. Open multiple Cloud Shell tabs (click the + icon) for running different services
3. Remember to `source set_env.sh` in each new terminal
4. The workshop is designed to be completed in order - don't skip modules!

## Troubleshooting During Setup

### "Permission denied" errors
Make sure you ran `chmod +x` on the scripts.

### "Project not set" errors
Run `source set_env.sh` again (remember to use `source`).

### API enablement fails
Check you have billing enabled on your project.

### Database creation fails
Verify your project ID is correct and APIs are enabled.

### Python package installation fails
Make sure UV is installed and you're using `uv pip install` instead of `pip install`.

### Virtual environment issues
UV creates `.venv` directory (not `env`). Activate with `source .venv/bin/activate`.

### Can't find things in Console
Use the search bar at the top of Google Cloud Console to quickly find services.

---
📌 Keep this guide open during setup - it will help you navigate successfully!