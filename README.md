Daylite Touch Notify -- A work in progress
==========================================

Monitor Daylite Touch syncs on your Mac.
This is useful for admins, who want to be sure that the Daylite Server is correctly working.

The software will use watchdog to check changes in the Daylite Touch logfile.
Whenever a user syncs with Daylite, this file gets modified.
A script will be triggered on the server side, which sends a message to a client (presumably with
websockets or a push service). On the client side, another script receives the
message and displays an OSX notification of the synchronization.
