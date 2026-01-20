"""Forms for the trips app."""

from django import forms

from trips.models import Car, Trip


class CarForm(forms.ModelForm):
    """Form for creating and editing cars."""

    class Meta:
        model = Car
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "maxlength": "20"}),
        }


class TripForm(forms.ModelForm):
    """Form for creating and editing trips."""

    class Meta:
        model = Trip
        fields = ["date", "destination", "reason", "distance", "car"]
        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "destination": forms.TextInput(attrs={"class": "form-control"}),
            "reason": forms.TextInput(attrs={"class": "form-control"}),
            "distance": forms.NumberInput(attrs={"class": "form-control", "step": "0.1"}),
            "car": forms.Select(attrs={"class": "form-select"}),
        }
