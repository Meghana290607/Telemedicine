import streamlit as st
from utils.session import init_session
from utils.data_handler import load_appointments
import datetime
import os

# Initialize session
init_session()

# Ensure only doctors can access this page
if st.session_state.role != "Doctor":
    st.warning("Access restricted to Doctors only.")
    st.stop()

# Page Title
st.title("🩺 Doctor Dashboard")
st.subheader(f"Welcome, Dr. {st.session_state.username}")

# View appointments
st.markdown("### 👥 Your Appointments")
appts = load_appointments()
doc_appts = appts[appts['doctor'] == st.session_state.username]

# Filter out past appointments and display only future appointments
current_datetime = datetime.datetime.now()
doc_appts['appointment_time'] = pd.to_datetime(doc_appts['appointment_time'])

# Filter out past appointments
doc_appts = doc_appts[doc_appts['appointment_time'] > current_datetime]
st.dataframe(doc_appts)

# Prescription upload
st.markdown("### 📝 Upload Prescription")

# Select patient from the list of appointments
upload_patient = st.selectbox("Select Patient", doc_appts['patient'].unique())

# Prescription upload option (Text or Document)
prescription_type = st.radio("Choose Prescription Type", ("Text", "Document"))

if prescription_type == "Text":
    # Text-based prescription input
    prescription_text = st.text_area("Enter Prescription Text")
    
    if st.button("Submit Prescription"):
        if prescription_text:
            # Save the text prescription to file or database (replace this with actual DB code)
            st.success("Prescription submitted successfully!")
        else:
            st.error("Please enter prescription text.")
else:
    # Document-based prescription upload
    uploaded_file = st.file_uploader("Upload Prescription (PDF/IMG)", type=['pdf', 'png', 'jpg'])

    if uploaded_file:
        # Define the path where to save the uploaded prescription
        path = f"data/prescriptions/{upload_patient}_{st.session_state.username}_{uploaded_file.name}"
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        # Save the uploaded file
        with open(path, "wb") as f:
            f.write(uploaded_file.read())
        st.success("Prescription uploaded successfully.")

# Appointments: Ensure no time clashes and 15-minute gap
st.markdown("### 🕒 Book an Appointment")

# Select patient and doctor
patient_name = st.selectbox("Select Patient for Appointment", doc_appts['patient'].unique())
appointment_date = st.date_input("Select Appointment Date", min_value=current_datetime.date())
appointment_time = st.time_input("Select Appointment Time", min_value=current_datetime.time())

# Combine the date and time into a single datetime object
selected_datetime = datetime.datetime.combine(appointment_date, appointment_time)

# Check if the selected appointment time is in the past
if selected_datetime < current_datetime:
    st.error("You cannot book an appointment in the past. Please select a future time.")
    st.stop()

# Check for any clashes with other appointments (minimum 15-minute gap)
existing_appointments = doc_appts[doc_appts['doctor'] == st.session_state.username]
for _, app in existing_appointments.iterrows():
    if abs((selected_datetime - app['appointment_time']).total_seconds()) < 900:  # 15-minute gap
        st.error("This time slot is already booked. Please choose another time.")
        st.stop()

if st.button("Book Appointment"):
    # Here, you'd typically save the appointment to the database
    # For now, we're just displaying a success message
    st.success(f"Appointment successfully booked for {patient_name} with Dr. {st.session_state.username} on {selected_datetime}.")
