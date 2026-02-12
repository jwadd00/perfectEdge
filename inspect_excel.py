import pandas as pd

try:
    # Load the Excel file
    xls = pd.ExcelFile('template_sheet.xlsx')
    
    print("Sheet names:", xls.sheet_names)
    
    for sheet_name in xls.sheet_names:
        print(f"\n--- Sheet: {sheet_name} ---")
        df = pd.read_excel(xls, sheet_name=sheet_name)
        print("Columns:", df.columns.tolist())
        print("First 5 rows:")
        print(df.head())
        print("Data types:")
        print(df.dtypes)

except Exception as e:
    print(f"Error reading Excel file: {e}")
