import streamlit as st
from src.data_manager import GSheetManager
from src.views import show_admin_page, show_schedule_page

# Set page config
st.set_page_config(
    page_title="Perfect Edge Schedule Manager",
    page_icon="📅",
    layout="wide",
)

st.title("Perfect Edge Schedule Manager")

# Setup connection
# We initialize the manager once, it handles the connection
manager = GSheetManager()

# Placeholder for navigation
page = st.sidebar.selectbox("Navigate", ["Schedule", "Admin"])

if page == "Schedule":
    show_schedule_page(manager)
    
elif page == "Admin":
    show_admin_page(manager)
