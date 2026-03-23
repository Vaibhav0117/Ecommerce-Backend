import sqlite3

conn = sqlite3.connect("food_app.db")
cursor = conn.cursor()

# Show all tables so you can confirm names
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
print("Tables:", cursor.fetchall())

# Query using the correct table name: menu_items
cursor.execute("""
SELECT u.username, r.name AS restaurant, m.name AS menu_item, oi.quantity
FROM orders o
JOIN users u ON o.user_id = u.user_id
JOIN restaurants r ON o.restaurant_id = r.restaurant_id
JOIN order_items oi ON o.order_id = oi.order_id
JOIN menu_items m ON oi.menu_item_id = m.menu_item_id;
""")

for row in cursor.fetchall():
    print(f"{row[0]} ordered {row[3]}x {row[2]} from {row[1]}")

conn.close()
