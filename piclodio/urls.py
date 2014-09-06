#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'piclodio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$','webgui.views.homepage'),
    url(r'^webradio/$','webgui.views.webradio'),
    url(r'^addwebradio/$','webgui.views.addwebradio'),
    url(r'^deleteWebRadio/(\d+)/$','webgui.views.deleteWebRadio'),
    url(r'^play/(\d+)/$','webgui.views.play'),
    url(r'^stop/$','webgui.views.stop'),
    url(r'^alarmclock/$','webgui.views.alarmclock'),
    url(r'^activeAlarmClock/(\d+)/$','webgui.views.activeAlarmClock'),

    ### URL for Clock Type (Music / Webradio) ### Added by Isador
    url(r'^typeAlarmClock/$','webgui.views.typeAlarmClock'),

    url(r'^addalarmclock$','webgui.views.addalarmclock'),
    url(r'^deleteAlarmClock/(\d+)/$','webgui.views.deleteAlarmClock'),
    url(r'^options/$','webgui.views.options'),
    url(r'^debug/$','webgui.views.debug'),
    url(r'^volume/set/(\d+)/$','webgui.views.volumeset'),
    url(r'^volume/up/(\d+)/$','webgui.views.volumeup'),
    url(r'^volume/down/(\d+)/$','webgui.views.volumedown'),
    url(r'^volume/tmute/$','webgui.views.volumetmute'),
)
