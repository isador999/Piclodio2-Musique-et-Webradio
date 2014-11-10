from __future__ import unicode_literals
from django import forms
from django.forms.formsets import formset_factory
#from django.forms.models import inlineformset_factory
from webgui.models import Webradio, Music, Artist


class WebradioForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    url = forms.CharField(max_length=200)
    
    class Meta:
        model = Webradio
        fields = ['name', 'url', ]






#class MusicForm(forms.ModelForm):
#    name = forms.CharField(max_length=60)  # will take automatically the name of the Music
#    artist = forms.CharField(max_length=60)
#    fichier = forms.FileField(required=False)

#    class Meta:
#        model = Music
#        fields = ['artist']

#class MusicfileForm(forms.ModelForm):
#    fichier = forms.FileField(required=False)

#    class Meta:
#	model = Music
#	fields = ['fichier']



#max_music_files = 10
#MusicFormset = formset_factory(MusicfileForm, extra = max_music_files)




class ArtistForm(forms.ModelForm):
    name = forms.CharField(max_length=60)
    style = forms.CharField(required=False, max_length=20)

    class Meta:
	model = Artist
	fields = ['name', 'style', ]

 


