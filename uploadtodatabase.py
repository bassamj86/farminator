import sqlite3
import requests
import os
import streamlit as st
import streamlit_authenticator as stauth
from deta import Deta  # pip install deta
from dotenv import load_dotenv  # pip install python-dotenv
import hashlib
from streamlit_option_menu import option_menu
import streamlit_authenticator as stauth
from deta import Deta 
import streamlit as st
import bcrypt
from passlib.context import CryptContext
import base64

from PIL import Image





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")




img = Image.open("preview.jpg")


st.set_page_config(page_title="Admin", page_icon=img, layout="centered", initial_sidebar_state="auto", menu_items=None)










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


def local_css(filename):
    with open(filename) as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

local_css('admin.css')


DETA_KEY_ADMIN = "d0k4fws8gi7_xKE62N6R1cmQ9C9dKdHoEqpCPY6yfRN3"
deta = Deta(DETA_KEY_ADMIN)

db_admin = deta.Base("admincredentials")

def fetch_admin():
    """Returns a dict of all users"""
    res = db_admin.fetch()
    return res.items







def delete_user(username):
    """Always returns None, even if the key does not exist"""
    return db_register.delete(username)



admins = fetch_admin()
usernames = [user["key"] for user in admins]
names = [user["name"] for user in admins]
hashed_passwords = [user["password"] for user in admins]


authenticator = stauth.Authenticate(names, usernames, hashed_passwords,
    "sales_dashboard", "abcdef", cookie_expiry_days=30)

name, authentication_status, username = authenticator.login("Login", "main")

if authentication_status == False:
    st.error("Username/password is incorrect")

if authentication_status == None:
    st.warning("Please enter your username and password")

if authentication_status:








    selected3 = option_menu(None, ["User Registration", "User Chart Add"],
        
        default_index=0, orientation="horizontal",
        styles = {
        "container": {
            "padding": "1rem 2rem",
            "background-color": "white",
            "border-radius": "10px",
            "box-shadow": "0 0 10px rgba(0, 0, 0, 0.1)",
            "font-color": "white"
        },
        "icon": {
            "color": "white",
            "font-size": "25px",
            "display": "none",
            "font-color": "white"
            
        },
        "nav-link": {
            "font-size": "18px",
            "font-color": "white",
            "text-align": "left",
            "padding": "0.5rem",
            "margin": "0",
            "border-radius": "5px",
            "transition": "background-color 0.3s",
            "--hover-color": "#e0e0e0",
            "cursor": "pointer"
        },
        "nav-link-selected": {
            "background-color": "#9C2222",
            "color": "white",
            "font-weight": "bold"
        },
    }
        
    )


    def hash_password(password):
        # Using hashlib to hash the password securely
        return hashlib.sha256(password.encode()).hexdigest()

    def insert_user(username, name, password):
        """Returns the user on a successful user creation, otherwise raises and error"""
        return db_register.put({"key": username, "name": username, "password": password})

    def fetch_all_users():

        res = db_register.fetch()
        return res.items


    DETA_KEY_REGISTER = "d0k4fws8gi7_xKE62N6R1cmQ9C9dKdHoEqpCPY6yfRN3"
    deta_register = Deta(DETA_KEY_REGISTER)
    db_register = deta_register.Base("users")
    def insert_user(username, name, password):
        """Returns the user on a successful user creation, otherwise raises and error"""
        return db_register.put({"key": username, "name": name, "password": password})

    users = fetch_all_users()
    un = [user["key"] for user in users]


    if selected3 == "User Registration":
        

        usernames = st.text_input("Username", key=9)
        names = st.text_input("Name", key=10)
        passs = st.text_input("Password", type="password", key=11)

        if st.button("Save"):
            
            # Hash the password
            hashed_password = pwd_context.hash(passs)

            # Now save the user information with the hashed password
            insert_user(usernames, names, hashed_password)


        st.header("Delete User")
        un.insert(0, "Select a username")

    # Selectbox to choose a username
        username_selected = st.selectbox('Select a username', un)

        if st.button('Delete'):
            delete_user(username_selected)

    
    




    if selected3=="User Chart Add":
        st.header("Add user Chart's Url here")
        un.insert(0, "Select a username")

    # Selectbox to choose a username
        username_selected = st.selectbox('Select a username', un)
        

        url = st.text_input('Enter the URL:',key=4)

        # "Add URL" button to add the URL to Deta
        if st.button('Add URL'):
            if username_selected.strip() and url.strip():
                insert_url(username_selected, url)
                st.success(f"URL added for user {username_selected}")

        # "Fetch Data" button to display URLs for the entered username
        if st.button('Fetch Data'):
            if username_selected.strip():
                user_data = fetch_user_data(username_selected)
                if user_data:
                    urls = [user["url"] for user in user_data]
                    for url in urls:
                        st.markdown(f'<div class="hover-shadow"><iframe class="graphs" src="{url}"></iframe></div>', unsafe_allow_html=True)
                else:
                    st.warning(f"No data found for user {username_selected}")
            else:
                st.warning("Please enter a valid username.")


