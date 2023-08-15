from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="username")
    password = forms.CharField(label="password", widget=forms.PasswordInput)


class RegistrationForm(forms.Form):
    username = forms.CharField(label="username")
    email = forms.CharField(label="email")
    first_name = forms.CharField(label="first_name")
    last_name = forms.CharField(label="last_name",)
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    repeat_password = forms.CharField(label="repeat password", widget=forms.PasswordInput)

