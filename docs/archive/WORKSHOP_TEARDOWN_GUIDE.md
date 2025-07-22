# NeuroHub Workshop - Complete Teardown Guide

This guide provides step-by-step instructions for cleaning up all Google Cloud resources created during the NeuroHub workshop. Follow these steps to avoid any ongoing charges.

## ⚠️ Important Notes Before Starting

- **Billing**: Google Cloud charges for resources even when not in use
- **Order Matters**: Some resources depend on others; delete in the correct order
- **Double-Check**: Verify your project ID before deleting anything
- **Downloads**: Save any work you want to keep before starting teardown

## 📥 Part 1: Save Your Work (Optional)

### Step 1.1: Export Your Code

If you made modifications you want to keep:

```bash
# Create a backup directory
mkdir ~/neurohub-backup

# Copy your modified files
cp -r ~/neurohub-workshop ~/neurohub-backup/

# Create a zip file
cd ~
zip -r neurohub-workshop-backup.zip neurohub-backup/

# Download via Cloud Shell
cloudshell download neurohub-workshop-backup.zip
```

### Step 1.2: Export Database Data

If you want to keep any custom data:

```bash
# Export Spanner data
gcloud spanner databases export neurohub-db \
  --instance=neurohub-graph-instance \
  --destination-uri=gs://${GOOGLE_CLOUD_PROJECT}-backup/neurohub-export \
  --project=${GOOGLE_CLOUD_PROJECT}
```

## 🛑 Part 2: Stop Running Services

### Step 2.1: Check Running Services

First, ensure you're in the correct project:

```bash
# Verify project
echo "Current project: $(gcloud config get-value project)"
echo "Expected project: $(cat ~/project_id.txt)"

# Set project if needed
gcloud config set project $(cat ~/project_id.txt)
```

### Step 2.2: Stop Local Services

If any services are still running in Cloud Shell:

```bash
# Find Python processes
ps aux | grep python

# Kill any running Flask/MCP/Agent servers
pkill -f "python app.py"
pkill -f "python mcp_server.py"
pkill -f "python a2a_server.py"
```

### Step 2.3: List Deployed Cloud Run Services

```bash
# List all Cloud Run services
gcloud run services list --platform=managed --region=us-central1
```

## 🗑️ Part 3: Delete Cloud Run Services

### Step 3.1: Delete Agent Services

Delete each deployed agent service:

```bash
# Delete documentation agent
gcloud run services delete documentation \
  --platform=managed \
  --region=us-central1 \
  --quiet

# Delete signal processor agent
gcloud run services delete signal-processor \
  --platform=managed \
  --region=us-central1 \
  --quiet

# Delete experiment designer agent
gcloud run services delete experiment-designer \
  --platform=managed \
  --region=us-central1 \
  --quiet

# Delete research orchestrator agent
gcloud run services delete research-orchestrator \
  --platform=managed \
  --region=us-central1 \
  --quiet
```

### Step 3.2: Delete Main Application Service

```bash
# Delete main NeuroHub app if deployed
gcloud run services delete neurohub \
  --platform=managed \
  --region=us-central1 \
  --quiet
```

### Step 3.3: Verify All Services Deleted

```bash
# Should return empty or "Listed 0 items"
gcloud run services list --platform=managed --region=us-central1
```

## 🐳 Part 4: Clean Up Container Images

### Step 4.1: List Container Images

```bash
# List all images in Artifact Registry
gcloud artifacts docker images list \
  us-central1-docker.pkg.dev/${GOOGLE_CLOUD_PROJECT}/neurohub-workshop
```

### Step 4.2: Delete All Images

```bash
# Delete the entire repository (easier than individual images)
gcloud artifacts repositories delete neurohub-workshop \
  --location=us-central1 \
  --quiet
```

## 💾 Part 5: Delete Database Resources

### Step 5.1: Delete Spanner Database

```bash
# Delete the database
gcloud spanner databases delete neurohub-db \
  --instance=neurohub-graph-instance \
  --quiet
```

### Step 5.2: Delete Spanner Instance

```bash
# Delete the instance (this also deletes all databases in it)
gcloud spanner instances delete neurohub-graph-instance \
  --quiet
```

### Step 5.3: Verify Deletion

```bash
# Should return empty
gcloud spanner instances list
```

## 🔑 Part 6: Clean Up API Keys and Credentials

### Step 6.1: Delete Maps API Key

1. **Via Console**:
   - Go to: https://console.cloud.google.com/apis/credentials
   - Find "Maps Platform API Key"
   - Click the trash icon 🗑️
   - Confirm deletion

2. **Via CLI** (alternative):
```bash
# List API keys
gcloud services api-keys list

# Delete the Maps key (replace KEY_ID with actual ID)
gcloud services api-keys delete KEY_ID --quiet
```

### Step 6.2: Remove Local Credential Files

```bash
# Remove stored keys
rm -f ~/mapkey.txt
rm -f ~/project_id.txt
```

## 🔐 Part 7: Clean Up IAM Permissions

### Step 7.1: List Service Account Permissions

```bash
# Get the service account email
SERVICE_ACCOUNT=$(gcloud iam service-accounts list \
  --filter="displayName:Compute Engine default service account" \
  --format="value(email)")

echo "Service account: $SERVICE_ACCOUNT"
```

### Step 7.2: Remove Custom IAM Bindings

```bash
# Remove all custom roles we added
ROLES_TO_REMOVE=(
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

for role in "${ROLES_TO_REMOVE[@]}"; do
  echo "Removing $role..."
  gcloud projects remove-iam-policy-binding ${GOOGLE_CLOUD_PROJECT} \
    --member="serviceAccount:${SERVICE_ACCOUNT}" \
    --role="$role" \
    --quiet 2>/dev/null || true
done
```

