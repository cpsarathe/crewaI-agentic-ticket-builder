from crewai.tools import tool
import pandas as pd
import logging

class FileUtils:
    
    @tool("Read CSV File")
    def read_csv(file_path: str):
        """Reads a CSV file and returns the content as a string."""
        try:
            df = pd.read_csv(file_path)
            return df.to_string(index=False)
        except Exception as e:
            logging.getLogger(__name__).exception("read_csv failed file_path=%s", file_path)
            return f"Error reading file: {str(e)}"

    @tool("Save Tickets to File")
    def save_to_file(content: str,fileName: str):
        """Saves text content to a file named 'final_tickets.md'."""
        try:
            with open(fileName, 'w') as f:
                f.write(content)
            return "Successfully saved tickets to final_tickets.md"
        except Exception as e:
            logging.getLogger(__name__).exception("save_to_file failed fileName=%s", fileName)
            return f"Error saving file: {str(e)}"