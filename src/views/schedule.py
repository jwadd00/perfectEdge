import streamlit as st
import pandas as pd
from datetime import date
from src.data_manager import GSheetManager

def show_schedule_page(conn: GSheetManager):
    st.header("Daily Schedule")

    # Date Picker
    selected_date = st.date_input("Select Date", date.today())
    
    # Load Options for Dropdowns
    options_df = conn.get_options()
    
    # Extract lists, filtering out NaNs
    staff_options = options_df['Staff'].dropna().astype(str).tolist() if 'Staff' in options_df.columns else []
    crew_colors = options_df['Crew Color'].dropna().astype(str).tolist() if 'Crew Color' in options_df.columns else []
    trailers = options_df['Trailer'].dropna().astype(str).tolist() if 'Trailer' in options_df.columns else []
    equipment = options_df['Equipment'].dropna().astype(str).tolist() if 'Equipment' in options_df.columns else []
    job_types = options_df['Job Type'].dropna().astype(str).tolist() if 'Job Type' in options_df.columns else []

    # --- Add New Job Form ---
    with st.expander("➕ Add New Job", expanded=True):
        with st.form("add_job_form"):
            st.write("Add a new job entry for the selected date.")
            col1, col2 = st.columns(2)
            
            with col1:
                # Defaults
                f_crew = st.selectbox("Crew Color", options=crew_colors)
                f_job = st.text_input("Job Name")
                f_type = st.selectbox("Job Type", options=job_types)
                f_staff = st.selectbox("Staff", options=staff_options)
            
            with col2:
                f_trailer = st.selectbox("Trailer", options=trailers)
                f_equip = st.selectbox("Equipment", options=equipment)
            
            if st.form_submit_button("Add Job"):
                # Create a 1-row DataFrame
                new_row = pd.DataFrame([{
                    "Date": selected_date,
                    "Crew Color": f_crew,
                    "Job Name": f_job,
                    "Job Type": f_type,
                    "Staff": f_staff,
                    "Trailer": f_trailer,
                    "Equipment": f_equip
                }])
                
                # Append to Google Sheet
                conn.add_schedule_rows(new_row)
                st.rerun()

    # --- View Schedule ---
    st.divider()
    st.subheader(f"Current Schedule")

    # Load Schedule
    schedule_df = conn.get_schedule()
    
    if schedule_df.empty:
        st.info("No schedule data found.")
        schedule_df = pd.DataFrame(columns=['Date', 'Crew Color', 'Job Name', 'Job Type', 'Staff', 'Trailer', 'Equipment'])
    else:
         # Ensure Date column exists and filter
        if 'Date' not in schedule_df.columns:
            schedule_df['Date'] = pd.to_datetime(selected_date) # Fallback

        # Filter for display - Show ALL or just Selected Date?
        # Let's show selected date by default, with option to show all?
        # User said "Master Daily Schedule", usually implies seeing the day.
        
        # Ensure we are comparing dates correctly
        # schedule_df['Date'] is likely object (date) from our manager fix
        
        # Filter
        daily_mask = schedule_df['Date'] == selected_date
        daily_df = schedule_df[daily_mask]
        
        st.dataframe(daily_df, use_container_width=True, hide_index=True)
        
        # Optional: Show full history
        with st.expander("View Full History"):
            st.dataframe(schedule_df, use_container_width=True)
