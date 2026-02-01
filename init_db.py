import os
import django
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'payment_gateway.settings')
django.setup()

from payments.db_utils import execute_query

def init_db():
    schema_path = os.path.join(os.path.dirname(__file__), 'schema.sql')
    with open(schema_path, 'r') as f:
        schema_sql = f.read()
    
    print("Executing schema...")
    try:
        with django.db.connection.cursor() as cursor:
            # Split statements and remove empty ones
            statements = [s.strip() for s in schema_sql.split(';') if s.strip()]
            for statement in statements:
                cursor.execute(statement)
        print("Schema executed successfully.")
    except Exception as e:
        print(f"Error executing schema: {e}")

if __name__ == '__main__':
    init_db()
