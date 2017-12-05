from django.db import models
from model_utils.models import TimeStampedModel

class Car(TimeStampedModel):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return "{0}".format(self.name,)

    class Meta:
        ordering = ['name',]

class Trip(TimeStampedModel):
    date = models.DateField()
    destination = models.CharField(max_length=20)
    reason = models.CharField(max_length=20)
    distance = models.DecimalField(max_digits=5, decimal_places=1)
    car = models.ForeignKey(Car)

    def __str__(self):
        return "{0} to {1} for {2} ({3} km)".format(self.date, self.destination, self.reason, self.distance)

    class Meta:
        ordering = ['-date',]

class Odometer(TimeStampedModel):
    date = models.DateField()
    car = models.ForeignKey(Car)
    km = models.IntegerField()

    def __str__(self):
        return "{0} {1} km ({2})".format(self.date, self.km, self.car)

    class Meta:
        ordering = ['-date',]
