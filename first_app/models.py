from django.db import models

class Person(models.Model):
    email = models.CharField(max_length=100)
