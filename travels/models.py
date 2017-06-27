from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.db import models
from login.models import User
from datetime import date
import re

# def validate_word(value):
#     if len(value) < 3:
#         raise ValidationError('Field must be longer than two character')
#     pattern = re.compile("[A-Za-z]+$")
#     match = pattern.match(value)
#     if not match:
#         raise ValidationError('Field must contain only letters')

def date_after_now(value):
    if date.today() > value:
        raise ValidationError('Start date must be after today')

# Create your models here.
class Trip(models.Model):
    destination = models.CharField(max_length=25)
    description = models.CharField(max_length=255)
    date_from = models.DateField(validators=[date_after_now])
    date_to = models.DateField()
    users = models.ManyToManyField(User, through='User_Trip')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)

class User_Trip(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE)
    creator = models.BooleanField()
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
