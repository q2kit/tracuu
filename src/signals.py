from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.models import Receipt
from src.tasks import receipt_created_notify_task


@receiver(post_save, sender=Receipt)
def receipt_saved(sender, instance, created, **kwargs):  # noqa: ARG001
    if created:
        transaction.on_commit(lambda: receipt_created_notify_task.delay(instance.pk))
