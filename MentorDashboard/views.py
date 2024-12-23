from django.shortcuts import render, redirect, get_object_or_404
from .models import DeliveryAddress, MealDelivery, Notification
from AdminDashboard.models import Meal, Branch, Company, BulkOrders, MealPlan
from .forms import MealDeliveryForm
from django.db.models import Sum, Case, When, IntegerField
import json
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm,DeliveryAddressForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
import datetime
from datetime import time 
from datetime import timedelta
from django.db.models import Sum
from django.utils.timezone import make_aware, now
from django.http import JsonResponse
from datetime import datetime
from django.utils import timezone  # Use Django's timezone-aware utilities

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.contrib.auth.decorators import login_required
from datetime import datetime
import json
from .models import BulkOrders, DeliveryAddress, MealDelivery, Notification  # Ensure to import your models
from datetime import datetime, time, timedelta
from django.utils.timezone import make_aware
from django.db.models import Sum, Case, When, IntegerField
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
import pytz
from django.core.paginator import Paginator
from itertools import chain
from datetime import date
from django.contrib.auth import logout
from django.shortcuts import redirect
# from django.shortcuts import get_list_or_40    

# Define the Indian timezone
india_tz = pytz.timezone('Asia/Kolkata')




from django.contrib.auth.decorators import login_required, user_passes_test

