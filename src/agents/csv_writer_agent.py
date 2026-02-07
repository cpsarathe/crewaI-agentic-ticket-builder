from crewai import Agent
from src.tools.FileUtils import FileUtils

def csv_writer_agent() -> Agent:
    return Agent(
        role="CSVWriter",
        goal="Writes data to CSV file with given name of the file",
        backstory="You will receive the CSV content and file name you are good in writing csv files",
        tools=[FileUtils.save_to_file],
        verbose=True,
        allow_delegation=False
    )
