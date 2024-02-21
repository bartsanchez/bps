from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("", include("bank_account_transfers.urls")),
    path("admin/", admin.site.urls),
]
