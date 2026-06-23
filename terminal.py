import pymysql

conn = None
cursor = None
try:
    conn = pymysql.connect(
        host="localhost", user="root", password="1234", database="RNG", autocommit=True
    )
    cursor = conn.cursor()
except pymysql.Error as e:
    print(f"SQL Error: {e}")


def initTables():
    if not cursor:
        return
    try:
        sql = """DROP TABLE IF EXISTS history;"""
        cursor.execute(sql)
        sql = """DROP TABLE IF EXISTS borrows;"""
        cursor.execute(sql)
        sql = """DROP TABLE IF EXISTS laptops;"""
        cursor.execute(sql)
        sql = """DROP TABLE IF EXISTS users;"""
        cursor.execute(sql)
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
        laptopID INTEGER PRIMARY KEY NOT NULL,
        grade TEXT NOT NULL,
        number TEXT NOT NULL
    )
    """
        cursor.execute(sql)
        sql = """
      CREATE TABLE IF NOT EXISTS borrows(
        laptopID INTEGER NOT NULL,
        userTake INTEGER NOT NULL,
        start DATETIME NOT NULL,
        PRIMARY KEY (laptopID, userTake),
        FOREIGN KEY (laptopID) REFERENCES laptops(laptopID),
        FOREIGN KEY (userTake) REFERENCES users(id)
      )
    """
        cursor.execute(sql)
        sql = """
      CREATE TABLE IF NOT EXISTS history(
         historyID INTEGER NOT NULL PRIMARY KEY AUTO_INCREMENT,
         userTake INTEGER REFERENCES users(id),
         userReturn INTEGER REFERENCES users(id) NOT NULL,
         laptopID INTEGER  REFERENCES laptops(laptopID) NOT NULL,
         start DATETIME NOT NULL,
     end DATETIME NOT NULL CHECK(end > start)
      );
    """
        cursor.execute(sql)
    except pymysql.Error as e:
        print(f"SQL Error: {e}")


def addUser(id_, password_, name_, mahzor_):
    if not cursor:
        return
    try:
        sql = f"""INSERT into users (id, password, name, mahzor, strikes) VALUES (
    '{id_}','{password_}','{name_}','{mahzor_}',0)
    """
        cursor.execute(sql)
    except pymysql.Error as e:
        print(f"SQL Error: {e}")


def addComputer(id_, grade_, number_):
    if not cursor:
        return
    try:
        sql = f"""INSERT into laptops (laptopID, grade, number) VALUES (
    '{id_}','{grade_}','{number_}')
    """
        cursor.execute(sql)
    except pymysql.Error as e:
        print(f"SQL Error: {e}")


def showMenu():
    if not cursor or not conn:
        return
    keepOn = True
    try:
        while keepOn:
            print("""
        1. Initiate Tables
        2. Add User
        3. Add Computer
        4. Show Users
        0. Exit""")
            choice = input("Enter your choice: ")
            if choice == "1":
                initTables()
            elif choice == "2":
                ID = input("id=?")
                NAME = input("name=?")
                PSWD = input("password=?")
                grade = input("machzor=?")
                addUser(ID, PSWD, NAME, grade)
            elif choice == "3":
                ID = input("id=?")
                GRADE = input("grade=?")
                NUMBER = input("number=?")
                addComputer(ID, GRADE, NUMBER)
            elif choice == "4":
                cursor.execute("SELECT * FROM users")
                results = cursor.fetchall()
                print(results)
            elif choice == "0":
                keepOn = False
                conn.close()
            if keepOn and conn:
                conn.commit()
    except pymysql.Error as e:
        print(f"SQL Error: {e}")


def main():
    showMenu()


if __name__ == "__main__":
    main()