def mentor_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                # Check if user is either a mentor or a staff (non-superuser)
                if user.role in ['MENTOR', 'BRANCH_MANAGER', 'COMPANY_ADMIN'] :
                    login(request, user)
                    return redirect('dashboard')  # Redirect to custom dashboard
                else:
                    messages.error(request, 'You do not have permission to access this area.')
                    return redirect('dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})



def logout_view(request):
    logout(request)  # Log out the user
    return redirect('mentor_login')  # Redirect to the login page or a different page

# Utility function to fetch notifications
@login_required
def get_notifications(request):
    if request.user.role != 'MENTOR':
        branch=Branch.objects.all()
        # company=branch.company
        return Notification.objects.order_by('-created_at').filter(branch__in=branch)[:5]
    else:
        branch = request.branch
        company = request.company
        return Notification.objects.order_by('-created_at').filter(branch=branch)[:5]
    
    # return Notification.objects.order_by('-created_at').filter(branch=branch)[:5]

@login_required
def dashboard_overview(request):
    if request.user.role != 'MENTOR':
        branch=Branch.objects.all()
        # company=branch.company
        now_ist = timezone.now().astimezone(india_tz)
        today = now_ist.date()  
        current_time = now_ist.time()  
        six_pm = time(18, 0)  
        print(today, current_time, six_pm)
        # Start and end of the current week in IST
        start_of_week = make_aware(datetime.combine(today, time.min), india_tz)
        end_of_week = make_aware(datetime.combine(today + timedelta(days=6), time.max), india_tz)

        active_subscriptions = BulkOrders.objects.filter(branch__in=branch).count() or 0
        dispatched = MealDelivery.objects.filter(status='DISPATCHED', branch__in=branch).exclude(status=0).count() or 0
        cooking = MealDelivery.objects.filter(status='COOKING', branch__in=branch).exclude(status=0).count() or 0
        deliveredcount = MealDelivery.objects.filter(status='DELIVERED', branch__in=branch).exclude(status=0).count() or 0
        canceled = MealDelivery.objects.filter(status='CANCELED', branch__in=branch).exclude(status=0).count() or 0
        
        addresses = DeliveryAddress.objects.filter(branch__in=branch)
        delivered = MealDelivery.objects.filter(status='DELIVERED', branch__in=branch).exclude(status=0).count() or 0
        addresses = DeliveryAddress.objects.filter(branch__in=branch)

    # Query all orders within the week, grouped by address and date
        orders = (
        MealDelivery.objects.filter(branch__in=branch, date__range=[start_of_week, end_of_week])
        .values('date','branch', 'delivery_address__name', 'delivery_address__pk')
        .annotate(
            total_breakfast=Sum(Case(When(meal_type='breakfast', then='quantity'), output_field=IntegerField())),   
            total_breakfast2=Sum(Case(When(meal_type='breakfast2', then='quantity'), output_field=IntegerField())),
            total_lunch=Sum(Case(When(meal_type='lunch', then='quantity'), output_field=IntegerField())),
            total_lunch2=Sum(Case(When(meal_type='lunch2', then='quantity'), output_field=IntegerField())),
            total_snack=Sum(Case(When(meal_type='snack', then='quantity'), output_field=IntegerField())),
            total_snack2=Sum(Case(When(meal_type='snack2', then='quantity'), output_field=IntegerField())),
            total_dinner=Sum(Case(When(meal_type='dinner', then='quantity'), output_field=IntegerField())),
            total_dinner2=Sum(Case(When(meal_type='dinner2', then='quantity'), output_field=IntegerField())),
            )
            .order_by('date', 'delivery_address__name')
        )
        branches=request.branch

    else:
        branch = request.branch  
        company = request.company  
    #Get current date and time in Indian timezone
        now_ist = timezone.now().astimezone(india_tz)
        today = now_ist.date()  
        current_time = now_ist.time()  
        six_pm = time(18, 0)  
        print(today, current_time, six_pm)
        # Start and end of the current week in IST
        start_of_week = make_aware(datetime.combine(today, time.min), india_tz)
        end_of_week = make_aware(datetime.combine(today + timedelta(days=6), time.max), india_tz)

        active_subscriptions = BulkOrders.objects.filter(branch=branch).count() or 0
        dispatched = MealDelivery.objects.filter(status='DISPATCHED', branch=branch).exclude(status=0).count() or 0
        cooking = MealDelivery.objects.filter(status='COOKING', branch=branch).exclude(status=0).count() or 0
        deliveredcount = MealDelivery.objects.filter(status='DELIVERED', branch=branch).exclude(status=0).count() or 0
        canceled = MealDelivery.objects.filter(status='CANCELED', branch=branch).exclude(status=0).count() or 0
        
        addresses = DeliveryAddress.objects.filter(branch=branch)
        delivered = MealDelivery.objects.filter(status='DELIVERED', branch=branch).exclude(status=0).count() or 0

        # if branch_id:
        #     notifications = get_notifications(request)
        # else:
        #     notifications = get_notifications(request)  # Fetch notifications

        # #
        # Query all addresses for the given branch and company
        addresses = DeliveryAddress.objects.filter(branch=branch)

        # Query all orders within the week, grouped by address and date
        orders = (
        MealDelivery.objects.filter(branch=branch, date__range=[start_of_week, end_of_week])
        .values('date','branch', 'delivery_address__name', 'delivery_address__pk')
        .annotate(
            total_breakfast=Sum(Case(When(meal_type='breakfast', then='quantity'), output_field=IntegerField())),
            total_breakfast2=Sum(Case(When(meal_type='breakfast2', then='quantity'), output_field=IntegerField())),
            total_lunch=Sum(Case(When(meal_type='lunch', then='quantity'), output_field=IntegerField())),
            total_lunch2=Sum(Case(When(meal_type='lunch2', then='quantity'), output_field=IntegerField())),
            total_snack=Sum(Case(When(meal_type='snack', then='quantity'), output_field=IntegerField())),
            total_snack2=Sum(Case(When(meal_type='snack2', then='quantity'), output_field=IntegerField())),
            total_dinner=Sum(Case(When(meal_type='dinner', then='quantity'), output_field=IntegerField())),
            total_dinner2=Sum(Case(When(meal_type='dinner2', then='quantity'), output_field=IntegerField())),
            )
            .order_by('date', 'delivery_address__name')
        )
        branches=request.branch

    date_format = "%Y-%m-%d"
   
    # Organize orders by address and date
    data_by_address = {}
    for order in orders:
        address = DeliveryAddress.objects.get(pk=order['delivery_address__pk'])
        address_pk = order['delivery_address__pk']
        date_str = str(order['date'])

        if address not in data_by_address:
            data_by_address[address] = {}

        # Determine the order date
        if isinstance(order['date'], str):
            order_date = datetime.strptime(order['date'], date_format).date()
        else:
            order_date = order['date']  # Assuming it's already a datetime.date object

        # Prepare default values for the day
        data_by_address[address][date_str] = {
            'day_name': datetime.strptime(date_str, date_format).strftime("%A"),
            'date': order_date,
            'total_breakfast': order.get('total_breakfast', '-'),
            'total_breakfast2': order.get('total_breakfast2', '-'),
            'total_lunch': order.get('total_lunch', '-'),
            'total_lunch2': order.get('total_lunch2', '-'),
            'total_snack': order.get('total_snack', '-'),
            'total_snack2': order.get('total_snack2', '-'),
            'total_dinner': order.get('total_dinner', '-'),
            'total_dinner2': order.get('total_dinner2', '-'),
            'is_future': "True" if datetime.strptime(date_str, date_format).date() > today or (order_date != today and current_time < six_pm) else "False",
            'address_pk': address,
            'branch': order.get('branch', None),
        }

        print(f'Data by address: {data_by_address}')
    
    # Fill missing dates with default data for all addresses
        for address in addresses:  # Loop through all addresses instead of data_by_address keys
            address_name = address
            address_pk = address.pk
            
            for i in range(7):
                day = today + timedelta(days=i)
                date_str = str(day)

                if date_str not in data_by_address.get(address_name, {}):
                    data_by_address.setdefault(address_name, {})[date_str] = {
                        'day_name': day.strftime("%A"),
                        'date': day,
                        'total_breakfast': '-',
                        'total_breakfast2': '-',
                        'total_lunch': '-',
                        'total_lunch2': '-',
                        'total_snack': '-',
                        'total_snack2': '-',
                        'total_dinner': '-',
                        'total_dinner2': '-',
                        'is_future': "True" if day > today or (day != today and current_time < six_pm) else "False",
                        'address_pk': address_pk,
                        'branch': order.get('branch', None),
                    }
    
    # Sort the addresses by name and dates within each address
    sorted_data = data_by_address

    notifications = get_notifications(request)  # Fetch notifications
    # print(week_days)  # Debug print to verify output

    context = {
        "date": now().strftime("%B %d, %Y"),
        "profile_name": request.user.username if request.user.is_authenticated else "Mentor",
        "active_subscriptions": active_subscriptions,
        "dispatched": dispatched,
        "cooking": cooking,
        "delivered": delivered,
        "deliveredcount": deliveredcount,
        "canceled": canceled,
        "addresses": addresses,
        "notifications": notifications,
        'data_by_address': sorted_data,
        'branches': branches
    }

    return render(request, 'mentor/home.html', context)

@login_required
def delivery_address_list(request, branch_id=None):
    notifications = get_notifications(request)  # Fetch notifications
    if request.user.role != 'MENTOR':
        # Get all branches managed by the Branch Manager
        branches = request.branch

        # Filter by specific branch if branch_id is provided
            # branches = branches.filter(id=branch_id)
        addresses = DeliveryAddress.objects.filter(branch__in=branches)
        return render(request, 'mentor/delivery/list.html', {'branches': branches, 'addresses': addresses, 'notifications': notifications})

    else:
        # Get all branches
        # Filter addresses for the selected branches
        addresses = DeliveryAddress.objects.filter(branch=request.branch)
        return render(request, 'mentor/delivery/list.html', { 'addresses': addresses, 'notifications': notifications})


@login_required
def delivery_address_create(request, branch_id=None):
    form = DeliveryAddressForm()
    branch_id = request.session.get('branch_id')
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications
  # Fetch notifications
    if request.method == 'POST':
        name = request.POST['name']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        city = request.POST['city']
        state = request.POST['state']
        pin_code = request.POST['pin_code']
        # latitude = request.POST['latitude']
        # longitude = request.POST['longitude']
        default_address = request.POST.get('default_address')
        if branch_id:
            branch=Branch.objects.get(id=branch_id)
            company=branch.company
        else:
            branch = request.branch
            company = request.company
        if default_address == "on":
            default_address = True
        else:
            default_address = False
        new=DeliveryAddress.objects.create(name=name, address_line_1=address_line_1, address_line_2=address_line_2, default_address=default_address, city=city, state=state, pin_code=pin_code, branch_id=branch.id, company=company)
        newd=MealDelivery.objects.create(branch=branch, company=company, delivery_address=new,status=0, quantity=0, date=datetime.now().date(),bulk_order=BulkOrders.objects.filter(branch=branch, company=company).first())
        print(f"New address created: {new}")
        print(f"New delivery created: {newd}")
        if request.user.role != "MENTOR":
            return redirect('delivery_address_list_by_branch', branch_id)
        else:
            return redirect('delivery_address_list')

    return render(request, 'mentor/delivery/form.html', {'branch_id': branch_id,'form': form, 'notifications': notifications})

@login_required
def delivery_address_edit(request, id, branch_id=None):
    address = get_object_or_404(DeliveryAddress, id=id)
    branch_id = request.session.get('branch_id')
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications
  # Fetch notifications
    
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST, instance=address)
        
        if form.is_valid():
            # Check if the default_address is set and handle accordingly
            default_address = form.cleaned_data.get('default_address')
            print(default_address)
            if branch_id:
                branch=Branch.objects.get(id=branch_id)
                company=branch.company
            else:
                branch = request.branch
                company = request.company
            if default_address and DeliveryAddress.objects.filter(branch=branch, default_address=True).exclude(id=id).exists():
                messages.error(request, 'A default address already exists in another address.')
            else:
                # Save the form if the default_address condition is met
                # form.instance.latitude = form.cleaned_data.get('latitude') or 0.0
                # form.instance.longitude = form.cleaned_data.get('longitude') or 0.0
                form.save()
                print(f"Address {address} updated successfully.")
                return redirect('delivery_address_list')
        else:
            print(form.errors)
            # If the form is not valid, handle errors accordingly
            messages.error(request, 'Please correct the errors below.')

    else:
        form = DeliveryAddressForm(instance=address)
        
    return render(request, 'mentor/delivery/form.html', {
        'form': form,
        'branch_id': branch_id,
        'object': address,
        'notifications': notifications
    })

