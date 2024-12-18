import pandas as pd

def process_response(response):
    """
    Process the LLM response to extract metadata and structure the DataFrame.

    Args:
        response (dict): The JSON response from the LLM containing metadata and dataframe_structure.

    Returns:
        tuple: A dictionary with metadata and a pandas DataFrame.
    """
    if not isinstance(response, dict):
        raise ValueError("Expected a dictionary response, got a non-dictionary object.")

    try:
        # Extract metadata
        metadata = response.get("metadata", {})
        print("Metadata:", metadata)

        # Extract DataFrame structure
        dataframe_structure = response.get("dataframe_structure", {})
        columns = dataframe_structure.get("columns", [])
        data = dataframe_structure.get("data", [])

        # Create the DataFrame
        df = pd.DataFrame(data, columns=columns)

        print("DataFrame Preview:")
        print(df.head())

        # Return both metadata and DataFrame for further processing
        return metadata, df

    except Exception as e:
        print(f"Error processing response: {e}")
        return None, None

