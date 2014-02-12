#!/bin/bash

# Stop on first error
set -e

echo "Run this script on the machine where the notifications shall appear"
echo "==================================================================="

echo "Copying the client program to the /usr/bin directory..."
echo "The installation requires root privileges."
sudo cp dtouchclient.py /usr/bin/.

echo "Copying the plist file into the LaunchAgents directory..."
cp de.matthias-endler.dtouchclient.plist ~/Library/LaunchAgents/.

echo "Loading the plist file..."
launchctl load ~/Library/LaunchAgents/de.matthias-endler.dtouchclient.plist

echo "All done. Client is now up and running"