@login_required
def delivery_address_delete(request, id, branch_id=None):
    address = get_object_or_404(DeliveryAddress, id=id)
    
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications
    
    if request.method == 'POST':
        address.delete()
        return redirect('delivery_address_list_by_branch' if branch_id else 'delivery_address_list')

    return render(request, 'mentor/delivery/confirm_delete.html', {'address': address, 'notifications': notifications})

@login_required
def meal_delivery_list(request, branch_id=None):
 
        # Filter by specific branch if branch_id is provided
    if branch_id:
            branch = request.branch.filter(id=branch_id)
            deliveries = MealDelivery.objects.filter(branch=branch).all()
    else:
        # Get all branches
        # Filter deliveries for the selected branches
        deliveries = MealDelivery.objects.filter(branch=request.branch).all()
    # deliveries = BulkOrders.objects.filter(branch=request.branch).all()
    
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications
  # Fetch notifications
    return render(request, 'mentor/meal/list.html', {'branch_id': branch_id,'deliveries': deliveries, 'notifications': notifications})

@login_required
def meal_delivered(request, branch_id=None):
    if branch_id:
        deliveries = MealDelivery.objects.filter(branch_id=branch_id).all()
    else:
        deliveries = MealDelivery.objects.filter(branch=request.branch).all()
    
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications
  # Fetch notifications
    return render(request, 'mentor/meal/form.html', {'branch_id': branch_id,'deliveries': deliveries, 'notifications': notifications})

