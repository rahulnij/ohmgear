from rest_framework.test import APITestCase, APIClient
from django.http import HttpRequest

from apps.businesscards.views import BusinessViewSet
from apps.users.functions import getToken
from apps.users.models import User
# Test api : create business card


class BusinessCardTestCase(APITestCase):
    client = APIClient()

    fixtures = ['default']

    user_token = ''

    business_card_id = ''

    business_card_data = {}

    def setUp(self):
        """ create the user and get the token """
        url = '/api/users/'
        user_info = {
            "email": "test1@kinbow.com",
            "password": "111111",
            "status": 1
        }
        self.user = User(**user_info)
        self.user.save()
        # response = self.client.post(url, data, format='json')
        self.user_token = getToken(self.user.id)

        """ End """

        """ create the business card """
        self.business_card_data = {"bcard_json_data": '{"side_first": {"basic_info": [{"value": "MyBusinesscar", "isUpper": "1", "keyName": "CardName", "indexPos": "0", "placeHolder": "NAME THIS CARD (Required)"}, {"value": "Detail Check", "isUpper": "1", "keyName": "FirstName", "indexPos": "2", "placeHolder": "First Name(Required)"}, {"value": "sdfsdfsdfdsf", "isUpper": "1", "keyName": "LastName", "indexPos": "3", "placeHolder": "Last Name"}, {"value": "sdfsdf", "isUpper": "1", "keyName": "NickName", "indexPos": "4", "placeHolder": "Nick Name Or Alias"}, {"value": "asfasf", "isUpper": "1", "keyName": "DEPTName", "indexPos": "5", "placeHolder": "Title & Department"}, {"value": "zvzxvx", "isUpper": "1", "keyName": "CompName", "indexPos": "6", "placeHolder": "Company Name"}], "contact_info": {"email": [{"data": "hhhhh@fff.fff1", "type": "home"}, {"data": "sdfsdf1@asfasfa.khk", "type": "work"}, {"data": "asdfas1@wee.qeq", "type": "iCloud"}], "phone": [{"data": "(122) 222-221", "type": "home", "countryCode": "+93", "countryFlag": "AF"}, {"data": "(yyy) yyy-yyy1", "type": "work", "countryCode": "+93", "countryFlag": "AF"}]}}, "side_second": {"contact_info": {"email": [{"data": "sec_12341@asf.dfsas", "type": "home"}, {"data": "sec_12351@adds.fghf", "type": "work"}, {"data": "asdfas1@gaff.utyu", "type": "iCloud"}], "phone": [{"data": "sec_12341", "type": "home", "countryCode": "+93", "countryFlag": "AF"}, {"data": "1234123412341", "type": "home", "countryCode": "+93", "countryFlag": "AF"}]}}}'}
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token)
        }
        response = self.client.post(
            '/api/businesscard/',
            self.business_card_data,
            format='json',
            **auth_headers)
        self.business_card_id = response.data["data"]["id"]

        """ End """

    def test_list_business_card(self):

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token),
        }
        """ call business list api """
        response = self.client.get(
            '/api/businesscard/', '', format='json', **auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_update_business_card(self):
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token),
        }
        response = self.client.put(
            '/api/businesscard/%s/' %
            (self.business_card_id),
            self.business_card_data,
            format='json',
            **auth_headers)

        self.assertEqual(response.status_code, 200)

    def test_set_default_businesscard(self):

        request = HttpRequest()
        request.user = self.user
        business_view_set = BusinessViewSet()
        request.query_params = {}
        request.query_params['bcard_id'] = self.business_card_id
        response = business_view_set.setdefault(request)
        self.assertEqual(response.status_code, 200)

    def test_set_default_invalid_businesscard_id(self):

        request = HttpRequest()
        request.user = self.user
        business_view_set = BusinessViewSet()
        request.query_params = {}
        request.query_params['bcard_id'] = 1000000
        response = business_view_set.setdefault(request)
        self.assertEqual(response.status_code, 400)

    def test_merge_business_cards(self):
        pass
