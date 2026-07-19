import streamlit as st
from database.auth import login_user
from utils.theme import load_theme


def show_login():
    """
    Display the login page.
    """

    load_theme()

    # Hide sidebar before login
    st.markdown(
        """
        <style>
        section[data-testid="stSidebar"]{
            display:none;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown("<div class='login-container'>", unsafe_allow_html=True)

    st.markdown(
        "<h1 style='color:white;text-align:center;'>Nifty500 Dashboard</h1>",
        unsafe_allow_html=True
    )
    
    
    col1, col2, col3 = st.columns([1, 2, 1])

    with col2:

        login = st.text_input(
            "Username or Email",
            placeholder="Enter username or email"
        )

        password = st.text_input(
            "Password",
            type="password",
            placeholder="Enter password"
        )

        remember = st.checkbox("Remember Me")

        if st.button("Login to Dashboard", use_container_width=True):

            user = login_user(login, password)

            if user:

                st.session_state.logged_in = True
                st.session_state.user = user
                st.session_state.is_admin = bool(user["is_admin"])

                st.success(f"Welcome {user['full_name']}!")

                st.rerun()

            else:

                st.error("Invalid username/email or password.")

    st.markdown(
        """
        <div class="login-footer">
            © 2026 Nifty500 Dashboard
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown("</div>", unsafe_allow_html=True)
