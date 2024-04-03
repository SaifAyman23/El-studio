from django import forms
from .models import Video


class DownloadedForm(forms.ModelForm):
    class Meta:
        model=Video
        fields = ['url','res']