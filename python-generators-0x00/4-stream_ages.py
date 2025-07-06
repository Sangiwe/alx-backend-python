import seed

def stream_user_ages():
    """
    Generator that yields user ages one by one from the user_data table.
    """
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row['age']
    connection.close()

def calculate_average_age():
    """
    Calculates and prints the average age of users using the generator.
    """
    total = 0
    count = 0
    for age in stream_user_ages():
        total += age
        count += 1

    if count > 0:
        print(f"Average age of users: {total / count:.2f}")
    else:
        print("No users found.")

# Uncomment this line if you're testing directly
# calculate_average_age()
