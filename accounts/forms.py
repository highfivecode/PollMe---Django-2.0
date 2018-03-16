from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, min_length=5)
    email = forms.EmailField()
    password1 = forms.CharField(label="Password", max_length=100, min_length=5)
    password2 = forms.CharField(label="Confirm Password", max_length=100, min_length=5)

    def clean_email(self):
        email = self.cleaned_data['email']
        qs = User.objects.filter(email=email)
        if qs.exists():
            raise ValidationError('Email is already registered.')
        return email
