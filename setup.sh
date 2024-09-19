#!/bin/bash

# Log file location
LOGFILE="setup.log"

# Function to log both stdout and stderr to a file
log() {
    echo "$1" | tee -a "$LOGFILE"
}

log "Starting setup..."

# Update system packages
log "Updating package list..."
sudo apt-get update >> $LOGFILE 2>&1

# Download Python script
log "Downloading Python script..."
sudo curl -O https://raw.githubusercontent.com/Flore1945/WhiteBull/main/main.py >> $LOGFILE 2>&1

# Install Python dependencies
log "Installing Python dependencies..."
sudo apt-get install -y python3-pip >> $LOGFILE 2>&1
sudo pip3 install simple-websocket requests >> $LOGFILE 2>&1

# Run Python script in background
log "Running Python script in the background..."
nohup python3 main.py --id="$1" --token="$2" --atoken="$3" > main.py.log 2>&1 &

log "Python setup completed."

# Download and install Gaganode
log "Downloading Gaganode package..."
curl -O https://assets.coreservice.io/public/package/60/app-market-gaga-pro/1.0.4/app-market-gaga-pro-1_0_4.tar.gz >> $LOGFILE 2>&1

log "Extracting Gaganode package..."
tar -zxf app-market-gaga-pro-1_0_4.tar.gz >> $LOGFILE 2>&1
rm -f app-market-gaga-pro-1_0_4.tar.gz >> $LOGFILE 2>&1

# Install Gaganode
log "Installing Gaganode..."
sudo ./apphub-linux-amd64/apphub service remove >> $LOGFILE 2>&1
sudo ./apphub-linux-amd64/apphub service install >> $LOGFILE 2>&1
sudo ./apphub-linux-amd64/apphub service start >> $LOGFILE 2>&1

# Check Gaganode status
log "Checking Gaganode status..."
./apphub-linux-amd64/apphub status >> $LOGFILE 2>&1

# Set Gaganode token
log "Setting Gaganode token..."
sudo ./apphub-linux-amd64/apps/gaganode/gaganode config set --token="ylyfkvzdgupeuuaw2f3d15a4b38ed7e6" >> $LOGFILE 2>&1

# Restart Gaganode
log "Restarting Gaganode..."
./apphub-linux-amd64/apphub restart >> $LOGFILE 2>&1

log "Gaganode setup completed."

# Finish
log "Setup completed."
