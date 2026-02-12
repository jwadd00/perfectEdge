import pandas as pd

try:
    # Load the Excel file, Sheet1, treating the second row (index 1) as header
    df = pd.read_excel('template_sheet.xlsx', sheet_name='Sheet1', header=1)
    
    print("Columns:", df.columns.tolist())
    print("\nFirst 10 rows:")
    print(df.head(10))
    
    # Also lets look for other lists in Sheet 2 or potential other hidden sheets
    xls = pd.ExcelFile('template_sheet.xlsx')
    if 'Sheet2' in xls.sheet_names:
        df2 = pd.read_excel(xls, sheet_name='Sheet2')
        print("\n--- Sheet 2 ---")
        print(df2.head())
        print(df2.columns.tolist())

except Exception as e:
    print(f"Error reading Excel file: {e}")