@login_required
def meal_delivery_edit(request, id, branch_id=None):
    delivery = get_object_or_404(MealDelivery, id=id)
    
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications
  # Fetch notifications
    
    if request.method == 'POST':
        form = MealDeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            old_status = delivery.status
            updated_delivery = form.save(commit=False)
            updated_delivery.save()
            if branch_id:
                branch = Branch.objects.get(id=branch_id)
                company = branch.company
            if old_status != updated_delivery.status:
                Notification.objects.create(
                    delivery=updated_delivery.deliver,
                    message=f"Status changed from {old_status} to {updated_delivery.status} for Meal Delivery ID {updated_delivery.id}.",
                    branch=branch,
                    company=company
                )

            return redirect('orders_today_branches')
    else:
        form = MealDeliveryForm(instance=delivery)

    return render(request, 'mentor/meal/edit.html', {'branch_id': branch_id,'form': form, 'delivery': delivery, 'notifications': notifications})

@login_required
def assign_address(request, id, branch_id=None):
    branch_id = request.session.get('branch_id')
    if branch_id:
        branch=Branch.objects.get(id=branch_id)
        company=branch.company
    else:
        branch = request.branch
        company = request.company
    delivery = get_object_or_404(MealDelivery, id=id)
    addresses = DeliveryAddress.objects.filter(branch=branch)
    
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications
    
    if request.method == 'POST':
        address_id = request.POST.get('address')
        delivery.delivery_address = get_object_or_404(DeliveryAddress, id=address_id)
        delivery.save()
        return redirect('meal_delivery_list')
    
    return render(request, 'mentor/meal/assign_address.html', {'branch_id': branch_id,'delivery': delivery, 'addresses': addresses, 'notifications': notifications})


@login_required
def orders_list(request, branch_id=None):
    # Get today's date
     # Get the current date and time in the timezone defined in settings.py
    tz = timezone.get_current_timezone()  # Uses the TIME_ZONE from settings
    today = timezone.localdate()  # Get the server's local date (timezone aware)
    branch_id = request.session.get('branch_id')
    old_date = today - timedelta(days=30)
    if request.user.role != "MENTOR":
        branch=request.branch
        # company=branch.company
        all_deliveries = MealDelivery.objects.filter(branch__in=branch).exclude(status=0,quantity=0)

    else:
        branch = request.branch
        company = request.company
        all_deliveries = MealDelivery.objects.filter(branch=branch,company=company).exclude(status=0,quantity=0)

    
    # Fetch all deliveries for the branch
    # print("All deliveries:", all_deliveries)

    # Fetch past deliveries (within the last 30 days)
    # past_deliveries = MealDelivery.objects.filter(
    #     branch=branch, 
    #     company=company,
    #     date__range=(old_date, today)
    # ).exclude(status=0)
    # # Fetch notifications
    
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications


    # Render the response
    return render(request, 'mentor/order/list.html', {
        # 'past_deliveries': past_deliveries,
        'branch_id': branch_id,
        'notifications': notifications,
        'all_deliveries': all_deliveries
    })

