import contextlib

from celery import shared_task
from src.funcs import receipt_created_notify
from src.models import Receipt


@shared_task(ignore_result=True)
def receipt_created_notify_task(receipt_id: int) -> None:
    with contextlib.suppress(Receipt.DoesNotExist):
        receipt = Receipt.objects.get(pk=receipt_id)
        receipt_created_notify(receipt)
