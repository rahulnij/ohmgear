from rest_framework.test import APITestCase, APIClient
from apps.users.functions import getToken
# Test api : create business card


class SendRequestTestCase(APITestCase):
    client = APIClient()

    fixtures = ['default']

    sender_user_token = ''
    receiver_user_token = ''

    sender_business_card_id = ''
    receiver_business_card_id = ''

    business_card_data = {}

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
        self.sender_user_token = getToken(response.data["data"]["id"])

        data = {
            "first_name": "sazid",
            "email": "test1@kinbow.com",
            "password": "1111",
            "user_type": 2,
            "status": 1}
        response = self.client.post(url, data, format='json')

        self.receiver_user_token = getToken(response.data["data"]["id"])

        """ End """

        """ create two business card """

        self.business_card_data = {"bcard_json_data": '{"side_first": {"basic_info": [{"value": "MyBusinesscar", "isUpper": "1", "keyName": "CardName", "indexPos": "0", "placeHolder": "NAME THIS CARD (Required)"}, {"value": "Detail Check", "isUpper": "1", "keyName": "FirstName", "indexPos": "2", "placeHolder": "First Name(Required)"}, {"value": "sdfsdfsdfdsf", "isUpper": "1", "keyName": "LastName", "indexPos": "3", "placeHolder": "Last Name"}, {"value": "sdfsdf", "isUpper": "1", "keyName": "NickName", "indexPos": "4", "placeHolder": "Nick Name Or Alias"}, {"value": "asfasf", "isUpper": "1", "keyName": "DEPTName", "indexPos": "5", "placeHolder": "Title & Department"}, {"value": "zvzxvx", "isUpper": "1", "keyName": "CompName", "indexPos": "6", "placeHolder": "Company Name"}], "contact_info": {"email": [{"data": "hhhhh@fff.fff1", "type": "home"}, {"data": "sdfsdf1@asfasfa.khk", "type": "work"}, {"data": "asdfas1@wee.qeq", "type": "iCloud"}], "phone": [{"data": "(122) 222-221", "type": "home", "countryCode": "+93", "countryFlag": "AF"}, {"data": "(yyy) yyy-yyy1", "type": "work", "countryCode": "+93", "countryFlag": "AF"}]}}, "side_second": {"contact_info": {"email": [{"data": "sec_12341@asf.dfsas", "type": "home"}, {"data": "sec_12351@adds.fghf", "type": "work"}, {"data": "asdfas1@gaff.utyu", "type": "iCloud"}], "phone": [{"data": "sec_12341", "type": "home", "countryCode": "+93", "countryFlag": "AF"}, {"data": "1234123412341", "type": "home", "countryCode": "+93", "countryFlag": "AF"}]}}}'}

        auth_headers = {'HTTP_AUTHORIZATION': 'Token ' +
                        str(self.sender_user_token)}
        response = self.client.post(
            '/api/businesscard/',
            self.business_card_data,
            format='json',
            **auth_headers)

        self.sender_business_card_id = response.data["data"]["id"]

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.receiver_user_token)
        }

        response = self.client.post(
            '/api/businesscard/',
            self.business_card_data,
            format='json',
            **auth_headers)

        self.receiver_business_card_id = response.data["data"]["id"]
        """ End """

    def test_accept_businesscard(self):

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.sender_user_token),
        }

        """ call accept_businesscard api """

        data = {
            "receiver_business_card_id": self.receiver_business_card_id,
            "sender_business_card_id": self.sender_business_card_id}

        response = self.client.post(
            '/api/send_accept_request/accept_businesscard/', data,
            format='json',
            **auth_headers)

        # Now check the request status 
        # Not yet api implemented 
        # End  
        self.assertEqual(response.status_code, 200)
