import json
import threading
import time
import websocket


def check_websocket(ws, request):
    ws.send(json.dumps(request))


def recieve_json_response(ws):
    response = ws.recv()
    if response:
        return json.loads(response)


def heartbeat(interval, ws):
    while True:
        time.sleep(interval)
        heartbeatJSON = {"op": 1, "d": "null"}
        check_websocket(ws, heartbeatJSON)
        print("Heartbeat sent")


def extract(event):
    message = f"{event['d']['author']['username']}:{event['d']['content']}"
    return message


ws = websocket.WebSocket()
ws.connect('wss://gateway.discord.gg/?v=6&encording=json')
event = recieve_json_response(ws)
heartbeat_interval = event['d']['heartbeat_interval'] / 1000
threading._start_new_thread(heartbeat, (heartbeat_interval, ws))
check_websocket(ws, {'op': 2, 'd': {'token': "โทเค่น", 'properties': {
                '$os': 'windows', '$browser': 'chrome', '$device': 'pc'}}})
while True:
    event = recieve_json_response(ws)
    try:
        if event['d']['channel_id'] == 'ห้อง' and event['d']['guild_id'] == 'เซิร์ฟ':
            message = extract(event)
            print(message)
    except:
        pass
