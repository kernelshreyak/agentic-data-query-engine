from crewai import Agent
import yaml
from agent_tools import download_data, filecheck, execute_python_code

agents_data = None
with open("agents.yaml", 'r') as file:
    agents_data = yaml.safe_load(file)

# define agents
coordinator_agent = Agent(
    role="Coordinator",
    goal="Manages user queries and delegates tasks to appropriate agents to retrieve and analyze data.",
    backstory= """
    The coordinator receives a user query: {user_query} and determines how to obtain and analyze the required data.
    If the data source is a local file, it verifies its existence using the filecheck tool. If the file exists, the coordinator assigns the task to the Data Analyst for processing.
    If the data source is a URL, it first delegates the task to the Data Downloader to retrieve the file, then assigns the downloaded file to the Data Analyst for processing.
    After receiving the analysis results, the coordinator validates them for accuracy and relevance to the original query. If necessary, it requests a reanalysis from the Data Analyst.""",
    verbose=True,
    tools=[filecheck],
    allow_delegation=True,
    llm="gpt-4o"
)

data_downloader_agent = Agent(
    role=" Data Downloader",
    goal="Retrieves data from a specified source.",
    backstory="""
    The Data Downloader is responsible for downloading data from a given source URL: {data_source_url}.
    If the provided source is invalid or inaccessible, it returns an error message: "Invalid data source."
    """,
    verbose=True,
    tools=[download_data],
    allow_delegation=False,
    llm="gpt-4o-mini"
)

data_analyst_agent = Agent(
    role=" Data Analyst",
    goal="Processes and analyzes data to prepare the Data Summary JSON.",
    backstory="""
    The Data Analyst is an expert in data processing and Python programming, specializing in pandas and SQL for efficient analysis.
    It processes data from a local file at {data_source_url} and applies appropriate analytical methods to answer the user query: {user_query}.
    If the data is in JSON format, it converts it into a pandas DataFrame for faster processing.
    The analyst executes well-formatted Python or SQL code as needed, ensuring that results are properly printed for correct output retrieval.

    """,
    verbose=True,
    tools=[execute_python_code],
    allow_delegation=False,
    llm="gpt-4o"
)
