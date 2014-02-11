#!/usr/bin/env python

"""
Monitor the Daylite Touch logfile and
notify the administrator of any syncs.

A sync is an up- or download of data
to a mobile device (iPad, iPhone)

This is useful to check the health of
a network with many mobile clients.

This is the CLIENT script.
Run this file on the machine where you
want to receive notifications about the
syncs.
"""


import time
import pusherclient
import sh

def sync_callback(data):
    """
    Show a notification about the sync.
    """
    title = "Daylite sync"
    cmd = '-e display notification {} with title "{}"'.format(data, title)
    sh.osascript(cmd)

def connect_handler(data):
    channel = pusher.subscribe("dtouch_channel")
    channel.bind('sync', sync_callback)

if __name__ == '__main__':

    # YOUR APPKEY HERE
    appkey = 'XXXXXXXXXXXXXXXXXXXX'

    pusher = pusherclient.Pusher(appkey)

    pusher.connection.bind('pusher:connection_established', connect_handler)
    pusher.connect()

    while True:
        time.sleep(1)

