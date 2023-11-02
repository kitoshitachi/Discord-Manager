from typing import Union
from supabase import create_client, Client
from settings import SUPABASE_URL, SUPABASE_KEY

class Database:
    '''
    
    '''
    def __init__(self) -> None:
        self.__supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    

    def select(self, id:int, *columns:str):
        if not isinstance(self, Database):
            return

        return self.__supabase.from_('Member') \
            .select(columns) \
            .eq('id', id) \
            .execute()


    def reset_limit(self):
        if not isinstance(self, Database):
            return

        self.__supabase.from_('Member') \
            .update({'limit_xp':3000, 'status' : 1000}) \
            .lt('limit_xp', 3000) \
            .execute()
        
        self.__supabase.from_('Member') \
            .update({'status' : 1000}) \
            .lt('status', 1000) \
            .execute()
    

    def update(self, _id:int, data:dict):
        if not isinstance(self, Database):
            return
        
        if isinstance(data, dict) and _id is not None:
            self.__supabase.from_('Member') \
                .update(data) \
                .eq('id', _id) \
                .execute()
    

    def insert(self, data: Union[dict, list]):
        if not isinstance(self, Database):
            return
        
        if isinstance(data, (dict, list)):
            return self.__supabase.from_('Member') \
                .insert(data) \
                .execute()
    