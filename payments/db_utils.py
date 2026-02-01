from django.db import connection

def execute_query(query, params=None, fetch_one=False, fetch_all=False):
    """
    Execute a raw SQL query using Django's connection cursor.
    """
    with connection.cursor() as cursor:
        cursor.execute(query, params)
        
        if fetch_one:
            columns = [col[0] for col in cursor.description]
            row = cursor.fetchone()
            if row:
                return dict(zip(columns, row))
            return None
            
        if fetch_all:
            columns = [col[0] for col in cursor.description]
            results = []
            for row in cursor.fetchall():
                results.append(dict(zip(columns, row)))
            return results
            
        return cursor.rowcount
