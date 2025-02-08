from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from pyuploadcare.dj.models import ImageField as UploadcareImageField

class CarModel(models.Model):
    car_name = models.CharField(max_length=200)
    title = models.CharField(default="", max_length=500, blank=True)
    description = models.CharField(default="", max_length=10000, blank=True)
    tags = models.CharField(default="", max_length=5000, blank=True)
    car_type = models.CharField(default="", max_length=200, blank=True)
    company = models.CharField(default="", max_length=200, blank=True)
    dealer = models.CharField(default="", max_length=200, blank=True)
    logo_url = models.CharField(max_length=1000, null=True, blank=True)  
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    public=models.BooleanField(default=True)
    def __str__(self):
        return self.car_name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class CarImage(models.Model):
    car = models.ForeignKey(CarModel, related_name='images', on_delete=models.CASCADE)
    image_url = models.CharField(max_length=1000, null=True, blank=True) 
    user = models.ForeignKey(User, on_delete=models.CASCADE)  

    def save(self, *args, **kwargs):
      
        if self.car.images.count() >= 10:
            raise ValidationError("A car can have a maximum of 10 images.")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.car.car_name}"