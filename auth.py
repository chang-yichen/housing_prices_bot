import streamlit as st

def check_password():
    """Prompt for a password and return True if correct."""
    password = st.sidebar.text_input("Enter your password:", type="password")
    if password == "your_password_here":  # Replace with your password
        return True
    else:
        st.sidebar.error("🚫 Incorrect password")
        return False
