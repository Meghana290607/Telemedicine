import pandas as pd
import os

USER_FILE = "data/users.csv"
APPT_FILE = "data/appointments.csv"

# --- Load user list ---
def load_users():
    if not os.path.exists(USER_FILE) or os.stat(USER_FILE).st_size == 0:
        return pd.DataFrame(columns=["username", "password", "role"])
    return pd.read_csv(USER_FILE)

# --- Load appointments ---
def load_appointments():
    if not os.path.exists(APPT_FILE) or os.stat(APPT_FILE).st_size == 0:
        return pd.DataFrame(columns=["patient", "doctor", "datetime", "status"])
    return pd.read_csv(APPT_FILE)

# --- Save a new appointment ---
def save_appointment(patient, doctor, appt_datetime):
    df = load_appointments()
    new_appt = {
        "patient": patient,
        "doctor": doctor,
        "datetime": appt_datetime,
        "status": "Scheduled"
    }
    df = pd.concat([df, pd.DataFrame([new_appt])], ignore_index=True)
    df.to_csv(APPT_FILE, index=False)
