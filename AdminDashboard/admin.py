from django.contrib import admin
from .models import Kitchen,Menu, DishInfo, Meal, CuisineChoice, DietaryChoice, MealChoice, MealPlan, City,\
    State, KitchenMenus,BulkOrders

# Register your models here.
admin.site.register(Kitchen)
admin.site.register(Menu)
admin.site.register(DishInfo)
admin.site.register(Meal)
admin.site.register(DietaryChoice)
admin.site.register(CuisineChoice)
admin.site.register(MealChoice)
admin.site.register(MealPlan)
# admin.site.register(CorperateMealPlan)
admin.site.register(State)
admin.site.register(City)
admin.site.register(KitchenMenus)
admin.site.register(BulkOrders)



