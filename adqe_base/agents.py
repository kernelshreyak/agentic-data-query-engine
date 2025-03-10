from crewai.project import CrewBase, agent, crew

agents_data = None
with open("agents.yaml", 'r') as file:
    agents_data = yaml.safe_load(file)
    
# define agents
coordinator_agent = Agent(
    config=agents_data['coordinator'],
    verbose=True,
    tools=[filecheck],
    allow_delegation=True,
    llm="gpt-4o"
)

data_downloader_agent = Agent(
    config=agents_data['data_downloader'],
    verbose=True,
    tools=[download_data],
    allow_delegation=False,
    llm="gpt-4o-mini"
)

data_analyst_agent = Agent(
    config=agents_data['data_analyst'],
    verbose=True,
    tools=[json_to_dataframe,execute_python_code],
    allow_delegation=False,
    llm="gpt-4o"
)


