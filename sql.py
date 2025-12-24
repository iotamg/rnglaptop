import pymysql

try:
  conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="RNG"
  )
  cursor = conn.cursor()
except pymysql.Error as e:
    print(f"SQL Error: {e}")
def initTables():
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
        regionalID INTEGER PRIMARY KEY NOT NULL,
        grade TEXT NOT NULL,
        number TEXT NOT NULL,
        date_of_purchase DATE NOT NULL
    )"""
    cursor.execute(sql)
    sql = """
      CREATE TABLE IF NOT EXISTS borrows(
        regionalID INTEGER NOT NULL,
        studentID INTEGER NOT NULL,
        startOfB TIMESTAMP NOT NULL,
        endOfB TIMESTAMP,
        hasReturned BOOLEAN NOT NULL,
        PRIMARY KEY (regionalID, studentID),
        FOREIGN KEY (regionalID) REFERENCES laptops(regionalID),
        FOREIGN KEY (studentID) REFERENCES users(id),
        CHECK(endOfB > startOfB)
      )
    """
    cursor.execute(sql)
  except pymysql.Error as e:
    print(f"SQL Error: {e}")
    
def addUser():
  try:
    sql = "INSERT into users (id, password, name, mahzor, strikes) VALUES ('"
    sql += input("Enter id: ") + "', '" + input("Enter password: ") + "', '" + input("Enter full name: ") + "', '" + input("Enter mahzor: ") + "', 0)"
    cursor.execute(sql)
  except pymysql.Error as e:
     print(f"SQL Error: {e}")

def showMenu():
  keepOn = True
  try:
    while (keepOn):
      print("""
        1. Initiate Tables
        2. Add User
        0. Exit""")
      choice = input("Enter your choice: ")
      if choice == "1":
        initTables()
      elif choice == "2":
        addUser()
      elif choice == "3":
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
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