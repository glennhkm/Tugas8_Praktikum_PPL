from django.db import models

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    brand = models.CharField(max_length=100)
    category = models.CharField(max_length=100, choices=[
        ('laptop', 'Laptop'),
        ('smartphone', 'Smartphone'),
        ('tablet', 'Tablet'),
        ('audio', 'Audio Devices'),
        ('camera', 'Cameras'),
        ('accessory', 'Accessories'),
        ('other', 'Other'),
    ])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
