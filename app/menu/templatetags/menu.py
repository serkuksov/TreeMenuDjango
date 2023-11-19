from copy import deepcopy

from django import template
from django.template import RequestContext

from menu.servises import TreeMenuFormatter

register = template.Library()


@register.inclusion_tag("menu/menu.html", takes_context=True)
def draw_menu(context: RequestContext, slug_menu: str):
    """Templatetags возвращающий отформатирование меню по его слагу и параметру URL"""
    params_url = deepcopy(context.request.GET)
    menu_item_id = params_url.get(slug_menu, 0)
    try:
        menu_item_id = int(menu_item_id)
    except ValueError:
        menu_item_id = 0
    return TreeMenuFormatter(
        menu_item_id, slug_menu, params_url
    ).get_formatted_tree_menu()
