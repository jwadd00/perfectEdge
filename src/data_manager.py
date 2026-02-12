import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
from datetime import datetime

class GSheetManager:
    def __init__(self):
        self.conn = st.connection("gsheets", type=GSheetsConnection)
        # Default sheet names
        self.SCHEDULE_SHEET = "Schedule"
        self.OPTIONS_SHEET = "Options"

    def get_options(self):
        """
        Fetches options from the 'Options' worksheet.
        Expected columns: 'Staff', 'Crew Color', 'Trailer', 'Equipment'
        """
        try:
            df = self.conn.read(worksheet=self.OPTIONS_SHEET)
            return df
        except Exception as e:
            st.error(f"Error reading Options sheet: {e}")
            return pd.DataFrame()

    def save_options(self, df):
        """
        Saves the options DataFrame back to the 'Options' worksheet.
        """
        try:
            self.conn.update(worksheet=self.OPTIONS_SHEET, data=df)
            st.success("Options updated successfully!")
            self.conn.reset() # Clear cache
        except Exception as e:
            st.error(f"Error saving Options: {e}")

    def get_schedule(self):
        """
        Fetches the full schedule from the 'Schedule' worksheet.
        """
        try:
            df = self.conn.read(worksheet=self.SCHEDULE_SHEET)
            # Ensure Date column is datetime
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date']).dt.date
            return df
        except Exception as e:
            st.error(f"Error reading Schedule sheet: {e}")
            return pd.DataFrame()

    def save_schedule(self, df):
        """
        Saves the schedule DataFrame back to the 'Schedule' worksheet.
        """
        try:
            self.conn.update(worksheet=self.SCHEDULE_SHEET, data=df)
            st.success("Schedule updated successfully!")
            self.conn.reset()
        except Exception as e:
            st.error(f"Error saving Schedule: {e}")

    def get_schedule_for_date(self, date):
        """
        Filters the schedule for a specific date.
        """
        df = self.get_schedule()
        if df.empty or 'Date' not in df.columns:
            return pd.DataFrame()
        
        # Filter by date
        mask = df['Date'] == date
        return df[mask]
