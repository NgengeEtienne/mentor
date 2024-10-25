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
    active_subscriptions = BulkOrders.objects.filter(branch=request.branch)
    dispatched = MealDelivery.objects.filter(status='DISPATCHED', branch=request.branch).count() or 0
    cooking = MealDelivery.objects.filter(status='COOKING', branch=request.branch).count() or 0
    deliveredcount = MealDelivery.objects.filter(status='DELIVERED', branch=request.branch).count() or 0
    canceled = MealDelivery.objects.filter(status='CANCELED', branch=request.branch).count() or 0
    
    addresses = DeliveryAddress.objects.filter(branch=request.branch)
    delivered = MealDelivery.objects.filter(status='DELIVERED', branch=request.branch)

    notifications = get_notifications(request)  # Fetch notifications

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
        "notifications": notifications
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

@login_required
def orders_list(request):
    deliveries = MealDelivery.objects.filter(branch=request.branch)
    paginator = Paginator(deliveries, 10)  # Show 10 deliveries per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    notifications = get_notifications(request)  # Fetch notifications
    return render(request,'mentor/order/list.html', {'deliveries': page_obj, 'notifications': notifications, 'paginator': paginator, 'page_obj': page_obj})
from django.http import JsonResponse


@login_required
def assign_meal(request, id):
    order_id = id
    order = get_object_or_404(BulkOrders, pk=order_id)
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

    return render(request, 'mentor/meal/assign.html', {
        'order': order,
        'addresses': addresses,
        'notifications': notifications
    })
def meal_plan_list(request):
    notifications = get_notifications(request)  # Fetch notifications
    orders = BulkOrders.objects.filter(branch=request.branch).prefetch_related('MealPlan')  # Optimize with prefetch
    mealplans = [mealplan for order in orders for mealplan in order.MealPlan.all()]  # Extract all meal plans
    
    return render(request, 'mentor/mealplan/list.html', {
        'notifications': notifications,
        'mealplans': mealplans,
    })

def meal_plan_detail(request, id):
    notifications = get_notifications(request)  # Fetch notifications
    mealplan = get_object_or_404(MealPlan, pk=id)
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 
            'friday', 'saturday', 'sunday']
    return render(request, 'mentor/mealplan/detail.html', {
        'notifications': notifications,
        'mealplan': mealplan,
        'days': days
    })


def meal_ordered(request):
    notifications = get_notifications(request)  # Fetch notifications
    #get all orders and categories them by date(mostly days like monday, tuesday etcc... put them in order such that i can list them like, monsday, tuesday, etc
    from django.db.models import Sum
    orders = (
        MealDelivery.objects.filter(branch=request.branch)
        .values('date','bulk_order__bulk_order_name')  # Group by date
        .annotate(
            # order_count=Count('id'),  # Count total orders for the date
            total_breakfast=Sum('bulk_order__breakfast'),
            total_lunch=Sum('bulk_order__lunch'),
            total_snack=Sum('bulk_order__snack'),
            total_dinner=Sum('bulk_order__dinner'),
            
        )
        .order_by('date')  # Sort by date
    )
    print(orders)
    return render(request, 'mentor/meal/meals.html', {
        'notifications': notifications,
        'orders': orders
    })
