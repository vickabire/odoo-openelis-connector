import csv
import re
import os

PRODUCTS_CSV_PATH = os.path.join(os.path.dirname(__file__), '..', 'odoo', 'initializer_config', 'product', 'products.csv')
OUTPUT_PROPERTIES_PATH = os.path.join(os.path.dirname(__file__), '..', 'odoo-test-product-mapping.properties')

MAPPING_PREFIX = 'odoo.test.product.map.'

def generate_test_code(test_name):
    """
    Generates a standardized test code from a test name.
    - Converts to uppercase
    - Replaces non-alphanumeric characters with underscores
    - Cleans up any resulting multiple or trailing underscores
    """
    # Replace common problematic characters and spaces with underscores
    test_code = re.sub(r'[\s/,\(\)\-°]+', '_', test_name)
    # Remove any characters that are not alphanumeric or underscore
    test_code = re.sub(r'[^A-Z0-9_]+', '', test_code.upper())
    # Replace multiple underscores with a single one
    test_code = re.sub(r'_+', '_', test_code)
    # Remove leading or trailing underscores
    test_code = test_code.strip('_')
    return test_code

def main():
    """
    Reads the products.csv file and generates mapping properties,
    then writes them to the output properties file (overwriting it).
    """
    mappings = []
    
    print(f"Reading products from: {PRODUCTS_CSV_PATH}")
    if not os.path.exists(PRODUCTS_CSV_PATH):
        print(f"Error: Products CSV file not found at {PRODUCTS_CSV_PATH}")
        return

    with open(PRODUCTS_CSV_PATH, 'r', newline='', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            product_name = row.get('name')
            list_price = row.get('list_price')
            
            if not product_name:
                print(f"Skipping row due to missing product name: {row}")
                continue
            
            test_code = generate_test_code(product_name)
            
            mapping_line = f"{MAPPING_PREFIX}{test_code}={product_name},{list_price}"
            mappings.append(mapping_line)

    print(f"Generated {len(mappings)} mappings.")
    
    print(f"Writing mappings to: {OUTPUT_PROPERTIES_PATH}")
    with open(OUTPUT_PROPERTIES_PATH, 'w', encoding='utf-8') as propfile:
        propfile.write('# ----- Odoo Test-to-Product Mappings -----\n')
        for line in mappings:
            propfile.write(line + '\n')
    print("Successfully wrote mappings to odoo-test-product-mapping.properties.")

if __name__ == '__main__':
    main()
