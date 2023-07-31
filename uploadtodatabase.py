import streamlit_authenticator as stauth
import streamlit as st

def insert_user_data(username, name, hashed_password):
    db.insert_user(username, name, hashed_password)


import streamlit as st
import sqlite3


import os

from deta import Deta  # pip install deta



# Load the environment variables
DETA_KEY = "d0k4fws8gi7_xKE62N6R1cmQ9C9dKdHoEqpCPY6yfRN3"
deta = Deta(DETA_KEY)

db = deta.Base("users")


def insert_user(username, name, password):
    """Returns the user on a successful user creation, otherwise raises and error"""
    return db.put({"key": username, "name": name, "password": password})


def fetch_all_users():
    """Returns a dict of all users"""
    res = db.fetch()
    return res.items


def get_user(username):
    """If not found, the function will return None"""
    return db.get(username)


def update_user(username, updates):
    """If the item is updated, returns None. Otherwise, an exception is raised"""
    return db.update(updates, username)


def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db.delete(username)

def create_table():
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS urls (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT,
            url TEXT
        )
    ''')
    conn.commit()
    conn.close()

def insert_url(username, url):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO urls (username, url)
        VALUES (?, ?)
    ''', (username, url))
    conn.commit()
    conn.close()

def get_urls(username):
    conn = sqlite3.connect('data.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT url FROM urls WHERE username=?
    ''', (username,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

# Create the table at the start of the app
# create_table()

st.title('URLs with Usernames')

username = st.text_input('Enter your username:')   
url = st.text_input('Enter the URL:')
if st.button('Add URL'):
    # create_table()

    if username.strip() and url.strip():
        insert_url(username, url)
        st.success(f"URL added for user {username}")

st.header('Your Saved URLs')
# if username.strip():
    
#     if urls:
#         for i, url in enumerate(urls):
#             st.write(f"{i + 1}. {url}")
urls = get_urls(username)
if username.strip() and urls:
    for url in urls:
        st.markdown(f'<div class="hover-shadow"><iframe src="{url}"></iframe></div>', unsafe_allow_html=True)

