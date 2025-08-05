# Odoo OpenELIS Connector

A unified deployment and integration stack for OpenELIS and Odoo, enabling automated laboratory billing and master data management with automated Odoo configuration via odoo-initializer.

## Overview

This repository provides a production-ready Docker Compose stack for running OpenELIS (Laboratory Information System) and Odoo (ERP/Billing) together, with automated product and billing integration.

- **OpenELIS**: Manages lab orders, results, and workflow
- **Odoo**: Handles billing, invoicing, and product catalog
- **odoo-initializer**: Ensures Odoo is pre-loaded with correct products and configuration
- **Integration**: When a lab order is created in OpenELIS, an invoice is automatically generated in Odoo

## Quick Start

### Prerequisites

- Docker and Docker Compose
- Maven 3.6+ (or use Docker Maven)

### Setup

1. **Extract the Odoo Initializer Addon**
   ```bash
   mvn clean generate-resources
   ```

2. **Start the services**
   ```bash
   docker-compose up -d
   ```

3. **Access the services**
   - **Odoo**: http://localhost:8069
   - **OpenELIS**: https://localhost:8443

## Configuration

### Odoo Product Catalog

Define your products in `configs/odoo/initializer_config/product/products.csv`:

```csv
id,name,list_price,type
odoo_product_hiv,HIV Test,15.00,service
odoo_product_glucose,Glucose Test,10.00,service
```

### Test Mapping

Map OpenELIS tests to Odoo products in `configs/openelis/properties/common.properties`:

```properties
odoo.test.product.map.HIV_TEST=HIV Test,15.00
odoo.test.product.map.GLUCOSE=Glucose Test,10.00
```

### Odoo Connection

Configure Odoo connection in `configs/openelis/properties/common.properties`:

```properties
odoo.server.url=http://odoo:8069
odoo.database.name=odoo
odoo.username=admin
odoo.password=admin
```

## Troubleshooting

### Check if services are running
```bash
docker-compose ps
```

### View logs
```bash
docker-compose logs odoo.openelis.org
docker-compose logs oe.openelis.org
```

### Restart services
```bash
docker-compose restart
```

### Clean up
```bash
docker-compose down -v
```
