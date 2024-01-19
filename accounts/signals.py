from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from accounts.models import User,ClinicWorker,ClinicAddress


User = get_user_model()

@receiver(post_save, sender=User)
def user_signal(sender, instance, created, **kwargs):

    if created:
        if instance.user_type == User.HC:
            ClinicWorker.objects.create(clinic=instance)
            # ClinicAddress.objects.create(clinic=instance)