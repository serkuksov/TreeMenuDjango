from django.shortcuts import render


def test_menu_view(request):
    """Отображение тестовой страницы с древовидными меню"""
    return render(request, template_name="menu/test_menu.html")
