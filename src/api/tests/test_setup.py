from rest_framework.test import APITestCase
from django.urls import include, path, reverse


class TestSetup(APITestCase):
    def setUp(self):
        self.login_url = reverse("login")
        self.register_url = reverse("register")
        self.add_bond = reverse("add_bond")
        self.convert_bond_price = reverse("bond_price")

        self.user_data = {
            "username": "testuser",
            "email": "test@test.com",
            "password": "test@123",
            "password2": "test@123",
            "first_name": "Dev",
            "last_name": "Test",
        }

        self.bond_data = {
            "bond_type": "test_bond",
            "no_of_bonds": "22",
            "selling_price": "126890.2500",
        }

        return super().setUp()

    def tearDown(self):
        return super().tearDown()
