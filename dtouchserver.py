#!/usr/bin/env python

"""
Monitor the Daylite Touch logfile and
notify the administrator of any syncs.

A sync is an up- or download of data
to a mobile device (iPad, iPhone)

This is useful to check the health of
a network with many mobile clients.
"""

# Needed for monitoring
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Needed to see what has changed
from sh import TAIL, GREP
import re

# Needed for notifications
import pusher

# Specify your pusher API credentials
app_id = 'XXXXX'
key = 'XXXXXXXXXXXXXXXXXXXX'
secret = 'XXXXXXXXXXXXXXXXXXXX'

DAYLITE_PATH = "/Library/Logs/Daylite Server 4/"
FILENAME = "DLTouchd.log"
logfile = DAYLITE_PATH + FILENAME

class SyncHandler(FileSystemEventHandler):
    """
    Handles Daylite Touch syncs.
    """
    def on_modified(self, event):
        """
        Gets called on modifications to the Daylite Touch logfile
        Try to get the user and the number of changes and send a push
        notification to a client (e.g. the administrator of the network)
        """
        try:
            # Get sync data
            last_login = get_last_login(logfile)
            username = get_username(last_login)
            outgoing, incoming = get_changes(last_login)

            # Send a push notification
            notification = 'Sync from {} (OUT:{}/IN:{})'.format(username, outgoing, incoming)
            p = pusher.Pusher(app_id=app_id, key=key, secret=secret)
            p['dtouch_channel'].trigger('sync', notification)

        except Exception, e:
            print e

def get_last_login(logfile):
  """
  Get last login from whole logfile
  E.g. from commandline: tail -n 11 logfile | grep -A 10 Login
  """
  # Look for a login within the last n lines of the logfile
  tail = TAIL.bake("-n", 15)
  # Print n lines of trailing context after each login
  grep = GREP.bake("-A", 10)
  try:
      # Look for "Login" in logfile
      return str(grep(tail(logfile), "Login"))
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


