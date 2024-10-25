from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from account.models import Branch,Company


class DietaryChoice(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class CuisineChoice(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class MealChoice(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='cities')

    def __str__(self):
        return self.name


class Kitchen(models.Model):
    kitchen_id = models.AutoField(primary_key=True)
    kitchenImage = models.ImageField(upload_to='media/menu_images/', blank=True, null=True)
    kitchenName = models.CharField(max_length=100)
    kitchenUrl = models.CharField(max_length=500, blank=True, null=True)
    kitchenDescription=models.CharField(max_length=1000,  blank=True, null=True)
    kitchenAddress=models.CharField(max_length=100,  blank=True)
    kitchenState=models.CharField(max_length=100,  blank=True, null=True)

    kitchenPinCode=models.IntegerField(blank=True)
    kitchenLatitude=models.CharField(max_length=100,  blank=True, null=True)
    kitchenLongitude=models.CharField(max_length=100,  blank=True, null=True)
    is_delivery_available = models.BooleanField(default=False, blank=True, null=True)
    kitchenCity = ArrayField(models.CharField(max_length=200), blank=True, null=True)

    data_create_time = models.DateTimeField(auto_now_add=True)
    last_data_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.kitchenName


class DishInfo(models.Model):
    dish_id = models.AutoField(primary_key=True)
    dish_name = models.CharField(max_length=100)
    dish_image = models.ImageField(upload_to='media/menu_item_images/', blank=True, null=True)
    DishImgUrl = models.CharField(max_length=500, blank=True, null=True)
    dish_description = models.TextField(blank=True)
    dish_base_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    dish_weight = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    dish_availability_status = models.CharField(max_length=50,
                                                choices=[('available', 'Available'), ('unavailable', 'Unavailable')],
                                                default='available', blank=True)
    dish_calories = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    dish_protein = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    dish_carbohydrates = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    dish_fat = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    dish_fiber = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

  
    dietary_choices = models.ManyToManyField(DietaryChoice)
    cuisine_choices = models.ManyToManyField(CuisineChoice)
    meal_choices = models.ManyToManyField(MealChoice)

    data_create_time = models.DateTimeField(auto_now_add=True)
    last_data_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.dish_name}"


class Meal(models.Model):
    meal_id = models.AutoField(primary_key=True)
    meal_name = models.CharField(max_length=100)
    meal_image = models.ImageField(upload_to='media/menu_item_images/', blank=True, null=True)
    MealImgUrl = models.CharField(max_length=500, blank=True, null=True)
    meal_description = models.TextField(blank=True)
    meal_base_price = models.DecimalField(max_digits=8, decimal_places=2)
    meal_weight = models.DecimalField(max_digits=8, decimal_places=2, null=True)
    meal_availability_status = models.CharField(max_length=50,
                                                choices=[('available', 'Available'), ('unavailable', 'Unavailable')],
                                                default='available')
    meal_qty = ArrayField(ArrayField(models.CharField(max_length=50)), blank=True, null=True)

    dietary_choices = models.ManyToManyField(DietaryChoice)
    cuisine_choices = models.ManyToManyField(CuisineChoice)
    meal_choices = models.ManyToManyField(MealChoice) 
    selected_dishes = models.ManyToManyField('DishInfo', related_name='selected_meals', blank=True)

    total_calories = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True)
    total_protein = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True)
    total_carbohydrates = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True)
    total_fat = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True)
    total_fiber = models.DecimalField(max_digits=8, decimal_places=2, default=0, null=True)

    data_create_time = models.DateTimeField(auto_now_add=True)
    last_data_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.meal_name}"


class Menu(models.Model):
    menu_id = models.AutoField(primary_key=True)
    dish_name = models.CharField(max_length=100,blank=True, null=True)
    meal_name = models.CharField(max_length=100, blank=True, null=True)
    menu_price = models.IntegerField()
    menu_qty = models.IntegerField()
    monday = models.BooleanField(default=True, blank=True, null=True)
    tuesday = models.BooleanField(default=True, blank=True, null=True)
    wednesday = models.BooleanField(default=True, blank=True, null=True)
    thursday = models.BooleanField(default=True, blank=True, null=True)
    friday = models.BooleanField(default=True, blank=True, null=True)
    saturday = models.BooleanField(default=True, blank=True, null=True)
    sunday = models.BooleanField(default=True, blank=True, null=True)

    data_create_time = models.DateTimeField(auto_now_add=True)
    last_data_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self. menu_id} Menu Added"


