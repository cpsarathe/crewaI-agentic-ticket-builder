from __future__ import annotations

from crewai import Agent

from src.config import AgentConfig

def bug_analyzer_agent(cfg: AgentConfig) -> Agent:
   mapping = cfg.priority_map

   return Agent(
            role='Bug Analyst',
            goal=(
                "Extracts technical details: steps to reproduce, platform info, severity assessment "
                f"Ensure ticket priority matches category using mapping: {mapping}. "
                "If mismatch, flag it in output."
            ),
            backstory="You are a team member who receives this bug report of your applicaiton from diverse sources , once you process your output will be used to create tickets like JIRA",
            verbose=True,
            allow_delegation=False
        )
