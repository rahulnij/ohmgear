import json

from rest_framework.test import APITestCase, APIClient
from django.test import TestCase
from .models import(
    Contacts,
    ContactMedia,
    # FavoriteContact,
    # AssociateContact
)
from apps.businesscards.models import BusinessCard
from apps.users.models import User  # UserType
from apps.users.functions import getToken

# Test api : create business card


class ContactTestCase(APITestCase):
    client = APIClient()

    fixtures = ['default']
    
    user_token = ''

    contact_data = {}

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

        """ create contact """
        self.contact_data = {
    "contact": [{
        "bcard_json_data": {
            "side_first": {
                "basic_info": [{
                    "value": "MyBusinesscar",
                    "isUpper": "1",
                    "keyName": "CardName",
                    "indexPos": "0",
                    "placeHolder": "NAME THIS CARD (Required)"
                }, {
                    "value": "Detail Check",
                    "isUpper": "1",
                    "keyName": "FirstName",
                    "indexPos": "2",
                    "placeHolder": "First Name(Required)"
                }, {
                    "value": "sdfsdfsdfdsf",
                    "isUpper": "1",
                    "keyName": "LastName",
                    "indexPos": "3",
                    "placeHolder": "Last Name"
                }, {
                    "value": "sdfsdf",
                    "isUpper": "1",
                    "keyName": "NickName",
                    "indexPos": "4",
                    "placeHolder": "Nick Name Or Alias"
                }, {
                    "value": "asfasf",
                    "isUpper": "1",
                    "keyName": "DEPTName",
                    "indexPos": "5",
                    "placeHolder": "Title & Department"
                }, {
                    "value": "zvzxvx",
                    "isUpper": "1",
                    "keyName": "CompName",
                    "indexPos": "6",
                    "placeHolder": "Company Name"
                }],
                "contact_info": {
                    "email": [{
                        "data": "hhhhh@fff.fff1",
                        "type": "home"
                    }, {
                        "data": "sdfsdf1@asfasfa.khk",
                        "type": "work"
                    }, {
                        "data": "asdfas1@wee.qeq",
                        "type": "iCloud"
                    }],
                    "phone": [{
                        "data": "(122) 222-221",
                        "type": "home",
                        "countryCode": "+93",
                        "countryFlag": "AF"
                    }, {
                        "data": "(yyy) yyy-yyy1",
                        "type": "work",
                        "countryCode": "+93",
                        "countryFlag": "AF"
                    }]
                }
            },
            "side_second": {
                "contact_info": {
                    "email": [{
                        "data": "sec_12341@asf.dfsas",
                        "type": "home"
                    }, {
                        "data": "sec_12351@adds.fghf",
                        "type": "work"
                    }, {
                        "data": "asdfas1@gaff.utyu",
                        "type": "iCloud"
                    }],
                    "phone": [{
                        "data": "sec_12341",
                        "type": "home",
                        "countryCode": "+93",
                        "countryFlag": "AF"
                    }, {
                        "data": "1234123412341",
                        "type": "home",
                        "countryCode": "+93",
                        "countryFlag": "AF"
                    }]
                }
            }
        }
    }]
}
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token)
        }
        response = self.client.post(
            '/api/contacts/uploads/', json.loads(json.dumps(self.contact_data)), format='json', **auth_headers)        
        """ End """

    def test_contact_list(self):
        
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token),
        }
        """ call business list api """
        response = self.client.get(
            '/api/contacts/', '', format='json', **auth_headers)
        self.assertEqual(response.status_code, 200)

    def test_contact_delete(self):
        pass    


class TestContactModel(TestCase):
    def setUp(self):
        self.user = User(
            email="joe@test.com",
            password="qwerty"
        )
        self.user.save()
        self.biz_card = BusinessCard(user_id=self.user)
        self.biz_card.save()
        self.contact = Contacts(businesscard_id=self.biz_card,
            user_id=self.user)
        self.contact.save()

    def test_user_create(self):
        self.assertIsInstance(self.user, User)

    def test_contact_create(self):
        self.assertIsInstance(self.biz_card, BusinessCard)
        contact = Contacts(businesscard_id=self.biz_card)
        # contact.save()
        self.assertIsInstance(contact, Contacts)

    def test_contact_media_create(self):
        contact_media = ContactMedia(user_id=self.user,
            contact_id=self.contact, 
            img_url=''
        )	
        self.assertIsInstance(contact_media, ContactMedia)

    def tearDown(self):
        self.user.delete()
        self.biz_card.delete()
        self.contact.delete()
