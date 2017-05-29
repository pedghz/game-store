from django import forms
from playing_area.models import Game


# validating the form for the shopping cart
class shoppingCartForm(forms.Form):
    action = forms.ChoiceField(choices=[('add', 'Add'), ('remove', 'Remove')], required=True)
    game = forms.ModelChoiceField(required=True, queryset=None)

    def __init__(self, *args, **kwargs):
        super(shoppingCartForm, self).__init__(*args, **kwargs)
        self.fields['game'].queryset = Game.objects.all()