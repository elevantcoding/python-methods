# get info from sql
import pyodbc
connstr = "DRIVER={ODBC Driver 18 for SQL Server};Server=CLIENTNAME\\SQLSERVER;Database=DATABASENAME;Encrypt=Yes;TrustServerCertificate=Yes;Trusted_Connection=Yes;"
    
# return a one-row result of an sql statement
def getresult(getsql: str): # getsql = string
    # initialize
    conn = None
    cursor = None
    result = None
    msg = ""
    
    # if not trimmed, upper case starts with SELECT, return result, msg
    if not getsql.strip().upper().startswith("SELECT"):
        msg = "Only SELECT statements may be parsed using getresult()."
        return result, msg
    
    try:
        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        cursor.execute(getsql) # parse getsql
        row = cursor.fetchone() # fetches first row
        if not row:
            msg = f"No results for {getsql}."
        else:
            second = cursor.fetchone() # fetches another row if it exists
            if second:
                msg = "Query returned more than one result."    
            else:
                result = row[0]
            
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

# return a count from sql statement either using select count or select specific
def getcount(getsql: str): # getsql = string
    # initialize
    conn = None
    cursor = None
    count = 0
    msg = ''
    selcount = False

    # if not trimmed, upper case starts with SELECT, return result, msg
    if not getsql.strip().upper().startswith("SELECT"):
        msg = "Only SELECT statements may be parsed using getcount()."
        return count, msg
    
    try:
        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()
        if "SELECT COUNT" in getsql.upper():
            selcount = True
        
        cursor.execute(getsql)
        if selcount:
            row = cursor.fetchone()
            count = row[0]
        else:
            row = cursor.fetchall()
            count = len(row)

    except pyodbc.Error as e:
        sqlstate, message = e.args[0], e.args[1]
        if "Invalid column name" in message or "42522" in sqlstate:            
            msg = "Invalid column name specified."
        elif "Invalid object name" in message or "42502" in sqlstate:
            msg = "Invalid table name specified."
        else:
            msg = message
    except Exception as ex:
        msg = f"Unexpected error: {ex}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return count, msg

# insert or update one row only
def insertupdate(getsql: str):
    
    conn = None
    cursor = None
    result = False
    msg = ""
    isupdate = "UPDATE" in getsql.upper()
    isinsert = "INSERT INTO" in getsql.upper()

    try:
        if not (isupdate or isinsert):
            msg = "Only INSERT or UPDATE statements may be parsed with insertupdate()."
            return result, msg

        conn = pyodbc.connect(connstr)
        cursor = conn.cursor()

        cursor.execute(getsql)
        cursor.execute("SELECT @@ROWCOUNT")
        rowsaffected = cursor.fetchone()[0]
        
        if rowsaffected == 1:
            conn.commit()
            result = True
            msg = "Success for: " + getsql
        else:
            conn.rollback()
            msg = f"Rolled back - {rowsaffected} rows potentially affected."

    except pyodbc.Error as e:
        if conn:
            conn.rollback()
        msg = f"Database error: {e}"
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
        return result, msg
  
