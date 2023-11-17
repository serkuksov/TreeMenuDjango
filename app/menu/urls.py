from django.urls import path

from menu.views import test_menu_view


urlpatterns = [
    path("", test_menu_view),
]