class KitchenMenus(models.Model):
    kitchens = models.ManyToManyField(Kitchen, related_name='kitchen_menus')
    kitchen_menus = models.ManyToManyField(Menu, related_name='kitchen_menus')

    def __str__(self):
        return f"{self. kitchens} - {self.kitchen_menus}"




class MealPlan(models.Model):
    meal_plan_id = models.AutoField(primary_key=True)
    meal_plan_name = models.CharField(max_length=100)
    meal_plan_image = models.ImageField(upload_to='media/menu_item_images/', blank=True, null=True)
    MealPlanImgUrl = models.CharField(max_length=500, blank=True, null=True)
    meal_plan_description = models.TextField(blank=True)
    meal_plan_availability_status = models.CharField(max_length=50,
                                                     choices=[('available', 'Available'),
                                                              ('unavailable', 'Unavailable')],
                                                     default='available')
    meal_plan_person_status = models.CharField(max_length=50,
                                                     choices=[('Corperate', 'Corperate'),
                                                              ('Individual', 'Individual')],
                                                     default='Individual')
    dietary_choices = models.ManyToManyField(DietaryChoice)
    cuisine_choices = models.ManyToManyField(CuisineChoice)

    daily_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    daily_breakfast_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    daily_lunch_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    daily_dinner_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    daily_snack_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    weekly_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    weekly_breakfast_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    weekly_lunch_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    weekly_dinner_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    weekly_snack_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

    monthly_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monthly_breakfast_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monthly_lunch_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monthly_dinner_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    monthly_snack_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)


    is_monday_available = models.BooleanField(default=False, blank=True, null=True)
    monday_breakfast_dish=models.ManyToManyField(DishInfo, blank=True, related_name='monday_breakfast_dish')
    monday_breakfast_meal=models.ManyToManyField(Meal, blank=True, related_name='monday_breakfast_meal')
    monday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='monday_breakfast_dish_option')
    monday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='monday_breakfast_meal_option')
    monday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='monday_lunch_dish')
    monday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='monday_lunch_meal')
    monday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='monday_lunch_dish_option')
    monday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='monday_lunch_meal_option')
    monday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='monday_dinner_dish')
    monday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='monday_dinner_meal')
    monday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='monday_dinner_dish_option')
    monday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='monday_dinner_meal_option')
    monday_snack_dish = models.ManyToManyField(DishInfo, blank=True, related_name='monday_snack_dish')
    monday_snack_meal = models.ManyToManyField(Meal, blank=True, related_name='monday_snack_meal')
    monday_snack_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='monday_snack_dish_option')
    monday_snack_meal_option = models.ManyToManyField(Meal, blank=True, related_name='monday_snack_meal_option')

    is_tuesday_available = models.BooleanField(default=False, blank=True, null=True)
    tuesday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='tuesday_breakfast_dish')
    tuesday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='tuesday_breakfast_meal')
    tuesday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='tuesday_breakfast_dish_option')
    tuesday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='tuesday_breakfast_meal_option')
    tuesday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='tuesday_lunch_dish')
    tuesday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='tuesday_lunch_meal')
    tuesday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='tuesday_lunch_dish_option')
    tuesday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='tuesday_lunch_meal_option')
    tuesday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='tuesday_dinner_dish')
    tuesday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='tuesday_dinner_meal')
    tuesday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='tuesday_dinner_dish_option')
    tuesday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='tuesday_dinner_meal_option')
    tuesday_snack_dish = models.ManyToManyField(DishInfo, blank=True, related_name='tuesday_snack_dish')
    tuesday_snack_meal = models.ManyToManyField(Meal, blank=True, related_name='tuesday_snack_meal')
    tuesday_snack_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='tuesday_snack_dish_option')
    tuesday_snack_meal_option = models.ManyToManyField(Meal, blank=True, related_name='tuesday_snack_meal_option')

    is_wednesday_available = models.BooleanField(default=False, blank=True, null=True)
    wednesday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='wednesday_breakfast_dish')
    wednesday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='wednesday_breakfast_meal')
    wednesday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='wednesday_breakfast_dish_option')
    wednesday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='wednesday_breakfast_meal_option')
    wednesday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='wednesday_lunch_dish')
    wednesday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='wednesday_lunch_meal')
    wednesday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='wednesday_lunch_dish_option')
    wednesday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='wednesday_lunch_meal_option')
    wednesday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='wednesday_dinner_dish')
    wednesday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='wednesday_dinner_meal')
    wednesday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='wednesday_dinner_dish_option')
    wednesday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='wednesday_dinner_meal_option')
    wednesday_snack_dish = models.ManyToManyField(DishInfo, blank=True, related_name='wednesday_snack_dish')
    wednesday_snack_meal = models.ManyToManyField(Meal, blank=True, related_name='wednesday_snack_meal')
    wednesday_snack_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='wednesday_snack_dish_option')
    wednesday_snack_meal_option = models.ManyToManyField(Meal, blank=True, related_name='wednesday_snack_meal_option')

    is_thursday_available = models.BooleanField(default=False, blank=True, null=True)
    thursday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='thursday_breakfast_dish')
    thursday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='thursday_breakfast_meal')
    thursday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='thursday_breakfast_dish_option')
    thursday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='thursday_breakfast_meal_option')
    thursday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='thursday_lunch_dish')
    thursday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='thursday_lunch_meal')
    thursday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='thursday_lunch_dish_option')
    thursday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='thursday_lunch_meal_option')
    thursday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='thursday_dinner_dish')
    thursday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='thursday_dinner_meal')
    thursday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='thursday_dinner_dish_option')
    thursday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='thursday_dinner_meal_option')
    thursday_snack_dish = models.ManyToManyField(DishInfo, blank=True, related_name='thursday_snack_dish')
    thursday_snack_meal = models.ManyToManyField(Meal, blank=True, related_name='thursday_snack_meal')
    thursday_snack_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='thursday_snack_dish_option')
    thursday_snack_meal_option = models.ManyToManyField(Meal, blank=True, related_name='thursday_snack_meal_option')

    is_friday_available = models.BooleanField(default=False, blank=True, null=True)
    friday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='friday_breakfast_dish')
    friday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='friday_breakfast_meal')
    friday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='friday_breakfast_dish_option')
    friday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='friday_breakfast_meal_option')
    friday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='friday_lunch_dish')
    friday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='friday_lunch_meal')
    friday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='friday_lunch_dish_option')
    friday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='friday_lunch_meal_option')
    friday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='friday_dinner_dish')
    friday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='friday_dinner_meal')
    friday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='friday_dinner_dish_dish_option')
    friday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='friday_dinner_meal_option')
    friday_snack_dish = models.ManyToManyField(DishInfo, blank=True, related_name='friday_snack_dish')
    friday_snack_meal = models.ManyToManyField(Meal, blank=True, related_name='friday_snack_meal')
    friday_snack_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='friday_snack_dish_option')
    friday_snack_meal_option = models.ManyToManyField(Meal, blank=True, related_name='friday_snack_meal_option')

    is_saturday_available = models.BooleanField(default=False, blank=True, null=True)
    saturday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='saturday_breakfast_dish')
    saturday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='saturday_breakfast_meal')
    saturday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='saturday_breakfast_dish_option')
    saturday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='saturday_breakfast_meal_option')
    saturday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='saturday_lunch_dish')
    saturday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='saturday_lunch_meal')
    saturday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='saturday_lunch_dish_option')
    saturday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='saturday_lunch_meal_option')
    saturday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='saturday_dinner_dish')
    saturday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='saturday_dinner_meal')
    saturday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='saturday_dinner_dish_option')
    saturday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='saturday_dinner_meal_option')
    saturday_snack_dish = models.ManyToManyField(DishInfo, blank=True, related_name='saturday_snack_dish')
    saturday_snack_meal = models.ManyToManyField(Meal, blank=True, related_name='saturday_snack_meal')
    saturday_snack_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='saturday_snack_dish_option')
    saturday_snack_meal_option = models.ManyToManyField(Meal, blank=True, related_name='saturday_snack_meal_option')

    is_sunday_available = models.BooleanField(default=False, blank=True, null=True)
    sunday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='sunday_breakfast_dish')
    sunday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='sunday_breakfast_meal')
    sunday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='sunday_breakfast_dish_option')
    sunday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='sunday_breakfast_meal_option')
    sunday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='sunday_lunch_dish')
    sunday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='sunday_lunch_meal')
    sunday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='sunday_lunch_dish_option')
    sunday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='sunday_lunch_meal_option')
    sunday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='sunday_dinner_dish')
    sunday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='sunday_dinner_meal')
    sunday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='sunday_dinner_dish_option')
    sunday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='sunday_dinner_meal_option')
    sunday_snack_dish = models.ManyToManyField(DishInfo, blank=True, related_name='sunday_snack_dish')
    sunday_snack_meal = models.ManyToManyField(Meal, blank=True, related_name='sunday_snack_meal')
    sunday_snack_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='sunday_snack_dish_option')
    sunday_snack_meal_option = models.ManyToManyField(Meal, blank=True, related_name='sunday_snack_meal_option')

    data_create_time = models.DateTimeField(auto_now_add=True)
    last_data_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.meal_plan_name



