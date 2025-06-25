# odoo-openelis-connector

**A unified deployment and integration stack for OpenELIS and Odoo, enabling automated laboratory billing and master data management.**

---

## Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [How the Integration Works](#how-the-integration-works)
- [odoo-initializer: Automated Odoo Configuration](#odoo-initializer-automated-odoo-configuration)
- [Test Mapping: Linking OpenELIS Tests to Odoo Products](#test-mapping-linking-openelis-tests-to-odoo-products)
- [Repository Structure](#repository-structure)
- [Configuration](#configuration)
- [How to Run](#how-to-run)
- [Extending and Customizing](#extending-and-customizing)
- [Troubleshooting](#troubleshooting)
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

![](./configs/odoo/addons/arch.svg)

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

## odoo-initializer: Automated Odoo Configuration

- **Purpose**: To ensure Odoo is always initialized with the correct master data (products, prices, partners, etc.) from version-controlled files.
- **How it works**:
  - You define your products in CSV files (e.g., `products.csv`).
  - You define which files to load in `initializer_config.json`.
  - On Odoo startup, odoo-initializer reads these files and loads/updates the data in Odoo.
- **Benefits**:
  - No manual product entry in Odoo.
  - All configuration is version-controlled and repeatable.
  - Easy to update or add new products/tests.

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
├── odoo/
│   ├── addons/                # odoo-initializer and other custom addons
│   ├── config/                # Odoo config files (odoo.conf)
│   └── initializer_config/    # CSV/JSON files for odoo-initializer
│       ├── product/
│       │   └── products.csv   # Product catalog for Odoo
│       └── initializer_config.json
├── configs/
│   └── openelis/
│       └── properties/
│           └── common.properties  # OpenELIS and integration config
...
```

---

## Configuration

### **Odoo Product Catalog**

- Define your products in `odoo/initializer_config/product/products.csv`:
  ```
  id,name,list_price,type
  odoo_product_hiv,HIV Test,15.00,service
  odoo_product_glucose,Glucose Test,10.00,service
  ```

- Reference this file in `odoo/initializer_config/initializer_config.json`:
  ```json
  [
    {
      "name": "product",
      "model": "product.product",
      "file": "product/products.csv"
    }
  ]
  ```

### **Test Mapping in OpenELIS**

- In `configs/openelis/properties/common.properties`:
  ```
  odoo.test.product.map.HIV_TEST=HIV Test,15.00
  odoo.test.product.map.GLUCOSE=Glucose Test,10.00
  ```

### **Odoo Connection Properties**

- Also in `common.properties`:
  ```
  odoo.server.url=http://odoo:8069
  odoo.database.name=odoo
  odoo.username=admin
  odoo.password=admin
  ```

---

## How to Run

1. **Clone this repository**  
   ```sh
   git clone <your-repo-url>
   cd odoo-openelis-connector
   ```

2. **(Optional) Edit product catalog and mappings**  
   - Update `products.csv` and `common.properties` as needed.

3. **Start the stack**  
   ```sh
   docker-compose up --build
   ```

4. **Access the services**  
   - OpenELIS: [https://localhost:8443](https://localhost:8443)
   - Odoo: [http://localhost:8069](http://localhost:8069)
   - (Login with the admin credentials set in your config)

---

## Extending and Customizing

- **Add new tests/products**:  
  - Add to `products.csv` and `common.properties`.
  - Restart the stack to apply changes.

- **Add more Odoo configuration**:  
  - Add more CSV/XML files and reference them in `initializer_config.json`.

- **Change Odoo or OpenELIS versions**:  
  - Update the image tags in `docker-compose.yml`.

---

## Troubleshooting

- **Products not appearing in Odoo?**  
  - Check the Odoo logs for odoo-initializer errors.
  - Ensure your CSV and JSON config files are correctly formatted.

- **Invoices not created?**  
  - Check OpenELIS logs for integration errors.
  - Ensure the test mapping matches the product names in Odoo.

- **Connection issues?**  
  - Make sure all services are on the same Docker network.
  - Check the Odoo connection properties in `common.properties`.

---

## Credits

- [OpenELIS](https://openelis-global.org/)
- [Odoo](https://www.odoo.com/)
- [odoo-initializer](https://github.com/mekomsolutions/odoo-initializer) by Mekom Solutions

---