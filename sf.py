from flask import Flask, request
import pymysql

app = Flask(__name__)

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
    if action == "login":
        if (check_login(request.args.get('user'), request.args.get('password'))):
            return {"status": "loggedIn", "name": cursor.execute(f"SELECT name FROM users WHERE id = {request.args.get('user')}")}
        else:
            return {"status": "notLoggedIn"}
    if action == "take":
        pass
def check_login(user, password):
    # Print to terminal
    print("Checking User: ", user)
    cursor.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE id = {user} AND password = \"{password}\")")
    result = cursor.fetchone()
    if result[0] == 1:
        print("Login Accepted")
        return True
    else:
        print("Login Failed")
        return False
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
