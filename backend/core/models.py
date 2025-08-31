from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Restaurant(models.Model):
    CATEGORY_CHOICES = [
        ('healthy', 'Healthy Food'),
        ('fastfood', 'Fast Food'),
        ('desi', 'Desi Cuisine'),
        ('desserts', 'Desserts'),
    ]
    
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='restaurants/', blank=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='healthy')
    delivery_time = models.PositiveIntegerField(default=30)
    min_order = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=4.5)
    created_at = models.DateTimeField(auto_now_add=True)

class MenuItem(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(upload_to='menu/', blank=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    items = models.JSONField()
    total = models.DecimalField(max_digits=10, decimal_places=2)
    address = models.TextField()
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)