from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import (
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
from.resources import (
    DietaryChoiceResource,
    CuisineChoiceResource,
    MealChoiceResource,
    StateResource,
    CityResource,
    KitchenResource,
    DishInfoResource,
    MealResource,
    MenuResource,
    KitchenMenusResource,
    UserOrderResource,
    BulkOrdersResource,
    MealPlanResource,
)
# Inline for selected dishes in Meal
class DishInfoInline(ImportExportModelAdmin):
    model = Meal.selected_dishes.through  # Correctly referencing the through model
    extra = 1  # Number of empty forms to display
    resource_class = DietaryChoiceResource

# Inline for Kitchen in KitchenMenus
class KitchenMenuInline(ImportExportModelAdmin):
    model = KitchenMenus.kitchens.through  # Correctly referencing the through model
    extra = 1  # Number of empty forms to display
    resource_class = KitchenResource

# Admin for DietaryChoice
@admin.register(DietaryChoice)
class DietaryChoiceAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    resource_class = DietaryChoiceResource

# Admin for CuisineChoice
@admin.register(CuisineChoice)
class CuisineChoiceAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    resource_class = CuisineChoiceResource

# Admin for MealChoice
@admin.register(MealChoice)
class MealChoiceAdmin(ImportExportModelAdmin):
    list_display = ('name',)

# Admin for State
@admin.register(State)
class StateAdmin(ImportExportModelAdmin):
    list_display = ('name',)
    resource_class = StateResource

# Admin for City
@admin.register(City)
class CityAdmin(ImportExportModelAdmin):
    list_display = ('name', 'state')
    resource_class = CityResource

# Admin for Kitchen
@admin.register(Kitchen)
class KitchenAdmin(ImportExportModelAdmin):
    list_display = ('kitchenName', 'kitchenAddress', 'kitchenState', 'is_delivery_available')
    # inlines = [KitchenMenuInline]  # Display menus for each kitchen
    resource_class = KitchenResource

# Admin for DishInfo
@admin.register(DishInfo)
class DishInfoAdmin(ImportExportModelAdmin):
    list_display = ('dish_name', 'dish_base_price', 'dish_availability_status')
    # inlines = [DishInfoInline]  # Display dish info in meals
    resource_class = DishInfoResource

# Admin for Meal
@admin.register(Meal)
class MealAdmin(ImportExportModelAdmin):
    list_display = ('meal_name', 'meal_base_price', 'meal_availability_status')
    # inlines = [DishInfoInline]  # Display selected dishes in the meal
    resource_class = MealResource

# Admin for Menu
@admin.register(Menu)
class MenuAdmin(ImportExportModelAdmin):
    list_display = ('menu_id', 'dish_name', 'meal_name', 'menu_price', 'menu_qty')
    resource_class = MenuResource

# Admin for KitchenMenus
@admin.register(KitchenMenus)
class KitchenMenusAdmin(ImportExportModelAdmin):
    list_display = ('get_kitchens', 'get_kitchen_menus')
    resource_class = KitchenMenusResource

    def get_kitchens(self, obj):
        return ", ".join([kitchen.kitchenName for kitchen in obj.kitchens.all()])
    get_kitchens.short_description = 'Kitchens'

    def get_kitchen_menus(self, obj):
        return ", ".join([menu.dish_name for menu in obj.kitchen_menus.all()])
    get_kitchen_menus.short_description = 'Kitchen Menus'

@admin.register(MealPlan)
class MealPlanAdmin(ImportExportModelAdmin):
    resource_class = MealPlanResource

# Admin for BulkOrders
@admin.register(BulkOrders)
class BulkOrdersAdmin(ImportExportModelAdmin):
    list_display = ('bulk_order_name', 'company', 'branch', 'bulk_order_start_date', 'bulk_order_end_date')
    search_fields = ('bulk_order_name', 'bulk_order_description')
    list_filter = ('company', 'branch')
    resource_class = BulkOrdersResource

# Inline for Meal in UserOrder
class MealInline(ImportExportModelAdmin):
    model = UserOrder.Meal.through  # Correctly referencing the through model
    extra = 1  # Number of empty forms to display
    resource_class = MealResource

# Admin for UserOrder
@admin.register(UserOrder)
class UserOrderAdmin(ImportExportModelAdmin):
    list_display = ('order_id', 'user_id', 'order_date', 'total_price', 'order_status')
    search_fields = ('user_id', 'order_id')
    list_filter = ('order_status', 'order_type', 'payment_status')
    # inlines = [MealInline]  # Display meals in user orders, not DishInfoInline
    resource_class = UserOrderResource
