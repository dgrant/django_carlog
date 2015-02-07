from django.db import models
from model_utils.models import TimeStampedModel

class Car(TimeStampedModel):
    name = models.CharField(max_length=20)
    license_plate = models.CharField(max_length=10)

    def __unicode__(self):
        return "{0} ({1})".format(self.name, self.license_plate)

class Trip(TimeStampedModel):
    date = models.DateField()
    destination = models.CharField(max_length=20)
    reason = models.CharField(max_length=20)
    distance = models.DecimalField(max_digits=5, decimal_places=1)
    car = models.ForeignKey('Car')

    def __unicode__(self):
        return "{0} to {1} for {2} ({3} km)".format(self.date, self.destination, self.reason, self.distance)

class Odometer(TimeStampedModel):
    date = models.DateField()
    car = models.ForeignKey('Car')
    km = models.IntegerField()

    def __unicode__(self):
        return "{0} {1} km ({2})".format(self.date, self.km, self.car)

