from __future__ import unicode_literals
from django import forms
from webgui.models import Webradio, Music



class WebradioForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    url = forms.CharField(max_length=200)
    
    class Meta:
        model = Webradio
        fields = ['name', 'url', ]

class MusicForm(forms.ModelForm):
    name = forms.CharField(max_length=60)
    path = forms.CharField(max_length=60)
    fichier = forms.FileField(required=False)
    
    class Meta:
	model = Music
	fields = ['name', 'path', 'fichier', ]

