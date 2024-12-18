import openai
import requests
import os
import json
from dotenv import load_dotenv

load_dotenv()
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")


class LLMAnalyzer:
    @staticmethod
    def analyze_content(file_content):
        prompt = f"""
You are an expert in data analysis. Analyze the following file content and dynamically identify all relevant column headers and corresponding rows for structuring the data into a DataFrame.

Your task:
1. Extract **all feasible column headers** based on the file content.
2. Ignore the examples given below as hard constraints. They are only illustrative. Dynamically identify headers based on the data content provided.

Return the result in JSON format with two keys:
- "dataframe_structure": This should include:
  - "columns": A list of dynamically identified column headers.
  - "data": A nested list where each inner list contains values corresponding to the identified columns.

Example format (but not limited to):
{{
    "dataframe_structure": {{
        "columns": ["Reading Date", "Total kWhs Used", "Average kWhs Per Day"],
        "data": [
            ["2023-08-20", 250, 16],
            ["2023-08-04", 426, 14]
        ]
    }}
}}

Content:
{file_content}

Ensure that:
- Your output dynamically adjusts to the content of the file.
- No unnecessary text or explanation is included. Only the JSON response is required.
"""

        try:
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
                    "Content-Type": "application/json"
                },
                data=json.dumps({
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}]
                })
            )

            # Parse the response JSON
            response_data = response.json()

            # Extract the content from the response
            if "choices" in response_data:
                raw_content = response_data["choices"][0]["message"]["content"]
                return json.loads(raw_content)  # Convert JSON string to dictionary
            else:
                return {"error": "Invalid LLM response format."}

        except requests.RequestException as e:
            return {"error": str(e)}
