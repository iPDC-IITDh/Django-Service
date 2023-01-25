import asyncio
import json
import random
import websockets

connected_clients = set()

async def send_random_number():
    while True:
        number = random.randint(100, 200)
        json_response = {"number": number}
        json_response = json.dumps(json_response)
        await asyncio.wait([client.send(json_response) for client in connected_clients])
        await asyncio.sleep(1)

async def handle_client(websocket, path):
    connected_clients.add(websocket)
    try:
        await asyncio.gather(websocket.recv(), send_random_number())
    finally:
        connected_clients.remove(websocket)

start_server = websockets.serve(handle_client, "localhost", 4443)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()

