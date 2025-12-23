from django.contrib import admin
from django.urls import path

from src.const import ENV, PRODUCTION_ENV
from src.views import (
    CustomLoginView,
    CustomLogoutView,
    DashboardView,
    IndexView,
    ReceiptCreateAPIView,
    ReceiptRetrieveAPIView,
    ReceiptUpdateAPIView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path("search/<str:code>/", ReceiptRetrieveAPIView.as_view(), name="search"),
    path("api/receipts/", ReceiptCreateAPIView.as_view(), name="receipt-create"),
    path(
        "api/receipts/<int:pk>/",
        ReceiptUpdateAPIView.as_view(),
        name="receipt-update",
    ),
]

if ENV != PRODUCTION_ENV:
    urlpatterns.insert(0, path("admin/", admin.site.urls))
