"""
Monitor the Daylite Touch logfile and
notify the administrator of any syncs.
"""

from sh import tail, grep
import re


def get_last_login(logfile):
  """
  Get last login from whole logfile
  E.g. from commandline: tail -n 11 logfile | grep -A 10 Login
  """
  return str(grep(tail("-n", 11, logfile), "-A", 10, "Login"))

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

logfile = "/Library/Logs/Daylite\ Server\ 4/DLTouchd.log"
#logfile = "DLTouchd.log"
last_log = get_last_login(logfile)
username = get_username(last_log)
outgoing, incoming = get_changes(last_log)

print "Sync from {} (OUT:{}/IN:{})".format(username, outgoing, incoming)
