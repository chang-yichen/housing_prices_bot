import streamlit as st

def main():
    st.title("About Us")
    
    st.header("Project Scope")
    st.write("""
        This project aims to provide an intuitive interface for querying and analyzing housing resale prices based on various factors such as month, town, flat type, and more.
    """)

    st.header("Objectives")
    st.write("""
        - Enable users to ask generic questions about housing prices.
        - Allow users to filter data based on multiple criteria.
        - Present insights and visualizations to help users understand the housing market.
    """)

    st.header("Data Sources")
    st.write("""
        The data used in this application comes from [https://data.gov.sg/collections/189/view].
    """)

    st.header("Features")
    st.write("""
        - Able to ask generic questions using natural language. (Query Page)
        - Interactive data filtering. (Data Summary Page)
    """)

if __name__ == "__main__":
    main()
