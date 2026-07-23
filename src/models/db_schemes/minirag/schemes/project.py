from sqlalchemy import Column, Integer, String, Text , DateTime , func
from .minirag_base import SQLAlchemeybase
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

import uuid

class Project(SQLAlchemeybase):
    __tablename__='projects'
    
    #in theory we can have both but usually we choose one and the best is uuid for security , more common in this kind of db creation but for sake of learning i ll do both 
    project_id = Column(Integer, primary_key=True , autoincrement=True)
    project_uuid = Column(UUID(as_uuid=True), default=uuid.uuid4, unique=True, nullable=False)
    created_at = Column(DateTime(timezone =True) , server_default = func.now() , nullable = False )
    updated_at = Column(DateTime(timezone = True), onupdate = func.now(), nullable =True)
    
    assets = relationship(
        "Asset",
        back_populates="project",
    )   
        
    chunks = relationship(
    "DataChunk",
    back_populates="project",
)