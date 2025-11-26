from flask import Flask, request

app = Flask(__name__)

@app.route('/action', methods=['GET'])
def action_handler():
    action = request.args.get('action')
    user = request.args.get('user')
    password = request.args.get('password')

    # Print to terminal
    print("---- Incoming Request ----")
    print("Action:", action)
    print("User:", user)
    print("Password:", password)
    print("--------------------------")

    return {
        "status": "received",
        "action": action,
        "user": user,
        "password": password
    }

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
