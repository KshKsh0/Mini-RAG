from .BaseDataModel import BaseDataModel
from .db_schemes import Assets
from .enums.DataBaseEnum import DataBaseEnum
from bson import ObjectId



class AssetModel(BaseDataModel):
    def __init__(self, db_client:object):
        super().__init__(db_client=db_client)
        self.collection = db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]




    @classmethod
    async def create_instance(cls , db_client:object):
        instance =cls(db_client)
        await instance.init_collection()
        return instance 
    
    
    async def init_collection(self):
        all_collection = await self.db_client.list_collection_names()
        if DataBaseEnum.COLLECTION_ASSET_NAME.value not in all_collection:
            self.collection = self.db_client[DataBaseEnum.COLLECTION_ASSET_NAME.value]
            indexes = Assets.get_index()
            for index in indexes:
                await self.collection.create_index(index['key'] , name = index['name'] , unique = index['unique'])
    
    

    async def create_asset(self , assets : Assets):
        doc = assets.model_dump(by_alias = True , exclude_none = True)
        res =await self.collection.insert_one(doc)
        assets.id = res.inserted_id 
        return assets
    
    async def get_all_project_assets(self ,assets_project_id :str , asset_type:str):
        
        records = await self.collection.find({

            'asset_project_id' : ObjectId(assets_project_id) if assets_project_id is  isinstance(assets_project_id ,str) else assets_project_id
,           'asset_type':asset_type
        }).to_list(length = None)

        return [
                Assets(**record)
            for record in records
        ]
    async def get_asset_record(self , asset_project_id:str , asset_name:str ):
        rec = await self.collection.find_one({

            'asset_project_id' : ObjectId(asset_project_id) if asset_project_id is  isinstance(asset_project_id ,str) else asset_project_id,
            'asset_name':asset_name
        })
        if rec :
            return Assets(**rec)
        return None 