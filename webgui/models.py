from django.db import models
import subprocess
import os
import string
from webgui.crontab import *
import threading
import time


    #### type # Added here and in SQLITE by Isador ####
class Music(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
#   track = models.CharField(max_length=40)
#   artist = models.CharField(max_length=40)
    name = models.CharField(max_length=60)
    path = models.CharField(max_length=60)
    selected = models.BooleanField(default=False)  # is the Music selected to be played


    def __unicode__(self):
	return self.name


class Webradio(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.CharField(max_length=100)
    url = models.CharField(max_length=100)
    selected = models.BooleanField()  # is the webradio selected to be played
    

class Alarmclock(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    label = models.CharField(max_length=100)
    hour = models.IntegerField(blank=True)
    minute = models.IntegerField(blank=True)
    period = models.CharField(max_length=100)    # cron syntax dow (day of week)
    active = models.BooleanField()
    snooze = models.IntegerField(blank=True)
    webradio = models.ForeignKey(Webradio)
    #### type # Added here and in SQLITE by Isador ####
    music = models.ForeignKey(Music)
    type = models.TextField(default='music')



    def enable(self):
        """
        enable The alarm clock. Set it into the crontab
        """
        base_dir = os.path.dirname(os.path.dirname(__file__))
        cron = Crontab()
        cron.minute = self.minute
        cron.hour = self.hour
        cron.period = self.period
        cron.comment = "piclodio "+str(self.id)
        cron.command = "env DISPLAY=:0.0 python "+base_dir+"/runWebRadio.py "+str(self.id)
        cron.create()

    ##### Add Crontab Line for Music ##### Added by Isador
    def enablemusic(self):
        """
        enable The alarm clock. Set it into the crontab
        """
        base_dir = os.path.dirname(os.path.dirname(__file__))
        cron = Crontab()
        cron.minute = self.minute
        cron.hour = self.hour
        cron.period = self.period
        cron.comment = "piclodio-music "+str(self.id)
        cron.command = "env DISPLAY=:0.0 python "+base_dir+"/random-music.sh "+str(self.id)
        cron.create()


    def disable(self):
        """
        disable the alarm clock. remove it from the crontab
        """
        cron = Crontab()
        cron.comment = "piclodio "+str(self.id)
        cron.remove()

    ##### Disable the Crontab Line for Music ##### Added by Isador
    def disablemusic(self):
        """
        disable the alarm clock. remove it from the crontab
        """
        cron = Crontab()
        cron.comment = "piclodio-music "+str(self.id)
        cron.remove()



class Player():
    """
    Class to play music with mplayer
    """
    def __init__(self):
        self.status = self.isStarted()

    def play(self, radio):
        # kill process if already running
        if self.isStarted():
            self.stop()

        url = radio.url  # get the url
        splitUrl =string.split(url, ".")
        sizeTab= len(splitUrl)
        extension=splitUrl[sizeTab-1]
        command= self.getthegoodcommand(extension)

        p = subprocess.Popen(command+radio.url, shell=True)



    def playmusic(self, path):
	if self.isStarted():
            self.stop()
	command = "sudo /usr/bin/mplayer "
	p = subprocess.Popen(command+path, shell=True)




    def stop(self):
        """
        Kill mplayer process
        """
        p = subprocess.Popen("sudo killall mplayer", shell=True)
        p.communicate()
   
    def getthegoodcommand(self, extension):
        """
        switch extension, start mplay differently
        """
        return {
            'asx': "sudo /usr/bin/mplayer -playlist "

        }.get(extension, "sudo /usr/bin/mplayer ")  # default is mplayer

    def isStarted(self):
            # check number of process
            p = subprocess.Popen("sudo pgrep mplayer", stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()
            if output == "":
                    return False
            else:
                    return True
