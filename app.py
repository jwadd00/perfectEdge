import streamlit as st
from src.data_manager import GSheetManager
from src.views import show_admin_page, show_schedule_page

# Set page config
st.set_page_config(
    page_title="Job Schedule",
    page_icon="📅",
    layout="wide",
)

st.title("Job Schedule")

# Authentication Check
def check_password():
    """Returns `True` if the user had the correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] == st.secrets["auth"]["password"]:
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    elif not st.session_state["password_correct"]:
        # Password not correct, show input + error.
        st.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    else:
        # Password correct.
        return True

if check_password():
    # Setup connection
    # We initialize the manager once, it handles the connection
    manager = GSheetManager()

    # Placeholder for navigation
    page = st.sidebar.selectbox("Navigate", ["Schedule", "Admin"])

    if page == "Schedule":
        show_schedule_page(manager)
        
    elif page == "Admin":
        show_admin_page(manager)
