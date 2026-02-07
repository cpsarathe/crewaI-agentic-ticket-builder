from crewai import Agent
from src.tools.FileUtils import FileUtils

def csv_reader_agent() -> Agent:
    return Agent(
        role="CSVReader",
        goal="Read and organize feedback data from CSV files.",
        backstory="You will receive the CSV content and file name you are good in reading csv files",
        tools=[FileUtils.read_csv],
        verbose=True,
        allow_delegation=False
    )
