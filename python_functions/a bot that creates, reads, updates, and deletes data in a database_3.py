import sqlite3

def database_bot(operation, data=None,id=None):
    conn = sqlite3.connect('database_name.db') 
    c = conn.cursor()

    if(operation == "create"):
        c.execute("""CREATE TABLE IF NOT EXISTS table_name (
            id integer PRIMARY KEY,
            data text)""")
        c.execute("INSERT INTO table_name VALUES (?,?)", (data[0], data[1])) 
        print(f"Record created: {data}")
        
    elif(operation == "read"):
        c.execute("SELECT * FROM table_name WHERE id=?", (id,))
        print(f"Record Read: {c.fetchone()}")

    elif(operation == "update"):
        c.execute("UPDATE table_name SET data=? WHERE id=?", (data, id)) 
        print(f"Record updated: {(id, data)}")
        
    elif(operation == "delete"):
        c.execute("DELETE from table_name where id=?", (id,)) 
        print(f"Record deleted with id {id}")

    else:
        print("Invalid operation.")

    conn.commit()
    conn.close()

# Example usage:
# database_bot("create", (1, "Hello"))
# database_bot("read", id=1)
# database_bot("update", "World", 1)
# database_bot("delete", id=1)