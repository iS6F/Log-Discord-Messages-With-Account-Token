import json, websocket, threading, time

def send(ws, request):
    ws.send(json.dumps(request))   
def receive(ws):
    response = ws.recv()
    if response:
        return json.loads(response)
def heartbeat(interval, ws):
    while True:
        time.sleep(interval)
        heartbeatJSON = {
            "op": 1,
            "d": "null"
        }
        send(ws, heartbeatJSON)

ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
heartbeat_interval = receive(ws)['d']['heartbeat_interval']
heartbeat_interval = heartbeat_interval / 800 # You can change the hearbeat ms here but i recommend 800, 750 or 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws, ))
token = '' # Enter your account token here

pl = {
    'op': 2,
    'd': {
        'token': token,
        'intents': 513,
        'properties': {
            '$os': 'linux',
            '$browser': 'chrome',
            '$device': 'pc',
        }
    }
}

send(ws, pl)
while True:
    e = receive(ws)   
    try:    
        content = e['d']['content']
        un = e['d']['author']['username']
        server = e['d']['guild_id']
        channel = e['d']['channel_id']      
        print(f'[{server} -> {channel}] {un} : {content}') # You can change the output message here      
    except:
        pass
