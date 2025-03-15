
from crewai.tools import tool
import os
import requests
import pandas as pd
import numpy as np
import sys
import io
from data_models import DataSource

@tool("filecheck")
def filecheck(file_path: str) -> str:
    """Check if a file exists at the given path."""
    if os.path.exists(file_path):
        return "File exists"
    else:
        return "File does not exist"   
        
@tool("extract_data")
def extract_data(datasource: DataSource) -> str:
    """Extract data from a data source based on its type."""
    try:
        if datasource.datasource_type == "csv":
            return pd.read_csv(datasource.datasource_url)
        elif datasource.datasource_type == "json":  
            return pd.read_json(datasource.datasource_url)

    except requests.exceptions.RequestException as e:
        return f"Error extracting data from data source {{datasource.datasource_url}}: {e}"

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