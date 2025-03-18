from crewai import Task
from adqe_base.adqe_agents.analysis_agents import analysis_coordinator_agent

# define tasks
analysis_task = Task(
    description="""
            Analyze the data present at {data_source_url} and perform detailed analysis on it to get a full picture of the data including all relationships between different parts of it. Any insturctions provided in user query: {user_query} can be used. 
            When working with databases, full schema understanding is to be developed and all the analysis results are to be compiled in a single text output (the data analysis report).
    """,
    expected_output="""
        A data analysis report in text as per the user query
    """,
    agent=analysis_coordinator_agent
)