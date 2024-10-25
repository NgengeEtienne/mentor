from rest_framework import serializers
from .models import Kitchen, Menu, DishInfo, Meal, MealPlan, DietaryChoice, CuisineChoice, MealChoice, \
    City, State, KitchenMenus, BulkOrders, UserOrder, Company
from django.contrib.contenttypes.models import ContentType


class DietaryChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = DietaryChoice
        fields = '__all__'


class CuisineChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CuisineChoice
        fields = '__all__'


class MealChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = MealChoice
        fields = '__all__'


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = ['id', 'name']


class StateSerializer(serializers.ModelSerializer):
    cities = CitySerializer(many=True, read_only=True)

    class Meta:
        model = State
        fields = ['id', 'name', 'cities']


class KitchenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Kitchen
        fields = '__all__'


class DishInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = DishInfo
        fields = '__all__'


class DishInfoSerializer(serializers.ModelSerializer):
    dietary_choices = serializers.PrimaryKeyRelatedField(queryset=DietaryChoice.objects.all(), many=True)
    cuisine_choices = serializers.PrimaryKeyRelatedField(queryset=CuisineChoice.objects.all(), many=True)
    meal_choices = serializers.PrimaryKeyRelatedField(queryset=MealChoice.objects.all(), many=True)

    class Meta:
        model = DishInfo
        fields = '__all__'




class MealSerializer(serializers.ModelSerializer):
    selected_dishes = serializers.PrimaryKeyRelatedField(queryset=DishInfo.objects.all(), many=True)

    class Meta:
        model = Meal
        fields = '__all__'


class UpdateMealSerializer(serializers.ModelSerializer):
    selected_dishes = DishInfoSerializer(many=True, read_only=True)

    class Meta:
        model = Meal
        fields = '__all__'


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class KitchenMenusSerializer(serializers.ModelSerializer):
    kitchens = serializers.PrimaryKeyRelatedField(many=True, queryset=Kitchen.objects.all())
    kitchen_menus = serializers.PrimaryKeyRelatedField(many=True, queryset=Menu.objects.all())

    class Meta:
        model = KitchenMenus
        fields = '__all__'


class MenuDataWithKitchenSerializer(serializers.ModelSerializer):
        kitchen_menus = MenuSerializer(many=True, read_only=True)
        kitchens = KitchenSerializer(many=True, read_only=True)

        class Meta:
            model = KitchenMenus
            fields = '__all__'


class MealPlanSerializer(serializers.ModelSerializer):
    monday_breakfast_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    monday_breakfast_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    monday_breakfast_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    monday_breakfast_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    monday_lunch_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    monday_lunch_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    monday_lunch_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    monday_lunch_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    monday_dinner_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    monday_dinner_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    monday_dinner_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    monday_dinner_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())

    tuesday_breakfast_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    tuesday_breakfast_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    tuesday_breakfast_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    tuesday_breakfast_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    tuesday_lunch_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    tuesday_lunch_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    tuesday_lunch_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    tuesday_lunch_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    tuesday_dinner_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    tuesday_dinner_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    tuesday_dinner_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    tuesday_dinner_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())

    wednesday_breakfast_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    wednesday_breakfast_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    wednesday_breakfast_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    wednesday_breakfast_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    wednesday_lunch_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    wednesday_lunch_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    wednesday_lunch_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    wednesday_lunch_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    wednesday_dinner_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    wednesday_dinner_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    wednesday_dinner_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    wednesday_dinner_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())

    thursday_breakfast_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    thursday_breakfast_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    thursday_breakfast_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    thursday_breakfast_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    thursday_lunch_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    thursday_lunch_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    thursday_lunch_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    thursday_lunch_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    thursday_dinner_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    thursday_dinner_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    thursday_dinner_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    thursday_dinner_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())

    friday_breakfast_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    friday_breakfast_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    friday_breakfast_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    friday_breakfast_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    friday_lunch_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    friday_lunch_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    friday_lunch_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    friday_lunch_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    friday_dinner_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    friday_dinner_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    friday_dinner_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    friday_dinner_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())

    saturday_breakfast_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    saturday_breakfast_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    saturday_breakfast_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    saturday_breakfast_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    saturday_lunch_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    saturday_lunch_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    saturday_lunch_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    saturday_lunch_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    saturday_dinner_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    saturday_dinner_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    saturday_dinner_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    saturday_dinner_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())

    sunday_breakfast_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    sunday_breakfast_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    sunday_breakfast_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    sunday_breakfast_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    sunday_lunch_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    sunday_lunch_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    sunday_lunch_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    sunday_lunch_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    sunday_dinner_dish = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    sunday_dinner_meal = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())
    sunday_dinner_dish_option = serializers.PrimaryKeyRelatedField(many=True, queryset=DishInfo.objects.all())
    sunday_dinner_meal_option = serializers.PrimaryKeyRelatedField(many=True, queryset=Meal.objects.all())

    class Meta:
        model = MealPlan
        fields = '__all__'


