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




def mentor_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                if user.role == 'MENTOR':
                    login(request, user)
                    return redirect('dashboard')  # Redirect to mentor dashboard
                else:
                    messages.error(request, 'You do not have permission to access this area.')
            else:
                messages.error(request, 'Invalid username or password.')
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

from django.contrib.auth import logout
from django.shortcuts import redirect

def logout_view(request):
    logout(request)  # Log out the user
    return redirect('mentor_login')  # Redirect to the login page or a different page

# Utility function to fetch notifications
@login_required
def get_notifications(request):
    return Notification.objects.order_by('-created_at').filter(branch=request.branch)[:5]

@login_required
def dashboard_overview(request):
    branch = request.branch  
    company = request.company  
    today = now().date()  
    current_time = now().time()  
    six_pm = time(18, 0)  

    # Start and end of the current week
    start_of_week = make_aware(datetime.combine(today, time.min))
    end_of_week = make_aware(datetime.combine(today + timedelta(days=6), time.max))

    active_subscriptions = BulkOrders.objects.filter(branch=request.branch)
    dispatched = MealDelivery.objects.filter(status='DISPATCHED', branch=request.branch).count() or 0
    cooking = MealDelivery.objects.filter(status='COOKING', branch=request.branch).count() or 0
    deliveredcount = MealDelivery.objects.filter(status='DELIVERED', branch=request.branch).count() or 0
    canceled = MealDelivery.objects.filter(status='CANCELED', branch=request.branch).count() or 0
    
    addresses = DeliveryAddress.objects.filter(branch=request.branch)
    delivered = MealDelivery.objects.filter(status='DELIVERED', branch=request.branch).count() or 0

    notifications = get_notifications(request)  # Fetch notifications

    # Query all orders within the week, grouped by address and date
    orders = (
        MealDelivery.objects.filter(branch=branch, date__range=[start_of_week, end_of_week])
        .values('date', 'delivery_address__name','delivery_address__pk')
        .annotate(
            total_breakfast=Sum(Case(When(meal_type='breakfast', then='quantity'), output_field=IntegerField())),
            total_lunch=Sum(Case(When(meal_type='lunch', then='quantity'), output_field=IntegerField())),
            total_snack=Sum(Case(When(meal_type='snack', then='quantity'), output_field=IntegerField())),
            total_dinner=Sum(Case(When(meal_type='dinner', then='quantity'), output_field=IntegerField())),
            total_dinner2=Sum(Case(When(meal_type='dinner2', then='quantity'), output_field=IntegerField())),
        )
        .order_by('date', 'delivery_address__name')
    )
    date_format = "%Y-%m-%d"
    
    # Organize orders by address and date
    data_by_address = {}
    for order in orders:
        # if isinstance(order['date'], str):
        #     order['date'] = datetime.strptime(order['date'], date_format)
        address = order['delivery_address__name']
        address_pk = order['delivery_address__pk']
        date_str = str(order['date'])

        if address not in data_by_address:
            data_by_address[address] = {}
        # today1 = datetime.combine(datetime.today().date(), datetime.min.time())  # Adjust if you need a specific time

        # Prepare default values for the day
        data_by_address[address][date_str] = {
            'day_name': datetime.strptime(date_str, date_format).strftime("%A"),
            'date': order['date'],
            'total_breakfast': order.get('total_breakfast', 0),
            'total_lunch': order.get('total_lunch', 0),
            'total_snack': order.get('total_snack', 0),
            'total_dinner': order.get('total_dinner', 0),
            'total_dinner2': order.get('total_dinner2', 0),
            'is_future':"True" if datetime.strptime(date_str, date_format).date() > today or (order['date'] != today and current_time < six_pm) else "False",
            # 'pk':order['pk'],
            'address_pk':address_pk,
        }
    # order['is_future'] = (
    #         "Yes" if day > today or (day != today and current_time < six_pm) else "No"
    #     )
    print(f'Data by address: {data_by_address}')
    # Fill missing dates with default data
    for address in data_by_address:
        for i in range(7):
            day = today + timedelta(days=i)
            date_str = str(day)
            if date_str not in data_by_address[address]:
                data_by_address[address][date_str] = {
                    'day_name': day.strftime("%A"),
                    'date': day,
                    'total_breakfast': 0,
                    'total_lunch': 0,
                    'total_snack': 0,
                    'total_dinner': 0,
                    'total_dinner2': 0,
                    'address_pk':DeliveryAddress.objects.get(name=address,branch=request.branch).pk,
                }
                

    # Sort the addresses by name and dates within each address
    sorted_data = {addr: dict(sorted(data.items())) for addr, data in sorted(data_by_address.items())}

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
    }

    return render(request, 'mentor/home.html', context)

