from flask import Flask, request
import pymysql
import subprocess
import sqlMain

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
        return sqlMain.borwoComputer(id, password)
    elif action == "return":
        return sqlMain.returnComputer(id, password,
                                      request.args.get('computer'))
    elif action == "listTakenComputers":
        return sqlMain.getAllTakenComputers(id, password)
    else:
        return {"status": "error", "reason": "invalid action"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
