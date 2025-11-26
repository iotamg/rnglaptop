import sqlite3

def initTables(cursor):
  try:
    sql = """
    CREATE TABLE IF NOT EXISTS users (
      username TEXT NOT NULL PRIMARY KEY,
      password  TEXT NOT NULL, 
      name TEXT NOT NULL,
      mahzor TEXT NOT NULL,
      strikes INTEGER NOT NULL CHECK(strikes>0)
      )
    """
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS laptops(
        regional_id TEXT NOT NULL,
        grade TEXT NOT NULL,
        number TEXT NOT NULL,
        date_of_purchess DATE NOT NULL
    )
    """
    cursor.execute(sql)

  except sqlite3.Error as e:
     print(f"SQL Error: {e}")
    
def addUser(cursor):
  try:
    sql = "INSERT into users (username, password, name, strikes) VALUES ('"
    sql += input("Enter username: ") + "', '" + input("Enter password: ") + "', '" + input("Enter full name: ") + "', 0)"
    cursor.execute(sql)
  except sqlite3.Error as e:
     print(f"SQL Error: {e}")

def showMenu():
  keepOn = True
  try:
    conn = sqlite3.connect('RNGL.db')
    stmt = conn.cursor()
    while (keepOn):
      print("""
        1. Initiate Tables
        2. Add User""")
      choice = input("Enter your choice: ")
      if choice == "1":
        initTables(stmt)
      elif choice == "2":
        addUser(stmt)
  except sqlite3.Error as e:
     print(f"SQL Error: {e}")

def main():
  showMenu()
  