
from crewai.tools import tool
import os
import requests
import pandas as pd
import numpy as np
import sys
import io
import matplotlib.pyplot as plt

@tool("filecheck")
def filecheck(file_path: str) -> str:
    """Check if a file exists at the given path."""
    if os.path.exists(file_path):
        return "File exists"
    else:
        return "File does not exist"   
        
@tool("extract_data")
def extract_data(datasource_url: str,datasource_type: str,rows_to_extract: int = 1000) -> str:
    """Extract data from a data source based on its type. rows_to_extract decides how many rows of data to extract"""
    try:
        if datasource_type == "csv":
            return pd.read_csv(datasource_url).head(rows_to_extract)
        elif datasource_type == "json":  
            return pd.read_json(datasource_url).head(rows_to_extract)
        elif datasource_type == "excel":
            return pd.read_excel(datasource_url).head(rows_to_extract)
        else:
            return f"Unsupported data source type for deterministic data extraction using extract_data tool: {datasource_url} so a custom connector code needs to be written"

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
        exec(code, {"pd": pd, "np": np, "plt": plt,"matplotlib": plt})  # Execute with Pandas & Numpy in the global scope
        output = sys.stdout.getvalue()  # Get printed output
    except Exception as e:
        output = f"Error executing code: {e}"
    finally:
        sys.stdout = old_stdout  # Restore original stdout

    return output


@tool("write_file")
def write_file(file_path: str, content: str) -> str:
    """Write content to a file at the specified path."""
    try:
        with open(file_path, "w") as file:
            file.write(content)
        return f"File '{file_path}' written successfully."
    except IOError as e:
        return f"Error writing to file '{file_path}': {e}"