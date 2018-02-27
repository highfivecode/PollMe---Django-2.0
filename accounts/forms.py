from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label="Password", max_length=100)
