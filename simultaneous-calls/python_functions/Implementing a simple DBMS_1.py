def simple_dbms(action, table=None, record=None):
    if not hasattr(simple_dbms, "database"):
        simple_dbms.database = {}  # A dictionary to store all the tables

    if action == "CREATE_TABLE":
        if table not in simple_dbms.database:
            simple_dbms.database[table] = []  # Create a new table (empty list)
            return f"Table '{table}' created."
        else:
            return f"Table '{table}' already exist."

    elif action == "INSERT":
        if table not in simple_dbms.database:
            return f"Table '{table}' does not exist."
        else:
            simple_dbms.database[table].append(record)
            return f"Record inserted in table '{table}'."

    elif action == "SELECT_ALL":
        if table not in simple_dbms.database:
            return f"Table '{table}' does not exist."
        else:
            return simple_dbms.database[table]

    elif action == "DELETE":
        if table not in simple_dbms.database:
            return f"Table '{table}' does not exist."
        else:
            try:
                simple_dbms.database[table].remove(record)
                return f"Record deleted from table '{table}'."
            except ValueError:
                return f"Record not found in table '{table}'."

    elif action == "DROP_TABLE":
        if table not in simple_dbms.database:
            return f"Table '{table}' does not exist."
        else:
            del simple_dbms.database[table]
            return f"Table '{table}' deleted."

    else:
        return f"Invalid action! Please choose from CREATE_TABLE, INSERT, SELECT_ALL, DELETE, DROP_TABLE."