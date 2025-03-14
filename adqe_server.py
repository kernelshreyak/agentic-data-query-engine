from fastapi import FastAPI, Depends
from sqlalchemy import create_engine,inspect
from sqlalchemy.orm import sessionmaker, Session
from data_models import DataSource, DataSourceModel
from sqlalchemy.ext.declarative import declarative_base
Base = declarative_base()

import os
from dotenv import load_dotenv

load_dotenv()

# Database Configuration
DATABASE_URL = os.environ["DATABASE_URL"]

engine = create_engine(DATABASE_URL)
inspector = inspect(engine)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# Create tables (only if they don't exist)
if not inspector.has_table("data_sources"):
    Base.metadata.create_all(bind=engine)

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

# POST endpoint - Perform Analysis Phase on the data source
@app.post("/datasources/analyze")
def add_data_source(data: DataSource, db: Session = Depends(get_db)):
    new_data_source = DataSourceModel(**data.dict())
    db.add(new_data_source)
    db.commit()
    db.refresh(new_data_source)
    return {"message": "Data source added successfully", "data_source": new_data_source}