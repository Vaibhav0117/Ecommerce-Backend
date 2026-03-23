import sqlite3

conn = sqlite3.connect("food_app.db")
cursor = conn.cursor()

# List all tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Inspect the users table schema
cursor.execute("PRAGMA table_info(users);")
print("Users table schema:", cursor.fetchall())

conn.close()
