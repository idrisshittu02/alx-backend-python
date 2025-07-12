import mysql.connector
import csv
import uuid

DB_NAME = "ALX_prodev"

def connect_db():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Better9ja"  # 👈 Update this
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Connection error: {err}")
        return None

def create_database(connection):
    try:
        cursor = connection.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {DB_NAME};")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Failed to create database: {err}")

def connect_to_prodev():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Better9ja",  # 👈 Update this
            database=DB_NAME
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to {DB_NAME}: {err}")
        return None

def create_table(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(36) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL,
                INDEX(user_id)
            );
        """)
        connection.commit()
        cursor.close()
        print("Table user_data created successfully")
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, filename):
    try:
        cursor = connection.cursor()
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                user_id = str(uuid.uuid4())
                name = row["name"]
                email = row["email"]
                age = row["age"]

                cursor.execute("SELECT * FROM user_data WHERE email = %s", (email,))
                if cursor.fetchone():
                    continue

                cursor.execute("""
                    INSERT INTO user_data (user_id, name, email, age)
                    VALUES (%s, %s, %s, %s);
                """, (user_id, name, email, age))
        connection.commit()
        cursor.close()
    except Exception as err:
        print(f"Error inserting data: {err}")
        
def stream_user_data(connection):
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM user_data;")
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            yield row
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error streaming data: {err}")