class MealPlanDataSerializer(serializers.ModelSerializer):
    dietary_choices = DietaryChoiceSerializer(many=True, read_only=True)
    cuisine_choices = CuisineChoiceSerializer(many=True, read_only=True)

    monday_breakfast_dish = DishInfoSerializer(many=True, read_only=True)
    monday_breakfast_meal = MealSerializer(many=True, read_only=True)
    monday_breakfast_dish_option = DishInfoSerializer(many=True, read_only=True)
    monday_breakfast_meal_option = MealSerializer(many=True, read_only=True)
    monday_lunch_dish = DishInfoSerializer(many=True, read_only=True)
    monday_lunch_meal = MealSerializer(many=True, read_only=True)
    monday_lunch_dish_option = DishInfoSerializer(many=True, read_only=True)
    monday_lunch_meal_option = MealSerializer(many=True, read_only=True)
    monday_dinner_dish = DishInfoSerializer(many=True, read_only=True)
    monday_dinner_meal = MealSerializer(many=True, read_only=True)
    monday_dinner_dish_option = DishInfoSerializer(many=True, read_only=True)
    monday_dinner_meal_option = MealSerializer(many=True, read_only=True)

    tuesday_breakfast_dish = DishInfoSerializer(many=True, read_only=True)
    tuesday_breakfast_meal = MealSerializer(many=True, read_only=True)
    tuesday_breakfast_dish_option = DishInfoSerializer(many=True, read_only=True)
    tuesday_breakfast_meal_option = MealSerializer(many=True, read_only=True)
    tuesday_lunch_dish = DishInfoSerializer(many=True, read_only=True)
    tuesday_lunch_meal = MealSerializer(many=True, read_only=True)
    tuesday_lunch_dish_option = DishInfoSerializer(many=True, read_only=True)
    tuesday_lunch_meal_option = MealSerializer(many=True, read_only=True)
    tuesday_dinner_dish = DishInfoSerializer(many=True, read_only=True)
    tuesday_dinner_meal = MealSerializer(many=True, read_only=True)
    tuesday_dinner_dish_option = DishInfoSerializer(many=True, read_only=True)
    tuesday_dinner_meal_option = MealSerializer(many=True, read_only=True)

    wednesday_breakfast_dish = DishInfoSerializer(many=True, read_only=True)
    wednesday_breakfast_meal = MealSerializer(many=True, read_only=True)
    wednesday_breakfast_dish_option = DishInfoSerializer(many=True, read_only=True)
    wednesday_breakfast_meal_option = MealSerializer(many=True, read_only=True)
    wednesday_lunch_dish = DishInfoSerializer(many=True, read_only=True)
    wednesday_lunch_meal = MealSerializer(many=True, read_only=True)
    wednesday_lunch_dish_option = DishInfoSerializer(many=True, read_only=True)
    wednesday_lunch_meal_option = MealSerializer(many=True, read_only=True)
    wednesday_dinner_dish = DishInfoSerializer(many=True, read_only=True)
    wednesday_dinner_meal = MealSerializer(many=True, read_only=True)
    wednesday_dinner_dish_option = DishInfoSerializer(many=True, read_only=True)
    wednesday_dinner_meal_option = MealSerializer(many=True, read_only=True)

    thursday_breakfast_dish = DishInfoSerializer(many=True, read_only=True)
    thursday_breakfast_meal = MealSerializer(many=True, read_only=True)
    thursday_breakfast_dish_option = DishInfoSerializer(many=True, read_only=True)
    thursday_breakfast_meal_option = MealSerializer(many=True, read_only=True)
    thursday_lunch_dish = DishInfoSerializer(many=True, read_only=True)
    thursday_lunch_meal = MealSerializer(many=True, read_only=True)
    thursday_lunch_dish_option = DishInfoSerializer(many=True, read_only=True)
    thursday_lunch_meal_option = MealSerializer(many=True, read_only=True)
    thursday_dinner_dish = DishInfoSerializer(many=True, read_only=True)
    thursday_dinner_meal = MealSerializer(many=True, read_only=True)
    thursday_dinner_dish_option = DishInfoSerializer(many=True, read_only=True)
    thursday_dinner_meal_option = MealSerializer(many=True, read_only=True)

    friday_breakfast_dish = DishInfoSerializer(many=True, read_only=True)
    friday_breakfast_meal = MealSerializer(many=True, read_only=True)
    friday_breakfast_dish_option = DishInfoSerializer(many=True, read_only=True)
    friday_breakfast_meal_option = MealSerializer(many=True, read_only=True)
    friday_lunch_dish = DishInfoSerializer(many=True, read_only=True)
    friday_lunch_meal = MealSerializer(many=True, read_only=True)
    friday_lunch_dish_option = DishInfoSerializer(many=True, read_only=True)
    friday_lunch_meal_option = MealSerializer(many=True, read_only=True)
    friday_dinner_dish = DishInfoSerializer(many=True, read_only=True)
    friday_dinner_meal = MealSerializer(many=True, read_only=True)
    friday_dinner_dish_option = DishInfoSerializer(many=True, read_only=True)
    friday_dinner_meal_option = MealSerializer(many=True, read_only=True)

    saturday_breakfast_dish = DishInfoSerializer(many=True, read_only=True)
    saturday_breakfast_meal = MealSerializer(many=True, read_only=True)
    saturday_breakfast_dish_option = DishInfoSerializer(many=True, read_only=True)
    saturday_breakfast_meal_option = MealSerializer(many=True, read_only=True)
    saturday_lunch_dish = DishInfoSerializer(many=True, read_only=True)
    saturday_lunch_meal = MealSerializer(many=True, read_only=True)
    saturday_lunch_dish_option = DishInfoSerializer(many=True, read_only=True)
    saturday_lunch_meal_option = MealSerializer(many=True, read_only=True)
    saturday_dinner_dish = DishInfoSerializer(many=True, read_only=True)
    saturday_dinner_meal = MealSerializer(many=True, read_only=True)
    saturday_dinner_dish_option = DishInfoSerializer(many=True, read_only=True)
    saturday_dinner_meal_option = MealSerializer(many=True, read_only=True)
    
    sunday_breakfast_dish = DishInfoSerializer(many=True, read_only=True)
    sunday_breakfast_meal = MealSerializer(many=True, read_only=True)
    sunday_breakfast_dish_option = DishInfoSerializer(many=True, read_only=True)
    sunday_breakfast_meal_option = MealSerializer(many=True, read_only=True)
    sunday_lunch_dish = DishInfoSerializer(many=True, read_only=True)
    sunday_lunch_meal = MealSerializer(many=True, read_only=True)
    sunday_lunch_dish_option = DishInfoSerializer(many=True, read_only=True)
    sunday_lunch_meal_option = MealSerializer(many=True, read_only=True)
    sunday_dinner_dish = DishInfoSerializer(many=True, read_only=True)
    sunday_dinner_meal = MealSerializer(many=True, read_only=True)
    sunday_dinner_dish_option = DishInfoSerializer(many=True, read_only=True)
    sunday_dinner_meal_option = MealSerializer(many=True, read_only=True)

    class Meta:
        model = MealPlan
        fields = '__all__'


class CompanyInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class BulkOrderSerializer(serializers.ModelSerializer):
    kitchen = KitchenSerializer(many=True, read_only=True)
    MealPlan = MealPlanSerializer(many=True, read_only=True)
    company = CompanyInfoSerializer(read_only=True)

    class Meta:
        model = BulkOrders
        fields = '__all__'


class UserOrderSerializer(serializers.ModelSerializer):
    dish_info = DishInfoSerializer(many=True, read_only=True)
    meal = MealSerializer(many=True, read_only=True)

    class Meta:
        model = UserOrder
        fields = '__all__'