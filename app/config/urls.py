from django.conf import settings
from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("menu.urls")),
]
if settings.DEBUG:
    urlpatterns.append(path("silk/", include("silk.urls", namespace="silk")))
