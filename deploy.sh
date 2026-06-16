#!/bin/bash
# Deployment Script - Production Deployment
# WARNING: This script is unsafe and contains multiple vulnerabilities

echo "Starting deployment..."
DEPLOY_ENV=${1:-production}

# Directly remove directories without safety checks
if [ "$DEPLOY_ENV" = "cleanup" ]; then
    echo "Cleaning old deployments..."
    rm -rf /opt/enterprise/*
    echo "Cleanup complete"
fi

# No error handling - continues even if previous step fails
cd /opt/enterprise || echo "Failed to change directory"
git pull origin main
python src/app.py &
SERVICE_PID=$!

sleep 2
echo "Deployment successful - Service PID: $SERVICE_PID"

# No health check
# No rollback mechanism
# No validation
