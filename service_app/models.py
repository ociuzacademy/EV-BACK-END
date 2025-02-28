from django.db import models
# Create your models here.

class Service_Centre(models.Model):
    name = models.CharField(max_length=100,default="")
    username = models.CharField(max_length=100,default="")
    phone=models.CharField(max_length=20,default="")
    email = models.CharField(max_length=100,default="",)
    password = models.CharField(max_length=100,default="")
    address = models.CharField(max_length=100,default="")
    longitude = models.DecimalField(decimal_places=10,max_digits=20,null=True,blank=True)
    latitude = models.DecimalField(decimal_places=10,max_digits=20,null=True,blank=True)
    image = models.ImageField(upload_to='service_center_photos/', null=True, blank=True)
    working_hours = models.CharField(max_length=55,default="")
    utype = models.CharField(max_length=20,default='service_centre')
    status = models.CharField(max_length=20,default='pending')
    

class Products(models.Model):
    service_centre = models.ForeignKey(Service_Centre,on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100,default="")
    description = models.TextField()
    price = models.DecimalField(decimal_places=2,max_digits=10,null=True,blank=True)
    quantity = models.CharField(max_length=50,default="")
    image = models.FileField(upload_to="product_images",null=True,blank=True)


class Employee(models.Model):
    service_centre = models.ForeignKey(Service_Centre,on_delete=models.CASCADE,null=True,blank=True)
    username = models.CharField(max_length=50,default="",unique=True)
    name = models.CharField(max_length=50,default='')
    email = models.CharField(max_length=100,default="")
    phone_number = models.CharField(max_length=15,default="")
    password = models.CharField(max_length=50,default="")
    utype = models.CharField(max_length=15,default='employee')


class Attendance(models.Model):
    service_centre = models.ForeignKey(Service_Centre,on_delete=models.CASCADE,null=True,blank=True)
    employee = models.ForeignKey(Employee,on_delete=models.CASCADE,null=True,blank=True)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=50,default="")

    class Meta:
        unique_together = ('employee', 'date')
    

