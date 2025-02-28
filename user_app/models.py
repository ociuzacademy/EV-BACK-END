from django.db import models
from service_app.models import *
from admin_app.models import *
# Create your models here.


class User(models.Model):
    name = models.CharField(max_length=100,default="")
    username = models.CharField(max_length=100,default="")
    phone=models.CharField(max_length=10,default="")
    email = models.CharField(max_length=100,default="",unique=True)
    password = models.CharField(max_length=50,default="")
    image = models.ImageField(upload_to='user_photos/', null=True, blank=True)


class Vehicle(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    brand = models.CharField(max_length=100,default="")
    model = models.CharField(max_length=100,default="")
    connector_type = models.CharField(max_length=100,default="")
    vin = models.CharField(max_length=30,default="")
    registration_num = models.CharField(max_length=100,default="")


class PurchaseProduct(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    product = models.ForeignKey(Products,on_delete=models.CASCADE,null=True,blank=True)
    service_centre = models.ForeignKey(Service_Centre,on_delete=models.CASCADE,null=True,blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    date = models.DateField(auto_now_add=True)


class Repair(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    vehicle = models.ForeignKey(Vehicle,on_delete=models.CASCADE,null=True,blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    service_centre = models.ForeignKey(Service_Centre,on_delete=models.CASCADE,null=True,blank=True)
    services = models.JSONField()
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,default="Repair Requested")
    updated_at = models.DateTimeField(auto_now=True)
    repair_cost = models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)


class Feedback(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True)
    service_centre = models.ForeignKey(Service_Centre,on_delete=models.CASCADE,null=True,blank=True)
    repair = models.ForeignKey(Repair,on_delete=models.CASCADE,null=True,blank=True)
    feedback = models.TextField()
    date = models.DateField(auto_now_add=True)


class Booking(models.Model):
    slot = models.OneToOneField(ChargingSlot, on_delete=models.CASCADE, related_name='booking')
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='booking')
    payment_status = models.CharField(
        max_length=20, choices=[("Pending", "Pending"), ("Completed", "Completed")], default="Pending"
    )
    booking_date = models.DateField(auto_now_add=True)
    connector = models.CharField(max_length=100,default='')
    charging_status = models.CharField(max_length=50,default='pending')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    def __str__(self):
        return f"Booking for Slot ID {self.slot.id} by {self.user}"
