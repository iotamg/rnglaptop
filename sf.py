from flask import Flask, request
import pymysql
import subprocess
import sqlMain
import serial

ard = serial.Serial('/dev/ttyACM0', 9600, timeout=1)
#n = ard.readline().decode().strip()

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
        return rsp if ard.readline().decode().strip() == True else {"status": "declined", "reason": "untaken"}
    elif action == "return":
        rsp = sqlMain.returnPC(id, password,
                                      request.args.get('computer'))
    elif action == "listTakenComputers":
        return sqlMain.getAllTakenComputers(id, password)
    else:
        return {"status": "error", "reason": "invalid action"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
