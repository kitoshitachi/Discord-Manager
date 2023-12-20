
from typing import Union
from postgrest import APIError

from .client import supabase

class QuerryError(Exception):...

class BaseTable:
    def __init__(self, name) -> None:
        self.name = name
        self.__supabase = supabase
    
    @property
    def client(self):
        return self.__supabase

    def select_one(self, id:int, columns:str) -> Union[dict, None]:
        data, error = self.client.from_(self.name) \
            .select(columns) \
            .eq('id', id) \
            .execute()
        
        if data[1] == []:
            return None

        return data[1][0]
    
    def select_(self, limit:int = -1) -> Union[list[dict], None]:
        querry = self.client.from_(self.name) \
            .select('*')
        
        if limit > 0:
            querry = querry.limit(limit)

        data, error = querry.execute()

        return data[1]

    def update(self, id:int, data):  
        try:
            self.client.from_(self.name) \
                .update(data) \
                .eq('id', id) \
                .execute()
        except APIError:
            raise QuerryError(f"Update {data} is corrupted or id {id} does not exist")
        

    def insert(self, data: Union[dict, list]): 
        try:       
            self.client.from_(self.name) \
                .insert(data) \
                .execute()
        except APIError:
            raise QuerryError(f"Cant insert {data} into {self.name} table")

    def delete(self, id:int):
        if id is None:
            raise QuerryError("Missing Id")

        self.client.from_(self.name) \
            .delete() \
            .eq('id', id) \
            .execute()