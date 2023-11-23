from typing import Union
from supabase import create_client, Client
from settings import SUPABASE_URL, SUPABASE_KEY

class Database:
    '''
    
    '''
    def __init__(self) -> None:
        self.__supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    

    def select(self, id:int, columns:str) -> Union[dict, None]:
        data, error = self.__supabase.from_('Member') \
            .select(columns) \
            .eq('id', id) \
            .execute()
        
        if data[1] == []:
            return None

        return data[1][0]


    def reset_limit(self):

        self.__supabase.from_('Member') \
            .update({'limit_xp':3000, 'status' : 1000}) \
            .lt('limit_xp', 3000) \
            .execute()
        
        self.__supabase.from_('Member') \
            .update({'status' : 1000}) \
            .lt('status', 1000) \
            .execute()
    

    def update(self, _id:int, data:Union[dict, None]):  
        if isinstance(data, dict) and _id is not None:
            self.__supabase.from_('Member') \
                .update(data) \
                .eq('id', _id) \
                .execute()
    

    def insert(self, data: Union[dict, list]):        
        if isinstance(data, (dict, list)):
            return self.__supabase.from_('Member') \
                .insert(data) \
                .execute()
    
    def delete(self, _id:int):
        if _id is not None:
            self.__supabase.from_('Member') \
                .delete() \
                .eq('id', _id) \
                .execute()