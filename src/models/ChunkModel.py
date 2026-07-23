from .BaseDataModel import BaseDataModel
from .enums.DataBaseEnum import DataBaseEnum
from .db_schemes import DataChunk
from sqlalchemy import select , delete , func
from pymongo import InsertOne

class ChunkModel(BaseDataModel):

    def __init__(self, db_client:object ):
        super().__init__(db_client = db_client)
        self.db_client = db_client
    
    @classmethod
    async def create_instance(cls , db_client:object):
        instance =cls(db_client)
        return instance 
    
    
   

    async def create_chunk(self , chunk :DataChunk):
        async with self.db_client() as session:
           async with session.begin():
               session.add(chunk)
           await session.commit()
           await session.refresh(chunk)

        return chunk

    
    async def get_chunk(self, chunk_id:str):
        async with self.db_client() as session:
            res = await session.exectue(DataChunk).where(DataChunk.chunk_id == chunk_id)
            chunk= res.scalar_one_or_none()
        return chunk

    
    async def insert_many_chunk(self, chunks:list ,batch_size = 100):
        async  with self.db_client() as session:
            async with session.begin():
                for i in range(0 , len(chunks) , batch_size):
                    batch = chunks[i : i+batch_size]
                    session.add_all(batch)
                    await session.flush()
                await session.commit()
        return len(chunks)

    
    async def delete_chunks_by_project_id(self, project_id:object):
        async with self.db_client() as session:
            stmt = delete(DataChunk).where(DataChunk.chunk_project_id == project_id)
            res = await session.execute(stmt)
            await session.commit()
        return res.rowcount

    async def get_project_chunk(self , project_id:object,page_no :int = 1, page_size :int = 50 ):
        async with self.db_client() as session:
            query = select(DataChunk).where(DataChunk.chunk_project_id == project_id).offset((page_no-1)* page_size).limit(page_size)
            res = await session.execute(query)
            records = res.scalars().all()
        return records