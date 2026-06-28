from flask import Flask, request
import pymysql
import subprocess
import systemA
import serial
from datetime import datetime
import time
import threading
import atexit


# to read: n = ard.readline().decode().strip()

try:
    ard = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
except serial.serialutil.SerialException:
    quit(f"{datetime.now()}\tError:\tArduino not connected.")
except Exception as e:
    quit(f"{datetime.now()}\tError:\t{e}")
    

openedLately = False

app = Flask(__name__)
ngrok_process = subprocess.Popen([
    "lxterminal", "-e",
    "ngrok http --domain=linette-exudative-delorse.ngrok-free.dev 5000"
])  # start ngrok public url forwarding to localhost:5000

def cleanup():
    ngrok_process.terminate()

atexit.register(cleanup)
db_conn = pymysql.connect(host="localhost",
                          user="root",
                          password="1234",
                          database="RNG",
                          autocommit=True)
cursor = db_conn.cursor()  

def backgroundWorker(user,pc,action): ##pc num, action True if return, False if take
    
    #### voltage version:
    # ard.write("check".encode())
    # ard.write(pc.encode())
    # wait = time.time()
    # while ard.in_waiting == 0:
    #     if time.time() - wait > 2:
    #         print(f"{datetime.now()}\tError:\tArduino timeout.")
    #         return #stop waiting for the arduino
    #     time.sleep(0.5)
    # if action: ## if action is return
    #     if ard.readline().decode().strip() == "True": ##if actually returned
    #         systemA.closeBorrow(user, pc)
    #     else:
    #         print(f"{datetime.now()}\tAlert:\tPC {pc} was assigned to be returned but user didn't returned in time.")
    # else: ##if action is take
    #     if ard.readline().decode().strip() == "False": ##if actually taken
    #         systemA.addBorrow(user, pc)
    #     else:
    #         print(f"{datetime.now()}\tAlert:\tPC {pc} was assigned to be taken but user didn't took in time.")

    #### no voltage version:
    pcs = systemA.checkInv()
    if action: ## if action is return
        if pc in pcs: ##if actually returned
            systemA.closeBorrow(user, pc)
        else:
            ## Dont sign as returned, keep borrow open
            print(f"{datetime.now()}\tAlert:\tPC {pc} was assigned to be returned but user didn't returned in time.")
    else: ##if action is take
        if pc not in pcs: ##if actually taken
            systemA.addBorrow(user, pc)
            print(f"{datetime.now()}\tTake:\tPC {pc} was taken by user {user}.")
        else:
            ## Dont sign as taken, do not make a borrow
            print(f"{datetime.now()}\tAlert:\tPC {pc} was assigned to be taken but user didn't took in time.")
thread = None

@app.route('/action', methods=['GET'])
def action_handler():
    global thread
    action = request.args.get('action')
    id = request.args.get('user')
    password = request.args.get('password')
    if action == "login":
        return systemA.login(id, password)
    elif action == "take":
        if thread is not None and thread.is_alive():
            thread.join() ##don't execute anything until thread is closed
        rsp = systemA.borrow(id, password)
        if rsp["status"] == "approved":
            ard.write("open".encode()) # send an "open" command to the arduino
            ard.write(rsp["computer"].encode()) # send the computer number to the arduino
            thread = threading.Thread(target=backgroundWorker, args=(id, rsp["computer"],False)) ##pc num, False to indicate a "take"
            thread.start()
            print(f"{datetime.now()}\tTake:\tAssigned PC {rsp['computer']} to user: {id}")
        print("Response: ", rsp)
        return rsp
    elif action == "return":
        if thread is not None and thread.is_alive():
            thread.join() ##don't execute anything until thread is closed
        if (request.args.get('computer') is None): ##no specific pc indicated
            userTakenComputers = systemA.userTakenComputers(id) ##then fetch a list of user taken pcs
        else: userTakenComputers = [request.args.get('computer')] ##indicated pc (specific), to list.
        if len(userTakenComputers) == 0: ##user has no computers and not indicated a pc
            print({"status": "declined", "reason": "userHasNoComputers", "taken": systemA
                     .getAllTakenComputers(id, password)})
            return {"status": "declined", "reason": "userHasNoComputers", "taken": systemA
                    .getAllTakenComputers(id, password)} ##give the app a list of taken computers to suggest to user
        if len(userTakenComputers) == 1: ##user has one computer or indicated a pc
            rsp = systemA.returnPC(id, password,
                                      userTakenComputers[0])
            if rsp["status"] == "approved":
                ard.write("open".encode()) # send a "open" command to the arduino
                ard.write(userTakenComputers[0].encode()) # send the computer number to the arduino
                # Wait up to 5 seconds for a response, checking every 50ms
                thread = threading.Thread(target=backgroundWorker, args=(id, userTakenComputers[0],True)) ##pc num, True to indicate a "return"
                thread.start()
            print("Response: ", rsp)
            return rsp
        else:
            print({"status": "declined", "reason": "multipleComputers", "list": userTakenComputers})
            return {"status": "declined", "reason": "multipleComputers", "list": userTakenComputers}
                
        
    elif action == "listTakenComputers":
        if thread is not None and thread.is_alive():
            thread.join() ##don't execute anything until thread is closed
        return systemA.getAllTakenComputers(id, password)
    else:
        return {"status": "error", "reason": "invalid action"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True, use_reloader=False)
