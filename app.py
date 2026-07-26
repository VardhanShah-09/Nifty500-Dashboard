import streamlit as st

# =====================================================
# Import Components
# =====================================================

from components.Login import show_login
from components.Dashboard import show as dashboard
from components.Stock_Analysis import show as stock_analysis
from components.Prediction import show as prediction
from components.Comparison import show as comparison
from components.About import show as about
from admin.User_Management import show_user_management


# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Nifty500 Dashboard",
    page_icon="📈",
    layout="wide"
)


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

st.sidebar.title("📈 Nifty500 Dashboard")

st.sidebar.write(f"**{st.session_state.user['full_name']}**")

if st.session_state.is_admin:
    st.sidebar.info("Administrator")
else:
    st.sidebar.info("User")


st.sidebar.subheader("Navigation")

# ---------------- Dashboard ----------------
if st.sidebar.button(
    "🏠 Dashboard",
    use_container_width=True,
):
    st.session_state.current_page = "Dashboard"

# ---------------- Stock Analysis ----------------
if st.sidebar.button(
    "📈 Stock Analysis",
    use_container_width=True,
):
    st.session_state.current_page = "Stock Analysis"

# ---------------- Prediction ----------------
if st.sidebar.button(
    "🤖 Prediction",
    use_container_width=True,
):
    st.session_state.current_page = "Prediction"

# ---------------- Comparison ----------------
if st.sidebar.button(
    "⚖️ Comparison",
    use_container_width=True,
):
    st.session_state.current_page = "Comparison"

# ---------------- User Management ----------------
if st.session_state.is_admin:

    if st.sidebar.button(
        "👥 User Management",
        use_container_width=True,
    ):
        st.session_state.current_page = "User Management"

# ---------------- About ----------------
if st.sidebar.button(
    "ℹ️ About",
    use_container_width=True,
):
    st.session_state.current_page = "About"

st.sidebar.markdown("---")

# =====================================================
# Logout
# =====================================================

if st.sidebar.button(
    "🚪 Logout",
    use_container_width=True,
):

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

elif page == "User Management":
    show_user_management()

elif page == "About":
    about()