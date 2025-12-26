import pandas as pd
from sqlalchemy import create_engine

# connstr = "DRIVER={ODBC Driver 18 for SQL Server};Server=BEECHE72\\SQLDEVELOPER;Database=GBLDBSYSTEM;Encrypt=Yes;TrustServerCertificate=Yes;Trusted_Connection=Yes;"
connstr = (
    "mssql+pyodbc://@BEECHE72\\SQLDEVELOPER/GBLDBSYSTEM?" 
    "driver=ODBC+Driver+18+for+SQL+Server"
    "@trusted_connection=yes"
)
excel_file = "C:/Users/mbryson/Desktop/Current/tblDeductions.xlsx"

engine = create_engine(connstr)
df = pd.read_excel(excel_file,sheet_name='Sheet1')
print(df.head())