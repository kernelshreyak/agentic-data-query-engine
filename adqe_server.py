from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from data_models import Base,DataSource, DataSourceModel, AnalysisRequest,TaskModel,get_db
from redis import Redis
from rq import Queue
from adqe_base.background_task import analysis_task_execution

app = FastAPI()

# GET endpoint - List all data sources
@app.get("/datasources/list")
def list_data_sources(db: Session = Depends(get_db)):
    data_sources = db.query(DataSourceModel).all()
    return {"data_sources": data_sources}

# GET endpoint - List all tasks
@app.get("/tasks/list")
def list_tasks(db: Session = Depends(get_db)):
    tasks = db.query(TaskModel).all()
    return {"tasks": tasks}

# POST endpoint - Add a new data source
@app.post("/datasources/add")
def add_data_source(data: DataSource, db: Session = Depends(get_db)):
    new_data_source = DataSourceModel(**data.model_dump())
    db.add(new_data_source)
    db.commit()
    db.refresh(new_data_source)
    return {"message": "Data source added successfully", "data_source": new_data_source}

# POST endpoint - Perform Analysis Phase on the data source
@app.post("/datasources/analyze")
def datasource_analyze(analysis_request: AnalysisRequest, db: Session = Depends(get_db)):
    # create analysis task and enqueue
    task = TaskModel(task_type="analysis", data_source_id=analysis_request.data_source_id)
    q = Queue(connection=Redis())
    job = q.enqueue(analysis_task_execution,analysis_request.user_query, analysis_request.data_source_id)
    task.rq_job_id = job.id
    db.add(task)
    db.commit()
    return {
        "message": "Data source analysis task started", 
        "data_source_id": analysis_request.data_source_id,
        "task_id": task.task_id
    }
