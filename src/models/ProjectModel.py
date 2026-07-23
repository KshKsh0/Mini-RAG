from .BaseDataModel import BaseDataModel
from .db_schemes import Project
from .enums.DataBaseEnum import DataBaseEnum
from sqlalchemy import select
from sqlalchemy import func

class ProjectModel(BaseDataModel):
    

    def __init__(self,db_client:object):
        super().__init__(db_client=db_client)

        self.db_client = db_client

    @classmethod
    async def create_instance(cls , db_client:object):
        return cls(db_client) 
    
    async def create_project(self , project :Project):
       async with self.db_client() as session:
           async with session.begin():
               session.add(project)
               await session.commit()
               await session.refresh(project)

       return project

    async def get_project_or_create_one(self , project_id:int):
        project_id = int(project_id)

      
        async with self.db_client() as session:
            async with session.begin():
                query = select(Project).where(
    Project.project_id == project_id
)

                result = await session.execute(query)
                project = result.scalar_one_or_none()

            if project is not  None:
                return project
            # we dont need to create multiple sessions , that will cause confilcts and error in long term so any opperation must be in the same session
            project=Project(project_id = project_id)
            session.add(project)
            await session.commit()
            await session.refresh(project)
            return project

    

    async def get_all_projects(self, page:int =1  , page_size = 10):
            
            async with self.db_client() as session:
                    total_docs = await session.execute(select(
                        func.count(Project.project_id)
                    ))

                    total_docs = total_docs.scalar_one()
                    total_pages = (total_docs + page_size - 1) // page_size
                    if total_pages % page_size > 0:
                           total_pages += 1
                    query = select(Project).order_by(Project.project_id).offset((page - 1) * page_size ).limit(page_size)
                    result = await (session.execute(query).scalars().all())
                    return result , total_pages
