from django.contrib import admin
from django.urls import path

from src.const import DEVELOPMENT_ENV, ENV, LOCAL_ENV
from src.views import (
    CustomLoginView,
    CustomLogoutView,
    DashboardView,
    IndexView,
    ReceiptCreateAPIView,
    ReceiptRetrieveUpdateDestroyAPIView,
    ReceiptSearchPublicAPIView,
)

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", CustomLogoutView.as_view(), name="logout"),
    path("dashboard/", DashboardView.as_view(), name="dashboard"),
    path(
        "search/<str:code>/",
        ReceiptSearchPublicAPIView.as_view(),
        name="receipt-search",
    ),
    path("api/receipts/", ReceiptCreateAPIView.as_view(), name="receipt-create"),
    path(
        "api/receipts/<int:pk>/",
        ReceiptRetrieveUpdateDestroyAPIView.as_view(),
        name="receipt-detail",
    ),
]

if ENV in [LOCAL_ENV, DEVELOPMENT_ENV]:
    urlpatterns.insert(0, path("admin/", admin.site.urls))
