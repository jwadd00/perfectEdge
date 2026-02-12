import streamlit as st
import pandas as pd
import gspread
from gspread_dataframe import get_as_dataframe, set_with_dataframe

class GSheetManager:
    def __init__(self):
        # Authenticate using secrets
        try:
            # st.secrets["connections"]["gsheets"] contains the service account info
            # We also need to strip out the 'spreadsheet' and 'worksheet' keys to pass to gspread credentials
            secrets = st.secrets["connections"]["gsheets"]
            
            # gspread needs the credentials dict. The extra keys 'spreadsheet' and 'worksheet' 
            # might cause issues if passed directly to from_dict, but usually it ignores extras.
            # Let's clean it just in case or use a subset.
            # Actually, service_account_from_dict expects specific keys.
            
            self.gc = gspread.service_account_from_dict(secrets)
            
            self.spreadsheet_url = secrets.get("spreadsheet")
            self.sh = self.gc.open_by_url(self.spreadsheet_url)
            
            self.SCHEDULE_SHEET_NAME = "Schedule"
            self.OPTIONS_SHEET_NAME = "Options"
            
        except Exception as e:
            st.error(f"Failed to authenticate with Google Sheets: {e}")
            self.sh = None

    def _get_worksheet(self, name):
        if not self.sh: return None
        try:
            return self.sh.worksheet(name)
        except gspread.WorksheetNotFound:
            # Create if not exists? Or return None
            st.warning(f"Worksheet '{name}' not found.")
            return None

    def get_options(self):
        ws = self._get_worksheet(self.OPTIONS_SHEET_NAME)
        if not ws: return pd.DataFrame()
        
        try:
            # get_as_dataframe reads the whole sheet
            df = get_as_dataframe(ws, evaluate_formulas=True)
            # Drop empty rows/cols
            df = df.dropna(how='all').dropna(axis=1, how='all')
            return df
        except Exception as e:
            st.error(f"Error reading Options: {e}")
            return pd.DataFrame()

    def save_options(self, df):
        ws = self._get_worksheet(self.OPTIONS_SHEET_NAME)
        if not ws: return
        
        try:
            ws.clear()
            set_with_dataframe(ws, df)
            st.success("Options updated!")
        except Exception as e:
            st.error(f"Error saving Options: {e}")

    def get_schedule(self):
        ws = self._get_worksheet(self.SCHEDULE_SHEET_NAME)
        if not ws: return pd.DataFrame()
        
        try:
            df = get_as_dataframe(ws, evaluate_formulas=True)
            df = df.dropna(how='all').dropna(axis=1, how='all')
            if 'Date' in df.columns:
                df['Date'] = pd.to_datetime(df['Date']).dt.date
            return df
        except Exception as e:
            st.error(f"Error reading Schedule: {e}")
            return pd.DataFrame()

    def add_schedule_rows(self, df):
        """Append new rows to the schedule without overwriting existing data."""
        ws = self._get_worksheet(self.SCHEDULE_SHEET_NAME)
        if not ws: return

        try:
            # Convert DataFrame to list of lists for appending
            # Handle Date conversion
            save_df = df.copy()
            if 'Date' in save_df.columns:
                save_df['Date'] = save_df['Date'].astype(str)
            
            # gspread append_rows expects a list of lists
            data_to_append = save_df.values.tolist()
            
            ws.append_rows(data_to_append)
            st.success("New jobs added successfully!")
        except Exception as e:
            st.error(f"Error adding rows: {e}")

    def save_schedule(self, df):
        # Keeping this for legacy or full overwrite if needed, but alerting user
        ws = self._get_worksheet(self.SCHEDULE_SHEET_NAME)
        if not ws: return
        
        try:
            save_df = df.copy()
            if 'Date' in save_df.columns:
                save_df['Date'] = save_df['Date'].astype(str)
                
            ws.clear()
            set_with_dataframe(ws, save_df)
            st.success("Schedule updated!")
        except Exception as e:
            st.error(f"Error saving Schedule: {e}")
