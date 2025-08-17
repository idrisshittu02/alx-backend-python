import seed

def stream_user_ages():
    """Generator that yields user ages one at a time"""
    connection = seed.connect_to_prodev()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT age FROM user_data")

    for row in cursor:
        yield int(row["age"])  # ✅ yield each age

    cursor.close()
    connection.close()


def compute_average_age():
    total = 0
    count = 0
    for age in stream_user_ages():  # ✅ Loop 1
        total += age
        count += 1

    if count > 0:
        average = total / count
        print(f"Average age of users: {average:.2f}")
    else:
        print("No users found.")
        
if __name__ == "__main__":
    compute_average_age()

