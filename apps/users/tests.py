from django.core.urlresolvers import reverse
from rest_framework import status
from rest_framework.test import APITestCase,APIClient
from ohmgear.functions import sql_select
from apps.users.models import UserType
from apps.email.models import EmailTemplate
from apps.users.models import User
from functions import getToken
## Test api : user registration
#           : user login
#           : social login
#           : forgot passoword

class UserTests(APITestCase):
  client = APIClient()
  
  #---------------------- First Insert the default value -------------------------------#
  #fixtures = ['usertype']
  def setUp(self):      
        #----------------------- Insert the INITIAL DATA ---------------------------------#
            #----------------------- Insert User Type --------------------------#
            UserType.objects.create(id=1,user_type="Admin")
            usertype=UserType.objects.create(id=2,user_type="Individual")
            UserType.objects.create(id=3,user_type="Corporate")
            #-------------------------------------------------------------------#
            EmailTemplate.objects.create(subject='account confirmation', content='ddddddd',slug='account_confirmation',status='True',from_email='',created_date='2015-09-03 00:00:00',updated_date='2015-09-03 00:00:00')
            #------------------------- Insert first user to check login --------#            
            User.objects.create(first_name='sazid',email='sazidk@clavax.us',status=1,user_type=usertype)
            user = User.objects.get(email='sazidk@clavax.us')
            user.set_password('1111')
            user.save()
            #--------------------------------------------------------------------#
       #-------------------------------------------------------------------------------------#
    
  def test_user_login(self):

    url = '/api/useractivity/'
    data = {"op":"login","username":"sazidk@clavax.us","password":"1111"}
    response = self.client.post(url, data)
    self.assertEqual(response.status_code, 200) 
     
  def test_social_login(self):

    url = '/api/sociallogin/'
    data = {"first_name":"sazid","email":"sazid.se1@gmail.com","status":1,"user_type":2}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, 201)

    
  def test_user_registration(self):

    url = '/api/users/'
    data = {"first_name":"sazid","email":"sazid.se@gmail.com","password":"1111","user_type":2}
    response = self.client.post(url, data, format='json')
    self.assertEqual(response.status_code, 201)
    
    
  def test_profile(self):
    user = User.objects.get(email='sazidk@clavax.us')
    Token = getToken(user.id)
    auth_headers = {
    'Authorization': 'Token'+str(Token),
    }
    response = self.client.post('/api/profile/', **auth_headers)
    
    print response
#    url = '/api/profile/'
#    data = {"user_id":user.id}
#    response = self.client.post(url, data, format='json')
    #self.assertEqual(response.status_code, 201)