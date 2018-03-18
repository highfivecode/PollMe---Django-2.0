from django.contrib.auth.models import User
from django.db import models

# Create your models here.
class Poll(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    text = models.CharField(max_length=255)
    pub_date = models.DateField()

    def __str__(self):
        return self.text

class Choice(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return "{} - {}".format(self.poll.text[:25], self.choice_text[:25])


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice, on_delete=models.CASCADE)
