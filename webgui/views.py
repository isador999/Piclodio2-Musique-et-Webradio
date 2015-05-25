#-*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from webgui.models import Webradio, Player, Alarmclock, BackupMP3, Music, Artist
from webgui.forms import WebradioForm, AlarmClockForm, BackupMP3Form, ArtistForm, TimeForm
import os, glob
import subprocess
from time import strftime
import time
import urllib
from utils.AudioManager import AudioManager

##### 
from django.views.decorators.csrf import csrf_exempt
from django.core.urlresolvers import reverse
from django.http import HttpResponse
import json
import threading



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
    return render(request, 'homepage.html', {'radio': radio,
                                             'music': music,
                                             'artist': artist,
                                             'player': player,
                                             'listalarmclock': listalarmclock,
                                             'clock': clock,
                                             'date': date})



#################################################################
################### MUSIC AND ARTIST METHODS ####################

def artist(request):
    if request.method == 'POST':
        form = ArtistForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('webgui.views.artist')
    else:
        form = ArtistForm()

    listartist = Artist.objects.all()
    return render(request, 'artist.html', {'form': form,
                                           'listartist': listartist})


def delartist(request, id):
    artist = Artist.objects.get(id=id)
    artist.delete()
    return redirect('webgui.views.artist')



############ USELESS NOW ############
#def allmusic(request):
#    listallmusic = Music.objects.all()
#    return render(request, 'allmusic.html',{'listallmusic': listallmusic})

def music(request, id):
    artist = Artist.objects.get(id=id)
    listmusic = Music.objects.filter(artist=id)
    return render(request, 'music.html', {'listmusic': listmusic,
                                          'artist': artist})

def addmusic(request, id):
    artist = Artist.objects.get(id=id)
    return render(request, 'addmusic.html', {'artist': artist})


def delmusic(request, id_m):
    music = Music.objects.get(id=id_m)
    artist_id = music.artist.id

    music.deletefile()
    music.delete()
    return redirect(reverse('webgui.views.music', args=[artist_id]))



def playmusic(request, id):
    try:
        selectedmusic = Music.objects.get(selected=1)
        selectedmusic.selected = False
        selectedmusic.save()
    except Music.DoesNotExist:
        #selectedmusic = None
	pass

    try:
        selectedartist = Artist.objects.get(selected=1)
        selectedartist.selected = False
        selectedartist.save()
    except Artist.DoesNotExist:
        #selectedartist = None
	pass

    music = Music.objects.get(id=id)
    artist_id = music.artist.id
    artist = Artist.objects.get(id=artist_id)

    artist.selected = True
    artist.save()

    music.selected = True
    music.save()
    player = Player()
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
    #player.playmusicrandom()
    t = threading.Thread(target=player.playmusicrandom)
    t.setDaemon(True)
    t.start()
    time.sleep(1.5)
    return redirect('webgui.views.homepage')


##################################################################
##################################################################

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

        result = [{'name': f.name,
#                  'size': f.size,
#                  'url': a.path.url,
                 },]

        #response_data = simplejson.dumps(result)
	response_data = json.dumps(result)
        if "application/json" in request.META['HTTP_ACCEPT_ENCODING']:
            mimetype = 'application/json'
        else:
            mimetype = 'text/plain'
        return HttpResponse(response_data, content_type=mimetype)
    else:
        return HttpResponse('Only POST accepted')



def webradio(request):
    listradio = Webradio.objects.all()
    return render(request, 'webradio.html', {'listradio': listradio})


def update_webradio(request, id_webradio):
    selected_webradio = get_object_or_404(Webradio, id=id_webradio)
    form = WebradioForm(request.POST or None, instance=selected_webradio)
    if form.is_valid():
        form.save()
        return redirect('webgui.views.webradio')

    return render(request, 'update_webradio.html', {'form': form, 'radio': selected_webradio})


def addwebradio(request):
    if request.method == 'POST':  # If the form has been submitted...
        form = WebradioForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # save web radio
            form.instance.selected = False
            form.save()
            return redirect('webgui.views.webradio')
    else:
        form = WebradioForm()

    return render(request, 'addwebradio.html', {'form': form})


def delete_web_radio(request, id_radio):
    radio = Webradio.objects.get(id=id_radio)
    radio.delete()
    return redirect('webgui.views.webradio')


def options(request):
    # get sound info
    am = AudioManager()
    current_volume = am.get_percent_volume()
    current_mute = am.get_mute_status()

    # get actual mp3 backup file
    actual_backup = _get_mp3_in_backup_folder()

    if request.method == 'POST':
        form = BackupMP3Form(request.POST, request.FILES)
        if form.is_valid():
            # remove backup save in database
            BackupMP3.objects.all().delete()
            # remove file in backup folder
            _delete_mp3_from_backup_folder()
            form.save()
            return redirect('webgui.views.options')
    else:
        form = BackupMP3Form()

    return render(request, 'options.html', {'currentVolume': current_volume,
                                            'currentMute': current_mute,
                                            'form': form,
                                            'backup': actual_backup})



################ MY PERSONNAL FUNCTION 'OPTIONS' ################
#################################################################
#def options(request):
#    soundPath = os.path.dirname(os.path.abspath(__file__))+"/utils/picsound.sh"
#    currentVolume = subprocess.check_output([soundPath, "--getLevel"])
#    currentMute = subprocess.check_output([soundPath, "--getSwitch"])

