from rest_framework.test import APITestCase, APIClient
from apps.users.functions import getToken
from apps.email.views import BaseSendMail
# Test api : create business card


class EmailCase(APITestCase):
    client = APIClient()

    fixtures = ['default']

    user_data = 0

    def setUp(self):
        """ create the user and get the token """
        url = '/api/users/'
        data = {
            "first_name": "sazid",
            "email": "sazidk@clavax.us",
            "password": "1111",
            "user_type": 2,
            "status": 1}
        response = self.client.post(url, data, format='json')
        self.user_data = response.data["data"]
        """ End """

    def test_send_emai_to_user(self):

        """ send mail to created user """
        send_mail = BaseSendMail.delay(
            self.user_data,
            type='test_email')
        self.assertEqual(send_mail.state, 'PENDING')
