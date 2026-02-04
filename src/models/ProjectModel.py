from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum

class ProjectModel(BaseDataModel):
    

    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_PROJECT_NAME.value]
    
    async def create_project(self , project :Project):
        doc = project.model_dump(by_alias = True , exclude_none = True)
        res = await self.collection.insert_one(doc) # Project pydantic class --> dict cause mongo accept jsons 
        project._id = res.inserted_id
        return project._id

    async def get_project_or_create_one(self , project_id:str):
        record = await self.collection.find_one({

            'project_id' : project_id
        })
        if record is None:
            #create new project 
            project= Project(project_id=project_id)
            project = await self.create_project(project)

            return project
        
        return Project(**record)  
    

    # dont use get_all without baggination how many pages and size of each page 
    async def get_all_projects(self, page:int =1  , page_size = 10):
        #count total number of docs 
        total_docs = await self.collection.count_documents({}) 


        #simple toal pages 
        total_pages =total_docs // page_size
        if total_pages % page_size > 0:
            total_pages+=1

        curser=self.collection.find().skip((page-1) * page_size).limit(page_size)
        projects = []
        async for doc in curser:
            projects.append(Project(**doc))
        return projects , total_pages



