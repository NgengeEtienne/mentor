# admin.py
from django.contrib import admin
from .models import DeliveryAddress, MealDelivery, Notification


from django.contrib import admin
from .models import DeliveryAddress, MealDelivery, Notification

# Inline for MealDelivery
from django.contrib import admin
from .models import DeliveryAddress, MealDelivery, Notification

#
# Admin for DeliveryAddress
@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('name','company','branch', 'address_line_1', 'city', 'state', 'pin_code', 'default_address')

# Admin for MealDelivery
@admin.register(MealDelivery)
class MealDeliveryAdmin(admin.ModelAdmin):
    list_display = ('bulk_order', 'company','branch','delivery_address', 'meal_type', 'quantity', 'date', 'status')
    # inlines = [NotificationInline]  # Include Notification inline here

# Admin for Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'message', 'branch', 'company', 'created_at')
