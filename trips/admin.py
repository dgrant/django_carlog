from django.contrib import admin

from trips.models import Car, Odometer, Trip


@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_filter = (
        "date",
        "car",
    )
    list_display = (
        "date",
        "destination",
        "reason",
        "distance",
        "car",
    )
    list_editable = ("car",)


class TripInline(admin.TabularInline):
    model = Trip
    extra = 10

    def get_queryset(self, request):
        """Alter the queryset to return no existing entries"""
        # get the existing query set, then empty it.
        qs = super().get_queryset(request)
        return qs.none()


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    inlines = [
        TripInline,
    ]


admin.site.register(Odometer)
