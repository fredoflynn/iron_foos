from django import forms
from foos.models import Tourney


class AddPlayerForm(forms.Form):
    player = forms.CharField(max_length=25)

class TourneyForm(forms.ModelForm):
    # player = forms.CharField(max_length=25)

    class Meta:
        model = Tourney
        fields = ('name',)

