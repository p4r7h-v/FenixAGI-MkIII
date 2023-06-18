def simple_dbms(operation, table=None, key=None, value=None):
    db = simple_dbms.db
    if operation == "create_table":
        if table not in db:
            db[table] = {}
            print(f"Table '{table}' created")
        else:
            print(f"Error: Table '{table}' already exists")
    elif operation == "insert":
        if table is not None and key is not None and value is not None:
            if table in db:
                db[table][key] = value
                print(f"Inserted key '{key}' with value '{value}' in table '{table}'")
            else:
                print(f"Error: Table '{table}' does not exist")
        else:
            print("Error: Missing table, key, or value")
    elif operation == "select":
        if table is not None and key is not None:
            if table in db:
                value = db[table].get(key, None)
                if value is not None:
                    print(f"Selected value '{value}' for key '{key}' in table '{table}'")
                else:
                    print(f"Error: No value found for key '{key}' in table '{table}'")
            else:
                print(f"Error: Table '{table}' does not exist")
        else:
            print("Error: Missing table, or key")
    elif operation == "delete":
        if table is not None and key is not None:
            if table in db:
                if key in db[table]:
                    del db[table][key]
                    print(f"Deleted key '{key}' in table '{table}'")
                else:
                    print(f"Error: No value found for key '{key}' in table '{table}'")
            else:
                print(f"Error: Table '{table}' does not exist")
        else:
            print("Error: Missing table, or key")
    else:
        print("Error: Invalid operation")


simple_dbms.db = {}