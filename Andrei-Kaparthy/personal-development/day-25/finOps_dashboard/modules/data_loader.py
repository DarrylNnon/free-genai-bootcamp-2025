import base64
import io
import pandas as pd

def parse_contents(contents, filename):
    """
    Parses the uploaded file content and returns a pandas DataFrame.
    """
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            # Basic validation: check for required columns
            required_cols = ['Service', 'UsageStartDate', 'Cost']
            if not all(col in df.columns for col in required_cols):
                return f"Error: CSV must contain the columns: {', '.join(required_cols)}"
            return df
    except Exception as e:
        return f"There was an error processing this file: {e}"
    return "Error: Please upload a valid CSV file."