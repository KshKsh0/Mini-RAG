from ..VectorDBInterface import VectorDBInterface
from ..VectorDBEnums import DistanceFunction
import uuid
from qdrant_client import QdrantClient , models
from typing import List
import logging

class QdrantDB(VectorDBInterface):

     def __init__(self, db_path:str ,distance_method):
          self.db_path = db_path 
          self.client = None
          print(db_path)

          self.distance_method =None
          if distance_method == DistanceFunction.COSINE.value:
               self.distance_method = models.Distance.COSINE
          elif distance_method ==DistanceFunction.DOT.value:
               self.distance_method = models.Distance.DOT

          self.logger = logging.getLogger(__name__)

     def count_points(self, collection_name: str) -> int:
          res = self.client.count(collection_name=collection_name, exact=True)
          return res.count

     def connect(self):

          self.client = QdrantClient(path = self.db_path)
     
     def disconnect(self):
               self.client = None

     def is_collection_existed(self, collection_name:str)->bool:

               if self.client is None:
                    raise RuntimeError("Qdrant client is not connected. Call connect() first (and ensure it succeeds).")
               return self.client.collection_exists(collection_name=collection_name)    
     def list_all_collection(self)->List:
          return self.client.get_collection()
     
     def get_collection_info(self ,collection_name :str )->dict :
          return self.client.get_collection(collection_name= collection_name)
     
     def delete_collection(self, collection_name:str):
          if self.is_collection_existed(collection_name=collection_name):
               return self.client.delete_collection(collection_name= collection_name)

     def create_collection(self, collection_name :str , embedding_size :int , do_reset:bool=False):
          if do_reset:
               _= self.delete_collection(collection_name=collection_name)


          if not self.is_collection_existed(collection_name=collection_name):
               _= self.client.create_collection(
                    collection_name = collection_name,
                    vectors_config=models.VectorParams(size=embedding_size, distance=self.distance_method),
               )
               
               return True
          
          return False

     def insert_one(self , collection_name :str , text:str , vector :list , 
                    metadata:dict,
                    recored_id:str):
          

          if not self.is_collection_existed(collection_name=collection_name):
               self.logger.error(f'can not insert new record to non-exsited collection')
               return False
          
          _ = self.client.upload_records(
               
               collection_name = collection_name,
               records = [
                    models.record(
                    vector = vector,
                    payload = {'text':text , 'metadata': metadata}
          ) ]
     )
          return True 
     


     def insert_many(self, collection_name , texts :list ,batch_size:int,
                         vectors:list ,metadata:list =None , 
                         record_ids:list =None  ):
          
          if metadata is None:
               metadata = [None] *len(texts)

          if record_ids is None:
                    record_ids = [str(uuid.uuid4()) for _ in texts]
          
          print("texts:", len(texts))
          print("vectors:", len(vectors))
          print("metadata:", len(metadata) if metadata else None)
          print("first vector dim:", len(vectors[0]) if vectors else None)
          print("any None vectors:", any(v is None for v in vectors))

          for i in range(0 , len(texts) , batch_size):
               batch_end = i +batch_size
               batch_texts = texts[i :  batch_end]
               batch_vectors = vectors[i: batch_end]
               batch_ids = record_ids[i:batch_end]
               batch_metadata = metadata[i :batch_end]
               print(f"start the points creation for {batch_size}")
               points = [
                              models.PointStruct(
                                   id=_id,
                                   vector=vec,
                                   payload={"text": txt, "metadata": meta},
                              )
                              for _id, vec, txt, meta in zip(batch_ids, batch_vectors, batch_texts, batch_metadata)
                              ]

               try:
                    self.client.upsert(collection_name=collection_name, points=points)
               except Exception as e:
                    self.logger.error(f"Error while insert batches {e}")
                    return False
          
          print("COLLECTION:", collection_name)
          print("POINT COUNT:", self.count_points(collection_name))
          return True



     def search_by_vector(self ,collection_name :str , vector:List , limit:int = 5,
                              query_filter=None,
     with_payload: bool = True,
     with_vectors: bool = False,):
               
               return self.client.query_points(
          collection_name=collection_name,
          query=vector,               # dense vector = nearest neighbor search
          limit=limit,
          query_filter=query_filter,
          with_payload=with_payload,
          with_vectors=with_vectors,
     )

          
     

     


     
