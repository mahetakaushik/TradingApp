from .test_setup import TestSetup
from django.contrib.auth.models import User


class TestViews(TestSetup):
    def test_user_authentication(self):
        # User Registration Test
        res = self.client.post(self.register_url, self.user_data, format="json")
        email = res.data["email"]
        user = User.objects.get(email=email)
        user.is_verified = True
        user.save()

        # User Login Test
        self.response = self.client.post(self.login_url, self.user_data, format="json")
        token = self.response.data["access"]
        self.client.credentials(HTTP_AUTHORIZATION="Bearer " + token)
        # self.assertEqual(res.status_code, 201)

        # Add Bond Test
        res = self.client.post(self.add_bond, self.bond_data, format="json")
        # self.assertEqual(res.status_code, 201)

        # Convert USD Rate  Test
        res = self.client.put(self.convert_bond_price, format="json")
        # self.assertEqual(res.status_code, 200)

        # Get All Bond
        res = self.client.get(self.add_bond, format="json")
        self.assertEqual(res.status_code, 200)
