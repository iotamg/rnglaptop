import sqlite3

def initTables(cursor):
  try:
    sql = """
    CREATE TABLE IF NOT EXISTS users (
      username TEXT NOT NULL PRIMARY KEY,
      password  TEXT NOT NULL, 
      name TEXT NOT NULL,
      mahzor TEXT NOT NULL,
      strikes INTEGER NOT NULL CHECK(strikes=>0)
      )
    """
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS laptops(
        regional_id TEXT NOT NULL,
        grade TEXT NOT NULL,
        number TEXT NOT NULL,
        date_of_purchase DATE NOT NULL
    )"""
    cursor.execute(sql)
    sql = """
      CREATE TABLE IF NOT EXISTS BOROWS(
        riginalID INTEGER NOT NULL REFERENCES laptops(riginalID),
        username INTEGER NOT NULL REFERENCES users(username),
        startOfB datetime NOT NULL,
        endOfB datetime CHECK(endOfB>startOfB),
        hasRiterned BOOLEAN NOT NULL,
        PRIMARY KEY (riginalID, username)
      )
    """
    cursor.execute(sql)

  except sqlite3.Error as e:
     print(f"SQL Error: {e}")
    
def addUser(cursor):
  try:
    sql = "INSERT into users (username, password, name, mahzor, strikes) VALUES ('"
    sql += input("Enter username: ") + "', '" + input("Enter password: ") + "', '" + input("Enter full name: ") + "', '" + input("Enter mahzor: ") + "', 0)"
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
        2. Add User
        0. Exit""")
      choice = input("Enter your choice: ")
      if choice == "1":
        initTables(stmt)
      elif choice == "2":
        addUser(stmt)
      elif choice == "0":
        keepOn = False
        conn.commit()
        conn.close()
  except sqlite3.Error as e:
     print(f"SQL Error: {e}")

def main():
  showMenu()
main()