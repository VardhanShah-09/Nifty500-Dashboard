import streamlit as st

# -----------------------------
# Import Components
# -----------------------------
from components.Login import show_login
from components.Dashboard import show as dashboard
from components.Stock_Analysis import show as stock_analysis
from components.Prediction import show as prediction
from components.Comparison import show as comparison
from components.About import show as about

# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="Nifty500 Dashboard",
    page_icon="📈",
    layout="wide"
)

# -----------------------------
# Session State Initialization
# -----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "user" not in st.session_state:
    st.session_state.user = None

if "is_admin" not in st.session_state:
    st.session_state.is_admin = False

# -----------------------------
# Login Check
# -----------------------------
if not st.session_state.logged_in:
    show_login()
    st.stop()

# -----------------------------
# Sidebar
# -----------------------------
st.sidebar.success(
    f"Welcome, {st.session_state.user['username']}"
)

if st.session_state.is_admin:
    st.sidebar.info("Role : Administrator")
else:
    st.sidebar.info("Role : User")

st.sidebar.divider()

# Logout Button
if st.sidebar.button("Logout", use_container_width=True):

    st.session_state.logged_in = False
    st.session_state.user = None
    st.session_state.is_admin = False

    st.rerun()

# -----------------------------
# Main Title
# -----------------------------
st.title("📈 Nifty500 Stock Market Dashboard")

# -----------------------------
# Tabs
# -----------------------------
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "📈 Stock Analysis",
    "🤖 Prediction",
    "⚖️ Comparison",
    "ℹ️ About"
])

with tab1:
    dashboard()

with tab2:
    stock_analysis()

with tab3:
    prediction()

with tab4:
    comparison()

with tab5:
    about()
