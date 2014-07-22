#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from webgui.models import Webradio, Player, Alarmclock
from webgui.forms import WebradioForm
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
import os
import subprocess
from time import gmtime, strftime


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


def deleteWebRadio(request, id):
    radio = Webradio.objects.get(id=id)
    radio.delete()
    return redirect('webgui.views.webradio')


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
        webradio = Webradio.objects.get(id=id_webradio)
        alarmclock.webradio = webradio
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
