Daylite Touch Notify - work in progress
=======================================

What is it?
-----------

Monitor Daylite Touch syncs on your Mac.
This is useful for admins, who want to be sure that the Daylite Server is correctly working.

The software will use [watchdog](https://pypi.python.org/pypi/watchdog) to check changes in the Daylite Touch logfile.
Whenever a user syncs with Daylite, this file gets modified.
A script will be triggered on the server side, which sends a message to a client (using [pusher](http://www.pusher.com)). On the client side, another script receives the
message and displays an OSX notification of the synchronization.


Howto
-----

1. Get an API key at [pusher.com](http://www.pusher.com)
2. Insert your key into `dtouchclient.py` and `dtouchserver.py`
3. Start `dtouchserver.py` on your server.
4. Start `dtouchclient.py` on your client.

Running the script in the background
------------------------------------

If you want to have the script running as a daemon process which starts automatically, you can use launchctl and a plist file on Mac OS X.

To have it run as a daemon process, move the included plist file into the
LaunchAgents directory:

    mv de.matthias-endler.dtouch.plist ~/Library/LaunchAgents/.

Move the client program to the `/usr/bin` directory:

    mv dtouchclient.py /usr/bin

Then use launchctl to load the plist from a terminal:

    launchctl load ~/Library/LaunchAgents/de.matthias-endler.dtouch.plist

This will load that script and immediately run the program in the <string> element beneath <key>Program</key>. You can also specify arguments for the program using a <ProgramArguments> node with an array of <string> elements. For more information see the launchd.plist man page

If you want to remove the script, you can use the unload command of launchctl:

    launchctl unload ~/Library/LaunchAgents/de.matthias-endler.dtouch.plist

(Instructions adapted from [mnem on StackOverflow](http://stackoverflow.com/a/9523030/270334))
