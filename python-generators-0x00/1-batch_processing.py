import mysql.connector

def stream_users_in_batches(batch_size):
    """
    Generator that yields batches of users from the user_data table.
    """
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='sql-Software-0745464042',
            database='ALX_prodev'
        )
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data")

        batch = []
        for row in cursor:
            batch.append(row)
            if len(batch) == batch_size:
                yield batch
                batch = []
        if batch:
            yield batch
        return

    finally:
        cursor.close()
        conn.close()

def batch_processing(batch_size):
    """
    Processes each batch and prints users over the age of 25.
    """
    for batch in stream_users_in_batches(batch_size):
        for user in batch:
            if user['age'] > 25:
                print(user)