@login_required
def delivery_address_list(request):
    addresses = DeliveryAddress.objects.filter(branch=request.branch)
    notifications = get_notifications(request)  # Fetch notifications
    return render(request, 'mentor/delivery/list.html', {'addresses': addresses, 'notifications': notifications})

@login_required
def delivery_address_create(request):
    form = DeliveryAddressForm()
    notifications = get_notifications(request)  # Fetch notifications
    if request.method == 'POST':
        name = request.POST['name']
        address_line_1 = request.POST['address_line_1']
        address_line_2 = request.POST['address_line_2']
        city = request.POST['city']
        state = request.POST['state']
        pin_code = request.POST['pin_code']
        latitude = request.POST['latitude']
        longitude = request.POST['longitude']
        default_address = request.POST.get('default_address')
    
        branch = request.branch
        company = request.company
        if default_address == "on":
            default_address = True
        else:
            default_address = False
        DeliveryAddress.objects.create(name=name, address_line_1=address_line_1, address_line_2=address_line_2, default_address=default_address, city=city, state=state, pin_code=pin_code, latitude=latitude, longitude=longitude, branch_id=branch.id, company=company)
        return redirect('delivery_address_list')

    return render(request, 'mentor/delivery/form.html', {'form': form, 'notifications': notifications})

@login_required
def delivery_address_edit(request, id):
    address = get_object_or_404(DeliveryAddress, id=id)
    notifications = get_notifications(request)  # Fetch notifications
    
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST, instance=address)
        
        if form.is_valid():
            # Check if the default_address is set and handle accordingly
            default_address = form.cleaned_data.get('default_address')
            print(default_address)
            if default_address and DeliveryAddress.objects.filter(branch=request.branch, default_address=True).exclude(id=id).exists():
                messages.error(request, 'A default address already exists in another address.')
            else:
                # Save the form if the default_address condition is met
                form.save()
                return redirect('delivery_address_list')
        else:
            # If the form is not valid, handle errors accordingly
            messages.error(request, 'Please correct the errors below.')

    else:
        form = DeliveryAddressForm(instance=address)
        
    return render(request, 'mentor/delivery/form.html', {
        'form': form,
        'object': address,
        'notifications': notifications
    })

@login_required
def delivery_address_delete(request, id):
    address = get_object_or_404(DeliveryAddress, id=id)
    notifications = get_notifications(request)  # Fetch notifications
    
    if request.method == 'POST':
        address.delete()
        return redirect('delivery_address_list')

    return render(request, 'mentor/delivery/confirm_delete.html', {'address': address, 'notifications': notifications})

@login_required
def meal_delivery_list(request):
    deliveries = BulkOrders.objects.filter(branch=request.branch).all()
    notifications = get_notifications(request)  # Fetch notifications
    return render(request, 'mentor/meal/list.html', {'deliveries': deliveries, 'notifications': notifications})

@login_required
def meal_delivered(request):
    deliveries = MealDelivery.objects.filter(branch=request.branch).all()
    notifications = get_notifications(request)  # Fetch notifications
    return render(request, 'mentor/meal/form.html', {'deliveries': deliveries, 'notifications': notifications})

