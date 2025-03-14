
from crewai.tools import tool
import os
import requests
import pandas as pd
import numpy as np
import sys
import io

@tool("filecheck")
def filecheck(file_path: str) -> str:
    """Check if a file exists at the given path."""
    if os.path.exists(file_path):
        return "File exists"
    else:
        return "File does not exist"   
        
@tool("download_data")
def download_data(datasource_url: str,datasource_type: str) -> str:
    """Download data from a given URL and save it to a local file."""
    try:
        response = requests.get(datasource_url, stream=True)
        response.raise_for_status()  # Raise an error for bad responses

        # Extract filename from URL
        filename = datasource_url.split("/")[-1]
        local_file = os.path.join(os.getcwd(), filename)
        
        # check if file exists
        if os.path.exists(local_file):
            return local_file

        # Save file locally
        with open(local_file, "wb") as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)

        return local_file  # Return the path of the downloaded file

    except requests.exceptions.RequestException as e:
        return f"Error downloading file: {e}"

@tool("json_to_dataframe")
def json_to_dataframe(json_data: str):
    """Convert a JSON string into a Pandas DataFrame."""
    try:
        data = pd.read_json(json_data)
        return data
    except ValueError as e:
        return f"Error parsing JSON: {e}"


@tool("execute_python_code")
def execute_python_code(code: str) -> str:
    """
    Execute custom Python code (Pandas/Numpy compatible) and return the printed output.
    """
    # Capture standard output
    old_stdout = sys.stdout
    sys.stdout = io.StringIO()

    try:
        exec(code, {"pd": pd, "np": np})  # Execute with Pandas & Numpy in the global scope
        output = sys.stdout.getvalue()  # Get printed output
    except Exception as e:
        output = f"Error executing code: {e}"
    finally:
        sys.stdout = old_stdout  # Restore original stdout

    return output