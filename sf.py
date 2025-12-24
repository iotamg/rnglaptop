from flask import Flask, request
import pymysql
import subprocess

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
        if (check_login(id, password)):
            cursor.execute(f"SELECT name FROM users WHERE id = {request.args.get('user')}")
            result = cursor.fetchone()
            if result:
                return {"status": "loggedIn", "name": result[0]}
        return {"status": "notLoggedIn"} # if it fails to find the user
    elif action == "take":
        if (check_login(id, password)):
            computer = getComputer(id) #0 if no computer available, else computer number
            if computer == 0:
                return {"status": "declined", "reason": "noComputers"}
            else:
                return {"status": "approved", "computer": computer}
        else:
            return {"status": "declined", "reason": "credentials"}
    elif action == "return":
        if (check_login(id, password)):
            computer = userTakenComputers(id) #a list, of what computers are taken by that user.
            if len(computer) == 0:
                return {"status": "declined", "reason": "userHasNoComputers"}
            else:
                return {"status": "approved", "computers": computer}
        else:
            return {"status": "declined", "reason": "credentials"}
    else:
        return {"status": "error", "reason": "invalid action"}
def check_login(user, password):
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
    if (id == 666): 
        return 5 #temporarily
    else: 
        return 0 #temporarily

def userTakenComputers(id):
    #return a list of computers that the user has taken
    if (id == 666): #temporarily
        return [1, 3, 4] 
    else:
        return []
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
