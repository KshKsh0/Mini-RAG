from .BaseDataModel import BaseDataModel
from .db_schemes import Asset
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId
from sqlalchemy import select , delete , func


class AssetModel(BaseDataModel):
    def __init__(self, db_client:object):
        super().__init__(db_client=db_client)
        self.db_client = db_client



    @classmethod
    async def create_instance(cls , db_client:object):
        instance =cls(db_client)
        return instance 
    
    

    async def create_asset(self , assets : Asset):
        async with self.db_client() as session:
           async with session.begin():
               session.add(assets)
           await session.commit()
           await session.refresh(assets)

        return assets
    
    async def get_all_project_assets(self ,assets_project_id :str , asset_type:str):
        
        async with self.db_client() as session:
            query = select(Asset).where(Asset.project_id == assets_project_id , 
                                         Asset.asset_type == asset_type)
            res = await session.execute(query)
            records = res.scalars().all()
        return records
    async def get_asset_record(self , asset_project_id:str , asset_name:str ):
        async with self.db_client() as session:
            query = select(Asset).where(Asset.asset_project_id == asset_project_id , 
                                         Asset.asset_name == asset_name)
            res = await session.execute(query)
            records = res.scalar_one_or_none()
        return records