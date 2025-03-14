
from crewai import Crew
from agents import coordinator_agent, data_downloader_agent, data_analyst_agent
from agent_tasks import analysis_task

analysis_team = Crew(
    agents=[coordinator_agent,data_downloader_agent,data_analyst_agent],
    tasks=[analysis_task],
    verbose=True
)
