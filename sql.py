import sqlite3
try:
  conn = sqlite3.connect('example.db')  # Creates a new database file if it doesn’t exist
  cursor = conn.cursor()
  stmt="CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT)"
except:
   print("Error")
  