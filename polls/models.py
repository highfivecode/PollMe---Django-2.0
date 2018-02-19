from django.db import models

# Create your models here.
class Poll(models.Model):
    text = models.CharField(max_length=255)
    pub_date = models.DateField()

    def __str__(self):
        return self.text
