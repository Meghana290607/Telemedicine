import streamlit as st
from utils.session import init_session
from utils.data_handler import load_users, load_appointments, save_prescription
import os
import datetime

# Initialize session
init_session()

# Ensure only Admins have access to this page
if st.session_state.role != "Admin":
    st.warning("Access restricted to Admins only.")
    st.stop()

# Page title
st.title("🛠 Admin Panel")
st.markdown("### 🩺 Manage Prescriptions")

# --- View All Users ---
st.markdown("### 👥 All Registered Users")
users = load_users()  # Get all registered users
st.dataframe(users)

# --- View All Appointments ---
st.markdown("### 📅 All Appointments")
appts = load_appointments()  # Get all appointments
st.dataframe(appts)

# --- Manage Prescriptions ---
st.markdown("### 📝 Manage Prescriptions")

# Select patient and doctor for prescription viewing
selected_patient = st.selectbox("Select Patient", appts['patient'].unique())
selected_doctor = st.selectbox("Select Doctor", appts['doctor'].unique())

# Filter the appointments for the selected patient and doctor
patient_appts = appts[(appts['patient'] == selected_patient) & (appts['doctor'] == selected_doctor)]

if patient_appts.empty:
    st.warning("No appointments found for this patient and doctor combination.")
else:
    st.write(f"Appointments for {selected_patient} with Dr. {selected_doctor}:")
    st.dataframe(patient_appts)

    # Prescription upload or text entry
    prescription_type = st.radio("Choose Prescription Type", ("Text", "Document"))

    if prescription_type == "Text":
        # Text-based prescription input
        prescription_text = st.text_area("Enter Prescription Text")

        if st.button("Submit Prescription"):
            if prescription_text:
                # Save the text prescription (you can save it to a file or database)
                save_prescription(selected_patient, selected_doctor, prescription_text, "text")
                st.success("Prescription submitted successfully!")
            else:
                st.error("Please enter prescription text.")
    else:
        # Document-based prescription upload
        uploaded_file = st.file_uploader("Upload Prescription (PDF/IMG)", type=['pdf', 'png', 'jpg'])

        if uploaded_file:
            # Define the path where to save the uploaded prescription
            path = f"data/prescriptions/{selected_patient}_{selected_doctor}_{uploaded_file.name}"
            os.makedirs(os.path.dirname(path), exist_ok=True)

            # Save the uploaded file
            with open(path, "wb") as f:
                f.write(uploaded_file.read())

            # Save the file path to the database (or adjust according to your saving logic)
            save_prescription(selected_patient, selected_doctor, path, "document")
            st.success("Prescription uploaded successfully.")
