from crewai import Agent

def bug_analyzer_agent() -> Agent:
   return Agent(
            role='Bug Analyst',
            goal='Extracts technical details: steps to reproduce, platform info, severity assessment',
            backstory="You are a team member who receives this bug report of your applicaiton from diverse sources , once you process your output will be used to create tickets like JIRA",
            verbose=True,
            allow_delegation=False
        )
