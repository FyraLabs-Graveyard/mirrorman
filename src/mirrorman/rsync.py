import threading
import sysrsync
import time
import os

import mirrorman.config as config

class rsyncThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.rsync = sysrsync
        self.name = "rsyncThread"
        self.config = config

    def run(self):
        print("Starting " + self.name)
        # write the pid to a file
        pid = str(os.getpid())
        pidfile = open("mirrorman.pid", "w")
        pidfile.write(pid)
        pidfile.close()
        try:
            self.rsync.run(
                source="rsync://lapis.ultramarine-linux.org:20251/pub",
                destination=self.config.get("sync_dir") + "pub",
                # follow symlinks
                verbose=True,
                sync_source_contents=True,
                options=["-a", "-L", "-K", "--progress"],
            )
            os.remove("mirrorman.pid")
        except:
            print("Error: unable to start thread")
            os.remove("mirrorman.pid")
        print("Exiting " + self.name)
        # delete the pid file


class syncWatcherThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.name = "syncWatcherThread"
        self.timer = 1800  # change to 1800 for 30 minutes

    def run(self):
        # every 30 minutes check the timestamp of the last sync
        # if it's older than 30 minutes, run rsync
        print("Starting " + self.name)
        while True:
            if self.timer == 1800:
                self.sync()
                self.timer = 0
            else:
                # print("Waiting for next sync")
                self.timer += 1
                time.sleep(1)

    def sync(self):
        # check if sync is already running
        # check the pid file
        if os.path.isfile("mirrorman.pid"):
            # check if the pid is still running
            pidfile = open("mirrorman.pid", "r")
            pid = pidfile.read()
            pidfile.close()
            if os.path.exists("/proc/" + pid):
                #print("Sync is already running")
                return
            else:
                # else if the process is not running, remove the pid file
                os.remove("mirrorman.pid")
                print(
                    "PID file exists but process is not running, probably crashed. Removing PID file"
                )
                rsyncThread().start()
        else:
            print("Running sync")
            rsyncThread().start()

    def resetTimer(self):
        self.timer = 0
