import json
from urllib.parse import urlsplit

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from src.forms import CustomAuthenticationForm
from src.models import Receipt
from src.serializers import ReceiptSerializer


class ReceiptImageS3ProxyResponse(HttpResponse):
    internal_location_prefix = "/_internal_image_proxy"

    def __init__(self, s3_proxy_url, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        url_parsed = urlsplit(s3_proxy_url)
        self["X-Accel-Redirect"] = (
            f"{self.internal_location_prefix}/{url_parsed.netloc}{url_parsed.path}?{url_parsed.query}"
        )


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["receipt"] = self.receipt
        return context

    def _is_html_request(self, request):
        dest = request.headers.get("Sec-Fetch-Dest")
        accept = request.headers.get("Accept")
        return dest == "document" or (accept and "text/html" in accept)

    def get(self, request, *args, **kwargs):
        receipt_code = request.GET.get("code", "").strip()

        try:
            self.receipt = Receipt.objects.get(
                is_deleted=False,
                code__iexact=receipt_code,
            )
        except Receipt.DoesNotExist:
            self.receipt = None

        if not self._is_html_request(request) and self.receipt:
            if settings.DEBUG:
                return HttpResponseRedirect(self.receipt.image.url)
            return ReceiptImageS3ProxyResponse(self.receipt.image.url)

        return super().get(request, *args, **kwargs)


class CustomLoginView(LoginView):
    template_name = "login.html"
    authentication_form = CustomAuthenticationForm

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.info(request, "Bạn đã đăng nhập.")
            return HttpResponseRedirect(self.get_success_url())
        return super().get(request, *args, **kwargs)


class CustomLogoutView(LogoutView):
    pass


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = "dashboard.html"
    login_url = "/login/"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["receipts"] = json.dumps(
            ReceiptSerializer(self.get_receipts(), many=True).data,
        )
        return context

    def get_receipts(self):
        return Receipt.objects.filter(is_deleted=False)


class ReceiptSearchAPIView(RetrieveAPIView):
    permission_classes = []
    serializer_class = ReceiptSerializer

    def get_object(self):
        code = self.kwargs.get("code").strip()
        return get_object_or_404(
            Receipt,
            is_deleted=False,
            code__iexact=code,
        )


class ReceiptCreateAPIView(CreateAPIView):
    queryset = Receipt.objects.filter(is_deleted=False)
    serializer_class = ReceiptSerializer


class ReceiptRUDAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.filter(is_deleted=False)
    serializer_class = ReceiptSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])