@login_required
def meal_delivery_edit(request, id):
    delivery = get_object_or_404(MealDelivery, id=id)
    notifications = get_notifications(request)  # Fetch notifications
    
    if request.method == 'POST':
        form = MealDeliveryForm(request.POST, instance=delivery)
        if form.is_valid():
            old_status = delivery.status
            updated_delivery = form.save(commit=False)
            updated_delivery.save()

            if old_status != updated_delivery.status:
                Notification.objects.create(
                    delivery=updated_delivery.deliver,
                    message=f"Status changed from {old_status} to {updated_delivery.status} for Meal Delivery ID {updated_delivery.id}.",
                    branch=request.branch,
                    company=request.company
                )

            return redirect('orders_list')
    else:
        form = MealDeliveryForm(instance=delivery)

    return render(request, 'mentor/meal/edit.html', {'form': form, 'delivery': delivery, 'notifications': notifications})

@login_required
def assign_address(request, id):
    delivery = get_object_or_404(MealDelivery, id=id)
    addresses = DeliveryAddress.objects.filter(branch=request.branch)
    notifications = get_notifications(request)  # Fetch notifications
    
    if request.method == 'POST':
        address_id = request.POST.get('address')
        delivery.delivery_address = get_object_or_404(DeliveryAddress, id=address_id)
        delivery.save()
        return redirect('meal_delivery_list')
    
    return render(request, 'mentor/meal/assign_address.html', {'delivery': delivery, 'addresses': addresses, 'notifications': notifications})

from django.core.paginator import Paginator
from itertools import chain
from datetime import date
@login_required
def orders_list(request):
    # Get today's date
     # Get the current date and time in the timezone defined in settings.py
    tz = timezone.get_current_timezone()  # Uses the TIME_ZONE from settings
    today = timezone.localdate()  # Get the server's local date (timezone aware)
    old_date = today - timedelta(days=30)

    print("Today's date:", today)
    print("Old date:", old_date)

    # Fetch today's deliveries for the branch
    todays_deliveries = MealDelivery.objects.filter(branch=request.branch, date=today)
    print("Today's deliveries:", todays_deliveries)

    # Fetch all deliveries for the branch
    all_deliveries = MealDelivery.objects.filter(branch=request.branch)
    print("All deliveries:", all_deliveries)

    # Fetch past deliveries (within the last 30 days)
    past_deliveries = MealDelivery.objects.filter(
        branch=request.branch, 
        date__range=(old_date, today)
    )
    print("Past deliveries:", past_deliveries)

    # Combine today's and past deliveries
    deliveries = list(chain(todays_deliveries, past_deliveries))

    # Paginate the combined deliveries
    paginator = Paginator(deliveries, 10)  # Show 10 deliveries per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Fetch notifications
    notifications = get_notifications(request)

    # Render the response
    return render(request, 'mentor/order/list.html', {
        'deliveries': page_obj,
        'todays_deliveries': todays_deliveries,
        'past_deliveries': past_deliveries,
        'notifications': notifications,
        'paginator': paginator,
        'page_obj': page_obj,
        'all_deliveries': all_deliveries
    })



