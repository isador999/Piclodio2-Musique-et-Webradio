#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'webgui.views.homepage'),
    url(r'^webradio/$', 'webgui.views.webradio'),
    url(r'^addwebradio/$', 'webgui.views.addwebradio'),
    url(r'^delete_web_radio/(\d+)/$', 'webgui.views.delete_web_radio'),
    url(r'^play/(\d+)/$', 'webgui.views.play'),
    url(r'^stop/$', 'webgui.views.stop'),
    url(r'^alarmclock/$', 'webgui.views.alarmclock'),
    url(r'^activeAlarmClock/(\d+)/$', 'webgui.views.activeAlarmClock'),
    url(r'^deleteAlarmClock/(\d+)/$', 'webgui.views.deleteAlarmClock'),
    url(r'^options/$', 'webgui.views.options'),
    url(r'^debug/$', 'webgui.views.debug'),
    url(r'^volume/set/(\d+)/$', 'webgui.views.volumeset'),
    url(r'^volume/up/(\d+)/$', 'webgui.views.volumeup'),
    url(r'^volume/down/(\d+)/$', 'webgui.views.volumedown'),
    url(r'^volume/tmute/$', 'webgui.views.volumetmute'),
    url(r'^update_webradio/(\d+)/$', 'webgui.views.update_webradio'),
    url(r'^create_alarmclock', 'webgui.views.create_alarmclock'),
    url(r'^update_alarmclock/(\d+)/$', 'webgui.views.update_alarmclock'),

    ### URL TO ARTIST FUNCTIONS ###
    url(r'^artist/$', 'webgui.views.artist'),
    url(r'^delartist/(\d+)/$', 'webgui.views.delartist'),

    ### URL TO MUSIC FUNCTIONS ###
    url(r'^music/(\d+)/$', 'webgui.views.music'),
    url(r'^delmusic/(\d+)/$', 'webgui.views.delmusic', name='delmusic'),
    url(r'^addmusic/(\d+)/$', 'webgui.views.addmusic'),
    url(r'^addmusic/add/(\d+)/$', 'webgui.views.multiple_uploader'),

    url(r'^playmusicrandom/$','webgui.views.playmusicrandom'),
    url(r'^playmusic/(\d+)/$','webgui.views.playmusic'),

    ### URL TO SET TIME (Options) ###
    url(r'^timeset$', 'webgui.views.timeset')

)
