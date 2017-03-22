from django.contrib import admin

from trips.models import *

class TripAdmin(admin.ModelAdmin):
    list_filter = ('date',)

class TripInline(admin.TabularInline):
    model = Trip
    extra = 10

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries"""
        # get the existing query set, then empty it.
        qs = super(TripInline, self).get_queryset(request)
        return qs.none() 

class CarAdmin(admin.ModelAdmin):
    inlines = [
        TripInline,
        ]

admin.site.register(Car, CarAdmin)
admin.site.register(Trip, TripAdmin)
admin.site.register(Odometer)
