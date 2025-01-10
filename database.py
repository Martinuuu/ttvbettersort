import sqlite3

def get_connection():
    connection = sqlite3.connect("cache.db")
    return connection

def addStreamer(name, id):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO streamer VALUES (?, ?)", (name, id))
    connection.commit()
    connection.close()
    print("Added streamer to cache")

def getIDCache(name):
    connection = get_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT id FROM streamer WHERE name = ?", (name,))
    result = cursor.fetchone()
    connection.close()
    print("Got streamer from cache")
    return result[0] if result else None