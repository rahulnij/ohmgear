from rest_framework.test import APITestCase, APIClient
from apps.users.functions import getToken

# Test api : create business card


class EmailCase(APITestCase):
    client = APIClient()

    fixtures = ['default']
    
    user_token = ''

    user_id = 0

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
        self.user_token = getToken(response.data["data"]["id"])
        self.user_id = response.data["data"]["id"]
        """ End """


    def test_send_emai_to_user(self):
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token),
        }
        """ call business list api """
        response = self.client.post('/api/profile/%s/' 
			% (self.user_id), '', format='json')
        print response
        self.assertEqual(response.status_code, 200)

