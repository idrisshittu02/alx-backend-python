import mysql.connector

def stream_users():
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Better9ja",  # 🔁 Replace with your real password
        database="ALX_prodev"
    )
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM user_data")

    for row in cursor:
        # convert Decimal to int for "age" if needed
        row["age"] = int(row["age"])
        yield row

    cursor.close()
    connection.close()
