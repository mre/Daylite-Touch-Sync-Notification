#!/usr/bin/env python

"""
Monitor the Daylite Touch syncfile (DLTouchd.log)
and notify the administrator of any syncs.

A sync is an up- or download of data
to a mobile device (iPad, iPhone)

This is useful to check the health of
a network with many mobile clients.
"""

# Needed for monitoring
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import traceback

# Needed to see what has changed
from sh import TAIL, GREP
import re

# Needed for notifications
import pusher
from os.path import expanduser
import logging

# Specify your pusher API credentials
app_id = 'XXXXX'
key = 'XXXXXXXXXXXXXXXXXXXX'
secret = 'XXXXXXXXXXXXXXXXXXXX'

DAYLITE_PATH = "/Library/Logs/Daylite Server 4/"
FILENAME = "DLTouchd.log"
syncfile = DAYLITE_PATH + FILENAME

# Store all notifications in a custom logfile
home = expanduser("~")
logfile = home + "/Library/Logs/dtouchserver.log"

class SyncHandler(FileSystemEventHandler):
    """
    Handles Daylite Touch syncs.
    """
    def on_modified(self, event):
        """
        Gets called on modifications to the Daylite Touch syncfile
        Try to get the user and the number of changes and send a push
        notification to a client (e.g. the administrator of the network)
        """
        if FILENAME not in event.src_path:
          # Wrong file was modified. Bail.
          return

        try:
            # Get sync data
            last_login = get_last_login(syncfile)
            username = get_username(last_login)
            outgoing, incoming = get_changes(last_login)

            # Send a push notification
            notification = 'Sync from {} (OUT:{}/IN:{})'.format(username, outgoing, incoming)
            p = pusher.Pusher(app_id=app_id, key=key, secret=secret)
            p['dtouch_channel'].trigger('sync', notification)

            # Store synchronization in logfile
            logging.info(notification)
        except Exception, e:
            # Print the whole traceback for debugging purposes
            traceback.print_exc()

def get_last_login(syncfile):
  """
  Get last login from whole syncfile
  E.g. from commandline: tail -n 11 syncfile | grep -A 10 Login
  """
  # Look for a login within the last n lines of the syncfile
  tail = TAIL.bake("-n", 15)
  # Print n lines of trailing context after each login
  grep = GREP.bake("-A", 10)
  try:
      # Look for "Login" in syncfile
      return str(grep(tail(syncfile), "Login"))
  except:
      return None

def get_username(last_log):
  """
  Match username. For instance, get "johannes" in the following string:
  'Login from client johannes:00000000-XXXX-XXXX.'
  """
  m = re.search("client (?P<username>.*):.*\s", last_log)
  return m.group("username")

def get_changes(last_log):
  """
  Match outgoing and incoming changes, e.g. 2 and 0 from:
  'Outgoing changes: 2; Incoming changes: 0'
  """
  m = re.search("Outgoing changes:\s(?P<outgoing>\d+)", last_log)
  outgoing = m.group("outgoing")
  m = re.search("Incoming changes:\s(?P<incoming>\d+)", last_log)
  incoming = m.group("incoming")
  return outgoing, incoming

if __name__ == "__main__":
    """
    Watch the Daylite Touch Sync log for changes.
    """

    logging.basicConfig(filename=logfile,
                        level=logging.DEBUG,
                        format='%(asctime)s %(message)s')

    logging.info("Starting Daylite Touch sync notification")
    sync_handler = SyncHandler()
    observer = Observer()
    observer.schedule(sync_handler, path=DAYLITE_PATH, recursive=False)
    observer.start()

    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
