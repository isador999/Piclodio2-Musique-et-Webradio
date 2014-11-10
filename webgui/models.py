from django.db import models
from django.conf import settings
from django.http import HttpResponse
import subprocess
import os
import string
from webgui.crontab import *
import threading
import time
import sqlite3
import random


class Artist(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.CharField(max_length=60)
    style = models.CharField(max_length=20, blank=True)
    selected = models.BooleanField(default=False)


class Music(models.Model):
    id = models.IntegerField(primary_key=True, blank=True)
    name = models.CharField(max_length=60)
    path = models.FileField(upload_to='music', max_length=100)
    artist = models.ForeignKey(Artist)
    selected = models.BooleanField(default=False)


    @models.permalink
    def get_absolute_url(self):
        return ('upload-new', )

    def save(self, *args, **kwargs):
        self.path = self.path.name
        super(Music, self).save(*args, **kwargs)


    def deletefile(self):
	f = settings.MEDIA_ROOT +str(self.path)
	if os.path.exists(f):
            command = ("rm "+settings.MEDIA_ROOT)
	    subprocess.Popen(command +str(self.path), shell=True)



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
    webradio = models.ForeignKey(Webradio, null=True)
    mode = models.TextField(default='music')

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

    def disable(self):
        """
        disable the alarm clock. remove it from the crontab
        """
        cron = Crontab()
        cron.comment = "piclodio "+str(self.id)
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


    def playmusic(self, music):
        if self.isStarted():
            self.stop()
	
        command = ("sudo /usr/bin/mplayer "+settings.MEDIA_ROOT)
  	path = music.path
        p = subprocess.Popen(command+str(music.path), shell=True)
	p.wait()



    def playmusicrandom(self):
	####### Select IDs from databases #######
	conn = sqlite3.connect(settings.DATABASES['default']['NAME'])
        cur = conn.cursor()
        cur.execute("SELECT id FROM webgui_music")
        list_id = [row[0] for row in cur.fetchall()]

	#selected_ids = random.sample(list_id, 3)
	selected_id = random.choice(list_id)

	#for i in (selected_ids):

 	try:
            selectedmusic = Music.objects.get(selected=1)
            # unselect it
            selectedmusic.selected = False
            selectedmusic.save()
        except Music.DoesNotExist:
            selectedmusic = None

	try:
	    selectedartist = Artist.objects.get(selected=1)
	    selectedartist.selected = False
	    selectedartist.save()
	except Artist.DoesNotExist:
	    selectedartist = None


	music = Music.objects.get(id=selected_id)
	artist_id = music.artist.id
	artist = Artist.objects.get(id=artist_id)

	artist.selected = True
	artist.save()
	music.selected = True
	music.save()

	#music = Music.objects.get(id=i)
	#player = Player()
	self.playmusic(music)

#        player.playmusic(music)


#	s_id=random.choice(list_id)
#	music = Music.objects.get(id=s_id)
#	artist_id = music.artist.id
#	artist = Artist.objects.get(id=artist_id)
#	artist.selected = True
#	artist.save()
#	music.selected = True
#	music.save()
#
#	player.playmusic(music)
#


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
