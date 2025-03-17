# ADQE Task Handler

from data_models import SessionLocal,TaskModel,DataSourceModel
from rq.job import get_current_job
import os
from adqe_base.agent_teams import analysis_team

def analysis_task_execution(task_input: str,data_source_id: str) -> None:
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

    datasource = db.query(DataSourceModel).filter(DataSourceModel.data_source_id == data_source_id).first()

    response = analysis_team.kickoff(inputs={"user_query": task_input,"data_source_url": datasource.datasource_url})

    task.task_status = "completed"
    db.commit()
    print(response)
    return
