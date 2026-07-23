from .BaseController import BaseController
from models.db_schemes import Project ,DataChunk
from typing import List
from stores.LLM.LLMEmums import DocumentTypeEnum
import json
class NLPController(BaseController):

    def __init__(self , vectordb_clinet , generatoin_client , embedding_client , template_parser):
        super().__init__()
        
        self. vectordb_clinet =vectordb_clinet
        self.generatoin_client =generatoin_client
        self.embedding_client = embedding_client
        self.template_parser = template_parser

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
              self.embedding_client.embed_text(text )
              for text in texts
         ]
        
        check = []
        for idx, text in enumerate(texts):
              v = self.embedding_client.embed_text(text)
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

         collection_name  =self.create_collection_name(project_id=project.project_id)

         #step 2 : get text embedding vector 
         vector = self.embedding_client.embed_text(texts )
         
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
    

    def answer_rag_question(self ,project:Project , query:str , limit:int = 10):
         
         # step 1 : retrieve related documents 

         retrived_documents = self.search_vector_db_collection(
              
              project=project,
              texts = query ,
              limit = limit,
         )
         
         if not retrived_documents  :
              return None , None  , None
         
         # step 2 : construct LLM prompt 

         system_prompt = self.template_parser.get('rag' , 'system_prompt')
         document_prompts = []
         
         for idx, doc in enumerate(retrived_documents):
               prompt = self.template_parser.get(
                    "rag",
                    "document_prompt",
                    {
                         "doc_no": idx + 1,
                         "content":self.generatoin_client.process_text( doc["text"])
                    }
               )

               print("Generated document prompt:", repr(prompt))

               if prompt is None:
                    raise ValueError(
                         "TemplateParser returned None for rag.document_prompt. "
                         "Check that locales/en/rag.py exists and contains document_prompt."
                    )

               document_prompts.append(prompt)

         documents_prompt = "\n".join(document_prompts)

         
         footer_prompt = self.template_parser.get(
    "rag",
    "footer_prompt",
    {
        "query": query
    }
)

         chat_history  = [
              self.generatoin_client.construct_prompt(
                   prompt = system_prompt,
                   role = self.generatoin_client.enums.SYSTEM.value
              )
         ]
         
         full_prompt = '\n\n'.join([documents_prompt , footer_prompt] )
         answer = self.generatoin_client.generate_text(full_prompt , chat_history)

         return answer , full_prompt , chat_history
             
    






