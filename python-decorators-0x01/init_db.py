import sqlite3

# Create a valid SQLite database and a users table
conn = sqlite3.connect('users.db')
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
)
""")

# Insert sample data
cursor.execute("INSERT INTO users (name) VALUES ('Alice')")
cursor.execute("INSERT INTO users (name) VALUES ('Bob')")

# Save (commit) the changes and close
conn.commit()
conn.close()

print("✅ users.db created successfully with sample data.")
