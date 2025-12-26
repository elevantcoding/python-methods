
#reference main module to use functions within it
import main
import pyodbc
connstr = "DRIVER={ODBC Driver 18 for SQL Server};Server=BEECHE72\\SQLDEVELOPER;Database=GBLDBSYSTEM;Encrypt=Yes;TrustServerCertificate=Yes;Trusted_Connection=Yes;"

# write functions that will return results using getresult
def geteename(eeid: int): # eeid = integer
    mysql = f"SELECT EmployeeName FROM dbo.View_Employee WHERE EEMasterID = {eeid};"
    result = main.getresult(mysql)[0]
    return result

def geteemasterid(empid: int): #empid = integer
    mysql = f"SELECT EEMasterID FROM dbo.tblEmployeeName WHERE EmpID = {empid};"
    return main.getresult(mysql)[0]

#table = "development.tblHappyDay"
#recordcount = main.getcount(f"SELECT COUNT(*) FROM {table};")[0]
#print(recordcount)

def geteemasterdept(eeid: int):
    mysql = f"SELECT Department FROM dbo.View_Employee WHERE EEMasterID = {eeid};"
    return main.getresult(mysql)[0]

def geteetype(empid: int):
    mysql = f"SELECT [Type] FROM dbo.tblEmployeeName WHERE EmpID = {empid};"
    return main.getresult(mysql)[0]

def getua(empid: int):
    gettype = geteetype(empid)
    mysql = f"SELECT UnionAffiliation FROM dbo.tblEEType WHERE [Type]='{gettype}';"
    return main.getresult(mysql)[0]

def geteeaddress(eeid: int):
    conn = None
    cursor = None
    result = None
    msg = ""    

    try:
        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        cursor.execute("SELECT Address, City, dbo.GetStateNameAbb(State) As St, ZipCode FROM dbo.View_Employee_CurrentAddress WHERE EEMasterID = ?", eeid)
        row = cursor.fetchone()
        if not row:
            msg = f"No results for {eeid}."
        else:
            second = cursor.fetchone()
            if second:
                msg = f"More than one result found for {eeid}."
            else:
                result = row

    except pyodbc.Error as e:
        msg = f"Database error: {e}"
    except Exception as ex:
        msg = f"Unexpected error: {ex}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return result, msg

def istermed(eeid: int):
    mysql = f"SELECT * FROM dbo.tblEmployeeMaster WHERE EEMasterID = {eeid} AND DOT IS NOT NULL;"
    count = main.getcount(mysql)[0]
    return count > 0

# use sql functions to return a value
def getstate(id: int):
    mysql = f"SELECT dbo.GetStateNameAbb({id}) As [State];"
    return main.getresult(mysql)[0]

import datetime

getdate = datetime.datetime.now()
getday = getdate.strftime("%A") #day of the week
#print(getday)

def is_valid_date(value, fmt="%Y-%m-%d"):
    try:
        datetime.datetime.strptime(value, fmt)
        return True
    except ValueError:
        return None

#my_date = "2025-11-03"
#print(is_valid_date(my_date))

def is_sunday(value):
    if not is_valid_date(value):
        return False
    datevalue = datetime.datetime.strptime(value, "%Y-%m-%d")
    return datevalue.strftime("%A") == "Sunday"
        
#print(is_sunday("2025-11-07"))

# return the day of the week for a date value
def getday(value):
    if not is_valid_date(value):
        return
    datevalue = datetime.datetime.strptime(value, "%Y-%m-%d")
    return datevalue.strftime("%A")

print(getday("2025-11-06"))

# write GetDate from VBA in Py
def GetDateInWEDate(targetDay: str, forWEDate):
    result = 0
    if not is_valid_date(forWEDate):
        return
    if not is_sunday(forWEDate):
        return
    
    days = ["sun","sat","fri","thu","wed","tue","mon"]    
    datevalue = datetime.datetime.strptime(forWEDate, "%Y-%m-%d")            
    for i, d in enumerate(days):
        if targetDay.lower() == d:
            return (datevalue - datetime.timedelta(days=i)).date()
            
#print(GetDateInWEDate("mon","2025-11-09"))