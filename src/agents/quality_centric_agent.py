from crewai import Agent

def quality_centric_agent() -> Agent:
  return Agent(
            role='Quality Centric Agent',
            goal='Reviews generated tickets for completeness and accuracy ',
            backstory="You will receive feature or bug request ticket in structured format and you need to assess the accuracy of the generated content",
            verbose=True,
            allow_delegation=False
        )
