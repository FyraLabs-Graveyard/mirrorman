
import mirrorman.rsync as rsync
import signal
import os
import sys
#rsync.rsyncThread().start()
rsync.syncWatcherThread().start()

# catch SIGINT and SIGTERM
def signal_handler(signal, frame):
    print('Interrupted')
    os.remove("mirrorman.pid")
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)