from django.test import TestCase, Client
from django.contrib.auth.models import User
from menu.models import Menu, MenuItem


class AdminMenuItemTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="admin",
            password="admin",
            is_superuser=True,
            is_staff=True,
        )
        self.client = Client()
        self.client.login(username="admin", password="admin")

        self.menu1 = Menu.objects.create(pk=30, title="Test Menu 1", slug="test-menu-1")
        self.menu2 = Menu.objects.create(title="Test Menu 2", slug="test-menu-2")
        self.menu_item1 = MenuItem.objects.create(
            title="Test Item 1",
            menu=self.menu1,
        )
        self.menu_item2 = MenuItem.objects.create(
            title="Test Item 2",
            menu=self.menu1,
            parent=self.menu_item1,
        )
        self.menu_item3 = MenuItem.objects.create(
            title="Test Item 3",
            menu=self.menu2,
        )

    def test_formfield_for_foreignkey(self):
        response = self.client.get(f"/admin/menu/menuitem/{self.menu_item1.id}/change/")

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, f'value="{self.menu_item1.id}"')
        self.assertContains(response, f'value="{self.menu_item2.id}"')
        self.assertNotContains(response, f'value="{self.menu_item3.id}"')

        response = self.client.get(f"/admin/menu/menuitem/{self.menu_item2.id}/change/")

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, f'value="{self.menu_item1.id}"')
        self.assertNotContains(response, f'value="{self.menu_item2.id}"')
        self.assertNotContains(response, f'value="{self.menu_item3.id}"')

    def test_get_readonly_fields(self):
        response = self.client.get(f"/admin/menu/menuitem/{self.menu_item1.id}/change/")

        self.assertEqual(response.status_code, 200)

        self.assertNotContains(response, "readonly")

        response = self.client.get(f"/admin/menu/menuitem/{self.menu_item2.id}/change/")

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "readonly")
