"""
0-main.py - Main script to test seed.py functionality
"""

seed = __import__('seed')

# Step 1: Connect to MySQL (no specific DB)
connection = seed.connect_db()
if connection:
    # Step 2: Create the ALX_prodev database
    seed.create_database(connection)
    connection.close()
    print("connection successful")

    # Step 3: Reconnect, this time to ALX_prodev
    connection = seed.connect_to_prodev()

    if connection:
        # Step 4: Create user_data table
        seed.create_table(connection)

        # Step 5: Insert data from CSV
        seed.insert_data(connection, 'user_data.csv')

        # Step 6: Confirm database and print some rows
        cursor = connection.cursor()
        cursor.execute("SELECT SCHEMA_NAME FROM INFORMATION_SCHEMA.SCHEMATA WHERE SCHEMA_NAME = 'ALX_prodev';")
        result = cursor.fetchone()
        if result:
            print("Database ALX_prodev is present")

        cursor.execute("SELECT * FROM user_data LIMIT 5;")
        rows = cursor.fetchall()
        print(rows)
        cursor.close()
        connection.close()
