
from django.db import models
from django.utils import timezone


class Xuser(models.Model):
	username = models.CharField(max_length=200)
	email = models.CharField(max_length=200)
	password = models.CharField(max_length=300)

    def publish(self):
        self.save()

    def __str__(self):
        return str(self.username) +"-"+ str(self.email)