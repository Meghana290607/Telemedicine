import pandas as pd

def load_users(path="data/users.csv"):
    return pd.read_csv(path)

def authenticate(username, password, users_df):
    user = users_df[(users_df['username'] == username) & (users_df['password'] == password)]
    if not user.empty:
        return user.iloc[0]['role']
    return None
