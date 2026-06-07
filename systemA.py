import pymysql
import time
import RPi.GPIO as GPIO
import random
from datetime import datetime



conn = None
cursor = None
try:
  conn = pymysql.connect(host="localhost",
                         user="root",
                         password="1234",
                         database="RNG")
  cursor = conn.cursor()
except pymysql.Error as e:
  print(f"SQL Error: {e}")


def initTables():
  if not cursor:
    return
  try:
    sql = """
    DROP TABLE IF EXISTS users;
    DROP TABLE IF EXISTS laptops;
    DROP TABLE IF EXISTS borrows;
    DROP TABLE IF EXISTS history;
    """
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
        number TEXT NOT NULL,
        date_of_purchase DATE NOT NULL,
        functional BOOLEAN NOT NULL
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
         hisrotyID INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
         userTake INTEGER REFERENCES users(id),
         userReturn INTEGER REFERENCES users(id) NOT NULL,
         laptopID INTEGER  REFERENCES laptops(laptopID) NOT NULL,
         start DATETIME NOT NULL,
     end DATETIME NOT NULL CHECK(endDate>startDate)
      );
    """
  except pymysql.Error as e:
    print(f"SQL Error: {e}")


def addBorrow(borrower, pc):
  if not cursor:
    return False
  try:
    sql = f"""
            WHEN NOT EXISTS (SELECT 1 FROM borrows WHERE laptopID={pc}) 
            THEN
              INSERT into borrows(laptopID,userTake,start) VALUES (
              {pc},{borrower},NOW()
              );
        """
    cursor.execute(sql)
    return True if cursor.rowcount == 1 else False
  except pymysql.Error as e:
    print(f"SQL Error: {e}")


def closeBorrow(returner, pc):
  if not cursor:
    return False
  try:
    cursor.execute(f"SELECT 1 FROM borrows WHERE laptopID={pc}")
    result = cursor.fetchone()
    if not result:
      return False
    sql = f"""
      INSERT INTO history (userTake, userReturn, laptopID, start, end)
SELECT userTake, {returner}, laptopID, start, NOW()
FROM borrows
WHERE laptopID = {pc}
LIMIT 1;
        """
    cursor.execute(sql)
    sql = f"""
            DELETE FROM borrows WHERE laptopID = {pc};
        """
    cursor.execute(sql)
    return True if cursor.rowcount == 1 else False
  except pymysql.Error as e:
    print(f"SQL Error: {e}")
    return f"{e}"


def addUser(id_, password_, name_, mahzor_):
  if not cursor:
    return
  try:
    sql = f"""INSERT into users (id, password, name, mahzor, strikes) VALUES (
    '{id_}','{password_}','{name_}','{mahzor_}')
    """
    cursor.execute(sql)
  except pymysql.Error as e:
    print(f"SQL Error: {e}")


def addComputer(id_, grade_, number_, date_, functional_):
  if not cursor:
    return
  try:
    sql = f"""INSERT into laptops (laptopID, grade, number, date_of_purchase, functional) VALUES (
    '{id_}','{grade_}','{number_}','{date_}',1)
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
        3. Add Computer
        4. Show Users
        5. not fucntional
        0. Exit""")
      choice = input("Enter your choice: ")
      if choice == "1":
        initTables()
      elif choice == "2":
        ID = input("id=?")
        NAME = input("name=?")
        PASWORD = input("password=?")
        grade = input("machzor=?")
        addUser(ID, PASWORD, NAME, grade)
      elif choice == "3":
        ID = input("id=?")
        GRADE = input("grade=?")
        NUMBER = input("number=?")
        DATE = input("date=?")
        addComputer(ID, GRADE, NUMBER, DATE, 1)
      elif choice == "4":
        cursor.execute("SELECT * FROM users")
        results = cursor.fetchall()
        print(results)
      elif choice == "5":
        if input("by id? (yes to confirm)") == "yes":
          ID = input("id=?")
          cursor.execute(f"SET functional=0 WHERE laptopID={ID}")
        FUCTIONAL = input("fuctional=?")
        GRADE = input("grade=?")
        NUMBER = input("number=?")
        cursor.execute(
            f"SET functional={FUCTIONAL} WHERE grade={GRADE} AND number={NUMBER}"
        )
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
  cursor.execute(
      f"SELECT EXISTS(SELECT 1 FROM users WHERE id = {user} AND password = \"{password}\")"
  )
  result = cursor.fetchone()
  if result and result[
      0] == 1:  # if it got a result and the result is 1 (null-safe)
    print("Login Accepted")
    return True
  else:
    print("Login Failed")
    return False


#return a list of computers that the user has taken
def userTakenComputers(id):
  if not cursor:
    return []
  sql = f"""
    SELECT laptopID FROM history
    WHERE borworer={id}
    GROUP BY laptopID
    """
  cursor.execute(sql)
  result = cursor.fetchall()
  arr = []
  for i in range(len(result)):
    arr[i] = result[i][0]
  return arr


def allTakenComputers():
  if not cursor:
    return []
  sql = """
    SELECT laptopID FROM borrows
    GROUP BY laptopID
    """
  cursor.execute(sql)
  result = cursor.fetchall()
  arr = []
  for i in range(len(result)):
    arr[i] = result[i][0]
  return arr


def login(id, password):
  if not cursor:
    return {"status": "notLoggedIn"}
  if (check_login(id, password)):
    cursor.execute(f"SELECT name FROM users WHERE id = {id}")
    result = cursor.fetchone()
    if result:
      return {"status": "loggedIn", "name": result[0]}
  return {"status": "notLoggedIn"}  # if it fails to find the user


def borrow(id, password):
  if (check_login(id, password)):
    
    ##code without voltage checking
    computer = checkInv()
    if not computer: ##empty list
      return {"status": "declined", "reason": "noComputers"}
    else:
      return {"status": "approved", "computer": computer[random.randint(0,len(computer)-1)]}
  else:
    return {"status": "declined", "reason": "credentials"}


def returnPC(id, password, pc):
  if (check_login(id, password)):
    pcs = allTakenComputers()
    if pc not in pcs:
      return {"status": "declined", "reason": "notTaken"}
    return {"status": "approved", "computer": pc}
  else:
    return {"status": "declined", "reason": "credentials"}


def getAllTakenComputers(id, password):
  if (check_login(id, password)):
    return {"list": allTakenComputers()}  #a list, of what computers are taken
  else:
    return {"status": "declined", "reason": "credentials"}

def main():
  showMenu()


if __name__ == "__main__":
  main()


GPIO.setmode(GPIO.BCM)
pcsPins = [26,19,13,6,5]
GPIO.setup(pcsPins[0], GPIO.IN, pull_up_down=GPIO.PUD_UP) ## 1
GPIO.setup(pcsPins[1], GPIO.IN, pull_up_down=GPIO.PUD_UP) ## 2
GPIO.setup(pcsPins[2], GPIO.IN, pull_up_down=GPIO.PUD_UP) ## 3
GPIO.setup(pcsPins[3], GPIO.IN, pull_up_down=GPIO.PUD_UP) ## 4
GPIO.setup(pcsPins[4], GPIO.IN, pull_up_down=GPIO.PUD_UP) ## 5

def checkInv(): ##check which pcs are in the inventory
    pcsAvailable = []
    for i in range(len(pcsPins)):
        if GPIO.input(pcsPins[i]) == GPIO.LOW:
            pcsAvailable.append(i+1) ##pc in stock
    print(f"{datetime.now()}\tCheckInv:\t{pcsAvailable}")
    return pcsAvailable