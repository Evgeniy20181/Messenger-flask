from flask import *
from datetime import datetime
import time
app = Flask(__name__)
messages = [
{"username":"Jack","text":"Hello","time":time.time()},
    ]
users = {
    # username:password
    'jack':'1234',
    'Geka':'2016'
    }
@app.route("/")
def hello():
    return "Hello, World!"
@app.route("/status")
def status():
    return {
        "status":True,
        "time":datetime.now(),
        "users":len(users),
        "messages":len(messages)
        }
@app.route("/send", methods=['POST'])
def send():
    data = request.json
    username = data["username"]
    text = data["text"]
    password = data['password']
    if username in users:
        password_real = users[username]
        if password_real != password:
            return {'ok':False}
    else:
        users[username] = password
    messages.append({"username":username,"text":text, "time":time.time()})
    return {"ok": True}
@app.route("/history")
def history():
    """
request: ?after 123456789.4567
response:{
    "messages":[
        {"username":"str","text":"str","time":"float"}
    ]
}
"""
    after = float(request.args['after'])
    filter_messages = []
    for message in messages:
        if after < message['time']:
            filter_messages.append(message)
    return {"messages":filter_messages}
app.run()
