# ADQE Task Handler

from crewai import LLM
from data_models import AnalysisTaskResponse
from data_models import SessionLocal,TaskModel
from rq.job import get_current_job
import os

def analysis_task_execution(task_input: str,data_source_id: int) -> None:
    db = SessionLocal()
    task = db.query(TaskModel).filter(
        TaskModel.data_source_id == data_source_id, 
        TaskModel.task_type == "analysis", 
        TaskModel.rq_job_id == get_current_job().id
    ).first()
    if not task:
        print("Task not found in the database")
        return
    print(f"""Task {task.task_id} started for data source {data_source_id} TASK_TYPE: {task.task_type} """)
    llm = LLM(model="gpt-4o-mini",api_key=os.environ["OPENAI_API_KEY"],response_format=AnalysisTaskResponse)
    response = llm.call(task_input)
    task.task_status = "completed"
    db.commit()
    print(response)
    return
