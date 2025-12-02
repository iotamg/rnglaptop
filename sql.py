import pymysql

def initTables(cursor):
  try:
    sql = """
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER NOT NULL PRIMARY KEY,
      password  TEXT NOT NULL, 
      name TEXT NOT NULL,
      mahzor TEXT NOT NULL,
      strikes INTEGER NOT NULL CHECK(strikes>=0)
      )
    """
    cursor.execute(sql)
    sql = """
    CREATE TABLE IF NOT EXISTS laptops(
        regionalID TEXT NOT NULL,
        grade TEXT NOT NULL,
        number TEXT NOT NULL,
        date_of_purchase DATE NOT NULL
    )"""
    cursor.execute(sql)
    sql = """
      CREATE TABLE IF NOT EXISTS BOROWS(
        riginalID INTEGER NOT NULL REFERENCES laptops(riginalID),
        studantID INTEGER NOT NULL REFERENCES users(username),
        startOfB TIMESTAMP NOT NULL,
        endOfB TIMESTAMP CHECK(endOfB>startOfB),
        hasRiterned BOOLEAN NOT NULL,
        PRIMARY KEY (regionalID, username)
      )
    """
    cursor.execute(sql)
  except pymysql.Error as e:
     print(f"SQL Error: {e}")
    
def addUser(cursor):
  try:
    sql = "INSERT into users (id, password, name, mahzor, strikes) VALUES ('"
    sql += input("Enter id: ") + "', '" + input("Enter password: ") + "', '" + input("Enter full name: ") + "', '" + input("Enter mahzor: ") + "', 0)"
    cursor.execute(sql)
  except pymysql.Error as e:
     print(f"SQL Error: {e}")

def showMenu():
  keepOn = True
  try:
    conn = pymysql.connect(
        host="localhost",
        user="root",
        password="your_password",
        database="RNG"
    )
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
      elif choice == "3":
        stmt.execute("SELECT * FROM users")
        results = stmt.fetchall()
        print(results)
      elif choice == "0":
        keepOn = False
        conn.close()
      conn.commit()
  except pymysql.Error as e:
     print(f"SQL Error: {e}")

def main():
  showMenu()
main()