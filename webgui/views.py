#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from webgui.models import Webradio, Player, Alarmclock, Music
from webgui.forms import WebradioForm, MusicForm
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import os
import subprocess
from time import gmtime, strftime
from django.core.files import File
import sqlite3
import random




def homepage(request):
    try:
        radio = Webradio.objects.get(selected=1)
    except Webradio.DoesNotExist:
        radio = None
    player = Player()
    listalarmclock = Alarmclock.objects.all()
    # clock
    clock = strftime("%H:%M:%S")
    return render(request, 'homepage.html', {'radio': radio,
                                             'player': player,
                                             'listalarmclock': listalarmclock,
                                             'clock': clock})


def webradio(request):
    listradio = Webradio.objects.all()
    return render(request, 'webradio.html', {'listradio': listradio})


def addwebradio(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = WebradioForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # save web radio
            form.instance.selected = False
            form.save()
            return redirect('webgui.views.webradio')
    else:
        form = WebradioForm() # An unbound form

    return render(request, 'addwebradio.html', {'form': form})


def addmusic(request):
    save = False

    if request.method == "POST":
	form = MusicForm(request.POST, request.FILES)
	if form.is_valid():
		music = Music()
		music.name = form.cleaned_data["name"]
		music.path = form.cleaned_data["path"]
		music.fichier = form.cleaned_data["fichier"]
		music.save()

		save = True
		return redirect('webgui.views.music')
    else:
	form = MusicForm()
    return render(request, 'addmusic.html', locals())
#    if request.method == 'POST':  # If the form has been submitted...
#        form = MusicForm(request.POST)  # A form bound to the POST data
#        if form.is_valid():  # All validation rules pass
            # save web radio
#            form.instance.selected = False
#            form.save()
#            return redirect('webgui.views.music')
#    else:
#        form = MusicForm() # An unbound form

#    return render(request, 'addmusic.html', {'form': form})



def deleteWebRadio(request, id):
    radio = Webradio.objects.get(id=id)
    radio.delete()
    return redirect('webgui.views.webradio')


def deleteMusic(request, id):
    music = Music.objects.get(id=id)
    music.delete()
    return redirect('webgui.views.music')



def options(request):
    scriptPath = os.path.dirname(os.path.abspath(__file__))+"/utils/picsound.sh"
    currentVolume = subprocess.check_output([scriptPath, "--getLevel"])
    currentMute = subprocess.check_output([scriptPath, "--getSwitch"])
    return render(request,'options.html', {'currentVolume':currentVolume,'currentMute':currentMute})


def debug(request):
    todisplay = 'hello world debug'
    return render(request,'debug.html', {'todisplay':todisplay})


def play(request, id):
    # get actual selected radio if exist
    try:
        selectedradio = Webradio.objects.get(selected=1)
        # unselect it
        selectedradio.selected = False
        selectedradio.save()
    except Webradio.DoesNotExist:
        selectedradio = None    
    
    # set the new selected radio
    radio = Webradio.objects.get(id=id)
    radio.selected = True
    radio.save()
    player = Player()
    player.play(radio)

    time.sleep(2)

    if not player.isStarted():  # then start the backup mp3
        player = Player()
        radio = Webradio
        radio.url = 'mplayer backup.mp3'
        player.play(radio)

    return redirect('webgui.views.homepage')


def stop(request):
    player = Player()
    player.stop()
    # sleep to be sure the process have been killed
    time.sleep(1)
    return redirect('webgui.views.homepage')
    

def alarmclock(request):
    listAlarm = Alarmclock.objects.all()
    return render(request, 'alarmclock.html',{'listAlarm': listAlarm})


#### type of AlarmClock (Music / Webradio) ####  Added by Isador
#def typeAlarmClock(request):
#    typeAlarm = Alarmclock.objects.get(type)
#    if (typeAlarm.type==music):
#	MusicAlarm = True
#	RadioAlarm = False
#        typeAlarm.enablemusic()
#    else:
#        typeAlarm.type==webradio
#	RadioAlarm = True
#	MusicAlarm = False
#        typeAlarm.disablemusic()
#    typeAlarm.save()
#    return redirect('webgui.views.alarmclock')


def music(request):
    listmusic = Music.objects.all()
#   print listmusic
    return render(request, 'music.html',{'listmusic': listmusic})



def playmusic(request, id):
    music = Music.objects.get(id=id)
    conn = sqlite3.connect("/var/www/Piclodio2/piclodio.db")
    cur = conn.cursor()

    cur.execute("SELECT path FROM webgui_music WHERE id=?", str(id))
    path = cur.fetchone()[0]

    player = Player()
    player.playmusic(path)

    return redirect('webgui.views.music')  



def playmusicrandom(request):
    conn = sqlite3.connect("/var/www/Piclodio2/piclodio.db")
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM webgui_music")
    rows = cur.fetchone()[0]

    selected_row = random.randint(1, rows)

    cur.execute("SELECT path FROM webgui_music WHERE id=?", str(selected_row))
    path = cur.fetchone()[0]

    player = Player()
    player.playmusic(path)

    return redirect('webgui.views.homepage')


def activeAlarmClock(request, id, type):
    typealarm = Alarmclock.objects.get(type=type)
    alarmclock = Alarmclock.objects.get(id=id)


    if typealarm == "radio":
	if not alarmclock.active:
	    alarmclock.active = True
	    alarmclock.enable()
	else:
	    alarmclock.active = False
	    alarmclock.disable()
    else:
	typealarm = "music"
	if not alarmclock.active:
	    alarmclock.active = True
	    alarmclock.enablemusic()
	else:
	    alarmclock.active = False
	    alarmclock.disablemusic()
        
    alarmclock.save()

    return redirect('webgui.views.alarmclock')



@csrf_exempt 
def addalarmclock(request):
    if request.method == 'POST':
        label = request.POST['label']
        hour = request.POST['hour']
        minute = request.POST['minute']
        snooze = request.POST['snooze']
        id_webradio = request.POST['webradio']
        dayofweek = request.POST['dayofweek']
        type = request.POST['type']
    
        # check if label not empty and days selected
        if label == "" or dayofweek == "" or type == "":
            json_data = json.dumps({"HTTPRESPONSE": "error"})
            return HttpResponse(json_data, mimetype="application/json")
        
        # save object in database
        alarmclock = Alarmclock()
        alarmclock.label = label
        alarmclock.hour = hour
        alarmclock.minute = minute
        alarmclock.period = dayofweek
        alarmclock.snooze = snooze
	alarmclock.type = type
	if alarmclock.type == "music":

	    webradio = Webradio.objects.get(id=id_webradio)
	    alarmclock.webradio = webradio
            alarmclock.active = True
            alarmclock.save()
        else:
	    alarmclock.active = True
	    alarmclock.save()
	


        # set the cron
        alarmclock = Alarmclock.objects.latest('id')
        alarmclock.enable()

        # return the base URL of current instance
        url = request.build_absolute_uri('alarmclock')

        json_data = json.dumps({"HTTPRESPONSE":url})
        return HttpResponse(json_data, mimetype="application/json")
    
    else:  # not post, show the form
        listradio = Webradio.objects.all()
        return render(request, 'addalarmclock.html', {'rangeHour': range(24),
                                                      'rangeMinute': range(60),
                                                      'rangeSnooze': range(121),
                                                      'listradio': listradio})


def deleteAlarmClock(request, id):
    alarmclock = Alarmclock.objects.get(id=id)
    alarmclock.disable()
    alarmclock.delete()
    return redirect('webgui.views.alarmclock')


def volumeup(request, count):
    scriptPath = os.path.dirname(os.path.abspath(__file__))+"/utils/picsound.sh"
    subprocess.call([scriptPath, "--up", count])
    return redirect('webgui.views.options')


def volumedown(request, count):
    scriptPath = os.path.dirname(os.path.abspath(__file__))+"/utils/picsound.sh"
    subprocess.call([scriptPath, "--down", count])
    return redirect('webgui.views.options')


def volumeset(request, volume):
    scriptPath = os.path.dirname(os.path.abspath(__file__))+"/utils/picsound.sh"
    subprocess.call([scriptPath, "--setLevel", volume])
    return redirect('webgui.views.options')


def volumetmute(request):
    scriptPath = os.path.dirname(os.path.abspath(__file__))+"/utils/picsound.sh"
    subprocess.call([scriptPath, "--toggleSwitch"])
    return redirect('webgui.views.options')

