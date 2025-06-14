# user/signals.py
import random
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, UserProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        email_prefix = instance.email.split('@')[0]
        random_number = random.randint(1000, 9999)
        username = f"{email_prefix}{random_number}"

        UserProfile.objects.create(
            user=instance,
            username=username,
        )
