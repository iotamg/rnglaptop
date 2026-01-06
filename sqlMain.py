import pymysql

conn = None
cursor = None
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
  if not cursor:
    return
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
    )
    """
    cursor.execute(sql)
    sql = """
      CREATE TABLE IF NOT EXISTS borrows(
        regionalID INTEGER NOT NULL,
        studentID INTEGER NOT NULL,
        startOfB DATETIME NOT NULL,
        PRIMARY KEY (regionalID, studentID),
        FOREIGN KEY (regionalID) REFERENCES laptops(regionalID),
        FOREIGN KEY (studentID) REFERENCES users(id)
      )
    """
    cursor.execute(sql)
    sql = """
      CREATE TABLE IF NOT EXISTS history(
         hisrotyID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
         reterner INTEGER REFERENCES users(id),
     borworer INTEGER REFERENCES users(id) NOT NULL,
         regionalID INTEGER  REFERENCES laptops(regionalID) NOT NULL,
         startDate DATETIME NOT NULL,
     endDate DATETIME NOT NULL CHECK(endDate>startDate)
      );
    """
  except pymysql.Error as e:
    print(f"SQL Error: {e}")

def addBorow(borower,coumputer,time):
    if not cursor:
        return
    try:
        sql=f"""
            WHEN NOT EXISTS (SELECT 1 FROM borrows WHERE regionalID={coumputer}) 
            THEN 
              INSERT into history(borworer,regionalID,startDate) VALUES (
              {borower},{coumputer},{time}
              )
              INSERT into borrows(regionalID,studentID,startOfB) VALUES (
              {coumputer},{borower},{time}
              )
        """
        cursor.execute(sql)
    except pymysql.Error as e:
        print(f"SQL Error: {e}")
def addReturn(returner,coumputer,time):
    if not cursor:
        return
    try:
        sql=f"""
            UPDATE history SET reterner={returner},endDate={time} WHERE regionalID={coumputer} AND endDate IS NULL
        """
        cursor.execute(sql)
        sql=f"""
            DELETE FROM borrows WHERE regionalID={coumputer} 
            AND EXISTS 
            (SELECT 1 FROM history WHERE regionalID={coumputer} AND endDate IS NOT NULL AND endDate={time} AND reterner={returner})
        """
        cursor.execute(sql)
    except pymysql.Error as e:
        print(f"SQL Error: {e}")
def addUser(id_,password_,name_,mahzor_):
  if not cursor:
    return
  try:
    sql = f"""INSERT into users (id, password, name, mahzor, strikes) VALUES (
    '{id_}','{password_}','{name_}','{mahzor_}')
    """
    cursor.execute(sql)
  except pymysql.Error as e:
     print(f"SQL Error: {e}")

def showMenu():
  if not cursor or not conn:
    return
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
        ID=input("id=?")
        NAME=input("name=?")
        PASWORD=input("password=?")
        grade=input("machzor=?")
        addUser(ID,PASWORD,NAME,grade)
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
def check_login(user, password):
  if not cursor:
    return False
  # Print to terminal
  print("Checking User: ", user)
  cursor.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE id = {user} AND password = \"{password}\")")
  result = cursor.fetchone()
  if result and result[0] == 1: # if it got a result and the result is 1 (null-safe)
      print("Login Accepted")
      return True
  else:
      print("Login Failed")
      return False
def getComputer(id):
  #if there is no computers availabe, return 0
  #else, return the computer number
  if id == "666": 
      return 5 #temporarily
  else: 
      return 0 #temporarily

def userTakenComputers(id):
  #return a list of computers that the user has taken
  if id == "666": #temporarily
      return [1, 3, 4] 
  else:
      return []
def allTakenComputers():
  #return a list of computers that are taken
  return [1, 3, 4]

def login(id, password):
    if not cursor:
        return {"status": "notLoggedIn"}
    if (check_login(id, password)):
        cursor.execute(f"SELECT name FROM users WHERE id = {id}")
        result = cursor.fetchone()
        if result:
            return {"status": "loggedIn", "name": result[0]}
    return {"status": "notLoggedIn"} # if it fails to find the user

def borwoComputer(id,password):
    if (check_login(id, password)):
        computer = getComputer(id) #0 if no computer available, else computer number
        if computer == 0:
            return {"status": "declined", "reason": "noComputers"}
        else:
            return {"status": "approved", "computer": computer}
    else:
        return {"status": "declined", "reason": "credentials"}

def returnComputer(id,password,computer):
    if (check_login(id, password)):
        computer = userTakenComputers(id) #a list, of what computers are taken by that user.
        if len(computer) == 0:
            return {"status": "declined", "reason": "userHasNoComputers"}
        else:
            return {"status": "approved", "computers": computer}
    else:
        return {"status": "declined", "reason": "credentials"}

def getAllTakenComputers(id,password):
    if (check_login(id, password)):
        return {"list": allTakenComputers()} #a list, of what computers are taken
    else:
        return {"status": "declined", "reason": "credentials"}


def main():
  showMenu()
main()