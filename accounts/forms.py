from django import forms

class UserRegistrationForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100, min_length=5)
    email = forms.EmailField()
    password1 = forms.CharField(label="Password", max_length=100, min_length=5)
    password2 = forms.CharField(label="Confirm Password", max_length=100, min_length=5)

    def clean_email(self):
        email = self.cleaned_data['email']
        print('cleaning_email field')
        print(email)
        return email
