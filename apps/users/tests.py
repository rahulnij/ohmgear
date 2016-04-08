from rest_framework.test import APITestCase, APIClient
# Test api : user registration
#           : user login
#           : social login


class UserTests(APITestCase):
    client = APIClient()

    fixtures = ['default']

    def setUp(self):
        url = '/api/users/'
        data = {
            "first_name": "sazid",
            "email": "test@kinbow.com",
            "password": "1111",
            "user_type": 2,
            "status": 1}
        response = self.client.post(url, data, format='json')

    def test_user_login(self):

        url = '/api/useractivity/'
        data = {
            "op": "login",
            "username": "test@kinbow.com",
            "password": "1111"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 200)

    def test_social_login(self):

        url = '/api/sociallogin/'
        data = {
            "first_name": "sazid",
            "email": "test1@kinbow.com",
            "status": 1,
            "user_type": 2,
            "social_type": "FB"}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, 201)
