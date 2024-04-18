from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.utils import timezone
from django.contrib.auth import get_user_model

@receiver(user_logged_in)
def update_last_access(sender, request, user, **kwargs):
    user.last_access = timezone.now()
    user.save(update_fields=['last_access'])
