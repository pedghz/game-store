from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", min_length=5, max_length=30, widget=forms.TextInput(
        attrs={'name': "username",
               'id': "username",
               'tabindex': "2",
               'class': "form-control",
               'placeholder': 'Username'}))
    password = forms.CharField(label="Password", min_length=6, widget=forms.PasswordInput(
        attrs={'name': "password",
               'id': "password",
               'tabindex': "2",
               'class': 'form-control',
               'placeholder': 'Password'}))

    def clean(self):
        """
        Transforming the username to lowercase.
        :return: cleaned_data
        """

        cleaned_data = super(LoginForm, self).clean()
        # transforming the username to lowercase.
        username = str(cleaned_data.get('username')).lower()
        cleaned_data['username'] = username

        return cleaned_data


class RegisterForm(forms.Form):
    first_name_reg = forms.CharField(label="First Name", max_length=30, widget=forms.TextInput(
        attrs={'name': "first_name_reg",
               'id': "first_name_reg",
               'tabindex': "1",
               'class': "form-control",
               'placeholder': 'First Name'}))
    last_name_reg = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'name': "last_name_reg",
               'id': "last_name_reg",
               'tabindex': "1",
               'class': 'form-control',
               'placeholder': 'Last Name'}))
    username_reg = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(
        attrs={'name': "username_reg",
               'id': "username_reg",
               'tabindex': "1",
               'class': "form-control",
               'placeholder': 'Username'}))
    email_reg = forms.CharField(label="Email", max_length=30, widget=forms.EmailInput(
        attrs={'name': "email_reg",
               'id': "email_reg",
               'tabindex': "1",
               'class': "form-control",
               'placeholder': 'Email'}))
    email_reg_confirm = forms.CharField(label="Email", max_length=30, widget=forms.EmailInput(
        attrs={'name': "email_reg_confirm",
               'id': "email_reg_confirm",
               'tabindex': "1",
               'class': "form-control",
               'placeholder': 'Confirm Email'}))
    password_reg = forms.CharField(label="Password", min_length=6, widget=forms.PasswordInput(
        attrs={'name': "password_reg",
               'id': "password_reg",
               'tabindex': "2",
               'class': 'form-control',
               'placeholder': 'Password'}))
    password_reg_confirm = forms.CharField(label="Password", min_length=6, widget=forms.PasswordInput(
        attrs={'name': "password_reg_confirm",
               'id': "password_reg_confirm",
               'tabindex': "2",
               'class': 'form-control',
               'placeholder': 'Confirm Password'}))

    def clean(self):
        """
        Making sure that the email and confirmation email are the same.
        Does the same for password and confirmation password,
        :return: cleaned_data
        """
        cleaned_data = super(RegisterForm, self).clean()
        email = cleaned_data.get('email_reg')
        email_confirm = cleaned_data.get('email_reg_confirm')
        password = cleaned_data.get('password_reg')
        password_confirm = cleaned_data.get('password_reg_confirm')
        # transforming the username to lowercase.
        username = str(cleaned_data.get('username')).lower()
        cleaned_data['username'] = username

        # If the both fields have been typed and are not similar, we get rid of the second one and signal an error.
        if (email and email_confirm) and email != email_confirm:
            self._errors['email_reg'] = self.error_class(['Emails do not match.'])
            del self.cleaned_data['email_reg_confirm']

        # If the both fields have been typed and are not similar, we get rid of the second one and signal an error.
        if (password and password_confirm) and password != password_confirm:
            self._errors['password_reg'] = self.error_class(['Passwords do not match.'])
            del self.cleaned_data['password_reg_confirm']

        # We return the cleaned version of the data.
        return cleaned_data


class AddGame(forms.Form):
    genre_choices = (
        ('ac', 'Action'),
        ('ad', 'Adventure'),
        ('bo', 'Board games'),
        ('pu', 'Puzzle'),
        ('rp', 'Role playing'),
        ('sm', 'Simulation'),
        ('st', 'Strategy'),
        ('sp', 'Sports'),
        ('ot', 'Other'),
    )

    game_name = forms.CharField(label="Game Name", max_length=30, widget=forms.TextInput(
        attrs={'name': "game_name",
               'id': "game_name",
               'class': "form-control",
               'placeholder': "Game's Name"}))
    price = forms.FloatField(label="Price", widget=forms.NumberInput(
        attrs={'name': "price",
               'id': "price",
               'class': 'form-control',
               'placeholder': 'Price'}))
    game_url = forms.URLField(label="GameURL", max_length=150, widget=forms.URLInput(
        attrs={'name': "game_url",
               'id': "game_url",
               'class': "form-control",
               'placeholder': 'Game URL'}))
    image_url = forms.URLField(label="ImageURL", max_length=150, widget=forms.URLInput(
        attrs={'name': "image_url",
               'id': "image_url",
               'class': 'form-control',
               'placeholder': "Game's image"}))
    genre = forms.ChoiceField(label="Genre", choices=genre_choices, initial='ac')

    def clean(self):
        cleaned_data = super(AddGame, self).clean()
        # transforming the username to lowercase and exchange white spaces with dashes.
        game_name = str(cleaned_data.get('game_name')).lower().replace(' ','-')
        cleaned_data['game_name'] = game_name
        return cleaned_data
