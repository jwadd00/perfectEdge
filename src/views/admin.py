import streamlit as st
import pandas as pd
from src.data_manager import GSheetManager

def show_admin_page(conn: GSheetManager):
    st.header("Admin / Options Configuration")
    
    # Load current options
    df = conn.get_options()
    
    st.write("Manage your lists below. You can add/remove items in each category independently.")
    
    # Define columns for layout
    col1, col2 = st.columns(2)
    col3, col4 = st.columns(2)
    
    # Helper to get dataframe for a specific column, dropping NaNs
    def get_col_df(source_df, col_name):
        # We need to find the column case-insensitively
        target_col = None
        for c in source_df.columns:
            if c.lower() == col_name.lower():
                target_col = c
                break
        
        if target_col:
            # Return as a dataframe with one column
            return pd.DataFrame(source_df[target_col].dropna().reset_index(drop=True))
        else:
            return pd.DataFrame(columns=[col_name])

    # 1. Staff
    with col1:
        st.subheader("Staff")
        staff_df = get_col_df(df, "Staff")
        # Ensure column name is normalized for the editor
        if not staff_df.empty: staff_df.columns = ["Staff"]
        edited_staff = st.data_editor(staff_df, num_rows="dynamic", use_container_width=True, key="editor_staff")
        
    # 2. Crew Colors
    with col2:
        st.subheader("Crew Colors")
        crew_df = get_col_df(df, "Crew Color")
        if not crew_df.empty: crew_df.columns = ["Crew Color"]
        edited_crew = st.data_editor(crew_df, num_rows="dynamic", use_container_width=True, key="editor_crew")

    # 3. Trailers
    with col3:
        st.subheader("Trailers")
        trailer_df = get_col_df(df, "Trailer")
        if not trailer_df.empty: trailer_df.columns = ["Trailer"]
        edited_trailer = st.data_editor(trailer_df, num_rows="dynamic", use_container_width=True, key="editor_trailer")
        
    # 4. Equipment
    with col4:
        st.subheader("Equipment")
        equip_df = get_col_df(df, "Equipment")
        if not equip_df.empty: equip_df.columns = ["Equipment"]
        edited_equip = st.data_editor(equip_df, num_rows="dynamic", use_container_width=True, key="editor_equip")

    # 5. Job Type (New)
    st.divider()
    st.subheader("Job Types")
    job_type_df = get_col_df(df, "Job Type")
    if not job_type_df.empty: job_type_df.columns = ["Job Type"]
    edited_job_type = st.data_editor(job_type_df, num_rows="dynamic", use_container_width=True, key="editor_job_type")

    if st.button("Save All Changes"):
        # Merge into one DataFrame for saving (longest list determines length)
        # We need to extract the columns
        
        # Helper to extract list from 'edited' df
        def get_list(d, col):
            return d[col].dropna().astype(str).tolist() if col in d.columns else []

        s_list = get_list(edited_staff, 'Staff')
        c_list = get_list(edited_crew, 'Crew Color')
        t_list = get_list(edited_trailer, 'Trailer')
        e_list = get_list(edited_equip, 'Equipment')
        j_list = get_list(edited_job_type, 'Job Type')
        
        # Create a dict with padding
        max_len = max(len(s_list), len(c_list), len(t_list), len(e_list), len(j_list))
        
        # Pad with empty strings or None? None is better for dropna later
        def pad(l, n):
            return l + [None] * (n - len(l))

        data = {
            "Staff": pad(s_list, max_len),
            "Crew Color": pad(c_list, max_len),
            "Trailer": pad(t_list, max_len),
            "Equipment": pad(e_list, max_len),
            "Job Type": pad(j_list, max_len)
        }
        
        # We might need to preserve other columns if they exist?
        # For now, we assume these 4 are the main ones managed here.
        
        final_df = pd.DataFrame(data)
        conn.save_options(final_df)
        
        # Prime the cache for the Schedule page
        with st.spinner("Preloading schedule data..."):
            conn.get_schedule()
        st.success("Options saved and schedule data refreshed!")
