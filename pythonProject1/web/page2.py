import streamlit as st


# Function to authenticate user (replace with your own authentication logic)
def authenticate(username, password):
    # In a real-world scenario, you would query a database or use an authentication service
    # For simplicity, let's assume there's a predefined list of users
    users = {"user": "password", "john": "doe123"}

    return users.get(username) == password


# Function to register a new user (replace with your own registration logic)
def register(username, password):
    # In a real-world scenario, you would insert the user into a database
    # For simplicity, let's just print the registered user
    print(f"New user registered - Username: {username}, Password: {password}")


# Function to create a unique session state variable
def get_state():
    session_state = st.session_state
    return session_state


# Streamlit app
def main():
    st.title("Streamlit Login/Signup Example")

    # Get the session state
    state = get_state()

    if not hasattr(state, "authenticated"):
        state.authenticated = False

    if not state.authenticated:
        # Create a selection widget to choose between login and signup
        choice = st.radio("Choose an action:", ["Login", "Signup"])

        if choice == "Login":
            # Create a login form on the main page
            with st.form("Login Form"):
                username = st.text_input("Username")
                password = st.text_input("Password", type="password")
                submit_button = st.form_submit_button("Login")

            # Check if the form is submitted
            if submit_button:
                # Authenticate the user
                if authenticate(username, password):
                    state.authenticated = True
                    st.success(f"Welcome, {username}!")
                    # You can add session variable or redirect to the main app content
                else:
                    st.error("Invalid username or password. Please try again.")

        elif choice == "Signup":
            # Create a signup form on the main page
            with st.form("Signup Form"):
                new_username = st.text_input("New Username")
                new_password = st.text_input("New Password", type="password")
                confirm_password = st.text_input("Confirm Password", type="password")
                submit_button = st.form_submit_button("Signup")

            # Check if the form is submitted
            if submit_button:
                # Check if passwords match
                if new_password == confirm_password:
                    # Register the new user
                    register(new_username, new_password)
                    state.authenticated = True
                    st.success(f"User {new_username} registered successfully!")
                else:
                    st.error("Passwords do not match. Please try again.")
    else:
        st.success("You are already authenticated. You can now access the main content.")


if __name__ == "__main__":
    main()
