import streamlit as st
from utils.session import init_session
from utils.data_handler import load_appointments, save_appointment, load_users
from datetime import datetime

# Initialize session state
init_session()

# Role-based access control
if not st.session_state.logged_in or st.session_state.role != "Patient":
    st.warning("Access restricted to Patients only. Please log in as a Patient.")
    st.stop()

# Page title
st.title("🧍 Patient Dashboard")
st.subheader(f"Welcome, {st.session_state.username}")

# --- Schedule Appointment ---
st.markdown("### 📅 Schedule an Appointment")
doctors = load_users()
doctor_names = doctors[doctors['role'] == 'Doctor']['username'].tolist()

selected_doctor = st.selectbox("Choose Doctor", doctor_names)
appt_date = st.date_input("Select Date")
appt_time = st.time_input("Select Time")
full_datetime = datetime.combine(appt_date, appt_time)

if st.button("Book Appointment"):
    save_appointment(st.session_state.username, selected_doctor, full_datetime)
    st.success("✅ Appointment scheduled successfully!")

# --- View Appointments ---
st.markdown("### 📋 Your Appointments")
appts = load_appointments()
user_appts = appts[appts['patient'] == st.session_state.username]
st.dataframe(user_appts)
