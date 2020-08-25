from django import forms


def get_video():
    pass

class IndexForm(forms.Form):
    url = forms.URLField()
 