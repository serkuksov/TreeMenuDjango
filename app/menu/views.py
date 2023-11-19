from django.shortcuts import render


def test_menu_view(request):
    """Отображение тестовой страницы с древовидными меню"""
    return render(request, template_name="menu/test_menu.html")


def test_index_view(request, slug):
    """Отображение тестовой страницы на которую ведет ссылка"""
    return render(request, template_name="menu/test_index.html", context={"slug": slug})
