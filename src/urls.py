from django.contrib import admin
from django.urls import path

from src.views import IndexView, SearchView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", IndexView.as_view(), name="index"),
    path("search/<str:code>/", SearchView.as_view(), name="search"),
]