def orders_today(request, branch_id=None):
    tz = timezone.get_current_timezone()  # Uses the TIME_ZONE from settings
    today = timezone.localdate()  # Get the server's local date (timezone aware)
    old_date = today - timedelta(days=30)
    notifications = get_notifications(request)  # Fetch notifications
    print("Today's date:", today)
    print("Old date:", old_date)
    if request.user.role != "MENTOR":
        branch=request.branch
        # company=branch.company
        todays_deliveries = MealDelivery.objects.filter(branch__in=branch, date=today).exclude(status=0,quantity=0)
        branches=request.branch
        return render(request, 'mentor/order/today.html', {'branches': branches,'branch_id': branch_id,'todays_deliveries': todays_deliveries, 'notifications': notifications})

    else:
        branch = request.branch
        company = request.company
        todays_deliveries = MealDelivery.objects.filter(branch=branch, date=today).exclude(status=0,quantity=0)
        return render(request, 'mentor/order/today.html', {'branch_id': branch_id,'todays_deliveries': todays_deliveries, 'notifications': notifications})



    # Fetch today's deliveries for the branch
    # print("Today's deliveries:", todays_deliveries)


@login_required
def assign_meal(request, date, branch_id=None):
    # Get the first order
    
    if branch_id:
        branch=Branch.objects.get(id=branch_id)
        company=branch.company
    else:
        branch = request.branch
        company = request.company
    
    order = BulkOrders.objects.filter(branch=branch,company=company).first()
    if order:
        # Calculate total for meals
        total_sum = (order.breakfast or 0) + (order.lunch or 0) + (order.snack or 0) + (order.dinner or 0) + (order.dinner2 or 0)
    else:
        total_sum = 0

    addresses = DeliveryAddress.objects.filter(branch=branch,company=company)
    
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications
  # Fetch notifications

    # Parse the date to get the day of the week
    try:
        date_obj = make_aware(datetime.strptime(date, '%Y-%m-%d'))
        day_name = date_obj.strftime('%A').lower()  # e.g., 'monday'
    except ValueError:
        return render(request, 'your_template.html', {'error': 'Invalid date format'})
    print(day_name)
    # Get all MealPlans related to the order
    meal_plans = order.MealPlan.all() if order else []
    
    # Meal types for iteration (e.g., breakfast, lunch, etc.)
    meals = ['breakfast', 'lunch', 'snack', 'dinner', 'dinner2']

    # Prepare a dictionary to store dishes for the selected day
    dishes_for_day = {}

    # Loop through each meal type and get the related dishes for the specific day
    for meal in meals:
        if meal == 'dinner2':
            field_name = f"{day_name}_dinner_dish_option"  # e.g., 'monday_dinner_dish_option'
        else:
            field_name = f"{day_name}_{meal}_dish"  # e.g., 'monday_breakfast_dish'

        # Get dishes for the current meal type and day
        dishes_for_day[meal] = [
            dish for meal_plan in meal_plans for dish in getattr(meal_plan, field_name).all()
        ]
    print(dishes_for_day)
    # Prepare data for rendering
    day_meals = {}
    meal_types = ['breakfast', 'lunch', 'snack', 'dinner', 'dinner2']

    for meal_plan in meal_plans:
        for meal_type in meal_types:
            # Dynamically generate the attribute name
            if meal_type == 'dinner2':
                dish_attr = f"{day_name}_dinner_dish_option"
            else:
                dish_attr = f"{day_name}_{meal_type}_dish"

            dishes = getattr(meal_plan, dish_attr).all()  # Fetch the dishes
            
            # Store dishes under the appropriate meal type
            if meal_type not in day_meals:
                day_meals[meal_type] = dishes
            else:
                # Append dishes if there are multiple meal plans
                day_meals[meal_type] |= dishes  # Merge QuerySets
            print(day_meals)
    # Handle POST request for meal assignments
   
    # Render the template with context data
    return render(request, 'mentor/meal/assign.html', {
        'order': order,
        'branch_id': branch_id,
        'addresses': addresses,
        'notifications': notifications,
        'total_sum': total_sum,
        'dishes_for_day': dishes_for_day,
        'day_name': day_name.capitalize(),
        'day_meals': day_meals, 
        'meals': meals,
        'date': date
    })

