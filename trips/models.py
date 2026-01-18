from django.db import models

from model_utils.models import TimeStampedModel


class Car(TimeStampedModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = [
            "name",
        ]


class Trip(TimeStampedModel):
    date = models.DateField()
    destination = models.CharField(max_length=20)
    reason = models.CharField(max_length=20)
    distance = models.DecimalField(max_digits=5, decimal_places=1)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.date} to {self.destination} for {self.reason} ({self.distance} km)"

    class Meta:
        ordering = [
            "-date",
        ]


class Odometer(TimeStampedModel):
    date = models.DateField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    km = models.IntegerField()

    def __str__(self):
        return f"{self.date} {self.km} km ({self.car})"

    class Meta:
        ordering = [
            "-date",
        ]
