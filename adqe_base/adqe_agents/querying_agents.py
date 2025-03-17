from crewai import Agent

querying_coordinator_agent = Agent(
    role="Querying Coordinator",
    goal="Manages querying of the given data source and delegates tasks to appropriate agents to query the data source (utilizing the data source summary).",
    backstory= """
    The coordinator receives a user query: {user_query} and determines how to best query the data source to return the information asked in the user query.
    If the data source is a local file, it verifies its existence using the filecheck tool. If the file exists, the coordinator assigns the task to the Data Analyst for processing.
    If the data source is a URL, it first delegates the task to the Data Downloader to retrieve the file, then assigns the downloaded file to the Data Analyst for processing.
    After receiving the analysis results, the coordinator validates them for accuracy and relevance to the original query. If necessary, it requests a reanalysis from the Data Analyst.""",
    verbose=True,
    # tools=[],
    allow_delegation=True,
    llm="gpt-4o"
)
