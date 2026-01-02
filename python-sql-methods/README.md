# Python SQL Methods

A small collection of Python helper functions for interacting with SQL Server using `pyodbc`.  
These utilities were adapted from long-standing VBA patterns developed and refined over many years of production use.

## Features

- Safe retrieval of single-value results from SELECT queries
- Efficient row counting with intelligent detection of COUNT queries
- Transaction-controlled INSERT and UPDATE execution
- Defensive SQL validation and structured error handling
- Guaranteed cleanup of database connections and cursors

## Included Functions

- `getresult(sql)`
  
  Executes a SELECT statement and returns a single scalar result.  
  Validates that exactly one row is returned.

- `getcount(sql)`
  
  Returns the number of rows produced by a query.  
  Uses `SELECT COUNT(*)` when applicable or falls back to result set evaluation.

- `insertupdate(sql)`
  
  Executes a single-row INSERT or UPDATE statement.  
  Enforces commit/rollback behavior based on rows affected.

## Connection Configuration

Update the `connstr` variable in `db_utils.py` with your own SQL Server connection information before use.  
The sample connection string in the repository is a placeholder and contains no real credentials.

## Design Philosophy

These utilities emphasize correctness, predictability, and data integrity.  
They are intentionally defensive and structured to behave safely in production environments.