# class CorperateMealPlan(models.Model):
#     meal_plan_id = models.AutoField(primary_key=True)
#     meal_plan_name = models.CharField(max_length=100)
#     meal_plan_image = models.ImageField(upload_to='media/menu_item_images/', blank=True, null=True)
#     MealPlanImgUrl = models.CharField(max_length=500, blank=True, null=True)
#     meal_plan_description = models.TextField(blank=True)
#     meal_plan_availability_status = models.CharField(max_length=50,
#                                                      choices=[('available', 'Available'),
#                                                               ('unavailable', 'Unavailable')],
#                                                      default='available')

#     dietary_choices = models.ManyToManyField(DietaryChoice)
#     cuisine_choices = models.ManyToManyField(CuisineChoice)

#     daily_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     daily_breakfast_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     daily_lunch_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     daily_dinner_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

#     weekly_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     weekly_breakfast_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     weekly_lunch_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     weekly_dinner_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

#     monthly_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     monthly_breakfast_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     monthly_lunch_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
#     monthly_dinner_price = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)

#     is_monday_available = models.BooleanField(default=False, blank=True, null=True)
#     monday_breakfast_dish=models.ManyToManyField(DishInfo, blank=True, related_name='corperate_monday_breakfast_dish')
#     monday_breakfast_meal=models.ManyToManyField(Meal, blank=True, related_name='corperate_monday_breakfast_meal')
#     monday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_monday_breakfast_dish_option')
#     monday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_monday_breakfast_meal_option')
#     monday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_monday_lunch_dish')
#     monday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_monday_lunch_meal')
#     monday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_monday_lunch_dish_option')
#     monday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_monday_lunch_meal_option')
#     monday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_monday_dinner_dish')
#     monday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_monday_dinner_meal')
#     monday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_monday_dinner_dish_option')
#     monday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_monday_dinner_meal_option')

