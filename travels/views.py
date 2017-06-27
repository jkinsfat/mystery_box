# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.core.exceptions import ValidationError
from .models import Trip, User_Trip
from login.models import User
# Create your views here.

def home(request):
    alltrips = User_Trip.objects.filter(creator=True).exclude(user__id=request.session['user_id'])
    strippedtrips = []
    for trip in alltrips:
        try:
            User_Trip.objects.get(user__id=request.session['user_id'],trip=trip.trip)
        except:
            strippedtrip = {}
            strippedtrip['username'] = trip.user.name
            strippedtrip['destination'] = trip.trip.destination
            strippedtrip['date_from'] = trip.trip.date_from
            strippedtrip['date_to'] = trip.trip.date_to
            strippedtrip['trip_id'] = trip.trip.id
            strippedtrips.append(strippedtrip)
    context = {
        'first_name' : request.session['user_name'],
        'mytrips' : Trip.objects.filter(users__id = request.session['user_id']),
        'alltrips' : strippedtrips
    }
    return render(request, 'travels/home.html', context)

def add_page(request):
    try:
        context = request.session['errors']
        request.session.pop('errors')
    except:
        context = {}
    return render(request, 'travels/add.html', context)

def new_trip(request):
    errors = {}
    print request.POST['date_from'] + '**********'
    new_trip = Trip(
        destination=request.POST['destination'],
        description=request.POST['description'],
        date_from=request.POST['date_from'],
        date_to=request.POST['date_to']
    )
    if new_trip.date_from > new_trip.date_to:
        errors['date_to'] = 'End date must be after start date'
    try:
        new_trip.full_clean()
    except ValidationError as e:
        for error in e:
            if error[1][0] == "'' value has an invalid date format. It must be in YYYY-MM-DD format.":
                errors[error[0]] = "Travel Date cannot be blank"
            else:
                errors[error[0]] = error[1][0]
    if errors == {}:
        new_trip.save()
        curr_user = User.objects.get(id=request.session['user_id'])
        new_user_trip = User_Trip(
            user=curr_user,
            trip=new_trip,
            creator=True
        )
        new_user_trip.save()
        return redirect('trav:home')
    errors['result'] = "Please correct errors before resubmitting"
    request.session['errors'] = errors
    return redirect('trav:add_page')

def join(request, tripid):
    new_user_trip = User_Trip(
        user = User.objects.get(id=request.session['user_id']),
        trip = Trip.objects.get(id=tripid),
        creator = False
    )
    new_user_trip.save()
    return redirect('trav:home')

def destination(request, tripid):
    this_trip = Trip.objects.get(id=tripid)
    user = User.objects.get(user_trip__trip=this_trip, user_trip__creator=True)
    others = User_Trip.objects.filter(trip=this_trip).exclude(user=user)
    print others
    context = {
        "trip": this_trip,
        "user": user,
        "others": others
    }
    return render(request, 'travels/destination.html', context)
