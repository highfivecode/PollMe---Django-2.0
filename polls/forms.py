from django import forms

from .models import Poll

class PollForm(forms.ModelForm):

    class Meta:
        model = Poll
        fields = '__all__'
