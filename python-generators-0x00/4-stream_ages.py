seed = __import__("seed")


def stream_user_ages():
    """Generator that yields ages one by one from the user_data table"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor()
    cursor.execute("SELECT age FROM user_data")
    for row in cursor:
        yield row[0]
    cursor.close()
    connection.close()


def calculate_average_age():
    """Calculates and prints the average age of users using the generator"""
    total = 0
    count = 0

    for age in stream_user_ages():
        total += age
        count += 1

    if count == 0:
        print("Average age of users: 0")
    else:
        average = total / count
        print(f"Average age of users: {average}")
