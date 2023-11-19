from django.urls import path

from menu.views import test_menu_view, test_index_view


urlpatterns = [
    path("", test_menu_view),
    path("test<slug:slug>/", test_index_view),
]