#     is_tuesday_available = models.BooleanField(default=False, blank=True, null=True)
#     tuesday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_tuesday_breakfast_dish')
#     tuesday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_tuesday_breakfast_meal')
#     tuesday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_tuesday_breakfast_dish_option')
#     tuesday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_tuesday_breakfast_meal_option')
#     tuesday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_tuesday_lunch_dish')
#     tuesday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_tuesday_lunch_meal')
#     tuesday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_tuesday_lunch_dish_option')
#     tuesday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_tuesday_lunch_meal_option')
#     tuesday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_tuesday_dinner_dish')
#     tuesday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_tuesday_dinner_meal')
#     tuesday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_tuesday_dinner_dish_option')
#     tuesday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_tuesday_dinner_meal_option')

#     is_wednesday_available = models.BooleanField(default=False, blank=True, null=True)
#     wednesday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_wednesday_breakfast_dish')
#     wednesday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_wednesday_breakfast_meal')
#     wednesday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_wednesday_breakfast_dish_option')
#     wednesday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_wednesday_breakfast_meal_option')
#     wednesday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_wednesday_lunch_dish')
#     wednesday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_wednesday_lunch_meal')
#     wednesday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_wednesday_lunch_dish_option')
#     wednesday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_wednesday_lunch_meal_option')
#     wednesday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_wednesday_dinner_dish')
#     wednesday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_wednesday_dinner_meal')
#     wednesday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_wednesday_dinner_dish_option')
#     wednesday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_wednesday_dinner_meal_option')

