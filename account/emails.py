import random
from django.core.mail import send_mail
from django.conf import settings
from .models import *



def send_otp_via_email(email,otp_code):
    subject = 'Account Verification Email'
    message = f'Your otp is {otp_code}'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)


    