from django import forms
from .models import Game
from authentication.models import User

class GameSelectionForm(forms.Form):
    game = forms.ModelChoiceField(queryset=Game.objects.all(), empty_label="Select a game",required=True)
    Opponent = forms.ModelChoiceField(queryset=User.objects.all(), empty_label="Select a user",required=False)
    have_code = forms.BooleanField(label='Already have a code', required=False)
    game_code = forms.CharField(max_length=5,min_length=5, label='Game Code')
    
    def __init__(self, *args, **kwargs):
        current_user = kwargs.pop('current_user', None)
        super(GameSelectionForm, self).__init__(*args, **kwargs)
        if current_user:
            opponents = User.objects.exclude(pk=current_user.pk)
            self.fields['Opponent'].queryset = opponents