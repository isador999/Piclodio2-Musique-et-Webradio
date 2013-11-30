import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'piclodio.settings'
import sys
from django.conf import settings
from django.db import models
from webgui.models import *
import subprocess

#Getting Alarmblock object from database
acid = sys.argv[1]
ac = Alarmclock.objects.get(id=acid)

#Check if autosnooz activated

snooz = ac.snooz
#snooz=20
if snooz != 0:
    cmd='echo "sudo /usr/bin/killall mplayer" | /usr/bin/at "now +'+str(snooz)+' minute"'
    p = subprocess.Popen(cmd, shell=True)

#Play the radio
player = Player()
player.play(ac.webradio)
