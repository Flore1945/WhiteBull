#!/bin/bash

log() {
    echo "$1"
}

sudo curl -O https://raw.githubusercontent.com/Flore1945/WhiteBull/main/main.py
sudo pip3 install simple-websocket requests
nohup python3 main.py --id="$1" --token="$2" --atoken="$3" > main.py.log 2>&1 &

curl -O https://assets.coreservice.io/public/package/60/app-market-gaga-pro/1.0.4/app-market-gaga-pro-1_0_4.tar.gz
tar -zxf app-market-gaga-pro-1_0_4.tar.gz
rm -f app-market-gaga-pro-1_0_4.tar.gz

sudo ./apphub-linux-amd64/apphub service remove
sudo ./apphub-linux-amd64/apphub service install
sudo ./apphub-linux-amd64/apphub service start

while true; do
    STATUS_OUTPUT=$(./apphub-linux-amd64/apphub status)
    echo "$STATUS_OUTPUT"
    if echo "$STATUS_OUTPUT" | grep -q "RUNNING"; then
        log "Gaganode is RUNNING."
        break
    else
        log "Gaganode not RUNNING yet. Waiting..."
        sleep 5
    fi
done

sudo ./apphub-linux-amd64/apps/gaganode/gaganode config set --token="ylyfkvzdgupeuuaw2f3d15a4b38ed7e6"
./apphub-linux-amd64/apphub restart
