from django.urls import path

from app.views import IndexView, SearchView

urlpatterns = [
    path("", IndexView.as_view(), name="index"),
    path("search/<str:code>/", SearchView.as_view(), name="search"),
]
