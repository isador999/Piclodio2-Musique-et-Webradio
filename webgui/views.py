#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from webgui.models import Webradio, Player, Alarmclock
from webgui.forms import WebradioForm
import time
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json

#---------------------------------
#   Show the homepage
#---------------------------------
def homepage(request):
    try:
        radio = Webradio.objects.get(selected=1)
    except Webradio.DoesNotExist:
        radio = None
    player = Player()
    listalarmclock = Alarmclock.objects.all()
    return render(request,'homepage.html',{ 'radio': radio,
                                            'player': player,
                                            'listalarmclock':listalarmclock })

#---------------------------------
#   Show list of web radio in db
#---------------------------------
def webradio(request):
    listRadio = Webradio.objects.all()
    return render(request,'webradio.html', {'listradio':listRadio})

#---------------------------------
#   Form to add new web radio
#---------------------------------
def addwebradio(request):
    if request.method == 'POST': # If the form has been submitted...
        form = WebradioForm(request.POST) # A form bound to the POST data
        if form.is_valid(): # All validation rules pass
            # save web radio
            form.instance.selected=False;
            form.save()
            return redirect('webgui.views.webradio')
    else:
        form = WebradioForm() # An unbound form

    return render(request, 'addwebradio.html', { 'form': form,})

def deleteWebRadio(request,id):
    radio = Webradio.objects.get(id=id)
    radio.delete()
    return redirect('webgui.views.webradio')

def options(request):
    todisplay = 'hello world';
    return render(request,'options.html', {'todisplay':todisplay})

def debug(request):
    todisplay = 'hello world debug';
    return render(request,'debug.html', {'todisplay':todisplay})
 
def play(request,id):
    # get actual selected radio if exist
    try:
        selectedradio = Webradio.objects.get(selected=1)
        # unselect it
        selectedradio.selected=False
        selectedradio.save()
    except Webradio.DoesNotExist:
        selectedradio = None    
    
    # set the new selected radio
    radio = Webradio.objects.get(id=id)
    radio.selected=True
    radio.save()
    player = Player()
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
    return render(request, 'alarmclock.html',{'listAlarm': listAlarm,})


def activeAlarmClock(request,id):
    alarmclock = Alarmclock.objects.get(id=id)
    if (alarmclock.active==False):
        alarmclock.active=True
        alarmclock.enable()
    else:
        alarmclock.active=False
        alarmclock.disable()
        
    alarmclock.save()
    return redirect('webgui.views.alarmclock')

@csrf_exempt 
def addalarmclock(request):
    if request.method == 'POST':
        label       = request.POST['label']
        hour        = request.POST['hour']
        minute      = request.POST['minute']
        snooze      = request.POST['snooze']
        id_webradio    = request.POST['webradio']
        dayofweek   = request.POST['dayofweek']
        
        # check if label not empty and days selected
        if label =="" or dayofweek=="":
            json_data = json.dumps({"HTTPRESPONSE":"error"})
            return HttpResponse(json_data, mimetype="application/json")
        
        # save object in database
        alarmclock = Alarmclock()
        alarmclock.label    = label
        alarmclock.hour     = hour
        alarmclock.minute   = minute
        alarmclock.period   = dayofweek
	alarmclock.snooze   = snooze
        webradio = Webradio.objects.get(id=id_webradio)
        alarmclock.webradio = webradio
        alarmclock.active=True
        alarmclock.save()
        
        # set the cron
        alarmclock= Alarmclock.objects.latest('id')
        alarmclock.enable()
        
        json_data = json.dumps({"HTTPRESPONSE":"ok"})
        return HttpResponse(json_data, mimetype="application/json")
    
    else: # not post, show the form
        listradio = Webradio.objects.all()
        return render(request, 'addalarmclock.html', {'rangeHour': range(24),
                                                      'rangeMinute': range(60),
                                                      'listradio':listradio})
                                                      
def deleteAlarmClock(request,id):
    alarmclock = Alarmclock.objects.get(id=id)
    alarmclock.disable()
    alarmclock.delete()
    return redirect('webgui.views.alarmclock')
