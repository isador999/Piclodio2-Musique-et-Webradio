#!/usr/bin/env python
import os
from os import path, getcwd
os.environ['DJANGO_SETTINGS_MODULE'] = 'piclodio.settings'
import sys
from django.core.wsgi import get_wsgi_application
SITE_ROOT = os.path.dirname(os.path.realpath(__file__))
sys.path.append(SITE_ROOT)
application = get_wsgi_application()
from webgui.models import *
import urllib

# Getting Alarmclock object from database
acid = sys.argv[1]
ac = Alarmclock.objects.get(id=acid)
# get base directory
base_dir = os.path.dirname(path.abspath(__file__))
# get player
player = Player()


# check alarmclock.mode to play music or radio
if ac.mode == "Radio":
	radio = ac.webradio
	player.play(radio)
else : 
	player.playmusicrandom()


mp3_backup_path = base_dir + '/backup_mp3/*.mp3'

# ----------------
# Class
# ----------------
class PlayerThread():
    def __init__(self, cmd):
        self.cmd = cmd
        self.process = None

    def run(self, timeout=0):
        def target():
            print 'Thread started'
            self.process = subprocess.Popen(self.cmd, shell=True)
            self.process.communicate()
            print 'Thread finished'

        thread = threading.Thread(target=target)
        thread.start()

        thread.join(timeout)
        try:
            if not thread.is_alive():
                print 'Mplayer not runing after timeout'
                self.process.terminate()
                thread.join()
        except OSError:
            print "Mplayer not runing after timeout. Start backup"
            if _backup_exist():
                PlayerThread('sudo mplayer '+mp3_backup_path).run(timeout=3)


def _backup_exist():
    filelist = glob.glob(mp3_backup_path)
    print filelist
    if filelist:
        return True
    return False

# ----------------
# Main programm
# ----------------
# Check if autosnooze activated
if ac.snooze != 0:
    cmd = 'echo "sudo /usr/bin/killall mplayer" | sudo /usr/bin/at "now +' + str(ac.snooze) + ' minute"'
    p = subprocess.Popen(cmd, shell=True)

# check if URL is available
try:
    http_code = urllib.urlopen(radio.url).getcode()
except IOError:
    http_code = 0
if http_code == 200:
    # URl may be availlable, but no stream inside, so we check if mplayer is running
    # Program a check in 3 secondes
    cmd = 'sudo mplayer '+radio.url
    player_thread = PlayerThread(cmd)
    player_thread.run(timeout=3)
else:
    # play backup MP3
    radio.url = mp3_backup_path
    player.play(radio)

