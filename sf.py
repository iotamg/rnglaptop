from flask import Flask, request
import mysql.connector

app = Flask(__name__)

db_conn = mysql.connector.connect(
    host="localhost",
    user="flask_user",
    password="your_password",
    database="mydb"
)
cursor = db_conn.cursor() # globally??

@app.route('/action', methods=['GET'])
def action_handler():
    action = request.args.get('action')
    if action == "login":
        user = request.args.get('user')
        password = request.args.get('password')
    
        # Print to terminal
        print("---- Incoming Request ----")
        print("Action:", action)
        print("User:", user)
        print("Password:", password)
        print("--------------------------")
        # SQL query
        cursor.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE id = {user} AND password = \"{password}\")")
        result = cursor.fetchone()
        if result[0] == 1:
            print("Login successful")
            return {"status": "success",
                    "user": user}
        else:
            print("Login failed")
            return {"status": "failed"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
