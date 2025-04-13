import streamlit as st
from utils.data_handler import load_users
from utils.session import init_session

# Initialize session state variables
init_session()

st.title("🔐 Login")

def authenticate(username, password, users_df):
    matched = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
    if not matched.empty:
        return matched.iloc[0]['role']
    return None

# Login Form
if not st.session_state.logged_in:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        users = load_users()
        role = authenticate(username, password, users)

        if role:
            st.session_state.logged_in = True
            st.session_state.username = username
            st.session_state.role = role
            st.success(f"✅ Logged in as {username} ({role})")
            st.rerun()
        else:
            st.error("❌ Invalid credentials. Please try again.")
else:
    st.success(f"✅ You are logged in as {st.session_state.username} ({st.session_state.role})")

    # Sidebar logout
    st.sidebar.markdown("## ⚙️ Session")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.username = ""
        st.session_state.role = ""
        st.rerun()
