import streamlit as st

# =====================================================
# Import Login Component Only
# =====================================================

from components.Login import show_login

st.set_page_config(layout="wide",)
# =====================================================
# Session State Initialization
# =====================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

if "role" not in st.session_state:
    st.session_state.role = "USER"

if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

# =====================================================
# Login Check
# =====================================================

if not st.session_state.logged_in:
    show_login()
    st.stop()

# =====================================================
# Sidebar
# =====================================================

with st.sidebar:

    st.subheader("📈 Nifty500")

    if st.button("🏠 Dashboard", width="stretch"):
        st.session_state.current_page = "Dashboard"

    if st.button("📊 Stock Analysis", width="stretch"):
        st.session_state.current_page = "Stock Analysis"

    if st.button("🤖 Prediction", width="stretch"):
        st.session_state.current_page = "Prediction"

    if st.button("⚖️ Comparison", width="stretch"):
        st.session_state.current_page = "Comparison"

    if st.button("ℹ️ Market Overview", width="stretch"):
        st.session_state.current_page = "About"

    if st.session_state.is_admin:
        if st.button("👥 User Management", width="stretch"):
            st.session_state.current_page = "User Management"

    st.divider()

    st.markdown(f"### {st.session_state.user['full_name']}")

    if st.session_state.is_admin:
        st.write("Admin")
    else:
        st.write("User")

    if st.button("🚪 Logout", key="nav_logout", width="stretch"):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.is_admin = False
        st.session_state.role = "USER"
        st.session_state.current_page = "Dashboard"

        st.rerun()

# =====================================================
# Main Content (Lazy Loading)
# =====================================================

page = st.session_state.current_page

if page == "Dashboard":

    from components.Dashboard import show
    show()

elif page == "Stock Analysis":

    from components.Stock_Analysis import show
    show()

elif page == "Prediction":

    from components.Prediction import show
    show()

elif page == "Comparison":
    
    from components.Comparison import show
    show()

elif page == "About":
    
    from components.Market_Overview import show
    show()

elif page == "User Management":

    from admin.User_Management import show_user_management
    show_user_management()
