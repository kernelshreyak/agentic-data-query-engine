from crewai import Agent
from agent_tools import download_data, filecheck, execute_python_code

analysis_coordinator_agent = Agent(
    role="Analysis Coordinator",
    goal="Manages analysis of the given data source and delegates tasks to appropriate agents to retrieve and analyze data.",
    backstory= """
    The coordinator receives a user query: {user_query} and determines how to obtain and analyze the required data.
    Data can be downloaded by the Data Downloader agent.
    Once data is downloaded and the coordinator receives the , it is processed by the Data Analyst agent.
    After receiving the analysis results, the coordinator validates them for accuracy and relevance to the original query. If necessary, it requests a reanalysis from the Data Analyst.""",
    verbose=True,
    tools=[filecheck],
    allow_delegation=True,
    llm="gpt-4o"
)

data_downloader_agent = Agent(
    role=" Data Downloader",
    goal="Retrieves data from a specified data source.",
    backstory="""
    The Data Downloader is responsible for downloading data from a given data source URL: {data_source_url}.
    If the provided source is invalid or inaccessible, it returns an error message: "Invalid data source."
    """,
    verbose=True,
    tools=[download_data],
    allow_delegation=False,
    llm="gpt-4o"
)

data_analyst_agent = Agent(
    role=" Data Analyst",
    goal="Processes and analyzes data to prepare the Data Summary JSON.",
    backstory="""
    The Data Analyst is an expert in data processing and Python programming, specializing in pandas and SQL for efficient analysis.
    It processes data from a local file at {data_source_url} and applies appropriate analytical methods to perform detailed analysis based on the type of data and get overall insights about the data so that any form of user query can be answered at a later stage.
    Use the execute_python_code tool to execute Python code to perform the analysis.

    """,
    verbose=True,
    tools=[execute_python_code],
    allow_delegation=False,
    llm="gpt-4o"
)
