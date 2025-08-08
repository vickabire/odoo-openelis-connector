#!/bin/bash

# Production Deployment Script for Odoo OpenELIS Connector
# This script deploys the built distribution package

set -e

echo "🚀 Deploying Odoo OpenELIS Connector..."

# Check if Maven is available
if ! command -v mvn &> /dev/null; then
    echo "❌ Maven is not installed. Please install Maven first."
    exit 1
fi

# Check if Docker Compose is available
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose is not installed. Please install Docker Compose first."
    exit 1
fi

# Build the distribution
echo "📦 Building distribution package..."
mvn clean package

# Create deployment directory
DEPLOY_DIR="deployment-$(date +%Y%m%d-%H%M%S)"
echo "📁 Creating deployment directory: $DEPLOY_DIR"
mkdir -p $DEPLOY_DIR

# Extract the distribution
echo "🔧 Extracting distribution package..."
cd target
tar -xzf odoo-openelis-connector-1.0.0-SNAPSHOT.tar.gz
cp -r odoo-openelis-connector-1.0.0-SNAPSHOT/* ../$DEPLOY_DIR/
cd ..

# Navigate to deployment directory
cd $DEPLOY_DIR

echo "✅ Distribution extracted to: $DEPLOY_DIR"
echo ""
echo "🎯 Starting services..."
docker-compose up -d

echo ""
echo "🌐 Services are starting up..."
echo "   - Odoo: http://localhost:8069"
echo "   - OpenELIS: https://localhost:8443"
echo "   - FHIR API: http://localhost:8081"
echo ""
echo "📝 Useful commands:"
echo "   - View logs: docker-compose logs -f"
echo "   - Stop services: docker-compose down"
echo "   - Restart services: docker-compose restart"
echo ""
echo "⏳ Services may take a few minutes to fully start up..."
