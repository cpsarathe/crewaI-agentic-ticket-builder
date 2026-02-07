from crewai import Agent

def feedback_classifier_agent() -> Agent:
   return Agent(
            role='Feedback Triage Specialist',
            goal='Categorizes feedback using NLP (bug, feature request, praise, complaint, spam) with confidence scores',
            backstory="You are an NLP linguist. You tag data and assign confidence scores. ",
            verbose=True,
            allow_delegation=False
        )
