import pandas as pd
import os
from datetime import datetime, timedelta

USER_FILE = "data/users.csv"
APPT_FILE = "data/appointments.csv"

# --- Load user list ---
def load_users():
    if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0:
        return pd.DataFrame(columns=["username", "password", "role", "contact_number", "age", "department"])
    return pd.read_csv(USER_FILE)

# --- Load appointments ---
def load_appointments():
    if not os.path.exists(APPT_FILE) or os.stat(APPT_FILE).st_size == 0:
        return pd.DataFrame(columns=["patient", "doctor", "datetime", "status"])
    return pd.read_csv(APPT_FILE)

# --- Save a new appointment ---
def save_appointment(patient, doctor, appt_datetime):
    df = load_appointments()

    # Ensure the appointment is not in the past
    if appt_datetime < datetime.now():
        raise ValueError("Cannot book appointments in the past.")

    # Ensure there's no overlap with existing appointments and a 15-minute gap
    for _, row in df.iterrows():
        existing_appt_time = pd.to_datetime(row["datetime"])
        if abs(existing_appt_time - appt_datetime) < timedelta(minutes=15):
            raise ValueError("Appointments must be scheduled with a minimum 15-minute gap.")

    new_appt = {
        "patient": patient,
        "doctor": doctor,
        "datetime": appt_datetime,
        "status": "Scheduled"
    }
    
    df = pd.concat([df, pd.DataFrame([new_appt])], ignore_index=True)
    df.to_csv(APPT_FILE, index=False)
    return True

# --- Save a new user ---
def save_user(username, password, role, contact_number, age, department):
    df = load_users()
    new_user = {
        "username": username,
        "password": password,
        "role": role,
        "contact_number": contact_number,
        "age": age,
        "department": department
    }
    df = pd.concat([df, pd.DataFrame([new_user])], ignore_index=True)
    df.to_csv(USER_FILE, index=False)
    return True