## 🧹 Part 8: Clean Up Storage Buckets

### Step 8.1: List Storage Buckets

```bash
# List all buckets in the project
gsutil ls -p ${GOOGLE_CLOUD_PROJECT}
```

### Step 8.2: Delete Workshop-Related Buckets

```bash
# Delete any backup buckets created
gsutil rm -r gs://${GOOGLE_CLOUD_PROJECT}-backup 2>/dev/null || true

# Delete Cloud Build staging bucket
gsutil rm -r gs://${GOOGLE_CLOUD_PROJECT}_cloudbuild 2>/dev/null || true
```

## 📁 Part 9: Clean Up Local Environment

### Step 9.1: Deactivate Python Environment

```bash
# If virtual environment is active
deactivate
```

### Step 9.2: Remove Project Files

```bash
# Remove the workshop directory
cd ~
rm -rf neurohub-workshop/

# Remove UV package manager (optional)
rm -rf ~/.cargo/bin/uv
rm -rf ~/.cargo/bin/uvx
```

### Step 9.3: Clean Shell Configuration

```bash
# Remove any workshop-specific configurations
unset GOOGLE_CLOUD_PROJECT
unset SPANNER_INSTANCE_ID
unset SPANNER_DATABASE_ID
unset SERVICE_ACCOUNT_NAME
unset FLASK_SECRET_KEY
```

## 🔍 Part 10: Final Verification

### Step 10.1: Create Verification Script

```bash
cat > verify_teardown.sh << 'EOF'
#!/bin/bash
echo "=== NeuroHub Workshop Teardown Verification ==="
echo

PROJECT_ID=$(gcloud config get-value project)
echo "Checking project: $PROJECT_ID"
echo

# Check Cloud Run services
echo "1. Cloud Run Services:"
SERVICE_COUNT=$(gcloud run services list --platform=managed --region=us-central1 2>/dev/null | grep -c neurohub || echo "0")
echo "   Found $SERVICE_COUNT neurohub-related services"
echo

# Check Spanner
echo "2. Spanner Instances:"
SPANNER_COUNT=$(gcloud spanner instances list 2>/dev/null | grep -c neurohub || echo "0")
echo "   Found $SPANNER_COUNT neurohub instances"
echo

# Check Artifact Registry
echo "3. Container Repositories:"
REPO_COUNT=$(gcloud artifacts repositories list --location=us-central1 2>/dev/null | grep -c neurohub || echo "0")
echo "   Found $REPO_COUNT neurohub repositories"
echo

# Check API Keys
echo "4. API Keys:"
KEY_COUNT=$(gcloud services api-keys list 2>/dev/null | grep -c "Maps Platform" || echo "0")
echo "   Found $KEY_COUNT Maps API keys"
echo

# Check local files
echo "5. Local Files:"
echo "   ~/neurohub-workshop: $([ -d ~/neurohub-workshop ] && echo "Still exists!" || echo "Removed ✓")"
echo "   ~/project_id.txt: $([ -f ~/project_id.txt ] && echo "Still exists!" || echo "Removed ✓")"
echo "   ~/mapkey.txt: $([ -f ~/mapkey.txt ] && echo "Still exists!" || echo "Removed ✓")"
echo

if [ "$SERVICE_COUNT" -eq 0 ] && [ "$SPANNER_COUNT" -eq 0 ] && [ "$REPO_COUNT" -eq 0 ]; then
  echo "✅ All major resources have been cleaned up!"
else
  echo "⚠️  Some resources may still exist. Check the counts above."
fi

echo
echo "=== Verification Complete ==="
EOF

chmod +x verify_teardown.sh
./verify_teardown.sh
```

## 💰 Part 11: Disable Billing (Optional)

If you created a new billing account just for this workshop:

### Step 11.1: Remove Project from Billing

1. Go to: https://console.cloud.google.com/billing
2. Click on your billing account
3. Click **Account management**
4. Find your project in the list
5. Click the three dots ⋮ → **Disable billing**

### Step 11.2: Delete the Project (Nuclear Option)

⚠️ **WARNING**: This permanently deletes EVERYTHING in the project!

```bash
# This will delete the entire project after a 30-day grace period
gcloud projects delete ${GOOGLE_CLOUD_PROJECT} --quiet
```

Or via Console:
1. Go to: https://console.cloud.google.com/iam-admin/settings
2. Click **SHUT DOWN**
3. Type the project ID to confirm
4. Click **SHUT DOWN**

## ✅ Teardown Complete!

Your Google Cloud resources have been cleaned up. You should not incur any further charges from the workshop resources.

## 📊 Billing Verification

To verify no resources are still running:

1. Go to: https://console.cloud.google.com/billing
2. Click your billing account
3. Go to **Reports**
4. Filter by your project
5. Check for any ongoing charges

## 🆘 Troubleshooting Teardown Issues

### "Resource not found" errors
- The resource may already be deleted
- Check if you're in the correct project

### "Permission denied" errors
- Ensure you have owner/editor role on the project
- Some resources may have deletion protection

### Can't delete Spanner instance
- Make sure all databases are deleted first
- Check for any backups that need deletion

### Billing still shows charges
- Some charges may take 24-48 hours to stop
- Check the billing reports for specific resources
- Contact Google Cloud Support if charges persist

## 📝 Final Checklist

- [ ] All Cloud Run services deleted
- [ ] Spanner instance and database deleted
- [ ] Container images and repository deleted
- [ ] API keys deleted
- [ ] Local files cleaned up
- [ ] Environment variables unset
- [ ] Billing verified or project deleted

---
*NeuroHub Workshop Teardown Guide v1.0 | Remember to check your billing!*