from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password

# Create your models here.
class stud(models.Model):
    s_name = models.CharField(max_length=30)
    s_class = models.CharField(max_length=30)
    s_add = models.CharField(max_length=30)
    s_email = models.EmailField(max_length=30)
    
    def __str__(self):
        return self.name
    

class StaffCredentials(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    password = models.CharField(max_length=128)  # Field to store hashed password

    def save(self, *args, **kwargs):
        if not self.pk:  # If it's a new instance
            self.password = make_password(self.password)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.username
    