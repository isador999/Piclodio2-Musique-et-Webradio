from __future__ import unicode_literals
from django import forms
from webgui.models import Webradio



class WebradioForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    url = forms.CharField(max_length=200)
    
    class Meta:
        model = Webradio
        fields = ['name', 'url', ]