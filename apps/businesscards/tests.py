from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from apps.users.models import User, UserType
from apps.users.functions import getToken
from apps.email.models import EmailTemplate
from apps.businesscards.models import BusinessCardTemplate
import json


class UserTests(APITestCase):
    client = APIClient()

    #---------------------- First Insert the default value -------------------------------#
    #fixtures = ['usertype']
    def setUp(self):
          #----------------------- Insert the INITIAL DATA ---------------------------------#
        #----------------------- Insert User Type --------------------------#
        UserType.objects.create(id=1, user_type="Admin")
        usertype = UserType.objects.create(id=2, user_type="Individual")
        UserType.objects.create(id=3, user_type="Corporate")
        #-------------------------------------------------------------------#
        EmailTemplate.objects.create(subject='account confirmation', content='ddddddd', slug='account_confirmation',
                                     status='True', from_email='', created_date='2015-09-03 00:00:00', updated_date='2015-09-03 00:00:00')
        #------------------------- Insert first user to check login --------#
        User.objects.create(
            first_name='sazid', email='sazidk@clavax.us', status=1, user_type=usertype)
        user = User.objects.get(email='sazidk@clavax.us')
        user.set_password('1111')
        user.save()
        #--------------------------------------------------------------------#
        #--------- insert business card template ----------------------------#
        BusinessCardTemplate.objects.create(
            template_name='test', template_content='testt')
   #-------------------------------------------------------------------------------------#

    def test_create_business_card(self):
        user = User.objects.get(email='sazidk@clavax.us')
        Token = getToken(user.id)
        #----------- insert template -------------------#

        #-----------------------------------------------#
        data = {"bcard_json_data": '{"side_second": {"card_name": "first","language":"eq", "personal_info": {"nick_name": "", "name": "sdf"}, "organization_info": {"company": "", "title": ""}, "contact_info": {"phone": "", "skype_id": "", "email": "", "address": ""}}, "side_first": {"card_name": "test","language":"df", "personal_info": {"nick_name": "", "name": ""}, "organization_info": {"company": "", "title": ""}, "contact_info": {"phone": "", "skype_id": "", "email": "", "address": ""}}}', "template": 1, "user": user.id}
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(Token),
        }
        response = self.client.post(
            '/api/businesscard/', data, format='json', **auth_headers)
        self.assertEqual(response.status_code, 201)
