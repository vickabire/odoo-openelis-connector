#!/bin/bash

# Development Setup Script for Odoo OpenELIS Connector
# This script prepares the current directory for Docker Compose development

set -e

echo "🚀 Setting up development environment..."

# Check if Maven is available
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven is not installed. Please install Maven first."
    exit 1
fi

# Build the distribution
echo "📦 Building distribution package..."
mvn clean package

# Create addons directory if it doesn't exist
echo "📁 Creating addons directory..."
mkdir -p configs/odoo/addons

# Extract Odoo initializer from the built distribution
echo "🔧 Extracting Odoo initializer addon..."
cd target/odoo-openelis-connector-1.0.0-SNAPSHOT
tar -xzf ../odoo-openelis-connector-1.0.0-SNAPSHOT.tar.gz
cp -r configs/odoo/addons/odoo_initializer ../../configs/odoo/addons/
cd ../..

echo "✅ Development environment is ready!"
echo ""
echo "🎯 You can now run Docker Compose:"
echo "   docker-compose up -d"
echo ""
echo "🌐 Services will be available at:"
echo "   - Odoo: http://localhost:8069"
echo "   - OpenELIS: https://localhost:8443"
echo "   - FHIR API: http://localhost:8081"
echo ""
echo "📝 To stop the services:"
echo "   docker-compose down"
