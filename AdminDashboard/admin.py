from django.contrib import admin
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

# Inline for selected dishes in Meal
class DishInfoInline(admin.TabularInline):
    model = Meal.selected_dishes.through  # Correctly referencing the through model
    extra = 1  # Number of empty forms to display

# Inline for Kitchen in KitchenMenus
class KitchenMenuInline(admin.TabularInline):
    model = KitchenMenus.kitchens.through  # Correctly referencing the through model
    extra = 1  # Number of empty forms to display

# Admin for DietaryChoice
@admin.register(DietaryChoice)
class DietaryChoiceAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Admin for CuisineChoice
@admin.register(CuisineChoice)
class CuisineChoiceAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Admin for MealChoice
@admin.register(MealChoice)
class MealChoiceAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Admin for State
@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ('name',)

# Admin for City
@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('name', 'state')

# Admin for Kitchen
@admin.register(Kitchen)
class KitchenAdmin(admin.ModelAdmin):
    list_display = ('kitchenName', 'kitchenAddress', 'kitchenState', 'is_delivery_available')
    inlines = [KitchenMenuInline]  # Display menus for each kitchen

# Admin for DishInfo
@admin.register(DishInfo)
class DishInfoAdmin(admin.ModelAdmin):
    list_display = ('dish_name', 'dish_base_price', 'dish_availability_status')
    inlines = [DishInfoInline]  # Display dish info in meals

# Admin for Meal
@admin.register(Meal)
class MealAdmin(admin.ModelAdmin):
    list_display = ('meal_name', 'meal_base_price', 'meal_availability_status')
    inlines = [DishInfoInline]  # Display selected dishes in the meal

# Admin for Menu
@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ('menu_id', 'dish_name', 'meal_name', 'menu_price', 'menu_qty')

# Admin for KitchenMenus
@admin.register(KitchenMenus)
class KitchenMenusAdmin(admin.ModelAdmin):
    list_display = ('get_kitchens', 'get_kitchen_menus')

    def get_kitchens(self, obj):
        return ", ".join([kitchen.kitchenName for kitchen in obj.kitchens.all()])
    get_kitchens.short_description = 'Kitchens'

    def get_kitchen_menus(self, obj):
        return ", ".join([menu.dish_name for menu in obj.kitchen_menus.all()])
    get_kitchen_menus.short_description = 'Kitchen Menus'

admin.site.register(MealPlan)

# Admin for BulkOrders
@admin.register(BulkOrders)
class BulkOrdersAdmin(admin.ModelAdmin):
    list_display = ('bulk_order_name', 'company', 'branch', 'bulk_order_start_date', 'bulk_order_end_date')
    search_fields = ('bulk_order_name', 'bulk_order_description')
    list_filter = ('company', 'branch')

# Inline for Meal in UserOrder
class MealInline(admin.TabularInline):
    model = UserOrder.Meal.through  # Correctly referencing the through model
    extra = 1  # Number of empty forms to display

# Admin for UserOrder
@admin.register(UserOrder)
class UserOrderAdmin(admin.ModelAdmin):
    list_display = ('order_id', 'user_id', 'order_date', 'total_price', 'order_status')
    search_fields = ('user_id', 'order_id')
    list_filter = ('order_status', 'order_type', 'payment_status')
    inlines = [MealInline]  # Display meals in user orders, not DishInfoInline
