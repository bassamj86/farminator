import streamlit_authenticator as stauth
import streamlit as st


import streamlit as st
import sqlite3




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

