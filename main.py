import asyncio
from simple_websocket import Client, ConnectionClosed
import requests
import json
import time
import threading
import argparse


# Function to get the container info
def _container(account_token, container_id, container_token):
    r = requests.get(
        f'https://paiza.cloud/api/containers/{container_id}?container_token={container_token}',
        headers={"Authorization": f"Bearer {account_token}"})
    print(f"[-] Container info request {r.status_code}")


# Function to keep the container alive
def _container_keep_alive(account_token, container_id, container_token, ssid):
    r = requests.get(
        f'https://paiza.cloud/api/containers/{container_id}/keepalive?container_token={container_token}&updatedBy={ssid}',
        headers={"Authorization": f"Bearer {account_token}"})
    print(f"[-] Container keep alive {r.status_code}")


# Function for active keep alive
def _active_keep_alive(account_token, container_id, container_token):
    while True:
        r = requests.get(
            f'https://paiza.cloud/api/containers/{container_id}/activeKeepalive?container_token={container_token}',
            headers={"Authorization": f"Bearer {account_token}"})
        print(f"[-] Active keep alive {r.status_code}")
        time.sleep(300)  # Active keep-alive interval


# Main function to handle WebSocket and keep the container alive
def main(account_token, container_id, container_token):
    while True:
        # Grab the post_ssid
        ws = Client.connect(
            f'wss://paiza.cloud/socket.io-client/?token={account_token}&EIO=3&transport=websocket'
        )
        while True:
            data = ws.receive()
            if 'sid' in data:
                ssid = json.loads(data[1:]).get('sid')
                print(f"[-] SSID {ssid}")
                break

        # Get container info
        _container(account_token, container_id, container_token)
        time.sleep(15)

        # Keep container alive
        _container_keep_alive(account_token, container_id, container_token,
                              ssid)
        time.sleep(5)

        # Ping the ssid and close the connection
        ws.send('2')
        time.sleep(1)
        ws.close()
        print('[-] Connection closed repeating..')
        print('')
        time.sleep(40)


# Function to start both the main and active keep alive functions in separate threads
def start_threads(account_token, container_id, container_token):
    # Create threads for main and _active_keep_alive
    main_thread = threading.Thread(target=main,
                                   args=(account_token, container_id,
                                         container_token))
    active_keep_alive_thread = threading.Thread(target=_active_keep_alive,
                                                args=(account_token,
                                                      container_id,
                                                      container_token))

    # Start both threads
    main_thread.start()
    active_keep_alive_thread.start()

    # Optionally, join the threads to ensure they continue running
    main_thread.join()
    active_keep_alive_thread.join()


if __name__ == "__main__":
    # Set up argument parsing
    parser = argparse.ArgumentParser(
        description="Paiza Cloud Container Manager")
    parser.add_argument('--id', type=str, required=True, help='Container ID')
    parser.add_argument('--token',
                        type=str,
                        required=True,
                        help='Container Token')
    parser.add_argument('--atoken',
                        type=str,
                        required=True,
                        help='Account Token')

    args = parser.parse_args()

    # Start the threads with the parsed arguments
    start_threads(args.atoken, args.id, args.token)
