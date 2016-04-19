from rest_framework.test import APITestCase, APIClient
from apps.users.functions import getToken
from apps.users.models import Profile
# Test api : create business card


class UserSettingsTestCase(APITestCase):
    client = APIClient()

    fixtures = ['default', 'usersetting']

    user_token = ''

    def setUp(self):
        """ create the user and get the token """
        url = '/api/users/'
        data = {
            "first_name": "sazid",
            "email": "test@kinbow.com",
            "password": "1111",
            "user_type": 2,
            "status": 1}
        response = self.client.post(url, data, format='json')
        self.user_token = getToken(response.data["data"]["id"])
        """ End """

        """ Get the activation code by using profile Model and call user activity api"""
        profile_obj = Profile.objects.get(user_id=response.data["data"]["id"])
        activation_key = profile_obj.activation_key

        url = '/api/useractivity/?activation_key=%s' % (activation_key)
        response = self.client.get(
            url, {"activation_key": activation_key}, format='json')
        """ End """

    def test_list_user_setting(self):

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token),
        }
        """ call user setting api """
        response = self.client.get(
            '/api/usersetting/', '', format='json', **auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_getsettingvalue(self):

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token),
        }

        """ call user setting api to get setting key value """
        response = self.client.post('/api/usersetting/getsettingvalue/',
                                    {"key": "DISPLAY_CONTACT_NAME_AS"},
                                    format='json',
                                    **auth_headers)

        self.assertEqual(response.status_code, 200)