@login_required
def edit_assign_meal(request,id, date, branch_id=None):
    # Fetch the bulk order for the current branch
    # branch_id = request.session.get('branch_id')
    if branch_id:
        branch=Branch.objects.get(id=branch_id)
        company=branch.company
    else:
        branch = request.branch
        company = request.company
    print(branch)
    address = DeliveryAddress.objects.filter(pk=id).first()
    print(address)
    notifications = get_notifications(request)  # Fetch notifications

    delivery=MealDelivery.objects.filter(delivery_address=id,date=date)
    print(delivery)
    print(f'address: {address.name}')
    
    meal_quantities = {
        'breakfast': 0,
        'breakfast2': 0,
        'lunch': 0,
        'lunch2': 0,
        'snack': 0,
        'snack2': 0,
        'dinner': 0,
        'dinner2': 0
        
    }

    # Aggregate quantities based on meal type
    for meal in delivery:
        meal_type_lower = meal.meal_type.lower()  # Convert to lowercase
        if meal_type_lower in meal_quantities:  # Ensure meal_type exists in our dictionary
            meal_quantities[meal_type_lower] = meal_quantities.get(meal_type_lower, 0) + (meal.quantity if meal.quantity else 0)
            print(meal_quantities)
        print(f'Address: {address.name}')
        print(f'Meal Quantities: {meal_quantities}')
        
    # Fetch the bulk order for the current branch
    order = get_object_or_404(BulkOrders, branch=request.branch)
    addresses = DeliveryAddress.objects.filter(branch=request.branch, company=request.company)
    
    notifications = get_notifications(request)  # Fetch notifications

    return render(request, 'mentor/meal/edit_assign.html', {
        'order': order,
        'addresses': addresses,
        'notifications': notifications,
        'selected_date': date,
        'address':address, 
         'meal_quantities': meal_quantities,
        'date': date,
        'branch_id': branch
    })
@login_required
def meal_plan_list(request, branch_id=None):
    branch_id = request.session.get('branch_id')
    if request.user.role != "MENTOR":
        branch = request.branch
        # company = request.company
        orders = BulkOrders.objects.filter(branch__in=branch)  # Optimize with prefetch
    else:
        branch = request.branch
        company = request.company
        orders = BulkOrders.objects.filter(branch=branch, company=company)  # Optimize with prefetch
    
    # Get notifications
    notifications = get_notifications(request)
    
    # Create a list of order data with status
    orders_data = []
    for order in orders:
        status = 1 if order.bulk_order_end_date > now().date() else 0
        mealplans = list(order.MealPlan.all())  # Extract all meal plans in a list
        # print(mealplans)
        # Append order details and status as a dictionary
        orders_data.append({
            'order': order,
            'status': status,
            'mealplans': mealplans,
        })
    # for mealplan in orders_data:
        # for plan in order['order']:
        # print(mealplan.order)
    return render(request, 'mentor/mealplan/list.html', {
        'notifications': notifications,
        'branch_id': branch_id,
        'orders_data': orders_data,
    })
@login_required
def meal_plan_detail(request, id, branch_id=None):
    # branch_id = request.session.get('branch_id')
    if branch_id:
        branch=Branch.objects.get(id=branch_id) if branch_id else request.branch
        company=request.company
    else:
        branch = request.branch
        company = request.company
    
    
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications
  # Fetch notifications
    print(branch_id)
    mealplan = get_object_or_404(MealPlan, pk=id)
    # print(mealplan)
    order = BulkOrders.objects.filter(MealPlan=mealplan, branch=branch).first()
    print(order)
    status = 1 if order.bulk_order_end_date > now().date() else 0
    sum = order.breakfast + order.lunch + order.snack + order.dinner
    days = [ 'sunday','monday', 'tuesday', 'wednesday', 'thursday', 
            'friday', 'saturday']
    print(sum)
    # print(order)
    # for day in days :
    #     print(day)
    #     for dish in mealplan.monday_breakfast_dish.all():
    #         print(status)
    
    return render(request, 'mentor/mealplan/detail.html', {
        'notifications': notifications,
        'mealplan': mealplan,
        'branch': branch,
        'days': days,
        'order': order,
        'sum': sum,
        'status': status,
    })

