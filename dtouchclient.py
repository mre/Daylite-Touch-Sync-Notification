#!/usr/bin/env python

import sys
sys.path.append('..')

import time
import pusherclient

global pusher

def sync_callback(data):
    print "Sync Callback: %s" % data

def connect_handler(data):
    channel = pusher.subscribe("dtouch_channel")
    channel.bind('sync', sync_callback)

if __name__ == '__main__':

    # YOUR APPKEY HERE
    appkey = 'XXXXXXXXXX'

    pusher = pusherclient.Pusher(appkey)

    pusher.connection.bind('pusher:connection_established', connect_handler)
    pusher.connect()

    while True:
        time.sleep(1)
