from django.db.models import QuerySet

from menu.models import MenuItem


class TreeMenuFormatter:
    """
    Класс для получения форматированого меню в виде дерева со следующей структурой:
    {
        "filtered_tree_menu_data": filtered_tree_menu_data,
        "slug_menu": slug_menu,
        "name_menu": name_menu,
        "menu_item_id": menu_item_id,
        "params_url": slag_menu1=11&slag_menu2=3...,
    }
    где
        filtered_tree_menu_data - список словарей данной структуры:
        [
            {"menu_item": menu_item, "children": [menu_item, menu_item ....]},
            {"menu_item": menu_item, "children": [menu_item, menu_item ....]},
            ...
        ]
        name_menu - название меню из БД
        slug_menu - слаг меню, указывается в БД
        menu_item_id - id активнго элемента меню
        params_url - GET параметры запроса для добавления к href
    """

    def __init__(self, menu_item_id: int, slug_menu: str, params_url: dict):
        self.menu_item_id = menu_item_id
        self.slug_menu = slug_menu
        self.params_url = params_url

    def get_formatted_tree_menu(self) -> dict:
        """Функция возвращает отформатирование древовидное меню"""
        menu_items: QuerySet[MenuItem] = MenuItem.objects.select_related("menu")
        menu_items = menu_items.filter(menu__slug=self.slug_menu)
        if self.menu_item_id:
            menu_items_values = menu_items.values(
                "id", "title", "parent_id", "url", "menu__title"
            )
            tree_menu_data = self._get_tree_menu_data(menu_items_values)
            filtered_tree_menu_data = self._get_filtered_and_formatted_tree_menu_data(
                tree_menu_data
            )
        else:
            menu_items = menu_items.filter(parent__isnull=True)
            menu_items_values = menu_items.values(
                "id", "title", "parent_id", "url", "menu__title"
            )
            filtered_tree_menu_data = self._get_formatted_first_level_menu_data(
                menu_items_values
            )
        name_menu = self._get_name_menu(menu_items_values)
        return {
            "filtered_tree_menu_data": filtered_tree_menu_data,
            "slug_menu": self.slug_menu,
            "name_menu": name_menu,
            "menu_item_id": self.menu_item_id,
            "params_url": self._get_filtered_params_url(),
        }

    def _get_filtered_params_url(self) -> str:
        """
        Вернуть строку GET параметров содержащихся в URL
        за исключением параметра slug_menu для использования в атребутах href в html
        """
        return "&".join(
            [
                f"{key}={value}"
                for key, value in self.params_url.items()
                if key != self.slug_menu
            ]
        )

    @staticmethod
    def _get_name_menu(menu_items) -> str:
        if menu_items:
            return menu_items[0].get("menu__title")
        return ""

    @staticmethod
    def _get_tree_menu_data(menu_items):
        """Получение древовидного меню из списка элементов меню"""
        menu_items_dict = {}
        new_menu_items = []
        for menu_item in menu_items:
            menu_item["children"] = []
            menu_items_dict[menu_item.get("id")] = menu_item
        for menu_item in menu_items:
            parent_id = menu_item.get("parent_id")
            if parent_id is None:
                new_menu_items.append(menu_item)
                continue
            elm = menu_items_dict.get(parent_id)
            elm.get("children").append(menu_item)
        return new_menu_items

    def _get_filtered_and_formatted_tree_menu_data(self, tree_menu_data):
        """
        Фильтрация и форматирование древовидного меню с учетом того что должны остаться
        толко все предки элемента меню с menu_item_id и его прямые потомки
        """
        menu_levels = []
        is_element_found = False
        for menu_item in tree_menu_data:
            elm = {"menu_item": menu_item, "children": None}
            if menu_item.get("id") == self.menu_item_id:
                is_element_found = True
                menu_item_children = menu_item.get("children")
                elm["children"] = self._get_formatted_first_level_menu_data(
                    menu_item_children
                )

            if not is_element_found:
                children = self._get_filtered_and_formatted_tree_menu_data(
                    menu_item.get("children")
                )
                elm["children"] = children
                if children:
                    is_element_found = True
            menu_levels.append(elm)
        if is_element_found:
            return menu_levels
        else:
            return None

    @staticmethod
    def _get_formatted_first_level_menu_data(tree_menu_data):
        """Функция для форматирования элементов меню певого уровня"""
        if tree_menu_data:
            children = []
            for child in tree_menu_data:
                children.append({"menu_item": child, "children": None})
            return children
        else:
            return None
