from crewai import Agent
from adqe_base.agent_tools import extract_data, filecheck, execute_python_code

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

data_extractor_agent = Agent(
    role=" Data Extractor",
    goal="Retrieves data from a specified data source.",
    backstory="""
    The Data Extractor is responsible for extracting data from a given data source URL(can be a local file path, remote file URL or a 
    database connection URI): {data_source_url}.
    Use the extract_data tool to extract data from the data source for common file types such as CSV, JSON, Excel, etc."
    If it is not possible to use the extract_data tool, use the execute_python_code tool to execute Python code to extract data from the data source (retry 5 times if code does not work).
    Data source type: {data_source_type}
    """,
    verbose=True,
    tools=[extract_data,execute_python_code],
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
