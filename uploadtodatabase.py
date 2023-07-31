import sqlite3
import requests
import os
import streamlit as st

from deta import Deta  # pip install deta
from dotenv import load_dotenv  # pip install python-dotenv

# Load the environment variables
DETA_KEY = "d0k4fws8gi7_xKE62N6R1cmQ9C9dKdHoEqpCPY6yfRN3"
deta = Deta(DETA_KEY)

db = deta.Base("urls")

def fetch_user_data(username):
    """Returns the data for a specific user, if found"""
    res = db.fetch({"username": username})
    return res.items

def insert_url(username, url):
    """Returns the user on a successful user creation, otherwise raises an error"""
    return db.put({"username": username, "url": url})

# Streamlit app
st.title("URL Manager")

# Input fields for username and URL
username = st.text_input('Enter your username:')
url = st.text_input('Enter the URL:')

# "Add URL" button to add the URL to Deta
if st.button('Add URL'):
    if username.strip() and url.strip():
        insert_url(username, url)
        st.success(f"URL added for user {username}")

# "Fetch Data" button to display URLs for the entered username
if st.button('Fetch Data'):
    if username.strip():
        user_data = fetch_user_data(username)
        if user_data:
            urls = [user["url"] for user in user_data]
            for url in urls:
                st.markdown(f'<div class="hover-shadow"><iframe src="{url}"></iframe></div>', unsafe_allow_html=True)
        else:
            st.warning(f"No data found for user {username}")
    else:
        st.warning("Please enter a valid username.")
