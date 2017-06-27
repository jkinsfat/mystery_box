# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from login.models import User
import bcrypt
# Create your views here.
def index(request):
    context = {}
    if 'context' in request.session:
        context = request.session['context']
        request.session.pop('context')
    return render(request, 'login/index.html', context)

def login(request):
    if request.POST['login_username'] == '' or request.POST['login_password'] == '':
        request.session['context'] = {'login_error' : 'Fields cannot be empty'}
    else:
        try:
            user_account = User.objects.filter(username=request.POST['login_username'])[0]
            hashed = bcrypt.hashpw(request.POST['login_password'].encode(), user_account.password.encode())
            if user_account.password == hashed:
                request.session['user_id'] = user_account.id
                request.session['user_name'] = user_account.name
                return redirect('trav:home')
        except:
            request.session['context'] = {'login_error' : 'One of these fields is incorrect'}
    return redirect('auth:index')

def register(request):
    context = {}
    if request.POST['password'] != request.POST['password_confirm']:
        context['password_confirm'] = 'Does not match password'
    hashed = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
    new_user = User(
        name=request.POST['name'],
        username=request.POST['username'],
        password=hashed
    )
    try:
        new_user.full_clean()
    except ValidationError as e:
        for key in e:
            context[key[0]] = key[1][0]
    if context == {}:
        new_user.save()
        context['result'] = 'Registration complete! Try logging in'
    else:
        context['result'] = 'Registration incomplete, correct errors above'
    request.session['context'] = context
    return redirect('auth:index')

def logout(request):
    request.session.clear()
    return redirect('auth:index')
