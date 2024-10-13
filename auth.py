# In your auth.py
import os
import streamlit as st

def check_password():
    """Prompt for a password and return True if correct."""
    password = st.sidebar.text_input("Enter your password:", type="password")
    correct_password = os.getenv("APP_PASSWORD")  # Make sure to set this in your environment
    if password == correct_password:
        return True
    else:
        st.sidebar.error("🚫 Incorrect password")
        return False
