from __future__ import annotations

from crewai import Agent

from src.config import AgentConfig

def feedback_classifier_agent(cfg: AgentConfig) -> Agent:
   mapping = cfg.priority_map
   return Agent(
            role='Feedback Triage Specialist',
            goal=(
               f"Categorizes feedback using NLP (bug, feature request, praise, complaint, spam) with confidence threshold of {cfg.classification_threshold}"
               f" Map categories to priority using: {mapping}."
               f" Default priority is {cfg.default_priority}."
               f" Only accept categories when confidence >= {cfg.classification_threshold}."
            ),
            backstory="You are an NLP linguist. You tag data and assign confidence scores. ",
            verbose=True,
            allow_delegation=False
        )
