import pyodbc
from openpyxl import load_workbook

connstr = "DRIVER={ODBC Driver 18 for SQL Server};Server=BEECHE72/SQLDEVELOPER;Database=GBLDBSYSTEM;Encrypt=Yes;TrustServerCertificate=Yes;Trusted_Connection=Yes;"
excel_file = "C:/Users/mbryson/Desktop/Current/tblDeductions.xlsx"

wb = load_workbook(filename = excel_file)
ws = wb.active


