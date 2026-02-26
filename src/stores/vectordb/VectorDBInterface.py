from abc import ABC , abstractmethod
from typing import List
class VectorDBInterface(ABC):


#usaully memo type DB is collection based db not tables 

    @classmethod
    @abstractmethod
    def connect(self):
        pass


    @classmethod
    @abstractmethod
    def is_collection_existed(self, collection_name:str) -> bool:
        pass
    
    
    @classmethod
    @abstractmethod
    def list_all_collection(self)-> List:
        pass

    @classmethod
    @abstractmethod
    def get_collection_info(self, collection_name:str ):
        pass


    @classmethod
    @abstractmethod
    def delete_collection(self, collection_name:str):
        pass

    
    @classmethod
    @abstractmethod
    def create_collection(self, collection_name :str , embedding_size :int , do_reset:bool=False):

        pass

    @classmethod
    @abstractmethod
    def insert_one(self ,collection_name :str , text:str ,vector:list , metadata:dict=None , recored_id:str =None):
        pass

    @classmethod
    @abstractmethod
    def insert_many(self, collection_name , texts :list ,
                     vectors:list ,metadata:list =None , 
                     recoredid:list =None , 
                     batch_size:int =None ):
        pass
        

    @classmethod
    @abstractmethod
    def search_by_vector(self ,collection_name :str , vector:List , limit:int):
        pass 
    


    
