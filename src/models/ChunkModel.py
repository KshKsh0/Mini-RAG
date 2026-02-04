from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemes import DataChunk
from bson.objectid import ObjectId
from pymongo import InsertOne

class ChunkModel(BaseDataModel):

    def __init__(self, db_client:object ):
        super().__init__(db_client = db_client)
        self.collection = db_client[DataBaseEnum.COLLECTION_CHUNK_NAME.value]
    async def create_chunk(self , chunk :DataChunk):
        doc = chunk.model_dump(by_alias = True ,exclude_none = True )
        res = await self.collection.insert_one(doc)
        chunk._id =res.inserted_id
        return chunk
    
    async def get_chunk(self, chunk_id:str):
        res = await self.collection.find_one({
            '_id':ObjectId(chunk_id)
        })
        if res is None:
            return None
        
        return DataChunk(**res)
    
    async def insert_many_chunk(self, chunks:list ,batch_size = 100):
        for i in range(0 , len(chunks) , batch_size):
            batch = chunks[i : i+batch_size]
            operations = [
                InsertOne(chunk.model_dump(by_alias = True ,exclude_none = True )) 
                for chunk in batch
                
            ]
            await self.collection.bulk_write(operations)
        return len(chunks)
    
    async def delete_chunks_by_project_id(self, project_id:ObjectId):
        res = await self.collection.delete_many({'chunk_project_id' :project_id}
                                                )   
        return res.deleted_count
