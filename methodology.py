import streamlit as st

def main():
    st.title("Methodology")

    st.subheader("First use case")
    st.write("""
        The first use case is querying based on natural language (query page). 
        This is done by loading 5 csv data into a pandas dataframe and caching it. 
        Afterwards a summary of the data is generated using python code from the dataframe and is included in the system prompt.
        The system prompt and user query is then passed to gpt-4o-mini model through the openai api.
        The model then generates a response which includes pandas query which are used to query the pandas dataframe to add values to 
        the response before outputing to the user.""")
    st.subheader("Second use case")
    st.write("""
        The second functionality make use of the same dataframe, allowing users to apply filters based on each column 
        and see the average resale prices in a bar chart and also a data summary of the data.""")

    st.header("Flowcharts")
    
    st.subheader("Use Case 1: Query with natural language")
    st.image("query.png", caption="Flowchart for Query with natural language")
    
    st.subheader("Use Case 2: Interactive data summary")
    st.image("data_summary.png", caption="Flowchart for Interactive data summary")

if __name__ == "__main__":
    main()
