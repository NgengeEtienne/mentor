# resources.py
from import_export import resources
from.models import DeliveryAddress, MealDelivery, Notification

class DeliveryAddressResource(resources.ModelResource):
    class Meta:
        model = DeliveryAddress
        fields = ('id', 'name', 'address_line_1', 'address_line_2', 'city','state', 'pin_code', 'latitude', 'longitude', 'date_created', 'date_updated', 'branch', 'company', 'default_address')

class MealDeliveryResource(resources.ModelResource):
    class Meta:
        model = MealDelivery
        fields = ('id', 'bulk_order', 'delivery_address','meal_type', 'quantity', 'date','status', 'branch', 'company', 'created_at', 'assigned_at')

class NotificationResource(resources.ModelResource):
    class Meta:
        model = Notification
        fields = ('id', 'delivery','message', 'branch', 'company', 'created_at')