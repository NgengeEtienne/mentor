# Generated by Django 4.2 on 2024-10-23 23:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AdminDashboard', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='mealplan',
            name='daily_snack_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='friday_snack_dish',
            field=models.ManyToManyField(blank=True, related_name='friday_snack_dish', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='friday_snack_dish_option',
            field=models.ManyToManyField(blank=True, related_name='friday_snack_dish_option', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='friday_snack_meal',
            field=models.ManyToManyField(blank=True, related_name='friday_snack_meal', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='friday_snack_meal_option',
            field=models.ManyToManyField(blank=True, related_name='friday_snack_meal_option', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='monday_snack_dish',
            field=models.ManyToManyField(blank=True, related_name='monday_snack_dish', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='monday_snack_dish_option',
            field=models.ManyToManyField(blank=True, related_name='monday_snack_dish_option', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='monday_snack_meal',
            field=models.ManyToManyField(blank=True, related_name='monday_snack_meal', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='monday_snack_meal_option',
            field=models.ManyToManyField(blank=True, related_name='monday_snack_meal_option', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='monthly_snack_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='saturday_snack_dish',
            field=models.ManyToManyField(blank=True, related_name='saturday_snack_dish', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='saturday_snack_dish_option',
            field=models.ManyToManyField(blank=True, related_name='saturday_snack_dish_option', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='saturday_snack_meal',
            field=models.ManyToManyField(blank=True, related_name='saturday_snack_meal', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='saturday_snack_meal_option',
            field=models.ManyToManyField(blank=True, related_name='saturday_snack_meal_option', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='sunday_snack_dish',
            field=models.ManyToManyField(blank=True, related_name='sunday_snack_dish', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='sunday_snack_dish_option',
            field=models.ManyToManyField(blank=True, related_name='sunday_snack_dish_option', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='sunday_snack_meal',
            field=models.ManyToManyField(blank=True, related_name='sunday_snack_meal', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='sunday_snack_meal_option',
            field=models.ManyToManyField(blank=True, related_name='sunday_snack_meal_option', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='thursday_snack_dish',
            field=models.ManyToManyField(blank=True, related_name='thursday_snack_dish', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='thursday_snack_dish_option',
            field=models.ManyToManyField(blank=True, related_name='thursday_snack_dish_option', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='thursday_snack_meal',
            field=models.ManyToManyField(blank=True, related_name='thursday_snack_meal', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='thursday_snack_meal_option',
            field=models.ManyToManyField(blank=True, related_name='thursday_snack_meal_option', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='tuesday_snack_dish',
            field=models.ManyToManyField(blank=True, related_name='tuesday_snack_dish', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='tuesday_snack_dish_option',
            field=models.ManyToManyField(blank=True, related_name='tuesday_snack_dish_option', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='tuesday_snack_meal',
            field=models.ManyToManyField(blank=True, related_name='tuesday_snack_meal', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='tuesday_snack_meal_option',
            field=models.ManyToManyField(blank=True, related_name='tuesday_snack_meal_option', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='wednesday_snack_dish',
            field=models.ManyToManyField(blank=True, related_name='wednesday_snack_dish', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='wednesday_snack_dish_option',
            field=models.ManyToManyField(blank=True, related_name='wednesday_snack_dish_option', to='AdminDashboard.dishinfo'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='wednesday_snack_meal',
            field=models.ManyToManyField(blank=True, related_name='wednesday_snack_meal', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='wednesday_snack_meal_option',
            field=models.ManyToManyField(blank=True, related_name='wednesday_snack_meal_option', to='AdminDashboard.meal'),
        ),
        migrations.AddField(
            model_name='mealplan',
            name='weekly_snack_price',
            field=models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True),
        ),
        migrations.DeleteModel(
            name='CorperateMealPlan',
        ),
    ]