#     is_thursday_available = models.BooleanField(default=False, blank=True, null=True)
#     thursday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_thursday_breakfast_dish')
#     thursday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_thursday_breakfast_meal')
#     thursday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_thursday_breakfast_dish_option')
#     thursday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_thursday_breakfast_meal_option')
#     thursday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_thursday_lunch_dish')
#     thursday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_thursday_lunch_meal')
#     thursday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_thursday_lunch_dish_option')
#     thursday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_thursday_lunch_meal_option')
#     thursday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_thursday_dinner_dish')
#     thursday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_thursday_dinner_meal')
#     thursday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_thursday_dinner_dish_option')
#     thursday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_thursday_dinner_meal_option')

#     is_friday_available = models.BooleanField(default=False, blank=True, null=True)
#     friday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_friday_breakfast_dish')
#     friday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_friday_breakfast_meal')
#     friday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_friday_breakfast_dish_option')
#     friday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_friday_breakfast_meal_option')
#     friday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_friday_lunch_dish')
#     friday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_friday_lunch_meal')
#     friday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_friday_lunch_dish_option')
#     friday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_friday_lunch_meal_option')
#     friday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_friday_dinner_dish')
#     friday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_friday_dinner_meal')
#     friday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_friday_dinner_dish_dish_option')
#     friday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_friday_dinner_meal_option')

#     is_saturday_available = models.BooleanField(default=False, blank=True, null=True)
#     saturday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_saturday_breakfast_dish')
#     saturday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_saturday_breakfast_meal')
#     saturday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_saturday_breakfast_dish_option')
#     saturday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_saturday_breakfast_meal_option')
#     saturday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_saturday_lunch_dish')
#     saturday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_saturday_lunch_meal')
#     saturday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_saturday_lunch_dish_option')
#     saturday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_saturday_lunch_meal_option')
#     saturday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_saturday_dinner_dish')
#     saturday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_saturday_dinner_meal')
#     saturday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_saturday_dinner_dish_option')
#     saturday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_saturday_dinner_meal_option')

#     is_sunday_available = models.BooleanField(default=False, blank=True, null=True)
#     sunday_breakfast_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_sunday_breakfast_dish')
#     sunday_breakfast_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_sunday_breakfast_meal')
#     sunday_breakfast_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_sunday_breakfast_dish_option')
#     sunday_breakfast_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_sunday_breakfast_meal_option')
#     sunday_lunch_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_sunday_lunch_dish')
#     sunday_lunch_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_sunday_lunch_meal')
#     sunday_lunch_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_sunday_lunch_dish_option')
#     sunday_lunch_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_sunday_lunch_meal_option')
#     sunday_dinner_dish = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_sunday_dinner_dish')
#     sunday_dinner_meal = models.ManyToManyField(Meal, blank=True, related_name='corperate_sunday_dinner_meal')
#     sunday_dinner_dish_option = models.ManyToManyField(DishInfo, blank=True, related_name='corperate_sunday_dinner_dish_option')
#     sunday_dinner_meal_option = models.ManyToManyField(Meal, blank=True, related_name='corperate_sunday_dinner_meal_option')

#     data_create_time = models.DateTimeField(auto_now_add=True)
#     last_data_updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.meal_plan_name

