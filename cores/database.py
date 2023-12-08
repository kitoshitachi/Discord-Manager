from typing import Union
from supabase import create_client, Client
from settings import SUPABASE_URL, SUPABASE_KEY, CONFIG

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
            .update({'limit_xp':CONFIG['LIMIT_XP'], 'status' : CONFIG['STATUS']}) \
            .lt('limit_xp', CONFIG['LIMIT_XP']) \
            .execute()
        
        self.__supabase.from_('Member') \
            .update({'status' : CONFIG['STATUS']}) \
            .lt('status', CONFIG['STATUS']) \
            .execute()
    

    def update(self, id:int, data:Union[dict, None]):  
        if isinstance(data, dict) and id is not None:
            self.__supabase.from_('Member') \
                .update(data) \
                .eq('id', id) \
                .execute()
    

    def insert(self, data: Union[dict, list]):        
        if isinstance(data, (dict, list)):
            return self.__supabase.from_('Member') \
                .insert(data) \
                .execute()
    
    def delete(self, id:int):
        if id is not None:
            self.__supabase.from_('Member') \
                .delete() \
                .eq('id', id) \
                .execute()