from rest_framework.test import APITestCase,APIClient
from apps.users.functions import getToken
from apps.users.models import User
# Test api : create business card


class AwsTests(APITestCase):
  client = APIClient()

  fixtures = ['default']
  
  def setUp(self):
    url = '/api/users/'
    data = {"first_name":"sazid","email":"test@kinbow.com","password":"1111","user_type":2,"status":1}
    response = self.client.post(url, data, format='json')
    
  def test_register_to_aws(self):
    """ TODO: Need valid device_token to run this test"""  
    pass
 
