from fastapi import FastAPI, Depends
from sqlalchemy import Column, Integer, String, create_engine,inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel
import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Model
class DataSourceModel(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    datasource_type = Column(String, nullable=False)
    description = Column(String, nullable=True)
    datasource_summary = Column(String, nullable=True)
    datasource_url = Column(String, nullable=False)

# Create tables (only if they don't exist)
if not inspector.has_table("data_sources"):
    Base.metadata.create_all(bind=engine)

# Pydantic Model
class DataSource(BaseModel):
    name: str
    datasource_type: str
    description: str = "n/a"
    datasource_summary: str = "n/a"
    datasource_url: str = "n/a"

app = FastAPI()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# GET endpoint - List all data sources
@app.get("/datasources/list")
def list_data_sources(db: Session = Depends(get_db)):
    data_sources = db.query(DataSourceModel).all()
    return {"data_sources": data_sources}

# POST endpoint - Add a new data source
@app.post("/datasources/add")
def add_data_source(data: DataSource, db: Session = Depends(get_db)):
    new_data_source = DataSourceModel(**data.dict())
    db.add(new_data_source)
    db.commit()
    db.refresh(new_data_source)
    return {"message": "Data source added successfully", "data_source": new_data_source}