#    timePath = os.path.dirname(os.path.abspath(__file__))+"/utils/time.sh"
#    currentTime = subprocess.check_output([timePath, "--get"])
#    return render(request,'options.html', {'currentVolume':currentVolume,'currentMute':currentMute,'currentTime':currentTime,'rangeHour':range(24),'rangeMinute':range(60) })
#################"

def debug(request):
    todisplay = 'hello world debug'
    return render(request, 'debug.html', {'todisplay': todisplay})


def play(request, id_radio):
    # get actual selected radio if exist
    try:
        selectedradio = Webradio.objects.get(selected=1)
        # unselect it
        selectedradio.selected = False
        selectedradio.save()
    except Webradio.DoesNotExist:
        pass

    # set the new selected radio
    radio = Webradio.objects.get(id=id_radio)
    radio.selected = True
    radio.save()
    player = Player()
    # check if url is available
    try:
        http_code = urllib.urlopen(radio.url).getcode()
    except IOError:
        http_code = 0
    print http_code
    if http_code == 200:
        player.play(radio)
    else:
        # play backup MP3
        radio.url = 'mplayer backup_mp3/*'
        player.play(radio)

    return redirect('webgui.views.homepage')


def stop(request):
    player = Player()
    player.stop()
    time.sleep(1)
    return redirect('webgui.views.homepage')


def alarmclock(request):
    list_alarm = Alarmclock.objects.all()
    return render(request, 'alarmclock.html', {'listAlarm': list_alarm})


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



def create_alarmclock(request):
    if request.method == 'POST':
        form = AlarmClockForm(request.POST)  # A form bound to the POST data
        if form.is_valid():  # All validation rules pass
            # convert period
            period = form.cleaned_data['period']
            period_crontab = _convert_period_to_crontab(period)
            form.period = _convert_period_to_crontab(period)
            # save in database
            form.save()
            # set the cron
            alarmclock = Alarmclock.objects.latest('id')
            alarmclock.period = period_crontab
            alarmclock.active = True
            alarmclock.enable()
            alarmclock.save()

            return redirect('webgui.views.alarmclock')
    else:
        form = AlarmClockForm()  # An unbound form
    return render(request, 'create_alarmclock.html', {'form': form})



def update_alarmclock(request, id_alarmclock):
    selected_webradio = get_object_or_404(Alarmclock, id=id_alarmclock)
    form = AlarmClockForm(request.POST or None, instance=selected_webradio)
    if form.is_valid():
        # convert period
        period = form.cleaned_data['period']
        period_crontab = _convert_period_to_crontab(period)
        form.period = period_crontab
        # save in database
        form.save()
        # set the cron
        alarmclock = Alarmclock.objects.latest('id')
        alarmclock.period = period_crontab
        # disble to remove from crontab
        alarmclock.disable()
        # then enable to create it again
        alarmclock.enable()
        alarmclock.save()

        return redirect('webgui.views.alarmclock')

    return render(request, 'update_alarmclock.html', {'form': form, 'alarmclock': selected_webradio})


def deleteAlarmClock(request, id_alarmclock):
    target_alarmclock = Alarmclock.objects.get(id=id_alarmclock)
    target_alarmclock.disable()
    target_alarmclock.delete()
    return redirect('webgui.views.alarmclock')



@csrf_exempt
def timeset(request):
    current_time = time.strftime("%H:%M")
    if request.method == 'POST':

        form = TimeForm(request.POST)
        if form.is_valid():
            hour = form.cleaned_data['hour']
            minutes = form.cleaned_data['minute']

            scriptPath = os.path.dirname(os.path.abspath(__file__))+"/utils/time.sh"
            subprocess.call(["sudo", scriptPath, "--set", hour, minutes])

            #url = request.build_absolute_uri('http://reveil/options')
            #url = request.get_host()
            #json_data = json.dumps({ "HTTPRESPONSE":request.get_host() })
            #mimetype = 'text/plain'
            #return HttpResponse(json_data, mimetype="application/json")
            #return HttpResponse(json_data, content_type=mimetype)
            return redirect('webgui.views.timeset')
    else:
	form = TimeForm()
    return render(request, 'timeset.html', { 'form': form, 'current_time': current_time })


def volumeup(request, count):
    am = AudioManager()
    am.volume_up()
    return redirect('webgui.views.options')


def volumedown(request, count):
    am = AudioManager()
    am.volume_down()
    return redirect('webgui.views.options')


def volumeset(request, volume):
    am = AudioManager()
    am.set_volume(int(volume))
    return redirect('webgui.views.options')


def volumetmute(request):
    am = AudioManager()
    am.togglemute()
    return redirect('webgui.views.options')


def _convert_period_to_crontab(period):
    # decode unicode
    period_decoded = [str(x) for x in period]

    # transform period into crontab compatible
    period_crontab = ""
    first_time = True  # first time we add a value
    for p in period_decoded:
        if first_time:  # we do not add ","
            period_crontab += str(p)
            first_time = False
        else:
            period_crontab += ","
            period_crontab += str(p)
    return period_crontab


def _get_mp3_in_backup_folder():
    path = os.path.dirname(os.path.abspath(__file__))+"/../backup_mp3"
    mp3 = os.listdir(path)
    if mp3:
        return mp3[0]

def _delete_mp3_from_backup_folder():
    path = os.path.dirname(os.path.abspath(__file__))+"/../backup_mp3/*"
    filelist = glob.glob(path)
    for f in filelist:
        os.remove(f)
