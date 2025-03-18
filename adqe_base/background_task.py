# ADQE Task Handler

from data_models import SessionLocal,TaskModel,DataSourceModel
from rq.job import get_current_job
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
    try:
        datasource = db.query(DataSourceModel).filter(DataSourceModel.datasource_id == data_source_id).first()
        if datasource.datasource_type == "analysis":
            response = analysis_team.kickoff(inputs={"user_query": task_input,"data_source_url": datasource.datasource_url,"data_source_type": datasource.datasource_type,"data_source_id": data_source_id})

            datasource.datasource_summary = response.raw
        elif datasource.datasource_type == "query":
            # TODO: implement agentic query kickoff
            pass
        else:
            response = "Unsupported data source type"
        task.task_status = "completed"
        print("task response",response)
    except Exception as e:
        print("Task failed. Error: ",e)
        task.task_status = "failed"
    
    db.commit()
    
    return
