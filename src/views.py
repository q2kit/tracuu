from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework.generics import RetrieveAPIView

from src.models import Receipt
from src.serializers import ReceiptSerializer


class IndexView(TemplateView):
    template_name = "index.html"


class SearchView(RetrieveAPIView):
    queryset = Receipt.objects.all()
    serializer_class = ReceiptSerializer

    def get_object(self):
        code = self.kwargs.get("code").strip()
        return get_object_or_404(
            Receipt,
            is_deleted=False,
            code__iexact=code,
        )
