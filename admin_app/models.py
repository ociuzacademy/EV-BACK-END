from django.db import models
from datetime import datetime, timedelta
# Create your models here.

class ChargingStations(models.Model):
    name = models.CharField(max_length=200,default="")
    image = models.ImageField(upload_to='ev_station/')
    address = models.TextField()
    working_hours = models.CharField(max_length=50,default="")
    connectors = models.JSONField()
    rate_per_slot = models.DecimalField(max_digits=10,decimal_places=2,default="")
    capacity = models.CharField(max_length=100,default="")


class ChargingSlot(models.Model):
    station = models.ForeignKey(ChargingStations, on_delete=models.CASCADE, related_name='slots')
    start_time = models.TimeField()
    end_time = models.TimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.station.name}: {self.start_time} - {self.end_time}"