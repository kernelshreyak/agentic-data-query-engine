from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()
# SQLAlchemy Models
class DataSourceModel(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    datasource_type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    datasource_summary = Column(String, nullable=True)
    datasource_url = Column(String, nullable=False)




# Pydantic Models
class DataSource(BaseModel):
    name: str
    datasource_type: str
    description: str = "n/a"
    datasource_summary: str = "n/a"
    datasource_url: str = "n/a"

class AnalysisRequest(BaseModel):
    data_source_id: int
    user_query: str