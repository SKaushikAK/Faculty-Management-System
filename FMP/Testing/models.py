from django.db import models

# Create your models here.
class Faculty(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=50)
    # Add other fields as needed
class YourModel(models.Model):
    # Define your model fields here
    name = models.CharField(max_length=100)
    # Add other fields as needed