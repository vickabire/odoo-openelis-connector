import os
import re
import csv

LIQUIBASE_DIR = 'src/main/resources/liquibase/'
SQL_ROOT_DIR = '.'  # Search from project root for .sql files

OUTPUT_CSV = 'openelis_tests_extracted.csv'

INSERT_XML_REGEX = re.compile(r"INSERT INTO clinlims\.test\([^)]*\)\s*VALUES \([^,]*,[^,]*,[^,]*,'([^']+)'", re.IGNORECASE)
INSERT_SQL_REGEX = re.compile(r"INSERT INTO (?:clinlims\.)?test\([^)]*description[^)]*\)\s*VALUES \((?:[^,]*,){3}\s*'([^']+)'", re.IGNORECASE)

def find_files(directory, exts):
    for root, _, files in os.walk(directory):
        for file in files:
            if any(file.endswith(ext) for ext in exts):
                yield os.path.join(root, file)

def extract_test_names_from_file(filepath, regex):
    test_names = []
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
        for match in regex.finditer(content):
            test_name = match.group(1)
            test_names.append(test_name)
    return test_names

def main():
    all_test_names = set()
    for xml_file in find_files(LIQUIBASE_DIR, ['.xml']):
        test_names = extract_test_names_from_file(xml_file, INSERT_XML_REGEX)
        all_test_names.update(test_names)
    for sql_file in find_files(SQL_ROOT_DIR, ['.sql']):
        test_names = extract_test_names_from_file(sql_file, INSERT_SQL_REGEX)
        all_test_names.update(test_names)

    with open(OUTPUT_CSV, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['id', 'name', 'list_price', 'type'])
        for name in sorted(all_test_names):
            id_slug = 'odoo_test_' + re.sub(r'[^a-zA-Z0-9]+', '_', name).lower().strip('_')
            writer.writerow([id_slug, name, '0.00', 'service'])
    print(f"Extracted {len(all_test_names)} test names. Output written to {OUTPUT_CSV}")

if __name__ == '__main__':
    main()
