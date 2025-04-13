import streamlit as st
import pandas as pd
import os
from utils.data_handler import load_users

USER_FILE = "data/users.csv"

st.title("📝 Sign Up")

username = st.text_input("Choose a Username")
password = st.text_input("Choose a Password", type="password")
confirm = st.text_input("Confirm Password", type="password")

if st.button("Create Account"):
    if password != confirm:
        st.error("Passwords do not match.")
    elif username.strip() == "":
        st.error("Username cannot be empty.")
    else:
        users = load_users()
        if username in users['username'].values:
            st.error("Username already exists.")
        else:
            new_user = pd.DataFrame([[username, password, "Patient"]], columns=["username", "password", "role"])
            new_user.to_csv(USER_FILE, mode='a', header=not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0, index=False)
            st.success("Account created successfully! You can now log in.")
