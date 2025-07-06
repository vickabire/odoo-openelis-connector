# Odoo OpenELIS Connector

**A unified deployment and integration stack for OpenELIS and Odoo, enabling automated laboratory billing and master data management with automated Odoo configuration via odoo-initializer.**

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [How the Integration Works](#how-the-integration-works)
- [Odoo Initializer: Automated Odoo Configuration](#odoo-initializer-automated-odoo-configuration)
- [Test Mapping: Linking OpenELIS Tests to Odoo Products](#test-mapping-linking-openelis-tests-to-odoo-products)
- [Repository Structure](#repository-structure)
- [Quick Start](#quick-start)
- [Configuration](#configuration)
- [Adding New Data Types](#adding-new-data-types)
- [Troubleshooting](#troubleshooting)
- [CI/CD Integration](#cicd-integration)
- [Extending and Customizing](#extending-and-customizing)
- [Credits](#credits)

---

## Overview

This repository provides a **production-ready Docker Compose stack** for running OpenELIS (Laboratory Information System) and Odoo (ERP/Billing) together, with automated product and billing integration.

- **OpenELIS**: Manages lab orders, results, and workflow.
- **Odoo**: Handles billing, invoicing, and product catalog.
- **odoo-initializer**: Ensures Odoo is always pre-loaded with the correct products and configuration, based on version-controlled CSV files.
- **Integration Layer**: When a lab order is created in OpenELIS, an invoice is automatically generated in Odoo for the correct products.

---

## Architecture

![](./arch.svg)

- **OpenELIS** triggers billing via the integration service.
- **Test/Product Mapping** ensures the right Odoo product is billed.
- **odoo-initializer** loads the product catalog into Odoo from CSV/JSON.
- **Odoo** receives invoice requests and manages billing.

---

## How the Integration Works

1. **Startup**:  
   - Odoo starts and runs the odoo-initializer add-on.
   - odoo-initializer reads configuration files (CSV/JSON) and loads products, prices, and other metadata into Odoo.

2. **Order Creation**:  
   - A user creates a lab order in OpenELIS.
   - OpenELIS fires an event (`SamplePatientUpdateDataCreatedEventListener`).
   - The integration service (`OdooIntegrationService`) reads the test-to-product mapping and calls Odoo (via XML-RPC) to create an invoice for the correct product(s).

3. **Billing**:  
   - Odoo receives the invoice request and creates the invoice, using the products that were loaded by odoo-initializer.

---

## Odoo Initializer: Automated Odoo Configuration

The odoo-initializer is an Odoo addon that automatically loads data from CSV files when Odoo starts up. This project uses Maven to automatically download and extract the addon, making the setup process more reliable and reproducible.

### How It Works

- **Purpose**: To ensure Odoo is always initialized with the correct master data (products, prices, partners, etc.) from version-controlled files.
- **Process**:
  - You define your products in CSV files (e.g., `products.csv`).
  - You define which files to load in `initializer_config.json`.
  - On Odoo startup, odoo-initializer reads these files and loads/updates the data in Odoo.
- **Benefits**:
  - No manual product entry in Odoo.
  - All configuration is version-controlled and repeatable.
  - Easy to update or add new products/tests.

### Maven Configuration

The `pom.xml` file is configured to:

1. **Download** the odoo-initializer artifact from Mekom Solutions Maven repository
2. **Extract** it to `configs/odoo/addons/odoo_initializer/` using the `maven-dependency-plugin`
3. **Clean** old files when needed
4. **Version Management** - Easy to update versions by changing properties

---

## Test Mapping: Linking OpenELIS Tests to Odoo Products

- **Purpose**: To ensure each OpenELIS test is billed as the correct Odoo product.
- **How it works**:
  - In `common.properties`, you define mappings like:
    ```
    odoo.test.product.map.HIV_TEST=HIV Test,15.00
    ```
  - When OpenELIS creates an order, it uses this mapping to find the Odoo product name and price.
  - The integration service uses this info to create the correct invoice in Odoo.

---

## Repository Structure

```
odoo-openelis-connector/
├── docker-compose.yml
├── pom.xml                          # Maven configuration for odoo-initializer
├── configs/
│   ├── odoo/
│   │   ├── addons/                 # odoo-initializer (extracted by Maven)
│   │   ├── config/                 # Odoo config files (odoo.conf)
│   │   └── initializer_config/     # CSV/JSON files for odoo-initializer
│   │       ├── product/
│   │       │   └── products.csv    # Product catalog for Odoo
│   │       └── initializer_config.json
│   └── openelis/
│       └── properties/
│           └── common.properties   # OpenELIS and integration config
└── .github/workflows/
    └── ci.yml                      # CI/CD pipeline configuration
```

---

## Quick Start

### Prerequisites

- Maven 3.6+ installed
- Docker and Docker Compose
- Java 8+

### Standard Workflow

```bash
# 1. Extract the Odoo Initializer Addon
mvn clean generate-resources

# 2. Start the containers
docker-compose up -d odoo.openelis.org
# OR for the complete stack
docker-compose up --build
```

### Alternative: Docker-only Setup

```bash
# Extract using Docker Maven (if you don't have Maven installed)
docker run --rm -v "$(pwd):/workspace" -w /workspace maven:3.9-eclipse-temurin-8 mvn clean generate-resources

# Start Odoo
docker-compose up -d odoo.openelis.org
```

### Access the Services

- **OpenELIS**: [https://localhost:8443](https://localhost:8443)
- **Odoo**: [http://localhost:8069](http://localhost:8069)
- **Database**: `odoo_openelis_db`

---

## Configuration

### Odoo Product Catalog

- Define your products in `configs/odoo/initializer_config/product/products.csv`:
  ```csv
  id,name,list_price,type
  odoo_product_hiv,HIV Test,15.00,service
  odoo_product_glucose,Glucose Test,10.00,service
  ```

- Reference this file in `configs/odoo/initializer_config/initializer_config.json`:
  ```json
  [
    {
      "name": "product",
      "model": "product.product",
      "file": "product/products.csv"
    }
  ]
  ```

### Test Mapping in OpenELIS

- In `configs/openelis/properties/common.properties`:
  ```
  odoo.test.product.map.HIV_TEST=HIV Test,15.00
  odoo.test.product.map.GLUCOSE=Glucose Test,10.00
  ```

### Odoo Connection Properties

- Also in `common.properties`:
  ```
  odoo.server.url=http://odoo:8069
  odoo.database.name=odoo
  odoo.username=admin
  odoo.password=admin
  ```

### Docker Setup

The `docker-compose.yml` is configured with:

```yaml
environment:
  - ADDONS=odoo_initializer,sale_management,stock,account_account
  - INITIALIZER_DATA_FILES_PATH=/mnt/odoo_config
  - INITIALIZER_CONFIG_FILE_PATH=/mnt/odoo_config/initializer_config.json
volumes:
  - ./configs/odoo/addons:/mnt/extra-addons
  - ./configs/odoo/initializer_config:/mnt/odoo_config
```

---

## Adding New Data Types

### 1. Create CSV File

Create a new CSV file in `configs/odoo/initializer_config/`:

```csv
id,name,email,phone
partner_001,John Doe,john@example.com,+1234567890
partner_002,Jane Smith,jane@example.com,+0987654321
```

### 2. Update Configuration

Add an entry to `configs/odoo/initializer_config/initializer_config.json`:

```json
[
  {
    "name": "product",
    "model": "product.product",
    "file": "product/products.csv"
  },
  {
    "name": "partners",
    "model": "res.partner", 
    "file": "partners/partners.csv"
  }
]
```

### 3. Restart Odoo

```bash
docker-compose restart odoo.openelis.org
```

## Supported Models

The odoo-initializer supports many Odoo models including:

- `product.product` - Products
- `res.partner` - Partners/Customers
- `res.company` - Companies
- `res.country` - Countries
- `res.currency` - Currencies
- `product.category` - Product Categories
- `stock.location` - Stock Locations
- `account.account` - Chart of Accounts
- `account.journal` - Journals
- `res.users` - Users
- And many more...

---

## Troubleshooting

### Initializer Not Running

1. Check if the addon is extracted:
   ```bash
   ls -la configs/odoo/addons/odoo_initializer/
   ```

2. Check Odoo logs:
   ```bash
   docker-compose logs odoo.openelis.org | grep -i initializer
   ```

3. Verify configuration:
   ```bash
   cat configs/odoo/initializer_config/initializer_config.json
   ```

### Data Not Loading

1. Check CSV format - ensure headers match Odoo field names
2. Verify file paths in configuration
3. Check for syntax errors in CSV files
4. Look for error messages in Odoo logs

### Products not appearing in Odoo?

- Check the Odoo logs for odoo-initializer errors.
- Ensure your CSV and JSON config files are correctly formatted.

### Invoices not created?

- Check OpenELIS logs for integration errors.
- Ensure the test mapping matches the product names in Odoo.

### Connection issues?

- Make sure all services are on the same Docker network.
- Check the Odoo connection properties in `common.properties`.

### Version Issues

If you need a different version of the odoo-initializer:

1. Update the version in `pom.xml`:
   ```xml
   <odooInitializerVersion>2.4.0</odooInitializerVersion>
   ```

2. Re-extract:
   ```bash
   mvn clean generate-resources
   ```

### Maven Repository Access

If you don't have access to the Mekom Solutions Maven repository, you can:

1. **Use a local repository**: Install the ZIP file locally:
   ```bash
   mvn install:install-file \
     -Dfile=configs/odoo/addons/odoo-initializer-2.3.0-SNAPSHOT.zip \
     -DgroupId=net.mekomsolutions.odoo \
     -DartifactId=odoo-initializer \
     -Dversion=2.3.0-SNAPSHOT \
     -Dpackaging=zip
   ```

2. **Fallback to local ZIP**: Use the `maven-antrun-plugin` approach

### Cleaning Up Generated Files

```bash
# Clean Maven-generated files (including odoo-initializer)
mvn clean

# Manual cleanup of odoo-initializer (if needed)
rm -rf configs/odoo/addons/odoo_initializer/

# Docker cleanup
docker-compose down -v
```

---

## CI/CD Integration

### GitHub Actions Example

The project includes a `.github/workflows/ci.yml` file that shows how to:

1. **Extract the initializer** in CI: `mvn clean generate-resources`
2. **Test the setup** with Docker containers
3. **Build and package** the project for deployment

### Key CI/CD Steps

```yaml
- name: Extract Odoo Initializer
  run: mvn clean generate-resources

- name: Verify Extraction
  run: |
    if [ ! -d "configs/odoo/addons/odoo_initializer" ]; then
      echo "odoo-initializer extraction failed"
      exit 1
    fi

- name: Test with Docker
  run: |
    docker-compose up -d odoo.openelis.org
    # Wait and verify Odoo is running
```

---

## Extending and Customizing

### Add new tests/products

- Add to `products.csv` and `common.properties`.
- Restart the stack to apply changes.

### Add more Odoo configuration

- Add more CSV/XML files and reference them in `initializer_config.json`.

### Change Odoo or OpenELIS versions

- Update the image tags in `docker-compose.yml`.

### Advanced Configuration

#### Custom Field Mappings

You can specify custom field mappings in the configuration:

```json
{
  "name": "custom_products",
  "model": "product.product",
  "file": "custom/products.csv",
  "field_mappings": {
    "external_id": "id",
    "product_name": "name",
    "price": "list_price"
  }
}
```

#### Conditional Loading

Use environment variables to conditionally load data:

```json
{
  "name": "test_data",
  "model": "product.product", 
  "file": "test/test_products.csv",
  "condition": "${LOAD_TEST_DATA}"
}
```

---

## Best Practices

1. **Version Control**: Keep CSV files in version control, exclude extracted addon
2. **Backup**: Always backup your data before running initializer
3. **Testing**: Test on development environment first
4. **Documentation**: Document your data structure and field mappings
5. **Validation**: Validate CSV data before loading
6. **CI/CD**: Always extract the initializer in your build pipeline
7. **Automation**: Use Maven commands to ensure consistent setup across environments

---

## Credits

- **OpenELIS**: [https://openelis-global.org/](https://openelis-global.org/)
- **Odoo**: [https://www.odoo.com/](https://www.odoo.com/)
- **Odoo Initializer**: [https://github.com/mekomsolutions/odoo-initializer](https://github.com/mekomsolutions/odoo-initializer)
- **Mekom Solutions**: [https://www.mekomsolutions.com/](https://www.mekomsolutions.com/)