from django import forms


class AddPlayerForm(forms.Form):
    player = forms.CharField(max_length=25)