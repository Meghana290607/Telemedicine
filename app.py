import streamlit as st
from utils.session import init_session

# Set the page config for Streamlit
st.set_page_config(page_title="Telemedicine App", layout="wide")

# Initialize session state (loads data from cookies or session)
init_session()

# Set the page title
st.title("🏥 Welcome to Telemedicine Portal")

# Show a message to use sidebar to navigate based on role
st.markdown("Use the sidebar to navigate based on your role.")

# Sidebar navigation and role-based display
role = st.session_state.get('role', None)

# Check if user is logged in
if 'role' not in st.session_state:
    st.warning("You are not logged in. Please log in first.")
    st.stop()

# Show role-based content
if role == "Admin":
    st.markdown("### 🛠 Admin Panel")
    st.write("As an Admin, you can manage all users and appointments.")
    st.markdown("You can navigate to the Admin features in the sidebar.")

elif role == "Doctor":
    st.markdown("### 🩺 Doctor Dashboard")
    st.write("As a Doctor, you can manage your appointments, view patient details, and upload prescriptions.")
    st.markdown("You can navigate to the Doctor's dashboard features in the sidebar.")

elif role == "Patient":
    st.markdown("### 👩‍⚕️ Patient Dashboard")
    st.write("As a Patient, you can book appointments, view your scheduled appointments, and upload medical information.")
    st.markdown("You can navigate to the Patient's features in the sidebar.")

else:
    st.warning("Role not recognized. Please log in with a valid role.")
