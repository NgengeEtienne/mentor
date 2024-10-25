from django.shortcuts import render, redirect, get_object_or_404
from .models import DeliveryAddress, MealDelivery, Notification
from AdminDashboard.models import Meal, Branch, Company, BulkOrders, MealPlan
from .forms import MealDeliveryForm
from django.utils.timezone import now
import json
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import LoginForm,DeliveryAddressForm
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.utils.timezone import now
import datetime



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
    
    today = now().date()
    current_time = now().time()  # Current time for comparison
    six_pm = datetime.time(18, 0)  # 6:00 PM time object
    print("current time", current_time, "six pm", six_pm)
    start_of_week = today - datetime.timedelta(days=today.weekday())  # Get Monday of the current week
    end_of_week = start_of_week + datetime.timedelta(days=6)  # Get Sunday of the current week

    active_subscriptions = BulkOrders.objects.filter(branch=request.branch)
    dispatched = MealDelivery.objects.filter(status='DISPATCHED', branch=request.branch,created_at__range=[start_of_week, end_of_week]).count() or 0
    cooking = MealDelivery.objects.filter(status='COOKING', branch=request.branch,created_at__range=[start_of_week, end_of_week]).count() or 0
    deliveredcount = MealDelivery.objects.filter(status='DELIVERED', branch=request.branch,created_at__range=[start_of_week, end_of_week]).count() or 0
    canceled = MealDelivery.objects.filter(status='CANCELED', branch=request.branch,created_at__range=[start_of_week, end_of_week]).count() or 0
    
    addresses = DeliveryAddress.objects.filter(branch=request.branch)
    delivered = MealDelivery.objects.filter(status='DELIVERED', branch=request.branch,created_at__range=[start_of_week, end_of_week])

    notifications = get_notifications(request)  # Fetch notifications


    # Fetch all orders within the week, grouped by date
    orders = (
        MealDelivery.objects.filter(branch=request.branch, date__range=[start_of_week, end_of_week])
        .values('date', 'bulk_order__bulk_order_name', 'delivery_address__name')  # Group by date
        .annotate(
            total_breakfast=Sum('bulk_order__breakfast'),
            total_lunch=Sum('bulk_order__lunch'),
            total_snack=Sum('bulk_order__snack'),
            total_dinner=Sum('bulk_order__dinner'),
        )
        .order_by('date')  # Sort by date
    )

    # Convert query results into a dictionary with dates as keys
    order_dict = {order['date']: order for order in orders}  # Store by date for quick lookup

    # Prepare the full week data, including missing days with placeholders
    week_days = []
    for i in range(7):
        day = start_of_week + datetime.timedelta(days=i)
        day_name = day.strftime("%A")

        order = order_dict.get(day, {
            'date': day,
            'bulk_order__bulk_order_name': None,
            'delivery_data': {},
            'total_breakfast': 0,
            'total_lunch': 0,
            'total_snack': 0,
            'total_dinner': 0,
        })

        order['day_name'] = day_name

        # Adjust is_future logic to check for 6 PM condition
        if day > today or (day == today and current_time < six_pm):
            order['is_future'] = "Yes"
        else:
            order['is_future'] = "No"

        order['has_values'] = bool(order.get('bulk_order__bulk_order_name'))

        # Calculate total sum and organize delivery data
        delivery_data = {}
        if order['has_values']:
            address = order['delivery_address__name']
            total_sum = (order['total_breakfast'] + order['total_lunch'] +
                         order['total_snack'] + order['total_dinner'])
            delivery_data[address] = {
                'total_sum': total_sum,
                'total_breakfast': order['total_breakfast'],
                'total_lunch': order['total_lunch'],
                'total_snack': order['total_snack'],
                'total_dinner': order['total_dinner'],
            }
        order['delivery_data'] = delivery_data

        week_days.append(order)

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
        "orders": week_days
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
        branch = request.branch
        company = request.company
        DeliveryAddress.objects.create(name=name, address_line_1=address_line_1, address_line_2=address_line_2, city=city, state=state, pin_code=pin_code, latitude=latitude, longitude=longitude, branch_id=branch.id, company=company)
        return redirect('delivery_address_list')

    return render(request, 'mentor/delivery/form.html', {'form': form, 'notifications': notifications})

