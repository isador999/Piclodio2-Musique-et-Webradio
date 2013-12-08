from django.db import models
from time import gmtime, strftime, localtime
import subprocess
import time, os, string
from crontab import CronTab

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
    active =    models.BooleanField()
    snooze =    models.IntegerField(blank=True)
    webradio =  models.ForeignKey(Webradio)
    
    # enable The alarm clock. Set it into the crontab   
    def enable(self):
        BASE_DIR = os.path.dirname(os.path.dirname(__file__))
        cron    = CronTab()                                      # get actual crontab
        cronLine = str(self.minute)+" "+str(self.hour)+" * * "+self.period
        job  = cron.new(command="python "+ BASE_DIR+"/runWebRadio.py "+str(self.id),comment='piclodio'+str(self.id))
        job.setall(cronLine)
        job.enable()
        cron.write()
        
    # disable the alarm clock. remove it from the crontab    
    def disable(self):    
        cron    = CronTab()
        cron.remove_all(comment='piclodio'+str(self.id))
        cron.write()
        
class Player():
    "Constructor"
    def __init__(self):
        self.status = self.isStarted()
        
    def isStarted(self):
        # check number of process
        p = subprocess.Popen("sudo pgrep mplayer", stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
        if output =="":
                return False
        else:
                return True
            
    def play(self,radio):
        # kill process if already running
        if (self.isStarted):
            self.stop()
        
        url = radio.url # get the url
        splitUrl =string.split(url, ".")
        sizeTab= len(splitUrl)
        extension=splitUrl[sizeTab-1]
        command= self.getthegoodcommand(extension)
        
        p = subprocess.Popen(command+radio.url, shell=True)    
        
    def stop(self):
        p = subprocess.Popen("sudo killall mplayer", shell=True)
        (output, err) = p.communicate()
   
    # switch extension, start mplay differently     
    def getthegoodcommand(self,extension):
         return {
                 'asx': "sudo /usr/bin/mplayer -playlist "

         }.get(extension,"sudo /usr/bin/mplayer ")  # default is mplayer  
