import sqlite3

connection = sqlite3.connect("cache.db")

print(connection.total_changes)