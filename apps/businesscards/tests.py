from StringIO import StringIO
from PIL import Image
from django.core.files.base import File
from rest_framework.test import APITestCase, APIClient
from django.http import HttpRequest

from apps.businesscards.views import BusinessViewSet
from apps.users.functions import getToken
from apps.users.models import User
# Test api : create business card


def create_image_file(
    name='test.png', ext='png', size=(
        5000, 5000), color=(
            5, 150, 100)):
    file_obj = StringIO()
    image = Image.new("RGBA", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


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

    def test_create_quick_business_card(self):
        # in case of quick_business_card random json data will accept means no
        # validation on business_card_data
        business_card_data = {"test": "ddd"}
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token),
        }
        data = {
            "business_card_data": business_card_data,
            "quick_business_card": True

        }
        response = self.client.post(
            '/api/businesscard/',
            data,
            format='json',
            **auth_headers)
        try:
            self.business_card_id = response.data["data"]["id"]
        except:
            response.status_code = 400

        self.assertEqual(response.status_code, 201)


    def test_bcard_logo(self):
        request = HttpRequest()
        request.user = self.user
        business_view_set = BusinessViewSet()
        request.data = {}
        request.data['card_logo'] = create_image_file()
        request.data['businesscard_id'] = self.business_card_id
        response = business_view_set.upload_card_logo(request)
        self.assertEqual(response.status_code, 200)



    def test_invalidbcard_logo(self):
        request = HttpRequest()
        request.user = self.user
        business_view_set = BusinessViewSet()
        request.data = {}
        request.data['card_logo'] = create_image_file()
        request.data['businesscard_id'] = 50
        response = business_view_set.upload_card_logo(request)
        self.assertEqual(response.status_code, 400,"Business card not found")



