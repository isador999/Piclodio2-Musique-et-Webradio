from django.db import models
from time import gmtime, strftime, localtime
import subprocess
import time

# WebRadio
class Webradio(models.Model):
    id =            models.IntegerField(primary_key=True, blank=True)
    name =          models.CharField(max_length=100)
    url =           models.CharField(max_length=100)
    selected =      models.BooleanField() # is the webradio selected to be played
    
# AlarmClock
class Alarmclock(models.Model):
    id =        models.IntegerField(primary_key=True, blank=True)
    label =     models.CharField(max_length=100)
    hour =      models.IntegerField(blank=True)
    minute =    models.IntegerField(blank=True)
    period =    models.CharField(max_length=100)    # cron syntax dow (day of week)
    active =    models.BooleanField()               # is this Alarm Clock active?
    webradio =  models.ForeignKey(Webradio)
    

class Player():
    "Constructor"
    def __init__(self):
        self.status = self.isStarted()
        
    def isStarted(self):
        # check number of process
        p = subprocess.Popen("pgrep mplayer", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output =="":
                return False
        else:
                return True
            
    def play(self,radio):
        # kill process if already running
        if (self.isStarted):
            self.stop()
        # play url
        p = subprocess.Popen("mplayer "+radio.url, stdout=subprocess.PIPE, shell=True)    
        
    def stop(self):
        p = subprocess.Popen("killall mplayer", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()