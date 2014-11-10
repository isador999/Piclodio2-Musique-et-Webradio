#-*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.views.generic import TemplateView
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'piclodio.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),


    url(r'^$','webgui.views.homepage'),
    url(r'^webradio/$','webgui.views.webradio'),
    url(r'^addwebradio/$','webgui.views.addwebradio'),
    url(r'^deleteWebRadio/(\d+)/$','webgui.views.deleteWebRadio'),
    url(r'^play/(\d+)/$','webgui.views.play'),
    url(r'^stop/$','webgui.views.stop'),
#    url(r'^stopmusic/$','webgui.views.stopmusic'),

#    url(r'^artist/$', TemplateView.as_view(template_name="artist.html"), name='artists'),
    url(r'^artist/$', 'webgui.views.artist'),
    url(r'^delartist/(\d+)/$', 'webgui.views.delartist'),

################## REGEXP FOR ANY NAME AS ARGUMENT OF URL 'webgui.views.music' ###################
#    url(r'^music/(?P<artist_name>[a-zA-Z0-9 \'&-])/$', 'webgui.views.music'),



    url(r'^music/(\d+)/$', 'webgui.views.music'),
    url(r'^delmusic/(\d+)/$', 'webgui.views.delmusic', name='delmusic'),


    url(r'^addmusic/(\d+)/$', 'webgui.views.addmusic'),
    url(r'^addmusic/add/(\d+)/$', 'webgui.views.multiple_uploader'),

    url(r'^playmusicrandom/$','webgui.views.playmusicrandom'),
    url(r'^playmusic/(\d+)/$','webgui.views.playmusic'),

    url(r'^alarmclock/$','webgui.views.alarmclock'),
    url(r'^activeAlarmClock/(\d+)/$','webgui.views.activeAlarmClock'),
    url(r'^addalarmclock$','webgui.views.addalarmclock'),
    url(r'^deleteAlarmClock/(\d+)/$','webgui.views.deleteAlarmClock'),
    url(r'^options/$','webgui.views.options'),
    url(r'^debug/$','webgui.views.debug'),

    url(r'^options/timeset$', 'webgui.views.timeset'),
    
    url(r'^volume/set/(\d+)/$','webgui.views.volumeset'),
    url(r'^volume/up/(\d+)/$','webgui.views.volumeup'),
    url(r'^volume/down/(\d+)/$','webgui.views.volumedown'),
    url(r'^volume/tmute/$','webgui.views.volumetmute'),
)
