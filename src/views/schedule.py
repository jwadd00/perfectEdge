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

    # Load Schedule
    schedule_df = conn.get_schedule()
    
    # Filter for selected date (for display/editing context)
    # Ideally, we want to edit the WHOLE schedule but filtered views are easier.
    # But st.data_editor on a filtered dataframe doesn't easily sync back to the main one unless we handle the merge.
    # Simplified approach: 
    # 1. Load full schedule.
    # 2. Add 'Date' column if missing.
    # 3. Use data_editor on the WHOLE dataframe but maybe filter visibility? 
    #    No, `st.data_editor` edits what is shown.
    # Better approach for scalable apps: Load only today's data, save it back by appending/updating.
    # But for a simple GSheet backend, reading standardizing on one big sheet is fine for now.
    
    # Let's show the WHOLE schedule for now with a column configuration to filter? 
    # Create a new entry mode vs View mode.
    
    st.subheader(f"Schedule for {selected_date}")

    if schedule_df.empty:
        schedule_df = pd.DataFrame(columns=['Date', 'Crew Color', 'Job Name', 'Staff', 'Trailer', 'Equipment'])

    # Ensure Date column exists
    if 'Date' not in schedule_df.columns:
        schedule_df['Date'] = pd.to_datetime(selected_date)

    # Convert Date to date object for comparison
    # schedule_df['Date'] = pd.to_datetime(schedule_df['Date']).dt.date
    
    # Filter for display
    # daily_data = schedule_df[schedule_df['Date'] == selected_date]
    # Actually, let's just show the full editor but sorted by date, 
    # and maybe highlight today?
    # Or just let them edit the main table.
    
    # Best UX: Show only selected date's rows, plus an "Add Row" button that pre-fills the date.
    # But st.data_editor doesn't support "pre-fill new row" easily.
    
    # Let's stick to: View/Edit the table.
    
    column_config = {
        "Date": st.column_config.DateColumn("Date", required=True, default=selected_date),
        "Crew Color": st.column_config.SelectboxColumn("Crew Color", options=crew_colors, required=True),
        "Staff": st.column_config.ListColumn("Staff"), # Multiselect for staff? Streamlit only validates ListColumn slightly. 
        # actually TextColumn or Selectbox. If multiple staff, maybe Text for now or Link.
        # Selectbox only allows one. 
        # Let's use Selectbox for 'Lead' and maybe another for 'Helper'? 
        # Or just a text field for "Staff List".
        "Job Name": st.column_config.TextColumn("Job Name", required=True),
        "Trailer": st.column_config.SelectboxColumn("Trailer", options=trailers),
        "Equipment": st.column_config.SelectboxColumn("Equipment", options=equipment) 
    }
    
    # If we want multiple staff, we might need a ListColumn which is display only, or just a text input.
    # Let's try Selectbox for simplicity first, assuming 1 generic "Staff" assignments or comma separated text.
    # User asked for "Master Daily Schedule".
    
    edited_schedule = st.data_editor(
        schedule_df,
        num_rows="dynamic",
        column_config=column_config,
        use_container_width=True,
        key="schedule_editor"
    )

    if st.button("Save Schedule"):
        conn.save_schedule(edited_schedule)
