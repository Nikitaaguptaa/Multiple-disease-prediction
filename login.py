import streamlit as st
from database import add_user, login_user, create_users_table

create_users_table()

def login_page():

    menu = ["Login", "Signup"]
    choice = st.sidebar.selectbox("Menu", menu)

    # ---------------- SIGNUP ----------------
    if choice == "Signup":
        st.subheader("📝 Create New Account")

        new_user = st.text_input("Username")
        new_pass = st.text_input("Password", type="password")

        if st.button("Signup"):
            if add_user(new_user, new_pass):
                st.success("Account created successfully ")
            else:
                st.error("Username already exists!")

    # ---------------- LOGIN ----------------
    elif choice == "Login":
        st.subheader("Login to your account")

        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if login_user(username, password):
                st.session_state.logged_in = True
                st.session_state.user = username
                st.success("Login successful ")
                st.rerun()
            else:
                st.error("Invalid credentials")