# class Company(models.Model):
#     company_id=models.AutoField(primary_key=True)
#     company_name=models.CharField(max_length=100)
#     company_description=models.TextField(null=True, blank=True)
#     company_phone_number=models.CharField(max_length=100, blank=True, null=True)
#     company_email=models.EmailField(max_length=100, blank=True, null=True)
#     company_address=models.CharField(max_length=100, blank=True, null=True)
#     latitude = models.DecimalField(max_digits=10, decimal_places=8,blank=True, null=True)
#     longitude = models.DecimalField(max_digits=11, decimal_places=8,blank=True, null=True)
#     data_create_time = models.DateTimeField(auto_now_add=True)
#     last_data_updated_time = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.company_name


class BulkOrders(models.Model):
    bulk_order_id=models.AutoField(primary_key=True)
    company=models.ForeignKey(Company, on_delete=models.CASCADE, related_name='company_info')
    branch=models.ForeignKey(Branch, on_delete=models.CASCADE, related_name='branch_info')
    bulk_order_name=models.CharField(max_length=100, null=True, blank=True)
    bulk_order_description=models.TextField(null=True, blank=True)
    kitchen = models.ManyToManyField(Kitchen, related_name='kitchen_bulk_orders')
    MealPlan = models.ManyToManyField(MealPlan, related_name='meal_plan_bulk_orders')
    breakfast = models.IntegerField()
    lunch = models.IntegerField()
    snack = models.IntegerField()
    dinner = models.IntegerField()
    bulk_order_start_date=models.DateField()
    bulk_order_end_date=models.DateField()

    data_create_time = models.DateTimeField(auto_now_add=True)
    last_data_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.bulk_order_name) or "unnamed"


class UserOrder(models.Model):
    order_id = models.AutoField(primary_key=True)
    user_id = models.CharField(max_length=100)
    order_date = models.DateField()
    order_time = models.TimeField()
    DishInfo = models.ManyToManyField(DishInfo, blank=True, related_name='user_ordered_dish')
    Meal = models.ManyToManyField(Meal, blank=True, related_name='user_ordered_meal')
    order_status = models.CharField(
        max_length=50, choices=[('placed', 'Placed'), ('cancelled', 'Cancelled'), ('delivered', 'Delivered')], default='placed'
    )
    order_type = models.CharField(
        max_length=50, choices=[('bulk', 'Bulk'), ('dish', 'Dish'), ('meal', 'Meal')], default='bulk'
    )
    total_price = models.DecimalField(max_digits=8, decimal_places=2)
    payment_status = models.CharField(
        max_length=50, choices=[('paid', 'Paid'), ('unpaid', 'Unpaid')], default='unpaid'
    )
    delivery_address = models.CharField(max_length=200)
    delivery_date = models.DateField()
    delivery_time = models.TimeField()
    delivery_status = models.CharField(
        max_length=50, choices=[('delivered', 'Delivered'), ('pending', 'Pending')], default='pending'
    )

    data_create_time = models.DateTimeField(auto_now_add=True)
    last_data_updated_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.order_id)
    
# class Company(models.Model):
#     name = models.CharField(max_length=255)
#     address_line_1 = models.CharField(max_length=255)
#     address_line_2 = models.CharField(max_length=255, blank=True)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     pin_code = models.CharField(max_length=10)
#     latitude = models.DecimalField(max_digits=10, decimal_places=8)
#     longitude = models.DecimalField(max_digits=11, decimal_places=8)
#     date_created = models.DateTimeField(default=timezone.now)
#     date_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return self.name
# class Branch(models.Model):
#     name = models.CharField(max_length=255)
#     company = models.ForeignKey(Company, on_delete=models.CASCADE)
#     address_line_1 = models.CharField(max_length=255)
#     address_line_2 = models.CharField(max_length=255, blank=True)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     pin_code = models.CharField(max_length=10)
#     latitude = models.DecimalField(max_digits=10, decimal_places=8)
#     longitude = models.DecimalField(max_digits=11, decimal_places=8)
#     date_created = models.DateTimeField(auto_now=True)
#     date_updated = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"{self.name} ({self.company.company_name})"
    
