#!/bin/bash
# Deploy NeuroHub to Firebase Hosting with Cloud Run backend

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 NeuroHub Firebase Deployment Script${NC}"
echo "======================================="

# Check if project ID is set
if [ -z "$GOOGLE_CLOUD_PROJECT" ]; then
    if [ -f ~/project_id.txt ]; then
        export GOOGLE_CLOUD_PROJECT=$(cat ~/project_id.txt)
    else
        echo -e "${RED}Error: Project ID not found. Run source set_env.sh first.${NC}"
        exit 1
    fi
fi

echo -e "${GREEN}Using project: $GOOGLE_CLOUD_PROJECT${NC}"

# Step 1: Build and deploy the Flask app to Cloud Run
echo -e "\n${BLUE}Step 1: Deploying Flask app to Cloud Run...${NC}"

# Create a simple Dockerfile for the Flask app if it doesn't exist
if [ ! -f neurohub/Dockerfile ]; then
    cat > neurohub/Dockerfile << 'EOF'
FROM python:3.11-slim

WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY neurohub/ ./neurohub/
COPY agents/ ./agents/

# Set environment variables
ENV PORT=8080
ENV FLASK_APP=neurohub/app.py

# Expose port
EXPOSE 8080

# Run the application
CMD ["python", "-m", "neurohub.app"]
EOF
fi

# Deploy to Cloud Run
echo "Building and deploying to Cloud Run..."
gcloud run deploy neurohub-app \
    --source=. \
    --region=us-central1 \
    --platform=managed \
    --allow-unauthenticated \
    --set-env-vars="GOOGLE_CLOUD_PROJECT=$GOOGLE_CLOUD_PROJECT,SPANNER_INSTANCE_ID=$SPANNER_INSTANCE_ID,SPANNER_DATABASE_ID=$SPANNER_DATABASE_ID,GOOGLE_MAPS_API_KEY=$GOOGLE_MAPS_API_KEY"

# Get the Cloud Run service URL
SERVICE_URL=$(gcloud run services describe neurohub-app --region=us-central1 --format='value(status.url)')
echo -e "${GREEN}Cloud Run deployment complete!${NC}"
echo -e "Service URL: ${SERVICE_URL}"

# Step 2: Initialize Firebase in the project
echo -e "\n${BLUE}Step 2: Initializing Firebase...${NC}"

# Update .firebaserc with actual project ID
sed -i "s/{{PROJECT_ID}}/$GOOGLE_CLOUD_PROJECT/g" .firebaserc

# Enable Firebase Hosting API
gcloud services enable firebase.googleapis.com firebasehosting.googleapis.com

# Step 3: Deploy to Firebase Hosting
echo -e "\n${BLUE}Step 3: Deploying to Firebase Hosting...${NC}"

# Install Firebase CLI if not already installed
if ! command -v firebase &> /dev/null; then
    echo "Installing Firebase CLI..."
    npm install -g firebase-tools
fi

# Deploy to Firebase
firebase deploy --only hosting --project $GOOGLE_CLOUD_PROJECT

# Get the Firebase Hosting URL
FIREBASE_URL="https://$GOOGLE_CLOUD_PROJECT.web.app"

echo -e "\n${GREEN}🎉 Deployment Complete!${NC}"
echo "======================================="
echo -e "Firebase Hosting URL: ${BLUE}${FIREBASE_URL}${NC}"
echo -e "Cloud Run Backend URL: ${BLUE}${SERVICE_URL}${NC}"
echo -e "\nYour NeuroHub application is now live and accessible to anyone!"
echo -e "\nShare your URL with others: ${BLUE}${FIREBASE_URL}${NC}"