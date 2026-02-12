import streamlit as st
import pandas as pd
from src.data_manager import GSheetManager

def show_admin_page(conn: GSheetManager):
    st.header("Admin / Options Configuration")
    st.info("Edit the options below and click 'Save Changes' to update the database.")

    # Load current options
    df = conn.get_options()
    
    if df.empty:
        # Initialize with some default structure if empty
        df = pd.DataFrame({
            "Staff": ["Alice", "Bob"],
            "Crew Color": ["Red", "Green"],
            "Trailer": ["Trailer 1", "Trailer 2"],
            "Equipment": ["Mower A", "Mower B"]
        })

    # specific editors for each option type?
    # Actually, a single data editor for all might be messy if columns have different lengths.
    # It's better to manage them as separate lists/tables if they are independent.
    # However, storing them in one sheet means they are side-by-side.
    # st.data_editor supports adding/deleting rows.
    
    edited_df = st.data_editor(df, num_rows="dynamic", use_container_width=True)

    if st.button("Save Changes"):
        conn.save_options(edited_df)
