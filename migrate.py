#!/usr/bin/env python3

from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime

import data
import sys

years = (2014, 2015, 2016,)

import django
django.setup()

from trips.models import Car, Trip, Odometer

client = MongoClient()
db = client.cartrips
trips = db['trips']
odometers = db['odometers']

def migrate_cars():
    cars = data.get_cars_for_user('Nasha')
    for mcar in cars:
        car = Car.objects.filter(name=mcar)
        if car:
            print('found car:', car)
        else:
            car = Car()
            car.name = mcar
            car.save()
            print('created car:', car)

def migrate_trips():
    years = data.get_years('Nasha')
    for year in years:
        trips = data.get_trips('Nasha', year)
        for mtrip in trips:
            print('mtrip:', mtrip)
            # get the car
            mcar = mtrip['car']
            car = Car.objects.filter(name=mcar).get()
            print('found car:', car)
            print('instance: ', type(car))

            trip = Trip()
            trip.car = car
            trip.created = mtrip['ctime']
            trip.date = mtrip['date']
            trip.destination = mtrip['destination']
            trip.distance = mtrip['distance']
            trip.reason = mtrip['reason']
            trip.save()

def migrate_odometers():
    years = data.get_years('Nasha')
    for year in years:
        odometers = data.get_odometers('Nasha', year)
        for modometer in odometers:
            print('modometer:', modometer)

            mcar = modometer['car']
            car = Car.objects.filter(name=mcar).get()

            odo = Odometer()
            odo.car = car
            odo.created = modometer['date']
            odo.km = modometer['km']
            odo.date = modometer['date']
            odo.save()

if __name__ == '__main__':
    migrate_cars()
#    migrate_trips()
    migrate_odometers()
