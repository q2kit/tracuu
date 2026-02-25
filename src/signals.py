import threading

from django.db import transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.funcs import receipt_created_notify
from src.models import Receipt


@receiver(post_save, sender=Receipt)
def receipt_saved(sender, instance, created, **kwargs):  # noqa: ARG001
    if created:

        def callback():
            # TODO: Use Celery instead of threading
            threading.Thread(target=receipt_created_notify, args=(instance,)).start()

        transaction.on_commit(callback)
