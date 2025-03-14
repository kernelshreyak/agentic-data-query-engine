from crewai import Task
from adqe_agents.analysis_agents import analysis_coordinator_agent

# define tasks
analysis_task = Task(
    description="""
        Analyze the data present at {data_source_url} and perform tasks neccessary to answer the user query: {user_query}
    """,
    expected_output="""
        A data analysis report in text as per the user query
    """,
    agent=analysis_coordinator_agent
)