from .BaseController import BaseController
from models.db_schemes import Project ,DataChunk
from typing import List
from stores.LLM.LLMEmums import DocumentTypeEnum
import json
class NLPController(BaseController):

    def __init__(self , vectordb_clinet , generatoin_client , embedding_client):
        super().__init__()
        
        self. vectordb_clinet =vectordb_clinet
        self.generatoin_client =generatoin_client
        self.embedding_client = embedding_client

    def create_collection_name(self, project_id:str):
        return f'collection_{project_id}'.strip()
    
    def reset_db_collection(self , project:Project):
        collectoin_name = self.create_collection_name(project_id=project.project_id)
        return self.vectordb_clinet.delete_collection(collectoin_name = collectoin_name)
    
    def get_db_collection_info(self,project:Project ):
            
            collection_name = self.create_collection_name(project_id=project.project_id)
            collection_info = self.vectordb_clinet.get_collection_info(collection_name=collection_name)            
            return json.loads(
                 
                 json.dumps(collection_info , default = lambda d : d.__dict__)
            )
    
    def index_into_vector_db(self, project:Project , chunks:List[DataChunk] ,
                             do_reset = False ):
         
        #step 1 : get collection name 
        collection_name  =self.create_collection_name(project_id=project.project_id)
        #step 2 : manage items  
        texts = [ c.chunk_text for c in chunks]
        metadata = [ c.chunk_metadata for c in chunks]
        print('text len : ' ,  len(texts))
        vectors = [
              self.embedding_client.embedd_text(text )
              for text in texts
         ]
        
        check = []
        for idx, text in enumerate(texts):
              v = self.embedding_client.embedd_text(text)
              if v is None:
                    raise ValueError(f"Embedding returned None at index {idx}. Text preview: {text[:80]!r}")
                    check.append(v)
        
         #step 3 " create collection if not exist
        _ = self.vectordb_clinet.create_collection(
             collection_name = collection_name,
             do_reset =  do_reset,
             embedding_size =self.embedding_client.embedding_size 

        )
         #insert in database 

        _= self.vectordb_clinet.insert_many(
             collection_name = collection_name,
             texts = texts , 
             metadata = metadata , 
             vectors =  vectors,
             batch_size = 100 

         )
        return True 
    

    def search_vector_db_collection(self, project:Project ,   texts:str , limit:int = 5):
         #step 1 : get collection name 

         collection_name = self.create_collection_name(project_id= project.project_id)

         #step 2 : get text embedding vector 
         vector = self.embedding_client.embedd_text(texts )
         
         if not vector or len(vector) == 0:
         
              return False
         res = self.vectordb_clinet.search_by_vector(
              
              collection_name = collection_name,
              vector = vector , 
              limit=limit
         )
         if not res :
              return False
         return json.loads(
              json.dumps(res ,default=lambda a:a.__dict__)
         )



