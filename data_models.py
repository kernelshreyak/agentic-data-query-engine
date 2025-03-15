from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
import uuid

Base = declarative_base()

from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# SQLAlchemy Models
class DataSourceModel(Base):
    __tablename__ = "data_sources"

    datasource_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    datasource_type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    datasource_summary = Column(String, nullable=True)
    datasource_url = Column(String, nullable=False)

class TaskModel(Base):
    __tablename__ = "tasks"

    task_id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    rq_job_id = Column(String, nullable=True)
    task_type = Column(String, nullable=False)
    task_status = Column(String, nullable=False,default="pending")
    data_source_id = Column(UUID, nullable=False)

# Pydantic Models
class DataSource(BaseModel):
    name: str
    datasource_type: str
    description: str = "n/a"
    datasource_summary: str = "n/a"
    datasource_url: str = "n/a"

class Task(BaseModel):
    task_id: str
    task_type: str
    task_status: str    

class AnalysisRequest(BaseModel):
    data_source_id: str
    user_query: str

class AnalysisTaskResponse(BaseModel):
    analysis_summary_report: str