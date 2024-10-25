# forms.py
from django import forms
from .models import DeliveryAddress, MealDelivery, Notification,MealPlan


class LoginForm(forms.Form):
    email = forms.EmailField(
        widget=forms.TextInput(attrs={
            'class': 'w-full rounded-lg border border-stroke bg-transparent py-4 pl-6 pr-10 outline-none focus:border-primary focus-visible:shadow-none dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary',
            'placeholder': 'Enter email'
        }),
        label='Email'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full rounded-lg border border-stroke bg-transparent py-4 pl-6 pr-10 outline-none focus:border-primary focus-visible:shadow-none dark:border-form-strokedark dark:bg-form-input dark:focus:border-primary',
            'placeholder': 'Enter password'
        }),
        label='Password'
    )
class DeliveryAddressForm(forms.ModelForm):
    class Meta:
        model = DeliveryAddress
        fields = ['name', 'address_line_1', 'address_line_2','city','state','pin_code','latitude','longitude']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-3/4 rounded-lg border-[1.5px] border-primary bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white', 'placeholder': 'Enter name'}),
            'address_line_1': forms.TextInput(attrs={'class': 'w-3/4 rounded-lg border-[1.5px] border-primary bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white', 'placeholder': 'Enter Address Line 1'}),
            'address_line_2': forms.TextInput(attrs={'class': 'w-3/4 rounded-lg border-[1.5px] border-primary bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white', 'placeholder': 'Enter Address Line 2'}),
            'city': forms.TextInput(attrs={'class': 'w-3/4 rounded-lg border-[1.5px] border-primary bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white', 'placeholder': 'Enter City'}),
            'state': forms.TextInput(attrs={'class': 'w-3/4 rounded-lg border-[1.5px] border-primary bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white', 'placeholder': 'Enter State'}),
            'pin_code': forms.TextInput(attrs={'class': 'w-3/4 rounded-lg border-[1.5px] border-primary bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white', 'placeholder': 'Enter Pin Code'}),
            'latitude': forms.TextInput(attrs={'class': 'w-3/4 rounded-lg border-[1.5px] border-primary bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white', 'placeholder': 'Enter Latitude'}),
            'longitude': forms.TextInput(attrs={'class': 'w-3/4 rounded-lg border-[1.5px] border-primary bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white', 'placeholder': 'Enter Longitude'}),
        }

# class MealDeliveryForm(forms.ModelForm):
#     class Meta:
#         model = MealDelivery
#         fields = ['meal', 'delivery_address', 'status']
#         widgets = {
#             'meal': forms.Select(attrs={'class': 'form-select'}),
#             'delivery_address': forms.Select(attrs={'class': 'form-select'}),
#             'status': forms.Select(attrs={'class': 'form-select'}),
#         }

# from django import forms
# from .models import MealDelivery

class MealDeliveryForm(forms.ModelForm):
    class Meta:
        model = MealDelivery
        fields = ['bulk_order', 'delivery_address', 'status','meal_type','quantity','date']
        widgets = {
            'bulk_order': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            }),
            'delivery_address': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            }),
            'status': forms.Select(attrs={
                'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
            }),
            'meal_type': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'quantity': forms.TextInput(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'date': forms.DateInput(attrs={'class': 'form-datepicker bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-full p-2.5 dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white','data-class': 'flatpickr-right'}),
        }


class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['delivery', 'message']
        widgets = {
            'delivery': forms.Select(attrs={'class': 'w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500'}),
            'message': forms.Textarea(attrs={'class': 'w-100 rounded-lg border-[1.5px] border-primary bg-transparent px-5 py-3 font-normal text-black outline-none transition focus:border-primary active:border-primary disabled:cursor-default disabled:bg-whiter dark:bg-form-input dark:text-white', 'rows': 4, 'placeholder': 'Enter notification message'}),
        }

class OrderSearchForm(forms.Form):
    status_choices = [
        ('', 'All'),
        ('COOKING', 'Cooking'),
        ('DISPATCHED', 'Dispatched'),
        ('DELIVERED', 'Delivered'),
        ('CANCELED', 'Canceled'),
    ]
    status = forms.ChoiceField(
        choices=status_choices, 
        required=False, 
        widget=forms.Select(attrs={'class': 'form-select'})
    )

