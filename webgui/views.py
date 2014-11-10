#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from webgui.models import Webradio, Player, Alarmclock, Music, Artist
from webgui.forms import WebradioForm, ArtistForm
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from django.utils import simplejson
import json
import os
import subprocess
from time import gmtime, strftime
from django.core.urlresolvers import reverse
from django.conf import settings
import logging
import threading
import multiprocessing as mp



def homepage(request):
    try:
        radio = Webradio.objects.get(selected=1)
    except Webradio.DoesNotExist:
        radio = None

    try:
	music = Music.objects.get(selected=1)
    except Music.DoesNotExist:
	music = None

    try:
	artist = Artist.objects.get(selected=1)
    except Artist.DoesNotExist:
	artist = None


    player = Player()
    listalarmclock = Alarmclock.objects.all()
    # clock
    clock = strftime("%H:%M:%S")
    date = strftime("%A %d %b %Y")

    while True:
        return render(request, 'homepage.html', {'radio': radio,
					     'music': music,
					     'artist': artist,
                                             'player': player,
                                             'listalarmclock': listalarmclock,
                                             'clock': clock,
					     'date': date})
	
	time.sleep(10)

        #return render(request, 'homepage.html', {'radio': radio,
	#				     'music': music,
#					     'artist': artist,
#                                             'player': player,
#                                             'listalarmclock': listalarmclock,
#                                             'clock': clock,
#					     'date': date})


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



def artist(request):
    if request.method == 'POST':
	form = ArtistForm(request.POST)
	if form.is_valid():
#	    form.name.save()
	    form.save()
	    return redirect('webgui.views.artist')
    else:
	form = ArtistForm()

    listartist = Artist.objects.all()
#    music = Music.objects.all()
    return render(request, 'artist.html', {'form': form, 
					   'listartist': listartist})
#					   'music': music})


def addmusic(request, id):
    artist = Artist.objects.get(id=id)
    return render(request, 'addmusic.html', {'artist': artist})


def response_mimetype(request):
    if "application/json" in request.META['HTTP_ACCEPT']:
        return "application/json"
    else:
        return "text/plain"


def multiple_uploader(request, id):
    if request.POST:
        if request.FILES == None:
            raise Http404("No objects uploaded")
        f = request.FILES['file']
	

	a = Artist.objects.get(id=id)
        b = Music()

	b.artist = a
	b.selected = False
	b.name = f.name	

	b.path.save(f.name, f)	
#        b.save()


	result = [{'name': f.name,
#                  'size': f.size,
#                  'url': a.path.url,
                 },]

	response_data = simplejson.dumps(result)
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, mimetype=mimetype)
    else:
        return HttpResponse('Only POST accepted')




def deleteWebRadio(request, id):
    radio = Webradio.objects.get(id=id)
    radio.delete()
    return redirect('webgui.views.webradio')



def delmusic(request, id_m):
    music = Music.objects.get(id=id_m) 
    artist_id = music.artist.id

    music.deletefile()
    music.delete()
    return redirect(reverse('webgui.views.music', args=[artist_id]))



def delartist(request, id):
    artist = Artist.objects.get(id=id)
    musics = Music.objects.filter(artist_id=id)
    for music in musics:
        music.deletefile()

    artist.delete()
    return redirect('webgui.views.artist')



#def timing(request):
#    scriptPath = os.path.dirname(os.path.abspath(__file__))+"/utils/time.sh"
#    currentTime = subprocess.check_output([scriptPath, "--get"])
#    return render(request,'time.html', {'currentTime':currentTime})


def options(request):
    soundPath = os.path.dirname(os.path.abspath(__file__))+"/utils/picsound.sh"
    currentVolume = subprocess.check_output([soundPath, "--getLevel"])
    currentMute = subprocess.check_output([soundPath, "--getSwitch"])

    timePath = os.path.dirname(os.path.abspath(__file__))+"/utils/time.sh"
    currentTime = subprocess.check_output([timePath, "--get"])
    return render(request,'options.html', {'currentVolume':currentVolume,'currentMute':currentMute,'currentTime':currentTime,'rangeHour':range(24),'rangeMinute':range(60) })



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
    time.sleep(2)
    return redirect('webgui.views.homepage')
    

def alarmclock(request):
    listAlarm = Alarmclock.objects.all()
    return render(request, 'alarmclock.html',{'listAlarm': listAlarm})


def allmusic(request):
    listallmusic = Music.objects.all()
    return render(request, 'allmusic.html',{'listallmusic': listallmusic})


def music(request, id):
    artist = Artist.objects.get(id=id)
    listmusic = Music.objects.filter(artist=id)
    return render(request, 'music.html', {'listmusic': listmusic,
					  'artist': artist})


def playmusic(request, id):
    try:
        selectedmusic = Music.objects.get(selected=1)
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

    music = Music.objects.get(id=id)
    artist_id = music.artist.id
    artist = Artist.objects.get(id=artist_id)

    artist.selected = True
    artist.save()

    music.selected = True
    music.save()
    player = Player()

    #t = threading.Thread(target=player.playmusic, args=music)    
    #t.setDaemon(True)
    #t.start()
    player.playmusic(music)

    time.sleep(1)

    if not player.isStarted():  # then start the backup mp3
        player = Player()
        music = Music
        music.path = 'mplayer /srv/fichiers/backup.mp3'
        player.playmusic(music)

    return redirect('webgui.views.homepage')



def playmusicrandom(request):
    player = Player()

    for i in ("one" "two" "three"):
        #player.playmusicrandom()
	i = mp.Process(target = player.playmusicrandom)
	i.start()
#	i.wait()
        #i = threading.Thread(target=player.playmusicrandom)
        #i.setDaemon(True)
        #i.start()

        time.sleep(1)
        return redirect('webgui.views.homepage')
        time.sleep(20)



def activeAlarmClock(request, id):
    alarmclock = Alarmclock.objects.get(id=id)
    if not alarmclock.active:
        alarmclock.active = True
        alarmclock.enable()
    else:
        alarmclock.active = False
        alarmclock.disable()
        
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
        mode = request.POST['mode']

        # check if label not empty and days selected
        if label == "" or dayofweek == "":
            json_data = json.dumps({"HTTPRESPONSE": "error"})
            return HttpResponse(json_data, mimetype="application/json")
        
        # save object in database
        alarmclock = Alarmclock()
        alarmclock.label = label
        alarmclock.hour = hour
        alarmclock.minute = minute
        alarmclock.period = dayofweek
        alarmclock.snooze = snooze
	alarmclock.mode = mode
        if alarmclock.mode != "music":

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



@csrf_exempt 
def timeset(request):
    if request.method == 'POST':
        hour = request.POST['hour']
        minute = request.POST['minute']

	hour = str(hour)
	minute = str(minute)

    	scriptPath = os.path.dirname(os.path.abspath(__file__))+"/utils/time.sh"
    	subprocess.call(["sudo", scriptPath, "--set", hour, minute])

	url = request.build_absolute_uri('http://reveil/options')

        json_data = json.dumps({"HTTPRESPONSE":url})
        return HttpResponse(json_data, mimetype="application/json")

    else:
	return render(request, 'options.html')
 

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
