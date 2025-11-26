import sqlite3

def initTables(stmt):
  try:
    stmt = "CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, password TEXT, name TEXT, strikes INTEGER)"
    stmt.execute(stmt)

  except sqlite3.Error as e:
     print("Error")
    
def addUser(stmt):
  try:
    stmt = "INSERT into users (username, password, name, strikes) VALUES ('"
    stmt += input("Enter username: ") + "', '" + input("Enter password: ") + "', '" + input("Enter full name: ") + "', '" + input("Enter mahzor: ") + "', 0)"
    stmt.execute(stmt)
  except sqlite3.Error as e:
     print("Error")

def showMenu():
  keepOn = True
  try:
    conn = sqlite3.connect('RNGL.db')  # Creates a new database file if it doesn’t exist
    stmt = conn.cursor()
    while (keepOn)
      print("""
        1. Initiate Tables
        2. Add User""")
      choice = input("Enter your choice: ")
      if choice == "1":
        initTables(stmt)
      elif choice == "2"
        addUser(stmt)
  except sqlite3.Error as e:
     print("Error")
  conn.close()

def main():
  showMenu();
  