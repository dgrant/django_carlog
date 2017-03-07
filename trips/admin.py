from django.contrib import admin

from trips.models import *

class TripAdmin(admin.ModelAdmin):
    list_filter = ('date',)

admin.site.register(Car)
admin.site.register(Trip, TripAdmin)
admin.site.register(Odometer)
