#!/bin/bash
# Odoo Initializer Runner Script
# This script runs the odoo_initializer to import configuration data

echo "Starting Odoo Initializer..."

# Check if Odoo is running
if ! docker-compose ps odoo.openelis.org | grep -q "Up"; then
    echo "Error: Odoo is not running. Please start the application first with 'docker-compose up -d'"
    exit 1
fi

# Wait for Odoo to be ready
echo "Waiting for Odoo to be ready..."
sleep 30

# Run the initializer
echo "Running initializer..."
docker-compose exec odoo.openelis.org python3 /tmp/test_initializer_fixed.py

echo "Initialization completed!"
