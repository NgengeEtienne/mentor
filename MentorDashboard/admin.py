# admin.py
from django.contrib import admin
from .models import DeliveryAddress, MealDelivery, Notification


admin.site.register(DeliveryAddress)
admin.site.register(MealDelivery)
admin.site.register(Notification)