@login_required
def meal_ordered(request, branch_id=None):
    if branch_id:
        branch=Branch.objects.get(id=branch_id)
        company=branch.company
    else:
        branch = request.branch
        company = request.company
    
    
    if branch_id:
        notifications = get_notifications(request)
    else:
        notifications = get_notifications(request)  # Fetch notifications
   

    # Get current date and time in Indian timezone
    now_ist = timezone.now().astimezone(india_tz)
    today = now_ist.date()  
    current_time = now_ist.time()  
    six_pm = time(18, 0)  
    print(today, current_time, six_pm)
    # Start and end of the current week in IST
    start_of_week = make_aware(datetime.combine(today, time.min), india_tz)
    end_of_week = make_aware(datetime.combine(today + timedelta(days=6), time.max), india_tz)
    print(branch)
    # Query all addresses for the given branch and company
    if request.user.role == 'MENTOR':
        addresses = DeliveryAddress.objects.filter(branch=branch, company=company)
        branches=request.branch
        company=request.company
    # Query all orders within the week, grouped by address and date
        orders = (
            MealDelivery.objects.filter(branch=branch, date__range=[start_of_week, end_of_week])
            .values('date','branch', 'delivery_address__name', 'delivery_address__pk')
            .annotate(
                total_breakfast=Sum(Case(When(meal_type='breakfast', then='quantity'), output_field=IntegerField())),
                total_breakfast2=Sum(Case(When(meal_type='breakfast2', then='quantity'), output_field=IntegerField())),
                total_lunch=Sum(Case(When(meal_type='lunch', then='quantity'), output_field=IntegerField())),
                total_lunch2=Sum(Case(When(meal_type='lunch2', then='quantity'), output_field=IntegerField())),
                total_snack=Sum(Case(When(meal_type='snack', then='quantity'), output_field=IntegerField())),
                total_snack2=Sum(Case(When(meal_type='snack2', then='quantity'), output_field=IntegerField())),
                total_dinner=Sum(Case(When(meal_type='dinner', then='quantity'), output_field=IntegerField())),
                total_dinner2=Sum(Case(When(meal_type='dinner2', then='quantity'), output_field=IntegerField())),
            )
            .order_by('date', 'delivery_address__name')
        )
    else:
        addresses = DeliveryAddress.objects.filter(branch__in=branch, company=company)
        # Query all orders within the week, grouped by address and date
        orders = (
            MealDelivery.objects.filter(branch__in=branch, date__range=[start_of_week, end_of_week])
            .values('date','branch', 'delivery_address__name', 'delivery_address__pk')
            .annotate(
                total_breakfast=Sum(Case(When(meal_type='breakfast', then='quantity'), output_field=IntegerField())),
                total_breakfast2=Sum(Case(When(meal_type='breakfast2', then='quantity'), output_field=IntegerField())),
                total_lunch=Sum(Case(When(meal_type='lunch', then='quantity'), output_field=IntegerField())),
                total_lunch2=Sum(Case(When(meal_type='lunch2', then='quantity'), output_field=IntegerField())),
                total_snack=Sum(Case(When(meal_type='snack', then='quantity'), output_field=IntegerField())),
                total_snack2=Sum(Case(When(meal_type='snack2', then='quantity'), output_field=IntegerField())),
                total_dinner=Sum(Case(When(meal_type='dinner', then='quantity'), output_field=IntegerField())),
                )
            .order_by('date', 'delivery_address__name')
        )
        branches=request.branch

    date_format = "%Y-%m-%d"
   
    # Organize orders by address and date
    data_by_address = {}
    for order in orders:
        address = DeliveryAddress.objects.get(pk=order['delivery_address__pk'])
        address_pk = order['delivery_address__pk']
        date_str = str(order['date'])

        if address not in data_by_address:
            data_by_address[address] = {}

        # Determine the order date
        if isinstance(order['date'], str):
            order_date = datetime.strptime(order['date'], date_format).date()
        else:
            order_date = order['date']  # Assuming it's already a datetime.date object

        # Prepare default values for the day
        data_by_address[address][date_str] = {
            'day_name': datetime.strptime(date_str, date_format).strftime("%A"),
            'date': order_date,
            'total_breakfast': order.get('total_breakfast', '-'),
            'total_breakfast2': order.get('total_breakfast2', '-'),
            'total_lunch': order.get('total_lunch', '-'),
            'total_lunch2': order.get('total_lunch2', '-'),
            'total_snack': order.get('total_snack', '-'),
            'total_snack2': order.get('total_snack2', '-'),
            'total_dinner': order.get('total_dinner', '-'),
            'total_dinner2': order.get('total_dinner2', '-'),
            'is_future': "True" if datetime.strptime(date_str, date_format).date() > today or (order_date != today and current_time < six_pm) else "False",
            'address_pk': address,
            'branch': order.get('branch', None),
        }

        print(f'Data by address: {data_by_address}')
        
        # Fill missing dates with default data for all addresses
        for address in addresses:  # Loop through all addresses instead of data_by_address keys
            address_name = address
            address_pk = address.pk
            
            for i in range(7):
                day = today + timedelta(days=i)
                date_str = str(day)

                if date_str not in data_by_address.get(address_name, {}):
                    data_by_address.setdefault(address_name, {})[date_str] = {
                        'day_name': day.strftime("%A"),
                        'date': day,
                        'total_breakfast': '-',
                        'total_breakfast2': '-',
                        'total_lunch': '-',
                        'total_lunch2': '-',
                        'total_snack': '-',
                        'total_snack2': '-',
                        'total_dinner': '-',
                        'total_dinner2': '-',
                        'is_future': "True" if day > today or (day != today and current_time < six_pm) else "False",
                        'address_pk': address_pk,
                        'branch': order.get('branch', None),
                    }
        
    # Sort the addresses by name and dates within each address
    sorted_data = data_by_address

    # Render the template
    return render(request, 'mentor/meal/meals.html', {
        'notifications': notifications,
        'data_by_address': sorted_data,
        'branch_id': branch_id,
        'branches': branches,
    })

