import os


from supabase import create_client, Client

class ConnectDatabaseError(Exception):...

try:
    SUPABASE_URL = os.getenv('SUPABASE_URL')
    SUPABASE_KEY = os.getenv('SUPABASE_KEY')
    supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
except Exception as error:
    raise ConnectDatabaseError(f"Cant connect to your database")
