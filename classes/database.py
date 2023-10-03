import json
from datetime import datetime
from supabase import create_client, Client
from settings import SUPABASE_URL, SUPABASE_KEY
class Database:
    def __init__(self) -> None:
        self.__supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
    
    def get(self, _id:int = None, _select:str = "*"):
        if _id is None:
            return None 

        data, error = self.__supabase.from_('Member') \
            .select(_select) \
            .eq('id', _id) \
            .execute()
        
        if data[1] == []:
            return None

        return data[1][0]

    
    def update(self, _id:int = None, data = None) -> bool:
        if _id is None or data == None:
            return False

        self.__supabase.from_('Member') \
            .update(data) \
            .eq('id', _id) \
            .execute()
        return True
    
    def init_member(self, _id:int = None) -> bool:
        if _id is None:
            return False
        
        self.__supabase.from_('Member') \
            .insert({
                'id':_id, 
                'joined_date': str(datetime.now().date()),
                'character': json.dumps({'hp':1,'mp':1,'str':1,'agi':1, 'def':1 ,'crit':1, 'spirit':10})
            }) \
            .execute()
        
        return True
    
    def delete(self, _id:int = None) -> bool:
        if _id is None:
            return False
        
        self.__supabase.from_('Member') \
            .delete() \
            .eq('id',_id) \
            .execute()
        
        return True