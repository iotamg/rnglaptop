from flask import Flask, request
import pymysql
import subprocess
import sqlMain
import serial
from datetime import datetime
import time
import threading

ard = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#n = ard.readline().decode().strip()
openedLately = False

app = Flask(__name__)
subprocess.Popen([
    "lxterminal", "-e",
    "ngrok http --domain=linette-exudative-delorse.ngrok-free.dev 5000"
])  # start ngrok public url forwarding to localhost:5000
db_conn = pymysql.connect(host="localhost",
                          user="root",
                          password="1234",
                          database="RNG")
cursor = db_conn.cursor()  # globally??


@app.route('/action', methods=['GET'])
def action_handler():
    action = request.args.get('action')
    id = request.args.get('user')
    password = request.args.get('password')
    if action == "login":
        return sqlMain.login(id, password)
    elif action == "take":
        rsp = sqlMain.borrow(id, password)
        if rsp["status"] == "approved":
            ard.write("open".encode()) # send an "open" command to the arduino
            ard.write(rsp["computer"].encode()) # send the computer number to the arduino
        if ard.readline().decode().strip() == "False": #False if the pc isnt in the slot
            if (!sqlMain.addBorrow(id, rsp["computer"])) print(f"{datetime.now()}\tError:\tPC taken but not added to database.")
            return rsp
        else: return {"status": "declined", "reason": "notTaken"}
    elif action == "return":
        if (request.args.get('computer') is None): 
            userTakenComputers = sqlMain.userTakenComputers(id)
        else: userTakenComputers = [request.args.get('computer')]
        if len(userTakenComputers) == 0:
            return {"status": "declined", "reason": "userHasNoComputers", "taken": sqlMain.getAllTakenComputers()}
        if len(userTakenComputers) == 1:
            rsp = sqlMain.returnPC(id, password,
                                      userTakenComputers[0])
            if rsp["status"] == "approved":
                ard.write("open".encode()) # send a "open" command to the arduino
                ard.write(userTakenComputers[0].encode()) # send the computer number to the arduino
                # Wait up to 5 seconds for a response, checking every 50ms
                start = time.time()
                while ard.in_waiting == 0:
                    if time.time() - start > 5:
                        return {"status": "declined", "reason": "arduinoTimeout"}
                    time.sleep(0.05)  # tiny sleep so we don't burn 100% CPU
                if ard.readline().decode().strip() == True: #True if the pc is in the slot
                    if (!sqlMain.closeBorrow(id, userTakenComputers[0])): print(f"{datetime.now()}\tError:\tPC returned but not updated in the database.")
                else: return {"status": "declined", "reason": "unreturned"}
            return rsp
        else:
            return {"status": "declined", "reason": "multipleComputers", "list": userTakenComputers}
                
        
    elif action == "listTakenComputers":
        return sqlMain.getAllTakenComputers(id, password)
    else:
        return {"status": "error", "reason": "invalid action"}

def backgroundWorker(pc,action): ##pc num, action True if return, False if take
    #### check in ard if taken or not
    ard.write("check".encode())
    ard.write(pc.encode())
    wait = time.time()
    while ard.in_waiting == 0:
        if time.time() - start > 2:
            print(f"{datetime.now()}\tError:\tArduino timeout.")
            break #stop waiting for the arduino
        time.sleep(0.5)
    ans = if ard.readline().decode().strip() == "True": #True if the pc is in the slot
    
    ### if falslely, adjust sql acrodingly to irl
def backgroundWorker():
    while True:
        if openedLately:
            openedLately = False
            if (gpio read if door open): ########
                ard.write("count".encode())
                wait = time.time()
                while ard.in_waiting == 0:
                    if time.time() - start > 2:
                        print(f"{datetime.now()}\tError:\tArduino timeout.")
                        break #stop waiting for the arduino
                    time.sleep(0.5)
                ans = are.readline().decode().strip() #returing 5 digits of which pc are counted for
                for (i = 0; i < 5; i+=1):
                    if (ans[i] == "1"):
                        if sqlMain.isTaken(i+1):
                            sqlMain.closeBorrow(0, i+1) #system user ID is 0
                            print(f"{datetime.now()}\tError:\tPC {i+1} was registered as taken but is counted for. Records fixed.")
                    elif !sqlMain.isTaken(i+1):
                        sqlMain.addBorrow(0, i+1) #system user ID is 0
                        print(f"{datetime.now()}\tError:\tPC {i+1} was registered as returned but is counted for. Records fixed.")
            
        

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
