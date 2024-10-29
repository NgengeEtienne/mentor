# models.py
from django.db import models
from django.utils import timezone

from AdminDashboard.models import MealPlan,Branch,Company,BulkOrders
from account.models import Branch,Company


class DeliveryAddress(models.Model):
    name = models.CharField(max_length=255)
    address_line_1 = models.CharField(max_length=255)
    address_line_2 = models.CharField(max_length=255, blank=True)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    latitude = models.DecimalField(max_digits=10, decimal_places=8)
    longitude = models.DecimalField(max_digits=11, decimal_places=8)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    default_address = models.BooleanField(default=False, blank=True, null=True)
    def __str__(self):
        return self.name
    
class MealDelivery(models.Model):
    bulk_order = models.ForeignKey(BulkOrders, on_delete=models.CASCADE)
    delivery_address = models.ForeignKey(DeliveryAddress, on_delete=models.CASCADE)
    meal_type = models.CharField(max_length=50, choices=[
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('snack', 'Snack'),
        ('dinner', 'Dinner'),
        ('dinner2', 'Dinner2')
    ])
    quantity = models.PositiveIntegerField()
    date=models.CharField(max_length=100)
    STATUS_CHOICES = (
        ('COOKING', 'Cooking'),
        ('DISPATCHED', 'Dispatched'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled')
    )
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='COOKING')
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    assigned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bulk_order} - {self.meal_type} to {self.delivery_address}"

class Notification(models.Model):
    id = models.AutoField(primary_key=True)
    delivery = models.ForeignKey(MealDelivery, on_delete=models.CASCADE)
    message = models.TextField()
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE)
    company=models.ForeignKey(Company, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)