import streamlit as st
import pandas as pd
import hashlib
import os

USER_DB = "users.csv"

# --------------------------
# Utility Functions
# --------------------------

def hash_password(password: str) -> str:
    """Hash a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()

def load_users():
    """Load users from CSV or create file if it doesn’t exist."""
    if not os.path.exists(USER_DB):
        df = pd.DataFrame(columns=["username", "password"])
        df.to_csv(USER_DB, index=False)
    return pd.read_csv(USER_DB)

def save_user(username: str, password: str):
    """Save a new user to the CSV."""
    df = load_users()
    if username in df["username"].values:
        return False  # User already exists
    new_user = pd.DataFrame([[username, hash_password(password)]], columns=["username", "password"])
    df = pd.concat([df, new_user], ignore_index=True)
    df.to_csv(USER_DB, index=False)
    return True

def authenticate(username: str, password: str) -> bool:
    """Check if username and password are valid."""
    df = load_users()
    if username in df["username"].values:
        stored_pw = df.loc[df["username"] == username, "password"].values[0]
        return stored_pw == hash_password(password)
    return False

def reset_password(username: str, new_password: str) -> bool:
    """Reset a user's password if the account exists."""
    df = load_users()
    if username in df["username"].values:
        df.loc[df["username"] == username, "password"] = hash_password(new_password)
        df.to_csv(USER_DB, index=False)
        return True
    return False

# --------------------------
# UI Components
# --------------------------

def signup():
    st.subheader("Create a New Account")
    with st.form("signup_form", clear_on_submit=True):
        new_username = st.text_input("Choose a Username")
        new_password = st.text_input("Choose a Password", type="password")
        confirm_password = st.text_input("Confirm Password", type="password")
        submitted = st.form_submit_button("Sign Up")

        if submitted:
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            elif save_user(new_username, new_password):
                st.success("Account created successfully! Please log in.")
            else:
                st.error("Username already exists. Try a different one.")

def forgot_password():
    st.subheader("Reset Your Password")
    with st.form("reset_form", clear_on_submit=True):
        username = st.text_input("Enter your Username")
        new_password = st.text_input("Enter New Password", type="password")
        confirm_password = st.text_input("Confirm New Password", type="password")
        submitted = st.form_submit_button("Reset Password")

        if submitted:
            if new_password != confirm_password:
                st.error("Passwords do not match.")
            elif reset_password(username, new_password):
                st.success("Password reset successfully! Please log in.")
            else:
                st.error("Username not found. Please check and try again.")

def login():
    st.title("Login to Access the Unified ChatBot")
    tab1, tab2, tab3 = st.tabs(["🔑 Login", "🆕 Sign Up", "🔄 Forgot Password"])

    with tab1:
        with st.form("login_form", clear_on_submit=False):
            username = st.text_input("Username")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("Login")

            if submitted:
                if authenticate(username, password):
                    st.session_state["authenticated"] = True
                    st.session_state["user"] = username
                    st.success(f"Welcome, {username}!")
                    st.rerun()
                else:
                    st.error("Invalid username or password.")

    with tab2:
        signup()

    with tab3:
        forgot_password()

def ensure_auth():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login()
        st.stop()

# --------------------------
# Main App
# --------------------------

def main():
    ensure_auth()
    st.title("🤖 Unified ChatBot Dashboard")
    st.write(f"Hello, **{st.session_state['user']}**! You are logged in.")
    if st.button("Logout"):
        st.session_state.update({"authenticated": False, "user": None})
        st.rerun()

if __name__ == "__main__":
    main()
