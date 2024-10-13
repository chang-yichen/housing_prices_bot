import pandas as pd
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Set up OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def get_data_summary(data):
    summary = f"""
    Data Summary:
    - **Time Range**: {data['month'].min()} to {data['month'].max()}
    - **Total Records**: {len(data)}
    - **Unique Towns**: {', '.join(data['town'].unique())}
    - **Unique Flat Types**: {', '.join(data['flat_type'].unique())}
    - **Price Range**: ${data['resale_price'].min()} to ${data['resale_price'].max()}
    - **Storey Ranges**: {', '.join(data['storey_range'].unique())}
    - **Unique Floor Areas**: {', '.join(data['floor_area_sqm'].astype(str).unique())}
    - **Unique Flat Models**: {', '.join(data['flat_model'].unique())}
    - **Remaining Lease Periods**: {', '.join(data['remaining_lease'].astype(str).unique())}    - Time range: {data['month'].min()} to {data['month'].max()}
    - Total records: {len(data)}
    - Towns: {', '.join(data['town'].unique())}
    - Flat types: {', '.join(data['flat_type'].unique())}
    - Price range: ${data['resale_price'].min()} to ${data['resale_price'].max()}
    """
    return summary

def query_dataframe(data, query):
    try:
        result = eval(query)
        if isinstance(result, pd.DataFrame):
            return result
        elif isinstance(result, pd.Series):
            return result
        elif isinstance(result, np.ndarray):
            return result
        else:
            return result
    except Exception as e:
        return f"Error executing query: {str(e)}"

def process_query(data, user_query):
    # Prepare context for the AI
    context = f"""
    You are an AI assistant that answers questions about Singapore housing prices.
    You have access to a pandas DataFrame 'data' with the following columns:
    {', '.join(data.columns)}

    {get_data_summary(data)}

    You can query the DataFrame using Python pandas syntax. To do this, use the following format in your response:
    [QUERY]data.your_pandas_query_here[/QUERY]

    For example, to get the average resale price, you would use:
    [QUERY]data['resale_price'].mean()[/QUERY]

    Make sure you dont assign variable name to the query. e.g. dont assign data_2020 = query

    Please answer the following query based on this information. Use DataFrame queries when necessary to provide accurate and specific answers.
    If multiple steps are required, use separate [QUERY] blocks for each step and explain the purpose of each query.

    Query: {user_query}
    """
    # Always explain your calculation process step by step before providing the final result.
    # Get AI response
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": user_query}
        ]
    )

    ai_response = response.choices[0].message.content

    # Execute any DataFrame queries in the AI's response
    while "[QUERY]" in ai_response and "[/QUERY]" in ai_response:
        start = ai_response.index("[QUERY]") + 7
        end = ai_response.index("[/QUERY]")
        query = ai_response[start:end]
        print(query)

        result = query_dataframe(data, query)
        
        # Format the result based on its type
        if isinstance(result, pd.DataFrame):
            result_str = f"\n{result.head().to_string()}\n...(showing first 5 rows)"
        elif isinstance(result, pd.Series):
            result_str = f"\n{result.head().to_string()}\n...(showing first 5 items)"
        elif isinstance(result, np.ndarray):
            result_str = str(result)
        else:
            result_str = str(result)
        
        ai_response = ai_response.replace(f"[QUERY]{query}[/QUERY]", "Answer: " + result_str)

    return ai_response

# You may want to keep some of your existing functions for specific queries
def get_average_price_by_year(data, year):
    filtered_data = data[data['month'].str.startswith(str(year))]
    if filtered_data.empty:
        return None
    return filtered_data['resale_price'].mean()

def get_average_price_by_town(data, town):
    filtered_data = data[data['town'].str.upper() == town.upper()]
    if filtered_data.empty:
        return None
    return filtered_data['resale_price'].mean()

# Additional helper functions can be added here as needed