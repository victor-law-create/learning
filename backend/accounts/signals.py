from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.apps import apps
from .models import Profile

@receiver(post_save, sender=User)
def create_user_profile_and_cart(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        Cart = apps.get_model('marketplace', 'Cart')
        Cart.objects.create(user=instance)
