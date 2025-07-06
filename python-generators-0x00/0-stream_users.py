import mysql.connector

def stream_users():
    """
    Generator function that connects to the ALX_prodev database
    and yields one user row at a time from the user_data table.
    """
    try:
        # Connect to the ALX_prodev database
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql-Software-0745464042',  
            database='ALX_prodev'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        # Yield one row at a time
        for row in cursor:
            yield row

    except mysql.connector.Error as e:
        print(f"Database error: {e}")

    finally:
        # Clean up connections
        if cursor:
            cursor.close()
        if conn:
            conn.close()