@login_required
def delivery_address_edit(request, id):
    address = get_object_or_404(DeliveryAddress, id=id)
    notifications = get_notifications(request)  # Fetch notifications
    
    if request.method == 'POST':
        form = DeliveryAddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            return redirect('delivery_address_list')
    else:
        form = DeliveryAddressForm(instance=address)

    return render(request, 'mentor/delivery/form.html', {'form': form, 'object': address, 'notifications': notifications})

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
    addresses = DeliveryAddress.objects.all()
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
    today = date.today()
    
    # Fetch today's deliveries
    todays_deliveries = MealDelivery.objects.filter(branch=request.branch, date=today)
    print(todays_deliveries)
    # Fetch past deliveries
    past_deliveries = MealDelivery.objects.filter(branch=request.branch, date__lt=today)
    print(past_deliveries)
    # Combine today's and past deliveries
    deliveries = list(chain(todays_deliveries, past_deliveries))
    # print(deliveries)
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
        'page_obj': page_obj
    })




from django.http import JsonResponse


@login_required
def assign_meal(request):
    order_id = id
    order = BulkOrders.objects.all().first()
    sum = order.breakfast + order.lunch + order.snack + order.dinner
    addresses = DeliveryAddress.objects.all()
    notifications = get_notifications(request)  # Fetch notifications
    
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            meal_assignments = data.get('mealData', [])
            meal_data = [item for item in meal_assignments if 'meal_plan' in item]

            for assignment in meal_data:
                meal_type = assignment.get('meal_plan')
                address_id = assignment.get('address')
                date = assignment.get('date')
                quantity = int(assignment.get('quantity', 0))
                
                delivery_address = get_object_or_404(DeliveryAddress, pk=address_id)
                
                # Save the meal assignment
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

    return render(request, 'mentor/meal/assign1.html', {
        'order': order,
        'addresses': addresses,
        'notifications': notifications,
        'sum': sum
    })

def edit_assign_meal(request, date):  # Include the date parameter here
    order_id = 1
    order = get_object_or_404(BulkOrders, pk=order_id)
    addresses = DeliveryAddress.objects.all()
    notifications = get_notifications(request)  # Fetch notifications
    meal_deliveries = MealDelivery.objects.filter(bulk_order=order, date=date)  # Filter by date

    if request.method == "POST":
        try:
            # print(request.body)
            data = json.loads(request.body)
            meal_assignments = data.get('mealData', [])
            meal_data = [item for item in meal_assignments if 'meal_plan' in item]
            print(meal_data)
            for assignment in meal_data:
                meal_type = assignment.get('meal_plan')
                address_id = assignment.get('address')
                date = assignment.get('date')  # Capture updated date
                quantity = int(assignment.get('quantity', 0))
                meal_id = assignment.get('id')
                print("in for")
                delivery_address = get_object_or_404(DeliveryAddress, pk=address_id)
                print("meal id", meal_id)
                # Update or create meal assignment
                if meal_id not in [None, '','null']:
                # Try to update the existing MealDelivery
                    meal_delivery = MealDelivery.objects.filter(id=meal_id, bulk_order=order).first()
                    if meal_delivery:
                        # Update existing record
                        meal_delivery.quantity = quantity
                        meal_delivery.date = date
                        meal_delivery.branch = request.branch
                        meal_delivery.company = request.company
                        meal_delivery.save()
                        print("meal_delivery updated", meal_delivery)
                    else:
                        # If no record is found for the given ID, create a new one
                        MealDelivery.objects.create(
                            bulk_order=order,
                            meal_type=meal_type,
                            quantity=quantity,
                            date=date,
                            delivery_address=delivery_address,
                            branch=request.branch,
                            company=request.company
                        )
                        print("meal_delivery created", meal_delivery)
                else:
                    # If no ID is provided, create a new MealDelivery
                    MealDelivery.objects.create(
                        bulk_order=order,
                        meal_type=meal_type,
                        quantity=quantity,
                        date=date,
                        delivery_address=delivery_address,
                        branch=request.branch,
                        company=request.company
                    )
                    print("meal_delivery created  out", meal_delivery)
                message = f"{quantity} {meal_type} assigned to {delivery_address} by {request.branch}"
                print("message", message)
                Notification.objects.create(
                    delivery=meal_delivery,
                    message=message,
                    branch=request.branch,
                    company=request.company
                )

            return JsonResponse({'success': True, 'message': 'Meal assignment updated successfully.'})
        except json.JSONDecodeError as e:
            return JsonResponse({'success': False, 'error': f'JSON decode error: {str(e)}'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=500)

    return render(request, 'mentor/meal/edit_assign1.html', {
        'order': order,
        'addresses': addresses,
        'notifications': notifications,
        'meal_deliveries': meal_deliveries,  # Pass existing meal deliveries filtered by date
        'selected_date': date  # Pass the selected date to the template if needed
    })

def meal_plan_list(request):
    notifications = get_notifications(request)  # Fetch notifications
    orders = BulkOrders.objects.filter(branch=request.branch).prefetch_related('MealPlan')  # Optimize with prefetch
    mealplans = [mealplan for order in orders for mealplan in order.MealPlan.all()]  # Extract all meal plans
    print(orders)
    return render(request, 'mentor/mealplan/list.html', {
        'notifications': notifications,
        'mealplans': mealplans,
        'orders': orders
    })

def meal_plan_detail(request, id):
    notifications = get_notifications(request)  # Fetch notifications
    mealplan = get_object_or_404(MealPlan, pk=id)
    order= get_object_or_404(BulkOrders, MealPlan=mealplan)
    sum = order.breakfast + order.lunch + order.snack + order.dinner
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 
            'friday', 'saturday', 'sunday']
    print(order)
    for day in days :
        print(day)
        for dish in mealplan.monday_breakfast_dish.all():
            print(dish)
    return render(request, 'mentor/mealplan/detail.html', {
        'notifications': notifications,
        'mealplan': mealplan,
        'days': days,
        'order': order,
        'sum': sum
    })

