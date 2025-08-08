#!/usr/bin/env python3
import os
import sys

# Add the addons path to Python path
sys.path.insert(0, '/mnt/extra-addons')

# Set up Odoo environment
os.environ['ODOO_RC'] = '/etc/odoo/odoo.conf'

# Import Odoo modules
import odoo
from odoo import api, SUPERUSER_ID

# Set database connection parameters
odoo.tools.config['db_host'] = 'db'
odoo.tools.config['db_user'] = 'odoo'
odoo.tools.config['db_password'] = 'odoo'
odoo.tools.config['db_name'] = 'postgres'
odoo.tools.config['initializer_checksums_path'] = '/var/lib/odoo/checksums'

# Initialize Odoo
odoo.tools.config.parse_config()
odoo.registry('postgres')

# Get the registry
registry = odoo.registry('postgres')
cr = registry.cursor()

try:
    from odoo_initializer.activator import start_init
    print("Successfully imported start_init")
    
    # Run the initialization
    start_init(cr)
    print("Initialization completed successfully")
    
    # Commit the changes
    cr.commit()
    
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    cr.rollback()
finally:
    cr.close()
