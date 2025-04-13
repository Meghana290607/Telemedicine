import streamlit as st
from utils.session import init_session
from utils.data_handler import load_users, load_appointments

init_session()
if st.session_state.role != "Admin":
    st.warning("Access restricted to Admins only.")
    st.stop()

st.title("🛠 Admin Panel")

st.markdown("### 👥 All Registered Users")
users = load_users()
st.dataframe(users)

st.markdown("### 📅 All Appointments")
appts = load_appointments()
st.dataframe(appts)