@login_required
def assign_meal(request, date):
    # Get the first order
    order = BulkOrders.objects.filter(branch=request.branch,company=request.company).first()
    if order:
        # Calculate total for meals
        total_sum = (order.breakfast or 0) + (order.lunch or 0) + (order.snack or 0) + (order.dinner or 0) + (order.dinner2 or 0)
    else:
        total_sum = 0

    addresses = DeliveryAddress.objects.filter(branch=request.branch,company=request.company)
    notifications = get_notifications(request)  # Fetch notifications

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
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            meal_assignments = data.get('mealData', [])
            print
            for assignment in meal_assignments:
                meal_type = assignment.get('meal_plan')
                address_id = assignment.get('address')
                delivery_date = assignment.get('date')
                quantity = int(assignment.get('quantity', 0))
                
                delivery_address = get_object_or_404(DeliveryAddress, pk=address_id)

                # Save the meal assignment
                deliver = MealDelivery.objects.create(
                    bulk_order=order,
                    meal_type=meal_type,
                    quantity=quantity,
                    date=delivery_date,
                    delivery_address=delivery_address,
                    branch=request.branch,
                    company=request.company
                )
                message = f"{quantity} {meal_type} assigned to {delivery_address} by {request.branch}"
                Notification.objects.create(
                    delivery=deliver,
                    message=message,
                    branch=request.branch,
                    company=request.company
                )

            return JsonResponse({'success': True, 'message': 'Meal assigned successfully.'})
        except json.JSONDecodeError as e:
            return JsonResponse({'success': False, 'error': f'JSON decode error: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    # Render the template with context data
    return render(request, 'mentor/meal/assign.html', {
        'order': order,
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
def edit_assign_meal(request,id, date):
    # Fetch the bulk order for the current branch
    address = DeliveryAddress.objects.filter(branch=request.branch, company=request.company,pk=id).first()
    notifications = get_notifications(request)
    delivery=MealDelivery.objects.filter(delivery_address=id,date=date)
    print(delivery)
    print(f'address: {address.name}')
    
    meal_quantities = {
        'breakfast': 0,
        'lunch': 0,
        'snack': 0,
        'dinner': 0,
        
    }

    # Aggregate quantities based on meal type
    for meal in delivery:
        meal_type_lower = meal.meal_type.lower()  # Convert to lowercase
        if meal_type_lower in meal_quantities:  # Ensure meal_type exists in our dictionary
            meal_quantities[meal_type_lower] = meal_quantities.get(meal_type_lower, 0) + (meal.quantity if meal.quantity else 0)

    print(f'Address: {address.name}')
    print(f'Meal Quantities: {meal_quantities}')
    return render(request, 'mentor/meal/edit_assign.html', {
        'address': address,
        'meal_quantities': meal_quantities, 
        'notifications': notifications,
        'date': date
   })


    # Fetch the bulk order for the current branch
    order = get_object_or_404(BulkOrders, branch=request.branch)
    addresses = DeliveryAddress.objects.filter(branch=request.branch, company=request.company)
    notifications = get_notifications(request)
    date = make_aware(datetime.now().date().isoformat())
    # Parse the date to get the day of the week
    try:
        date_obj = make_aware(datetime.strptime(date, '%Y-%m-%d'))
        day_name = date_obj.strftime('%A').lower()  # e.g., 'monday'
    except ValueError:
        return render(request, 'your_template.html', {'error': 'Invalid date format'})

    # Get all MealPlans related to the order
    meal_plans = order.MealPlan.all()
    
    # Prepare a dictionary to store dishes for the selected day
    dishes_for_day = {}
    
    # Meal types for iteration (e.g., breakfast, lunch, etc.)
    meals = ['breakfast', 'lunch', 'snack', 'dinner', 'dinner2']
    
    # Loop through each meal type and get the related dishes for the specific day
    for meal in meals:
        if meal == 'dinner2':
            field_name = f"{day_name}_dinner_meal_option"
            meal_field = f"{day_name}_dinner_meal_option"  # Optional meal field for dinner2
        else:
            field_name = f"{day_name}_{meal}_meal"
            meal_field = f"{day_name}_{meal}_meal"  # Optional meal field for other meals

        # Get dishes for the current meal type and day
        dishes = []
        for meal_plan in meal_plans:
            selected_meals = getattr(meal_plan, meal_field).all()
            for meal in selected_meals:
                dishes += list(meal.selected_dishes.all())

        dishes_for_day[meal] = list(set(dishes))  # Remove duplicates

    # Prepare data for rendering
    day_meals = {}
    
    for meal_plan in meal_plans:
        for meal_type in meals:
            if meal_type == 'dinner2':
                dish_attr = f"{day_name}_dinner_meal_option"
            else:
                dish_attr = f"{day_name}_{meal_type}_meal"

            dishes = getattr(meal_plan, dish_attr).all()
            
            if meal_type not in day_meals:
                day_meals[meal_type] = dishes
            else:
                day_meals[meal_type] |= dishes

    # Prepare meal delivery data
    meal_delivery_data = {}
    for address in addresses:
        meal_delivery_data[address] = {}
        for meal_type in meals:
            # Fetch the quantity for this address, meal type, and date
            meal_delivery = MealDelivery.objects.filter(
                delivery_address=address,
                date=date,
                meal_type=meal_type,
                branch=request.branch,
                company=request.company,
                bulk_order=order
            ).first()
            meal_delivery_data[address][meal_type] = meal_delivery.quantity if meal_delivery else 0
    print(meal_delivery_data)

    return render(request, 'mentor/meal/edit_assign1.html', {
        'order': order,
        'addresses': addresses,
        'notifications': notifications,
        'selected_date': date,
        'dishes_for_day': dishes_for_day,
        'day_name': day_name.capitalize(),
        'day_meals': day_meals, 
        'meals': meals,
        'date': date,
        'dinner': sum((order.dinner or 0, order.dinner2 or 0)),
        'selected_dishes': dishes_for_day,
        'total_sum': sum((order.breakfast or 0, order.lunch or 0, order.snack or 0, order.dinner or 0, order.dinner2 or 0)),
        'meal_delivery_data': meal_delivery_data  # Pass the meal delivery data to the template
    })
@login_required
def meal_plan_list(request):
    notifications = get_notifications(request)  # Fetch notifications
    orders = BulkOrders.objects.filter(branch=request.branch) # Optimize with prefetch
    mealplans = [mealplan for order in orders for mealplan in order.MealPlan.all()]  # Extract all meal plans
     # Check the status of each order's `bulk_order_end_date`
    for order in orders:
        print(order.bulk_order_end_date)  # Access individual order attributes
        status = 1 if order.bulk_order_end_date > now().date() else 0
        end= order.bulk_order_end_date
        start= order.bulk_order_start_date
        print(f"Order {order.bulk_order_name} status: {status}")
    return render(request, 'mentor/mealplan/list.html', {
        'notifications': notifications,
        'mealplans': mealplans,
        'orders': orders,
        'status': status,
        'start': start,
        'end': end
    })
@login_required
def meal_plan_detail(request, id):
    notifications = get_notifications(request)  # Fetch notifications
    mealplan = get_object_or_404(MealPlan, pk=id)
    order= get_object_or_404(BulkOrders, MealPlan=mealplan, branch=request.branch)
    status = 1 if order.bulk_order_end_date > now().date() else 0
    sum = order.breakfast + order.lunch + order.snack + order.dinner
    days = [ 'sunday','monday', 'tuesday', 'wednesday', 'thursday', 
            'friday', 'saturday']
    
    # print(order)
    # for day in days :
    #     print(day)
    #     for dish in mealplan.monday_breakfast_dish.all():
    #         print(status)
    
    return render(request, 'mentor/mealplan/detail.html', {
        'notifications': notifications,
        'mealplan': mealplan,
        'days': days,
        'order': order,
        'sum': sum,
        'status': status,
    })

@login_required
def meal_ordered(request):
    notifications = get_notifications(request)  
    branch = request.branch  
    company = request.company  
    today = now().date()  
    current_time = now().time()  
    six_pm = time(18, 0)  

    # Start and end of the current week
    start_of_week = make_aware(datetime.combine(today, time.min))
    end_of_week = make_aware(datetime.combine(today + timedelta(days=6), time.max))

    # Query all orders within the week, grouped by address and date
    orders = (
        MealDelivery.objects.filter(branch=branch, date__range=[start_of_week, end_of_week])
        .values('date', 'delivery_address__name','delivery_address__pk')
        .annotate(
            total_breakfast=Sum(Case(When(meal_type='breakfast', then='quantity'), output_field=IntegerField())),
            total_lunch=Sum(Case(When(meal_type='lunch', then='quantity'), output_field=IntegerField())),
            total_snack=Sum(Case(When(meal_type='snack', then='quantity'), output_field=IntegerField())),
            total_dinner=Sum(Case(When(meal_type='dinner', then='quantity'), output_field=IntegerField())),
            total_dinner2=Sum(Case(When(meal_type='dinner2', then='quantity'), output_field=IntegerField())),
        )
        .order_by('date', 'delivery_address__name')
    )
    date_format = "%Y-%m-%d"
    
    # Organize orders by address and date
    data_by_address = {}
    for order in orders:
        # if isinstance(order['date'], str):
        #     order['date'] = datetime.strptime(order['date'], date_format)
        address = order['delivery_address__name']
        address_pk = order['delivery_address__pk']
        date_str = str(order['date'])

        if address not in data_by_address:
            data_by_address[address] = {}
        # today1 = datetime.combine(datetime.today().date(), datetime.min.time())  # Adjust if you need a specific time

        # Prepare default values for the day
        data_by_address[address][date_str] = {
            'day_name': datetime.strptime(date_str, date_format).strftime("%A"),
            'date': order['date'],
            'total_breakfast': order.get('total_breakfast', 0),
            'total_lunch': order.get('total_lunch', 0),
            'total_snack': order.get('total_snack', 0),
            'total_dinner': order.get('total_dinner', 0),
            'total_dinner2': order.get('total_dinner2', 0),
            'is_future':"True" if datetime.strptime(date_str, date_format).date() > today or (order['date'] != today and current_time < six_pm) else "False",
            # 'pk':order['pk'],
            'address_pk':address_pk,
        }
    # order['is_future'] = (
    #         "Yes" if day > today or (day != today and current_time < six_pm) else "No"
    #     )
    print(f'Data by address: {data_by_address}')
    # Fill missing dates with default data
    for address in data_by_address:
        for i in range(7):
            day = today + timedelta(days=i)
            date_str = str(day)
            if date_str not in data_by_address[address]:
                data_by_address[address][date_str] = {
                    'day_name': day.strftime("%A"),
                    'date': day,
                    'total_breakfast': 0,
                    'total_lunch': 0,
                    'total_snack': 0,
                    'total_dinner': 0,
                    'total_dinner2': 0,
                    'address_pk':DeliveryAddress.objects.get(name=address,branch=request.branch).pk,
                }
                

    # Sort the addresses by name and dates within each address
    sorted_data = {addr: dict(sorted(data.items())) for addr, data in sorted(data_by_address.items())}

    # Render the template
    return render(request, 'mentor/meal/meals.html', {
        'notifications': notifications,
        'data_by_address': sorted_data,
    })

@login_required
def assign_meal_post(request):
    order = BulkOrders.objects.first()

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            meal_assignments = data.get('mealData', [])
            meal_data = [item for item in meal_assignments if 'meal_plan' in item]
            print("in post")
            for assignment in meal_data:
                print("in for loop")
                meal_type = assignment.get('meal_plan')
                address_id = assignment.get('address')
                date = assignment.get('date')
                quantity = int(assignment.get('quantity', 0))
                print(meal_type, address_id, date, quantity)

                # if quantity == 0:
                #     continue

                delivery_address = get_object_or_404(DeliveryAddress, pk=address_id)

                # Check for existing MealDelivery entry
                existing_delivery = MealDelivery.objects.filter(
                    bulk_order=order,
                    meal_type=meal_type,
                    date=date,
                    delivery_address=delivery_address,
                    branch=request.branch,
                    company=request.company
                ).first()

                if existing_delivery:
                    # Update the quantity if it exists
                    existing_delivery.quantity = quantity
                    existing_delivery.save()
                    message = f"{quantity} {meal_type} updated for {delivery_address} by {request.branch}"
                    print("Updated", existing_delivery)
                else:
                    # Save a new meal assignment
                    deliver = MealDelivery.objects.create(
                        bulk_order=order,
                        meal_type=meal_type,
                        quantity=quantity,
                        date=date,
                        delivery_address=delivery_address,
                        branch=request.branch,
                        company=request.company
                    )
                    message = f"{quantity} {meal_type} assigned to {delivery_address} by {request.branch}"
                    print("Saved", deliver)

                # Create a notification for the action
                Notification.objects.create(
                    delivery=deliver if not existing_delivery else existing_delivery,
                    message=message,
                    branch=request.branch,
                    company=request.company
                )
                print(message)

            return JsonResponse({'success': True, 'message': 'Meal assigned successfully.'})
        except json.JSONDecodeError as e:
            return JsonResponse({'success': False, 'error': f'JSON decode error: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)


