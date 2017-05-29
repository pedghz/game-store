from django import forms


class LoginForm(forms.Form):
    # This form is used to handle the login process.
    username = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(
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
    # This form is used to handle the registration process.
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
    email_reg = forms.CharField(label="Email", max_length=30, min_length=4, widget=forms.EmailInput(
        attrs={'name': "email_reg",
               'id': "email_reg",
               'tabindex': "1",
               'class': "form-control",
               'placeholder': 'Email'}))
    email_reg_confirm = forms.CharField(label="Email", max_length=30, min_length=4, widget=forms.EmailInput(
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
    DEVELOPER = 'DEV'
    NORMAL_USER = 'USR'
    CHOICES = (
        (NORMAL_USER, 'Normal user (You can only buy & play games.)'),
        (DEVELOPER, 'Developer (You can also upload your own games.)'),
    )
    account_type = forms.ChoiceField(widget=forms.RadioSelect, choices=CHOICES, required=True)

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
        username = str(cleaned_data.get('username_reg')).lower()
        if not username.isalnum() or username.startswith('none'):
            self._errors['username_reg'] = self.error_class(['Username contains non alphanumeric characters.'])
            del self.cleaned_data['username_reg']

        cleaned_data['username_reg'] = username

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


class AccountSettings(forms.Form):
    # This form allows the user to modify some account information.
    username_settings = forms.CharField(label="Username", max_length=30, widget=forms.TextInput(
        attrs={'name': "username_settings",
               'id': "username_settings",
               'tabindex': "1",
               'class': "form-control",
               'readonly': 'True'}))
    first_name_settings = forms.CharField(label="First Name", max_length=30, widget=forms.TextInput(
        attrs={'name': "first_name_settings",
               'id': "first_name_settings",
               'tabindex': "1",
               'class': "form-control",
               'placeholder': 'First Name'}))
    last_name_settings = forms.CharField(label="Last Name", widget=forms.TextInput(
        attrs={'name': "last_name_settings",
               'id': "last_name_settings",
               'tabindex': "1",
               'class': 'form-control',
               'placeholder': 'Last Name'}))
    email_settings = forms.CharField(label="Email", max_length=30, widget=forms.EmailInput(
        attrs={'name': "email_settings",
               'id': "email_settings",
               'tabindex': "1",
               'class': "form-control",
               'placeholder': 'Email'}))


class ResetPassword(forms.Form):
    # This form allows the users to update their password.
    current_password_settings = forms.CharField(label="Password", min_length=6, widget=forms.PasswordInput(
        attrs={'name': "current_password_settings",
               'id': "current_password_settings",
               'tabindex': "2",
               'class': 'form-control',
               'placeholder': 'Current password'}))
    password_settings = forms.CharField(label="Password", min_length=6, widget=forms.PasswordInput(
        attrs={'name': "password_settings",
               'id': "password_settings",
               'tabindex': "2",
               'class': 'form-control',
               'placeholder': 'New Password'}))
    password_settings_confirm = forms.CharField(label="Password", min_length=6, widget=forms.PasswordInput(
        attrs={'name': "password_settings_confirm",
               'id': "password_settings_confirm",
               'tabindex': "2",
               'class': 'form-control',
               'placeholder': 'Confirm New Password'}))

    def clean(self):
        """
        Making sure that the password and confirmation password are the same.
        :return: cleaned_data
        """
        cleaned_data = super(ResetPassword, self).clean()
        password = cleaned_data.get('password_settings')
        password_confirm = cleaned_data.get('password_settings_confirm')

        # If the both fields have been typed and are not similar, we get rid of the second one and signal an error.
        if (password and password_confirm) and password != password_confirm:
            self._errors['password_settings'] = self.error_class(['Passwords do not match.'])
            del self.cleaned_data['password_settings_confirm']

        # We return the cleaned version of the data.
        return cleaned_data


# The form for adding a game
class AddGame(forms.Form):
    # we want to offer a dropdown menu for selecting genre of the game he/she is uploading
    genre_choices = (
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('BoardGames', 'BoardGames'),
        ('Puzzle', 'Puzzle'),
        ('Simulation', 'Simulation'),
        ('Sports', 'Sports'),
        ('Strategy', 'Strategy'),
        ('Other', 'Other'),
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
    # we offer people to put a link to an image which represents their game
    image_url = forms.URLField(label="ImageURL", max_length=150, required=False, widget=forms.URLInput(
        attrs={'name': "image_url",
               'id': "image_url",
               'class': 'form-control',
               'placeholder': "Game's image URL (Best size: 260x140)"}))
    # the genre dropdown
    genre = forms.ChoiceField(label="Genre", choices=genre_choices, initial='Action')

    def clean(self):
        cleaned_data = super(AddGame, self).clean()
        # transforming the game's name to lowercase and exchange white spaces with dashes.
        game_name = str(cleaned_data.get('game_name')).lower().replace(' ', '-')
        cleaned_data['game_name'] = game_name
        return cleaned_data


# The form for editing a game
class EditGame(forms.Form):
    # data the genre dropdown
    genre_choices = (
        ('Action', 'Action'),
        ('Adventure', 'Adventure'),
        ('BoardGames', 'BoardGames'),
        ('Puzzle', 'Puzzle'),
        ('Simulation', 'Simulation'),
        ('Sports', 'Sports'),
        ('Strategy', 'Strategy'),
        ('Other', 'Other'),
    )
    # The game's name is unique in our db and it cannot be changed.
    game_name_edit = forms.CharField(label="Game Name", max_length=30, widget=forms.TextInput(
        attrs={'name': "game_name",
               'id': "game_name",
               'class': "form-control",
               'readonly': 'True',
               'placeholder': "Game's name",}))
    price_edit = forms.FloatField(label="Price", widget=forms.NumberInput(
        attrs={'name': "price",
               'id': "price",
               'class': 'form-control',
               'placeholder': 'Price'}))
    game_url_edit = forms.URLField(label="GameURL", max_length=150, widget=forms.URLInput(
        attrs={'name': "game_url",
               'id': "game_url",
               'class': "form-control",
               'placeholder': "Game's URL"}))
    image_url_edit = forms.URLField(label="ImageURL", max_length=150, required=False, widget=forms.URLInput(
        attrs={'name': "image_url",
               'id': "image_url",
               'class': 'form-control',
               'placeholder': "Game's image URL (Best size: 260x140)"}))
    # genre dropdown
    genre_edit = forms.ChoiceField(label="Genre", choices=genre_choices, initial='Action')

    def clean(self):
        cleaned_data = super(EditGame, self).clean()
        return cleaned_data
