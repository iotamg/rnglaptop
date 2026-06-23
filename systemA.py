import pymysql
import time
import RPi.GPIO as GPIO
import random
from datetime import datetime
import atexit



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

def addBorrow(borrower, pc):
  if not cursor:
    return False
  try:
    sql = f"""
        INSERT INTO borrows (laptopID, userTake, start)
        SELECT {pc}, {borrower}, NOW()
        WHERE NOT EXISTS (SELECT 1 FROM borrows WHERE laptopID = {pc});
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
  sql = f"SELECT laptopID FROM borrows WHERE userTake = {id}"
  cursor.execute(sql)
  result = cursor.fetchall()
  arr = []
  for pc in result:
    arr.append(pc[0])
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
  for pc in result:
    arr.append(pc[0])
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
    if int(pc) not in pcs:
      return {"status": "declined", "reason": "notTaken"}
    return {"status": "approved", "computer": pc}
  else:
    return {"status": "declined", "reason": "credentials"}


def getAllTakenComputers(id, password):
  if (check_login(id, password)):
    return {"list": allTakenComputers()}  #a list, of what computers are taken
  else:
    return {"status": "declined", "reason": "credentials"}

pcsPins = [26,19,13,6,5]
try:
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    for pin in pcsPins:
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
except Exception as e:
    print(f"GPIO setup error: {e}")
    print("Tip: run 'sudo pkill -f server.py' to kill old processes holding the GPIO pins, then restart.")

def checkInv(): ##check which pcs are in the inventory
    pcsAvailable = []
    for i in range(len(pcsPins)):
        if GPIO.input(pcsPins[i]) == GPIO.LOW:
            pcsAvailable.append(i+1) ##pc in stock
    print(f"{datetime.now()}\tCheckInv:\t{pcsAvailable}")
    return pcsAvailable

def cleanup():
    GPIO.cleanup()
atexit.register(cleanup)