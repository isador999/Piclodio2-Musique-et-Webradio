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
    url(r'^addalarmclock$','webgui.views.addalarmclock'),
    url(r'^deleteAlarmClock/(\d+)/$','webgui.views.deleteAlarmClock'),
    url(r'^options/$','webgui.views.options'),
    url(r'^debug/$','webgui.views.options'),
)
