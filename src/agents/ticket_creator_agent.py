from crewai import Agent

def ticket_creator_agent() -> Agent:
  return Agent(
            role='Ticket Creator Agent',
            goal='Generates structured tickets and logs them to output CSV files ',
            backstory="You will receive extracted feature or bugs summary and you need to utilize it to create Atlassian JIRA supported structured content which will then be written to CSV ",
            verbose=True,
            allow_delegation=False
        )
