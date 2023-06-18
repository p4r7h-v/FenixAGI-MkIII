import sqlite3
from sqlite3 import Error

def manage_db(action, table, data=None, condition=None):
    # Establish a connection
    try:
        conn = sqlite3.connect('example.db')  # use your database name

        # Create a cursor object
        c = conn.cursor()

        # Based on action perform operation
        if action.lower() == 'create':
            c.execute(f'CREATE TABLE {table} ({data})') 

        elif action.lower() == 'read':
            c.execute(f'SELECT * FROM {table}')

            # Fetch all rows
            rows = c.fetchall()
            for row in rows:
                print(row)

        elif action.lower() == 'update':
            c.execute(f'UPDATE {table} SET {data} WHERE {condition}')
        
        elif action.lower() == 'delete':
            c.execute(f'DELETE FROM {table} WHERE {condition}')
        
        else:
            print("Invalid action")

        # Commit the transaction
        conn.commit()

    except Error as e:
        print(e)

    finally:
        if conn:
            # Close connection
            conn.close()

# Examples of usage
manage_db(action='create', table='employees', data='id int, name text')
manage_db(action='read', table='employees')
manage_db(action='update', table='employees', data='name = "John Doe"', condition='id = 1')
manage_db(action='delete', table='employees', condition='id = 1')