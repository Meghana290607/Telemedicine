import streamlit as st
from utils.session import init_session
from utils.data_handler import load_appointments
import os

init_session()
if st.session_state.role != "Doctor":
    st.warning("Access restricted to Doctors only.")
    st.stop()

st.title("🩺 Doctor Dashboard")
st.subheader(f"Welcome, Dr. {st.session_state.username}")

# View appointments
st.markdown("### 👥 Your Appointments")
appts = load_appointments()
doc_appts = appts[appts['doctor'] == st.session_state.username]
st.dataframe(doc_appts)

# Prescription upload
st.markdown("### 📝 Upload Prescription")
upload_patient = st.selectbox("Select Patient", doc_appts['patient'].unique())
uploaded_file = st.file_uploader("Upload Prescription (PDF/IMG)", type=['pdf', 'png', 'jpg'])

if uploaded_file:
    path = f"data/prescriptions/{upload_patient}_{st.session_state.username}_{uploaded_file.name}"
    with open(path, "wb") as f:
        f.write(uploaded_file.read())
    st.success("Prescription uploaded.")
