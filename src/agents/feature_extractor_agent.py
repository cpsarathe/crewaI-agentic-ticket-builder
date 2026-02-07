from crewai import Agent

def feature_extractor_agent() -> Agent:
  return Agent(
            role='Feature Extractor',
            goal='Identifies feature requests and estimates user impact/demand with confidence scores',
            backstory="You are a team member who receives this user feedback report of your applicaiton from diverse sources , once you process your output will be used to create tickets like JIRA",
            verbose=True,
            allow_delegation=False
        )
