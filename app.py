import streamlit as st
from data_loader import load_data
from query_handler import process_query
import pandas as pd
import plotly.express as px
import numpy as np
from auth import check_password 

def display_data_summary(data):
    """Function to display the data summary and visualizations."""
    st.write("### Data Summary")
    
    # Display total entries and columns
    st.write(f"**Total Entries:** {data.shape[0]}")
    st.write(f"**Columns:** {', '.join(data.columns)}")

    # Display sample data in a table
    sample_data = data.sample(min(5, data.shape[0]))  # Get a sample of the data
    st.write("### Sample Data:")
    st.dataframe(sample_data)  # Display sample data in a table format

    # Convert remaining_lease to numeric and handle errors
    data['remaining_lease'] = pd.to_numeric(data['remaining_lease'], errors='coerce')

    # Sidebar filters for various columns
    st.sidebar.header("Filter Data")
    
    # Filter for month
    unique_months = sorted(data['month'].unique())
    unique_months.insert(0, "All")  # Add "All" option
    selected_month = st.sidebar.selectbox("Select Month", options=unique_months)

    # Filter for town
    unique_towns = sorted(data['town'].unique())
    unique_towns.insert(0, "All")  # Add "All" option
    selected_town = st.sidebar.selectbox("Select Town", options=unique_towns)

    # Filter for flat type
    unique_flat_types = sorted(data['flat_type'].unique())
    unique_flat_types.insert(0, "All")  # Add "All" option
    selected_flat_type = st.sidebar.selectbox("Select Flat Type", options=unique_flat_types)

    # Filter for block
    unique_blocks = sorted(data['block'].unique())
    unique_blocks.insert(0, "All")  # Add "All" option
    selected_block = st.sidebar.selectbox("Select Block", options=unique_blocks)

    # Filter for street name
    unique_street_names = sorted(data['street_name'].unique())
    unique_street_names.insert(0, "All")  # Add "All" option
    selected_street_name = st.sidebar.selectbox("Select Street Name", options=unique_street_names)

    # Filter for storey range
    unique_storey_ranges = sorted(data['storey_range'].unique())
    unique_storey_ranges.insert(0, "All")  # Add "All" option
    selected_storey_range = st.sidebar.selectbox("Select Storey Range", options=unique_storey_ranges)

    # Filter for floor area sqm
    unique_floor_areas = sorted(data['floor_area_sqm'].unique())
    unique_floor_areas.insert(0, "All")  # Add "All" option
    selected_floor_area = st.sidebar.selectbox("Select Floor Area (sqm)", options=unique_floor_areas)

    # Filter for flat model
    unique_flat_models = sorted(data['flat_model'].unique())
    unique_flat_models.insert(0, "All")  # Add "All" option
    selected_flat_model = st.sidebar.selectbox("Select Flat Model", options=unique_flat_models)

    # Filter for lease commence date
    unique_lease_dates = sorted(data['lease_commence_date'].unique())
    unique_lease_dates.insert(0, "All")  # Add "All" option
    selected_lease_date = st.sidebar.selectbox("Select Lease Commence Date", options=unique_lease_dates)

    # Filter for remaining lease (excluding NaN values)
    unique_remaining_leases = sorted(data['remaining_lease'].dropna().unique())
    unique_remaining_leases.insert(0, "All")  # Add "All" option
    selected_remaining_lease = st.sidebar.selectbox("Select Remaining Lease", options=unique_remaining_leases)

    # Filter the data based on selections
    filtered_data = data[
        ((selected_month == "All") | (data['month'] == selected_month)) &
        ((selected_town == "All") | (data['town'] == selected_town)) &
        ((selected_flat_type == "All") | (data['flat_type'] == selected_flat_type)) &
        ((selected_block == "All") | (data['block'] == selected_block)) &
        ((selected_street_name == "All") | (data['street_name'] == selected_street_name)) &
        ((selected_storey_range == "All") | (data['storey_range'] == selected_storey_range)) &
        ((selected_floor_area == "All") | (data['floor_area_sqm'] == selected_floor_area)) &
        ((selected_flat_model == "All") | (data['flat_model'] == selected_flat_model)) &
        ((selected_lease_date == "All") | (data['lease_commence_date'] == selected_lease_date)) &
        ((selected_remaining_lease == "All") | (data['remaining_lease'] == selected_remaining_lease))
    ]

    # Visualization of average resale price based on filtered data
    if not filtered_data.empty:
        avg_price = filtered_data['resale_price'].astype(float).mean()
        st.write(f"The average resale price for **{selected_town}** in **{selected_month}** is **${avg_price:.2f}**.")

        # Create a bar chart for average resale prices by flat type
        avg_price_by_type = filtered_data.groupby('flat_type')['resale_price'].mean().reset_index()
        fig = px.bar(avg_price_by_type, x='flat_type', y='resale_price', 
                     title=f'Average Resale Prices for {selected_town} in {selected_month}', 
                     labels={'resale_price': 'Average Resale Price', 'flat_type': 'Flat Type'})
        st.plotly_chart(fig)
    else:
        st.warning("No data available for the selected filters.")

def display_sample_qns():
    st.write("### Sample questions")
    st.write("What is the average resale price for 3-room flats?")
    st.write("What is the average resale price for 4-room flats in Ang Mo Kio?")
    st.write("What is the average resale price for flats between 80 and 100 sqm?")
    st.write("How do resale prices in Bukit Batok compare to Tampines for 4-room flats?")


def main():
    # Call the password check at the beginning
    if not check_password():
        return  # Exit if the password is incorrect
    
    st.title("Housing Prices Query App")

    # Load the data
    data = load_data()

    # Sidebar for page navigation
    st.sidebar.header("Navigation")
    page = st.sidebar.radio("Select a page:", ["Query", "Data Summary", "About Us", "Methodology"])

    if page == "Query":
        # User input for query
        user_query = st.text_input("Ask a question about housing prices:")
        display_sample_qns()

        if user_query:
            for i in range(5):
                response = process_query(data, user_query)
                if "Error executing query" not in response:
                    break
            
            # Improved error handling
            if "Error executing query" in response:
                st.error("There was an issue processing your query. Please try again with a different question.")
            else:
                st.write("Response:")
                st.write(response)

    elif page == "Data Summary":
        if data is not None and not data.empty:
            display_data_summary(data)
        else:
            st.warning("No data available.")

    elif page == "About Us":
        import about_us # Import the About Us page
        about_us.main()
    elif page == "Methodology":
        import methodology # Import the Methodology page
        methodology.main()

if __name__ == "__main__":
    main()
