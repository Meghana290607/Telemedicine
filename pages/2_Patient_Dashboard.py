import streamlit as st
from utils.session import init_session
from utils.data_handler import load_appointments, save_appointment, load_users, save_user
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

# Load doctors and department options
doctors = load_users()
doctor_names = doctors[doctors['role'] == 'Doctor']['username'].tolist()
departments = ["Cardiology", "Gynecology", "Dermatology", "Pediatrics", "Orthopedics"]

# Select doctor and department
selected_doctor = st.selectbox("Choose Doctor", doctor_names)
selected_department = st.selectbox("Choose Department", departments)

# Select appointment date and time
appt_date = st.date_input("Select Date", min_value=datetime.today().date())
appt_time = st.time_input("Select Time", min_value=datetime.now().time())
full_datetime = datetime.combine(appt_date, appt_time)

# Validate appointment (no past dates and 15-minute gap)
def validate_appointment_time(selected_datetime, doctor_name):
    current_datetime = datetime.now()
    if selected_datetime < current_datetime:
        st.error("You cannot book an appointment in the past! Please choose a future time.")
        return False

    # Check for time conflicts with existing appointments
    appts = load_appointments()
    doctor_appts = appts[appts['doctor'] == doctor_name]
    for _, app in doctor_appts.iterrows():
        if abs((selected_datetime - app['appointment_time']).total_seconds()) < 900:  # 15 minutes
            st.error("This time slot is already booked. Please choose another time.")
            return False

    return True

# Book appointment button action
if st.button("Book Appointment"):
    if validate_appointment_time(full_datetime, selected_doctor):
        # Save the appointment details
        save_appointment(st.session_state.username, selected_doctor, full_datetime, selected_department)
        st.success("✅ Appointment scheduled successfully!")

# --- View Appointments ---
st.markdown("### 📋 Your Appointments")
appts = load_appointments()
user_appts = appts[appts['patient'] == st.session_state.username]
st.dataframe(user_appts)

