from django import forms

class SearchGame(forms.Form):
    keyword = forms.CharField(label="Search Game", max_length=30, widget=forms.TextInput(
        attrs={'name': "search",
               'id': "search_game",
               'class': "form-control",
               'placeholder': "Search game",
               'style': "display: inline; width: inherit; margin-left: 10px;",}))

    def clean(self):
        cleaned_data = super(SearchGame, self).clean()
        return cleaned_data


class GameScoreForm(forms.Form):
    score = forms.FloatField()

    def clean(self):
        cleaned_data = super(GameScoreForm, self).clean()
        return cleaned_data


class GameStateForm(forms.Form):
    score = forms.FloatField(initial=0)
    gameState = forms.CharField(max_length=1500)

    def clean(self):
        cleaned_data = super(GameStateForm, self).clean()
        return cleaned_data
