
from crewai import Crew
from adqe_base.adqe_agents.analysis_agents import analysis_coordinator_agent, data_extractor_agent, data_analyst_agent
from adqe_base.adqe_agents.querying_agents import querying_coordinator_agent
from adqe_base.agent_tasks import analysis_task

# Analysis crew that performs data analysis tasks
analysis_team = Crew(
    agents=[analysis_coordinator_agent,data_extractor_agent,data_analyst_agent],
    tasks=[analysis_task],
    verbose=True
)

querying_team = Crew(
    agents=[querying_coordinator_agent],
    tasks=[analysis_task],
    verbose=True
)
