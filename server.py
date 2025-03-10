from crewai import Agent, Crew, Process,Task
from crewai.project import CrewBase, agent, crew
from crewai.tools import tool
import requests
import os
import yaml


agents_data = None
with open("../agents.yaml", 'r') as file:
    agents_data = yaml.safe_load(file)


coordinator_agent = Agent(
    role="Coordinator",
    goal="Accepts user query and coordinates team of agents to answer the query using the available data source(s)  ",
    backstory="The coordinator accepts user query: {user_query} and coordinates team of agents to answer the query using the available data source(s). If the data is not locally available, it should be downloaded",
    verbose=True,
)

analysis_task = Task(
    description="""
        Based on the requirement: {requirement}
        Make sure you find any interesting and relevant information given
        the current year is 2025.
    """,
    expected_output="""
        A list with 10 bullet points of the most relevant information about AI Agents
    """,
    agent=coordinator_agent
)

crew = Crew(
    agents=[coordinator_agent],
    tasks=[],
    verbose=True
)

crew = Crew(
    agents=[coordinator_agent],
    tasks=[analysis_task],
    verbose=True
)

crew.kickoff()
