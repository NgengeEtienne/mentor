# Generated by Django 4.2 on 2024-10-25 19:40

from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('AdminDashboard', '0002_mealplan_daily_snack_price_and_more'),
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DeliveryAddress',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('address_line_1', models.CharField(max_length=255)),
                ('address_line_2', models.CharField(blank=True, max_length=255)),
                ('city', models.CharField(max_length=100)),
                ('state', models.CharField(max_length=100)),
                ('pin_code', models.CharField(max_length=10)),
                ('latitude', models.DecimalField(decimal_places=8, max_digits=10)),
                ('longitude', models.DecimalField(decimal_places=8, max_digits=11)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_updated', models.DateTimeField(auto_now=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.branch')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.company')),
            ],
        ),
        migrations.CreateModel(
            name='MealDelivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('meal_type', models.CharField(choices=[('breakfast', 'Breakfast'), ('lunch', 'Lunch'), ('snack', 'Snack'), ('dinner', 'Dinner')], max_length=50)),
                ('quantity', models.PositiveIntegerField()),
                ('date', models.CharField(max_length=100)),
                ('status', models.CharField(choices=[('COOKING', 'Cooking'), ('DISPATCHED', 'Dispatched'), ('DELIVERED', 'Delivered'), ('CANCELED', 'Canceled')], default='COOKING', max_length=10)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('assigned_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.branch')),
                ('bulk_order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='AdminDashboard.bulkorders')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.company')),
                ('delivery_address', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MentorDashboard.deliveryaddress')),
            ],
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('message', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('branch', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.branch')),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.company')),
                ('delivery', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='MentorDashboard.mealdelivery')),
            ],
        ),
    ]
