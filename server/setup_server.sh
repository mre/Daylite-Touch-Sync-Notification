#!/bin/bash

# Stop on first error
set -e

echo "Run this script on the machine with your Daylite Server installed."
echo "=================================================================="

echo "Copying the server program to the /usr/bin directory..."
echo "The installation requires root privileges."
sudo cp dtouchserver.py /usr/bin/.

echo "Copying the plist file into the LaunchAgents directory..."
cp de.matthias-endler.dtouchserver.plist ~/Library/LaunchAgents/.

echo "Loading the plist file..."
launchctl load ~/Library/LaunchAgents/de.matthias-endler.dtouchserver.plist

echo "All done. Server is now up and running"
