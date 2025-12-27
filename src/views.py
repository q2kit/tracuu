import contextlib
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic import TemplateView
from rest_framework.generics import (
    CreateAPIView,
    RetrieveAPIView,
    RetrieveUpdateDestroyAPIView,
)

from src.const import SEARCH_API_IMAGE_EXPIRY_SECONDS
from src.forms import CustomAuthenticationForm
from src.models import Receipt
from src.serializers import ReceiptSerializer


class IndexView(TemplateView):
    template_name = "index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        receipt_code = self.request.GET.get("code", "").strip()
        with contextlib.suppress(Receipt.DoesNotExist):
            receipt = Receipt.objects.get(is_deleted=False, code__iexact=receipt_code)
            context["receipt"] = receipt
        return context


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


class ReceiptSearchPublicAPIView(RetrieveAPIView):
    permission_classes = []
    serializer_class = ReceiptSerializer

    def get_object(self):
        code = self.kwargs.get("code").strip()
        return get_object_or_404(
            Receipt,
            is_deleted=False,
            code__iexact=code,
        )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context["image_expire_seconds"] = SEARCH_API_IMAGE_EXPIRY_SECONDS
        return context


class ReceiptCreateAPIView(CreateAPIView):
    queryset = Receipt.objects.filter(is_deleted=False)
    serializer_class = ReceiptSerializer


class ReceiptRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = Receipt.objects.filter(is_deleted=False)
    serializer_class = ReceiptSerializer

    def perform_destroy(self, instance):
        instance.is_deleted = True
        instance.save(update_fields=["is_deleted"])
