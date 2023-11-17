from django.core.exceptions import ValidationError
from django.test import TestCase

from menu.models import Menu, MenuItem


class MenuModelTest(TestCase):
    def test_menu_creation(self):
        menu = Menu.objects.create(title="Test Menu", slug="test-menu")
        self.assertEqual(menu.title, "Test Menu")
        self.assertEqual(menu.slug, "test-menu")

    def test_menu_str_representation(self):
        menu = Menu.objects.create(title="Test Menu", slug="test-menu")
        self.assertEqual(str(menu), "Test Menu")

    def test_menu_title_min_length_validator(self):
        with self.assertRaises(ValidationError):
            menu = Menu.objects.create(title="A", slug="test-menu")
            menu.full_clean()

    def test_menu_slug_validator(self):
        with self.assertRaises(ValidationError):
            menu = Menu.objects.create(title="Test Menu", slug="A)(   -l")
            menu.full_clean()

    def test_menu_slug_min_length_validator(self):
        with self.assertRaises(ValidationError):
            menu = Menu.objects.create(title="Test Menu", slug="A")
            menu.full_clean()


class MenuItemModelTest(TestCase):
    def setUp(self):
        self.menu1 = Menu.objects.create(title="Test Menu 1", slug="test-menu-1")
        self.menu2 = Menu.objects.create(title="Test Menu 2", slug="test-menu-2")
        self.menu_item1 = MenuItem.objects.create(
            title="Test Item 1",
            menu=self.menu1,
        )

    def test_menu_item_creation(self):
        menu_item2 = MenuItem.objects.create(
            title="Test Item 2",
            menu=self.menu1,
            parent=self.menu_item1,
        )
        self.assertEqual(menu_item2.title, "Test Item 2")
        self.assertEqual(menu_item2.menu, self.menu1)
        self.assertEqual(menu_item2.parent, self.menu_item1)

        menu_item2.clean()

    def test_menu_item_clean(self):
        with self.assertRaises(ValidationError):
            menu_item2 = MenuItem.objects.create(
                title="Test Item 2",
                menu=self.menu2,
                parent=self.menu_item1,
            )
            menu_item2.full_clean()

        with self.assertRaises(ValidationError):
            self.menu_item1.parent = self.menu_item1
            self.menu_item1.full_clean()

    def test_menu_item_str_representation(self):
        self.assertEqual(str(self.menu_item1), "Test Item 1")
