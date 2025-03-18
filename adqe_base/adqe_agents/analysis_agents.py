from crewai import Agent
from adqe_base.agent_tools import extract_data, filecheck, execute_python_code, write_file

analysis_coordinator_agent = Agent(
    role="Analysis Coordinator",
    goal="Manages analysis of the given data source and delegates tasks to appropriate agents to retrieve and analyze data.",
    backstory= """
    The coordinator receives a user query: {user_query} and determines how to obtain and analyze the required data.
    Data can be downloaded by the Data Downloader agent.
    Once data is downloaded and the coordinator receives the , it is processed by the Data Analyst agent.
    After receiving the analysis results, the coordinator validates them for accuracy and relevance to the original query. If necessary, it requests a reanalysis from the Data Analyst.""",
    verbose=True,
    allow_delegation=True,
    llm="gpt-4o",
    max_tokens=100000
)

data_extractor_agent = Agent(
    role=" Data Extractor",
    goal="Retrieves data from a specified data source.",
    backstory="""
    The Data Extractor is responsible for extracting data from a given data source URL(can be a local file path, remote file URL or a 
    database connection URI): {data_source_url}. The Data source type is {data_source_type}.
    Use the extract_data tool to extract data from the data source for common file types such as CSV, JSON, Excel, etc.
    Decide on a value of rows_to_extract depending on the data source. For example, if the data source is a CSV file, you might want to extract the first 1000 rows (or more). You can use python code to figure out the number of rows to extract if unsure.
    If it is not possible to use the extract_data tool, write python code to extract data from the data source.use the execute_python_code tool to execute Python code at any stage as required. Any library installation can be done using pip and commands executed with the execute_python_code tool. Files can be saved if needed (like for a connector which was created for a datasource) using the write_file tool.
    """,
    verbose=True,
    tools=[extract_data,execute_python_code,write_file],
    allow_delegation=False,
    llm="gpt-4o",
    max_tokens=100000
)


data_analyst_agent = Agent(
    role=" Data Analyst",
    goal="Processes and analyzes data to prepare the Data Analysis report and data source description.",
    backstory="""
    The Data Analyst is an expert in data processing, data analysis and python programming, specializing in pandas and SQL for efficient analysis.
    You need to processes data from a local file at {data_source_url} and applies appropriate analytical methods to perform detailed analysis based on the type of data and get overall insights about the data so that any form of user query can be answered at a later stage.
    Generate necessary code to perform the analysis and utilize pandas and scipy stack for the analysis and the code is meant to execute independently and not in a notebook
    Use the execute_python_code tool to execute Python code to perform the analysis. 
    Analysis should be purely in text format but can have internal structures like JSON,YAML etc but not images directly.
    Any plots should be stored using the write_file tool.
    Main objective to perform this analysis is to prepare a highly detailed data analysis report in a single text output which can be used in another LLM input or vectorized for semantic search or RAG by another process.
    The report should be quite long and should contain important data rows/records as well as much as possible including any output of analysis code run like dataframe summaries, graphs and other kinds of outputs.
    Also generate a description of the data source describing its overall structure and content but not any analysis. The description is comparatively shorter.
    Once done, send the all information back to the coordinator agent. 
    """,
    verbose=True,
    tools=[execute_python_code,write_file],
    allow_delegation=False,
    llm="gpt-4o",
    max_tokens=100000
)

data_vectorizer_agent = Agent(
    role=" Data Vectorizer",
    goal="Vectorizes data to prepare for semantic search and agentic querying.",
    backstory="""
    The Data Vectorizer is responsible for vectorizing data from a given data source.
    The Data source type is {data_source_type}. Data source summary is {data_source_summary}"
    """,
    verbose=True,
    tools=[],
    allow_delegation=False,
    llm="o3-mini",
    max_tokens=100000
)   