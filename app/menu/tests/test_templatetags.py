from django.test import TestCase, RequestFactory
from django.template import RequestContext

from menu.models import Menu, MenuItem
from menu.templatetags.menu import draw_menu


class MenuTagTest(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.menu1 = Menu.objects.create(title="Test Menu", slug="test-menu")
        self.menu_item1 = MenuItem.objects.create(
            title="Test Item 1",
            menu=self.menu1,
        )
        self.menu_item2 = MenuItem.objects.create(
            title="Test Item 2",
            menu=self.menu1,
        )
        self.menu_item3 = MenuItem.objects.create(
            title="Test Item 3",
            menu=self.menu1,
            parent=self.menu_item2,
        )
        self.menu_item4 = MenuItem.objects.create(
            title="Test Item 4",
            menu=self.menu1,
            parent=self.menu_item3,
        )

    def test_draw_menu_not_params(self):
        request = self.factory.get("/")
        context = RequestContext(request)

        test_result = {
            "filtered_tree_menu_data": [
                {
                    "menu_item": {
                        "id": 1,
                        "title": "Test Item 1",
                        "parent_id": None,
                        "url": None,
                        "menu__title": "Test Menu",
                    },
                    "children": None,
                },
                {
                    "menu_item": {
                        "id": 2,
                        "title": "Test Item 2",
                        "parent_id": None,
                        "url": None,
                        "menu__title": "Test Menu",
                    },
                    "children": None,
                },
            ],
            "slug_menu": "test-menu",
            "name_menu": "Test Menu",
            "menu_item_id": 0,
            "params_url": "",
        }

        result = draw_menu(context, "test-menu")

        self.assertEqual(result, test_result)

    def test_draw_menu_with_param(self):
        request = self.factory.get(f"/?test-menu={self.menu_item1.id}")
        context = RequestContext(request)

        test_result = {
            "filtered_tree_menu_data": [
                {
                    "menu_item": {
                        "id": 1,
                        "title": "Test Item 1",
                        "parent_id": None,
                        "url": None,
                        "menu__title": "Test Menu",
                        "children": [],
                    },
                    "children": None,
                },
                {
                    "menu_item": {
                        "id": 2,
                        "title": "Test Item 2",
                        "parent_id": None,
                        "url": None,
                        "menu__title": "Test Menu",
                        "children": [
                            {
                                "id": 3,
                                "title": "Test Item 3",
                                "parent_id": 2,
                                "url": None,
                                "menu__title": "Test Menu",
                                "children": [
                                    {
                                        "id": 4,
                                        "title": "Test Item 4",
                                        "parent_id": 3,
                                        "url": None,
                                        "menu__title": "Test Menu",
                                        "children": [],
                                    }
                                ],
                            }
                        ],
                    },
                    "children": None,
                },
            ],
            "slug_menu": "test-menu",
            "name_menu": "Test Menu",
            "menu_item_id": 1,
            "params_url": "",
        }

        result = draw_menu(context, "test-menu")
        self.assertEqual(result, test_result)

    def test_draw_menu_with_erroneous_param(self):
        # TODO нужно переделать логику чтобы возвращалось дерево 0 уровня
        request = self.factory.get("/?test-menu=100")
        context = RequestContext(request)

        test_result = {
            "filtered_tree_menu_data": None,
            "slug_menu": "test-menu",
            "name_menu": "Test Menu",
            "menu_item_id": 100,
            "params_url": "",
        }

        result = draw_menu(context, "test-menu")
        self.assertEqual(result, test_result)
