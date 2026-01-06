from flask import Flask, request
import pymysql
import subprocess
import sqlMain
app = Flask(__name__)
subprocess.Popen(["lxterminal", "-e", "ngrok http --domain=linette-exudative-delorse.ngrok-free.dev 5000"]) # start ngrok public url forwarding to localhost:5000
db_conn = pymysql.connect(
    host="localhost",
    user="root",
    password="1234",
    database="RNG"
)
cursor = db_conn.cursor() # globally??

@app.route('/action', methods=['GET'])
def action_handler():
    action = request.args.get('action')
    id = request.args.get('user')
    password = request.args.get('password')
    if action == "login":
        return login(id,password)
    elif action == "take":
        return getComputer(id,password)
    elif action == "return":
        if (sqlMain.check_login(id, password)):
            computer = sqlMain.userTakenComputers(id) #a list, of what computers are taken by that user.
            if len(computer) == 0:
                return {"status": "declined", "reason": "userHasNoComputers"}
            else:
                return {"status": "approved", "computers": computer}
        else:
            return {"status": "declined", "reason": "credentials"}
    elif action == "listTakenComputers":
        if (sqlMain.check_login(id, password)):
            return {"list": sqlMain.allTakenComputers()} #a list, of what computers are taken
        else:
            return {"status": "declined", "reason": "credentials"}
    else:
        return {"status": "error", "reason": "invalid action"}

def login(id, password):
    if (sqlMain.check_login(id, password)):
        cursor.execute(f"SELECT name FROM users WHERE id = {request.args.get('user')}")
        result = cursor.fetchone()
        if result:
            return {"status": "loggedIn", "name": result[0]}
    return {"status": "notLoggedIn"} # if it fails to find the user
def getComputer(id,password):
    if (sqlMain.check_login(id, password)):
        computer = sqlMain.getComputer(id) #0 if no computer available, else computer number
        if computer == 0:
            return {"status": "declined", "reason": "noComputers"}
        else:
            return {"status": "approved", "computer": computer}
    else:
        return {"status": "declined", "reason": "credentials"}



if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
