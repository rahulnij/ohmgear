from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from ohmgear.functions import sql_select
from apps.users.models import User,UserType
from apps.email.models import EmailTemplate
from functions import getToken
## Test api : user registration
#           : user login
#           : social login
#           : forgot passoword

class UserTests(APITestCase):
  client = APIClient()

  fixtures = ['default']
  def setUp(self):
      pass
    
  def test_user_registration(self):
    url = '/api/users/'
    data = {"first_name":"sazid","email":"sazid.se@gmail.com","password":"1111","user_type":2,"status":1}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, 201)
    
  def test_user_login(self):

    url = '/api/useractivity/'
    data = {"op":"login","username":"sazid.se@gmail.com","password":"1111"}
    response = self.client.post(url, data)
    self.assertEqual(response.status_code, 200) 
     
  def test_social_login(self):

    url = '/api/sociallogin/'
    data = {"first_name":"sazid","email":"sazid.se1@gmail.com","status":1,"user_type":2}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, 201)
    
#  def test_profile(self):
#    user = User.objects.get(email='sazidk@clavax.us')
#    Token = getToken(user.id)
#    auth_headers = {
#    'Authorization': 'Token'+str(Token),
#    }
#    response = self.client.post('/api/profile/', **auth_headers)
#    
#    print response
