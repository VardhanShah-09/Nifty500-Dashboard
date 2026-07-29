import streamlit as st

# =====================================================
# Import Components
# =====================================================

from components.Login import show_login
from components.Dashboard import show as dashboard
from components.Stock_Analysis import show as stock_analysis
from components.Prediction import show as prediction
from components.Comparison import show as comparison
from components.Market_Overview import show as market_overview
from admin.User_Management import show_user_management

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
    if st.button("🏠 Dashboard", width= 'stretch'):
        st.session_state.current_page = "Dashboard"

    if st.button("📊 Stock Analysis", width='stretch'):
        st.session_state.current_page = "Stock Analysis"

    if st.button("🤖 Prediction", width='stretch'):
        st.session_state.current_page = "Prediction"

    if st.button("⚖️ Comparison", width='stretch'):
        st.session_state.current_page = "Comparison"

    if st.button("ℹ️ Market Overview", width='stretch'):
        st.session_state.current_page = "About"
    
    if st.session_state.is_admin:
        if st.button("👥 User Management", width='stretch'):
            st.session_state.current_page = "User Management"
    

    st.markdown(
        f"### {st.session_state.user['full_name']}")

    if st.session_state.is_admin:
        st.write("Admin")
    else:
        st.write("User")


    if st.button("🚪 Logout", key="nav_logout", width='stretch'):

        st.session_state.logged_in = False
        st.session_state.user = None
        st.session_state.is_admin = False
        st.session_state.role = "USER"
        st.session_state.current_page = "Dashboard"

        st.rerun()

# =====================================================
# Main Content
# =====================================================

page = st.session_state.current_page

if page == "Dashboard":
    dashboard()

elif page == "Stock Analysis":
    stock_analysis()

elif page == "Prediction":
    prediction()

elif page == "Comparison":
    comparison()

elif page == "About":
    market_overview()

elif page == "User Management":
    show_user_management()
