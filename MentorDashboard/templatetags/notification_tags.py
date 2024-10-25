# notification_tags.py
from django import template
from MentorDashboard.models import Notification

register = template.Library()

@register.inclusion_tag('partials/notifications.html')
def show_notifications():
    notifications = Notification.objects.all().order_by('created_at')
    return {'notifications': notifications}
