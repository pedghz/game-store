from django import forms
from playing_area.models import Game


class shoppingCartForm(forms.Form):
    action = forms.ChoiceField(choices=[('remove', 'Remove')], required=True)
    game_name = forms.ModelChoiceField(required=True, queryset=None)


    def __init__(self, *args, **kwargs):
        super(shoppingCartForm, self).__init__(*args, **kwargs)
        # Dynamically populate the category set
        self.fields['game_name'].queryset = Game.objects.all()