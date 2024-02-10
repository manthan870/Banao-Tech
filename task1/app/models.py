import os
from django.db import models
from django.contrib.auth.models import AbstractUser

# def user_profile_picture_path(instance, filename):
#     username = instance.username
#     ext = 'jpg'
#     path =os.path.join('profile_pictures', f'{username}.{ext}')
#     print("image username is ", username)
#     print("uploading to ", path)
#     return path

def user_profile_picture_path(instance, filename):
    print("Instance is_patient:", instance.is_patient)
    print("Instance is_doctor:", instance.is_doctor)

    if instance.is_patient:
        upload_to = 'profile_pictures/patient/'
    elif instance.is_doctor:
        upload_to = 'profile_pictures/doctor/'
    else:
        raise ValueError('User must be either patient or doctor.')
    ext = 'jpg'
    path = os.path.join(upload_to, f'{instance.username}.{ext}')
    print("image username is ", instance.username)
    print("uploading to ", path)
    return path

    

class CustomUser(AbstractUser):
    is_patient = models.BooleanField(default=False)
    is_doctor = models.BooleanField(default=False)
    address_line1 = models.CharField(max_length=100, null=True, blank=True)
    city = models.CharField(max_length=100, null =True, blank=True)
    state = models.CharField(max_length=100, null=True, blank=True)
    pincode = models.CharField(max_length=6, null=True, blank=True)
    profile_pictures = models.ImageField(upload_to=user_profile_picture_path, null=True, blank=True)

class Patient(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
  

class Doctor(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
   