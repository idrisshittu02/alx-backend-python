import sqlite3

with sqlite3.connect("users.db") as conn:
    cursor = conn.cursor()
    try:
        cursor.execute("ALTER TABLE users ADD COLUMN age INTEGER")
    except sqlite3.OperationalError:
        pass  # Column might already exist

    # Optional: Update some users to have an age
    cursor.execute("UPDATE users SET age = 30 WHERE name = 'John Doe'")
    conn.commit()

