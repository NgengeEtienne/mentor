# admin.py
from django.contrib import admin
from .models import DeliveryAddress, MealDelivery, Notification


from django.contrib import admin
from .models import DeliveryAddress, MealDelivery, Notification

# Inline for MealDelivery
from django.contrib import admin
from .models import DeliveryAddress, MealDelivery, Notification

# Inline for MealDelivery
class MealDeliveryInline(admin.TabularInline):
    model = MealDelivery
    extra = 1  # Number of empty forms to display
    fields = ('bulk_order', 'meal_type', 'quantity', 'date', 'status')

# Inline for Notification
class NotificationInline(admin.TabularInline):
    model = Notification
    extra = 1  # Number of empty forms to display
    fields = ('message',)

# Admin for DeliveryAddress
@admin.register(DeliveryAddress)
class DeliveryAddressAdmin(admin.ModelAdmin):
    list_display = ('name', 'address_line_1', 'city', 'state', 'pin_code', 'default_address')
    inlines = [MealDeliveryInline]  # Only include MealDelivery here

# Admin for MealDelivery
@admin.register(MealDelivery)
class MealDeliveryAdmin(admin.ModelAdmin):
    list_display = ('bulk_order', 'delivery_address', 'meal_type', 'quantity', 'date', 'status', 'created_at')
    inlines = [NotificationInline]  # Include Notification inline here

# Admin for Notification
@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('delivery', 'message', 'branch', 'company', 'created_at')