def meal_ordered(request):
    notifications = get_notifications(request)  # Fetch notifications
    from django.db.models import Sum
    from django.utils.timezone import now
    import datetime

    today = now().date()
    current_time = now().time()  # Current time for comparison
    six_pm = datetime.time(18, 0)  # 6:00 PM time object
    print("current time", current_time, "six pm", six_pm)
    start_of_week = today - datetime.timedelta(days=today.weekday())  # Get Monday of the current week
    end_of_week = start_of_week + datetime.timedelta(days=6)  # Get Sunday of the current week

    # Fetch all orders within the week, grouped by date
    orders = (
        MealDelivery.objects.filter(branch=request.branch, date__range=[start_of_week, end_of_week])
        .values('date', 'bulk_order__bulk_order_name', 'delivery_address__name')  # Group by date
        .annotate(
            total_breakfast=Sum('bulk_order__breakfast'),
            total_lunch=Sum('bulk_order__lunch'),
            total_snack=Sum('bulk_order__snack'),
            total_dinner=Sum('bulk_order__dinner'),
        )
        .order_by('date')  # Sort by date
    )

    # Convert query results into a dictionary with dates as keys
    order_dict = {order['date']: order for order in orders}  # Store by date for quick lookup

    # Prepare the full week data, including missing days with placeholders
    week_days = []
    for i in range(7):
        day = start_of_week + datetime.timedelta(days=i)
        day_name = day.strftime("%A")

        order = order_dict.get(day, {
            'date': day,
            'bulk_order__bulk_order_name': None,
            'delivery_data': {},
            'total_breakfast': 0,
            'total_lunch': 0,
            'total_snack': 0,
            'total_dinner': 0,
        })

        order['day_name'] = day_name

        # Adjust is_future logic to check for 6 PM condition
        if day > today or (day == today and current_time < six_pm):
            order['is_future'] = "Yes"
        else:
            order['is_future'] = "No"

        order['has_values'] = bool(order.get('bulk_order__bulk_order_name'))

        # Calculate total sum and organize delivery data
        delivery_data = {}
        if order['has_values']:
            address = order['delivery_address__name']
            total_sum = (order['total_breakfast'] + order['total_lunch'] +
                         order['total_snack'] + order['total_dinner'])
            delivery_data[address] = {
                'total_sum': total_sum,
                'total_breakfast': order['total_breakfast'],
                'total_lunch': order['total_lunch'],
                'total_snack': order['total_snack'],
                'total_dinner': order['total_dinner'],
            }
        order['delivery_data'] = delivery_data

        week_days.append(order)

    print(week_days)  # Debug print to verify output

    # Render the template with notifications and the complete week data
    return render(request, 'mentor/meal/meals.html', {
        'notifications': notifications,
        'orders': week_days  # Full week of orders including placeholders
    })
