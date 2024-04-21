from django.db import models

# Create your models here
class Members(models.Model):
    fname = models.CharField(max_length=20)
    lname = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    username = models.CharField(max_length=20)
    
    GENDER_CHOICES = [
        ('male', 'Male'),
        ('female', 'Female'),
    ]
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    
    birthdate = models.DateField()
    password1 = models.CharField(max_length=20)  # Assuming you want to store the password as text
    password2 = models.CharField(max_length=20)  # Assuming you want to store the password as text
