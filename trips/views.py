from datetime import date
from decimal import Decimal

from django.contrib import messages
from django.contrib.auth.models import User
from django.db.models import Sum
from django.urls import reverse_lazy
from django.views.generic import (
    CreateView,
    DeleteView,
    ListView,
    TemplateView,
    UpdateView,
)

from django_filters import rest_framework as filters
from rest_framework import viewsets

from trips.forms import TripForm
from trips.models import Car, Odometer, Trip
from trips.serializers import (
    CarSerializer,
    OdometerSerializer,
    TripSerializer,
    UserSerializer,
)


# =============================================================================
# REST API ViewSets
# =============================================================================


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer


class TripFilter(filters.FilterSet):
    date = filters.DateFromToRangeFilter(field_name="date")

    class Meta:
        model = Trip
        fields = ["car", "date"]


class TripViewSet(viewsets.ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filterset_class = TripFilter


class OdometerViewSet(viewsets.ModelViewSet):
    queryset = Odometer.objects.all()
    serializer_class = OdometerSerializer


# =============================================================================
# Template Views
# =============================================================================


class DashboardView(TemplateView):
    """Main dashboard with stats and quick actions."""

    template_name = "trips/dashboard.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_year = date.today().year

        # Get trips for current year
        year_trips = Trip.objects.filter(date__year=current_year)
        medical_trips = year_trips.filter(reason__icontains="medical")

        context["current_year"] = current_year
        context["trips_this_year"] = year_trips.count()
        context["total_distance_year"] = year_trips.aggregate(total=Sum("distance"))["total"] or Decimal("0")
        context["medical_trips_year"] = medical_trips.count()
        context["medical_distance_year"] = medical_trips.aggregate(total=Sum("distance"))["total"] or Decimal("0")
        context["recent_trips"] = Trip.objects.all()[:10]

        return context


class TripListView(ListView):
    """List all trips with filtering."""

    model = Trip
    template_name = "trips/trip_list.html"
    context_object_name = "trips"

    def get_queryset(self):
        queryset = Trip.objects.select_related("car").all()

        # Apply filters
        year = self.request.GET.get("year")
        car = self.request.GET.get("car")
        reason = self.request.GET.get("reason")

        if year:
            queryset = queryset.filter(date__year=year)
        if car:
            queryset = queryset.filter(car_id=car)
        if reason:
            queryset = queryset.filter(reason__icontains=reason)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get filter options
        context["years"] = Trip.objects.dates("date", "year").values_list("date__year", flat=True).distinct()
        context["cars"] = Car.objects.all()
        context["reasons"] = Trip.objects.values_list("reason", flat=True).distinct().order_by("reason")

        # Selected filters
        context["selected_year"] = self.request.GET.get("year", "")
        context["selected_car"] = self.request.GET.get("car", "")
        context["selected_reason"] = self.request.GET.get("reason", "")

        # Calculate total distance for filtered results
        context["total_distance"] = self.get_queryset().aggregate(total=Sum("distance"))["total"] or Decimal("0")

        return context


class TripCreateView(CreateView):
    """Create a new trip."""

    model = Trip
    form_class = TripForm
    template_name = "trips/trip_form.html"
    success_url = reverse_lazy("trips:trip_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars"] = Car.objects.all()
        context["today"] = date.today().isoformat()

        # Pre-fill from query params (for quick add)
        context["prefill_destination"] = self.request.GET.get("destination", "")
        context["prefill_reason"] = self.request.GET.get("reason", "")

        # Common destinations and reasons for autocomplete
        context["common_destinations"] = (
            Trip.objects.values_list("destination", flat=True).distinct().order_by("destination")[:20]
        )
        context["common_reasons"] = Trip.objects.values_list("reason", flat=True).distinct().order_by("reason")[:20]

        # Default car (most recently used)
        last_trip = Trip.objects.order_by("-date", "-created").first()
        context["default_car"] = last_trip.car if last_trip else None

        return context

    def form_valid(self, form):
        messages.success(self.request, "Trip added successfully!")
        return super().form_valid(form)


class TripQuickAddView(TripCreateView):
    """Quick add trip with pre-filled values."""

    def get_initial(self):
        initial = super().get_initial()
        initial["date"] = date.today()
        initial["destination"] = self.request.GET.get("destination", "")
        initial["reason"] = self.request.GET.get("reason", "")
        return initial


class TripUpdateView(UpdateView):
    """Edit an existing trip."""

    model = Trip
    form_class = TripForm
    template_name = "trips/trip_form.html"
    success_url = reverse_lazy("trips:trip_list")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["cars"] = Car.objects.all()
        context["today"] = date.today().isoformat()
        context["prefill_destination"] = ""
        context["prefill_reason"] = ""
        context["common_destinations"] = (
            Trip.objects.values_list("destination", flat=True).distinct().order_by("destination")[:20]
        )
        context["common_reasons"] = Trip.objects.values_list("reason", flat=True).distinct().order_by("reason")[:20]
        return context

    def form_valid(self, form):
        messages.success(self.request, "Trip updated successfully!")
        return super().form_valid(form)


class TripDeleteView(DeleteView):
    """Delete a trip."""

    model = Trip
    template_name = "trips/trip_confirm_delete.html"
    success_url = reverse_lazy("trips:trip_list")
    context_object_name = "trip"

    def form_valid(self, form):
        messages.success(self.request, "Trip deleted successfully!")
        return super().form_valid(form)


class CRAReportView(TemplateView):
    """CRA-compliant mileage report for tax purposes."""

    template_name = "trips/cra_report.html"

    # CRA mileage rates by year (cents per km)
    CRA_RATES = {
        2024: Decimal("0.70"),
        2025: Decimal("0.72"),
        2026: Decimal("0.72"),  # Placeholder
    }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Get available years
        years = list(Trip.objects.dates("date", "year").values_list("date__year", flat=True).distinct())
        if not years:
            years = [date.today().year]

        context["years"] = sorted(years, reverse=True)

        # Selected year
        selected_year = self.request.GET.get("year")
        if selected_year:
            selected_year = int(selected_year)
        else:
            selected_year = years[0] if years else date.today().year
        context["selected_year"] = selected_year

        # Get all trips for the year (for total km calculation)
        all_trips = Trip.objects.filter(date__year=selected_year).select_related("car")

        # Get medical/business trips
        medical_trips = all_trips.filter(reason__icontains="medical").order_by("date")
        context["medical_trips"] = medical_trips

        # Summary statistics
        total_all_trips = all_trips.aggregate(
            trip_count=Sum("pk"),  # Will be replaced with Count
            total_distance=Sum("distance"),
        )
        context["all_trips_summary"] = {
            "trip_count": all_trips.count(),
            "total_distance": total_all_trips["total_distance"] or Decimal("0"),
        }

        medical_summary = medical_trips.aggregate(total_distance=Sum("distance"))
        context["medical_summary"] = {
            "trip_count": medical_trips.count(),
            "total_distance": medical_summary["total_distance"] or Decimal("0"),
        }

        # Monthly breakdown
        monthly_data = []
        month_names = [
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ]
        for month in range(1, 13):
            month_trips = medical_trips.filter(date__month=month)
            if month_trips.exists():
                month_total = month_trips.aggregate(total=Sum("distance"))["total"] or Decimal("0")
                monthly_data.append(
                    {
                        "month": month,
                        "month_name": month_names[month - 1],
                        "trip_count": month_trips.count(),
                        "total_distance": month_total,
                    }
                )
        context["monthly_data"] = monthly_data

        # CRA rate and estimated deduction
        cra_rate = self.CRA_RATES.get(selected_year, Decimal("0.70"))
        context["cra_rate"] = cra_rate
        medical_distance = context["medical_summary"]["total_distance"]
        context["estimated_deduction"] = medical_distance * cra_rate

        # Odometer readings for fiscal year (CRA requirement)
        cars = Car.objects.all()
        car_odometer_data = []
        for car in cars:
            # Get odometer reading closest to start of year
            start_reading = (
                Odometer.objects.filter(car=car, date__year__lte=selected_year)
                .filter(date__lte=date(selected_year, 1, 31))
                .order_by("-date")
                .first()
            )
            # Get odometer reading closest to end of year
            end_reading = (
                Odometer.objects.filter(car=car, date__year__gte=selected_year)
                .filter(date__gte=date(selected_year, 12, 1))
                .order_by("date")
                .first()
            )

            # Calculate total km driven for the year
            total_km_driven = None
            if start_reading and end_reading:
                total_km_driven = end_reading.km - start_reading.km

            # Get car's trips for the year
            car_trips = all_trips.filter(car=car)
            car_medical_trips = medical_trips.filter(car=car)
            car_logged_km = car_trips.aggregate(total=Sum("distance"))["total"] or Decimal("0")
            car_medical_km = car_medical_trips.aggregate(total=Sum("distance"))["total"] or Decimal("0")

            # Calculate business use percentage
            business_percentage = None
            if total_km_driven and total_km_driven > 0:
                business_percentage = (float(car_medical_km) / total_km_driven) * 100

            car_odometer_data.append(
                {
                    "car": car,
                    "start_reading": start_reading,
                    "end_reading": end_reading,
                    "total_km_driven": total_km_driven,
                    "logged_km": car_logged_km,
                    "medical_km": car_medical_km,
                    "business_percentage": business_percentage,
                }
            )
        context["car_odometer_data"] = car_odometer_data

        return context
