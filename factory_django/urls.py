from django.contrib import admin
from django.urls import path

import restapi

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", restapi.api.urls)
]