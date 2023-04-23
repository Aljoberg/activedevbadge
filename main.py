from flask import Flask, request, redirect
import requests, json, threading, websocket, sys, os
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

def host_temp(token):
    def on_open(ws): ws.send(json.dumps({"op": 2, "d": {"token": token, "intents": 1, "properties": {"os": "linux"}}}))
    def rai(ws): 
       ws.close()
       sys.exit()
    def on_message(ws, msg):
        print(msg)
        msg = json.loads(msg)
        if msg["t"] == "INTERACTION_CREATE": requests.post(f"https://discord.com/api/interactions/{msg['d']['id']}/{msg['d']['token']}/callback", headers={"authorization": f"Bot {token}"}, json={"type": 4, "data": {"content": "hello", "flags": 64}})
    #websocket.enableTrace(True)
    websocket.WebSocketApp("wss://gateway.discord.gg", on_open=on_open, on_message=on_message, on_close=rai).run_forever()
@app.route('/', methods=["GET", "POST"])
def hello_world():
    if request.method == "GET": return redirect("https://adb.js.org")
    headers = {'Authorization': f'Bot {request.json["token"]}'}
    resp = requests.get('https://discord.com/api/users/@me', headers=headers)
    if resp.status_code == 401:
        return "invalid token", 401
    else:
        data = resp.json()
        command_data = {'name': 'devbadge', 'description': 'Execute this for the dev badge!'}
        headers = {'Content-Type': 'application/json', 'Authorization': f'Bot {request.json["token"]}'}
        url = f'https://discord.com/api/applications/{data["id"]}/commands'
        sus = requests.post(url, headers=headers, json=command_data)
        if sus.ok:
            threading.Thread(target=host_temp, args=[request.json["token"]]).start()
    return "worked"
app.run("0.0.0.0", os.getenv("PORT"))
