# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.db import models
import re

def validate_word(value):
    if len(value) < 3:
        raise ValidationError('Field must be longer than two character')
    pattern = re.compile("[A-Za-z\s]+$")
    match = pattern.match(value)
    if not match:
        raise ValidationError('Field must contain only letters')

def validate_password(value):
    if len(value) < 6:
        raise ValidationError('Password must be at least 6 characters')

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=25, validators=[validate_word])
    username = models.CharField(max_length=25, unique=True, validators=[validate_word])
    password = models.CharField(max_length=125, validators=[validate_password])
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    updated_at = models.DateTimeField(auto_now_add=True, blank=True)
