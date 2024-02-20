from django.urls import path
from . import views


urlpatterns = [
    path("bulk_transfer", views.bulk_transfer, name="bulk_transfer"),
]
