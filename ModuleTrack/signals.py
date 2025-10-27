from django.db.models.signals import post_save, post_delete
from django.contrib.auth.models import User
from django.dispatch import receiver

@receiver(post_save, sender=User)
def promote_first_user_to_superuser(sender, instance, created, **kwargs):
    if created and User.objects.count() == 1:
        instance.is_superuser = True
        instance.is_staff = True
        instance.save()

@receiver(post_delete, sender=User)
def promote_last_user_to_superuser(sender, instance, **kwargs):
    if User.objects.count() == 1:
        last_user = User.objects.first()
        if last_user:
            last_user.is_superuser = True
            last_user.is_staff = True
            last_user.save()
