# resources.py
from import_export import resources
from.models import (
    DietaryChoice,
    CuisineChoice,
    MealChoice,
    State,
    City,
    Kitchen,
    DishInfo,
    Meal,
    Menu,
    KitchenMenus,
    UserOrder,
    BulkOrders,
    MealPlan,
)

class DietaryChoiceResource(resources.ModelResource):
    class Meta:
        model = DietaryChoice
        fields = ('id', 'name')

class CuisineChoiceResource(resources.ModelResource):
    class Meta:
        model = CuisineChoice
        fields = ('id', 'name')

class MealChoiceResource(resources.ModelResource):
    class Meta:
        model = MealChoice
        fields = ('id', 'name')

class StateResource(resources.ModelResource):
    class Meta:
        model = State
        fields = ('id', 'name')

class CityResource(resources.ModelResource):
    class Meta:
        model = City
        fields = ('id', 'name','state')

class KitchenResource(resources.ModelResource):
    class Meta:
        model = Kitchen
        fields = ('id', 'kitchenName', 'kitchenAddress', 'kitchenState', 'is_delivery_available')

class DishInfoResource(resources.ModelResource):
    class Meta:
        model = DishInfo
        fields = ('id', 'dish_name', 'dish_base_price', 'dish_availability_status')

class MealResource(resources.ModelResource):
    class Meta:
        model = Meal
        fields = ('id','meal_name','meal_base_price','meal_availability_status')

class MenuResource(resources.ModelResource):
    class Meta:
        model = Menu
        fields = ('id','menu_id', 'dish_name','meal_name','menu_price','menu_qty')

class KitchenMenusResource(resources.ModelResource):
    class Meta:
        model = KitchenMenus
        fields = ('id', 'kitchens', 'kitchen_menus')

class UserOrderResource(resources.ModelResource):
    class Meta:
        model = UserOrder
        fields = ('id', 'order_id', 'user_id', 'order_date', 'total_price', 'order_status')

class BulkOrdersResource(resources.ModelResource):
    class Meta:
        model = BulkOrders
        fields = ('id', 'bulk_order_name', 'company', 'branch', 'bulk_order_start_date', 'bulk_order_end_date')

class MealPlanResource(resources.ModelResource):
    class Meta:
        model = MealPlan
        fields = ('id','meal_plan_name','meal_plan_description','meal_plan_start_date','meal_plan_end_date')