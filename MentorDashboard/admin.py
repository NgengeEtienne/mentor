# admin.py
from django.contrib import admin
from .models import DeliveryAddress, MealDelivery, Notification
from import_export.admin import ImportExportModelAdmin

from django.contrib import admin
from .models import DeliveryAddress, MealDelivery, Notification

# Inline for MealDelivery
from django.contrib import admin
from .models import DeliveryAddress, MealDelivery, Notification
from.resources import DeliveryAddressResource, MealDeliveryResource, NotificationResource

#
# Admin for DeliveryAddress
@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(ImportExportModelAdmin):
    list_display = ('name','company','branch', 'address_line_1', 'city', 'state', 'pin_code', 'default_address')
    resource_class = DeliveryAddressResource
# Admin for MealDelivery
@admin.register(MealDelivery)
class MealDeliveryAdmin(ImportExportModelAdmin):
    list_display = ('bulk_order', 'company','branch','delivery_address', 'meal_type', 'quantity', 'date', 'status')
    # inlines = [NotificationInline]  # Include Notification inline here
    resource_class = MealDeliveryResource

# Admin for Notification
@admin.register(Notification)
class NotificationAdmin(ImportExportModelAdmin):
    list_display = ('delivery', 'message', 'branch', 'company', 'created_at')
    resource_class = NotificationResource