@login_required
def assign_meal_post(request, branch_id=None):
    order = BulkOrders.objects.first()
        
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            meal_assignments = data.get('mealData', [])
            meal_data = [item for item in meal_assignments if 'meal_plan' in item]
            print("in post", meal_data)
            for assignment in meal_data:
                print("in for loop")
                meal_type = assignment.get('meal_plan')
                address_id = assignment.get('address')
                date = assignment.get('date')
                quantity = int(assignment.get('quantity', 0))
                branch_id = assignment.get('branch')
                print(meal_type, address_id, date, quantity)
                branch=Branch.objects.get(id=branch_id)
                company=branch.company
    
                delivery_address = get_object_or_404(DeliveryAddress, pk=address_id)
                if quantity == 0:
                    print("Skipping quantity 0")
                    continue
                
                # Check for existing MealDelivery entry
                existing_delivery = MealDelivery.objects.filter(
                    bulk_order=order,
                    meal_type=meal_type,
                    date=date,
                    delivery_address=delivery_address,
                    branch=branch,
                    company=company
                ).first()

                if existing_delivery:
                    # Update the quantity if it exists
                    existing_delivery.quantity = quantity
                    existing_delivery.save()
                    message = f"{quantity} {meal_type} updated for {delivery_address} by {branch}"
                    print("Updated", existing_delivery)
                else:
                    # Save a new meal assignment
                    deliver = MealDelivery.objects.create(
                        bulk_order=order,
                        meal_type=meal_type,
                        quantity=quantity,
                        date=date,
                        delivery_address=delivery_address,
                        branch=branch,
                        company=company
                    )
                    message = f"{quantity} {meal_type} assigned to {delivery_address} by {branch}"
                    print("Saved", deliver)

                # Create a notification for the action
                Notification.objects.create(
                    delivery=deliver if not existing_delivery else existing_delivery,
                    message=message,
                    branch=branch,
                    company=company
                )
                print(message)

            print("Meal assignments processed successfully.")
            return JsonResponse({'success': True, 'message': 'Meal assigned successfully.', 'debug': 'All meal assignments were processed without errors.'})
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {str(e)}")
            return JsonResponse({'success': False, 'error': f'JSON decode error: {str(e)}'}, status=400)
        except Exception as e:
            print(f"Unexpected error: {str(e)}")
            return JsonResponse({'success': False, 'error': str(e)}, status=500)






################################ BRANCH MANAGER AND COMPANY ADMIN ####################################

def meal_plan_branches(request):
    branches=request.branch
    company=request.company
    return render(request, 'branches/meal_plan_branches.html', {'branches': branches, 'company': company})
def delivery_address_branches(request): 
    branches=request.branch
    company=request.company
    return render(request, 'branches/delivery_address_branches.html', {'branches': branches, 'company': company})
def meal_delivery_branches(request): 
    branches=request.branch 
    company=request.company
    return render(request, 'branches/meal_delivery_branches.html', {'branches': branches, 'company': company})
def meal_ordered_branches(request):
    branches=request.branch 
    company=request.company
    return render(request, 'branches/meal_ordered_branches.html', {'branches': branches, 'company': company})
def orders_today_branches(request):
    branches=request.branch
    company=request.company
    return render(request, 'branches/orders_today_branches.html', {'branches': branches, 'company': company})
def orders_branches(request):
    branches=request.branch
    company=request.company
    return render(request, 'branches/orders_branches.html', {'branches': branches, 'company': company})



def set_branch_session(request, branch_id):
    if request.method == "POST":
        request.session['branch_id'] = branch_id
        print(branch_id)
        return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'Invalid request method'}, status=400)