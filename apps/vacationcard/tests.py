from rest_framework.test import APITestCase, APIClient
from apps.users.functions import getToken
from apps.users.models import Profile
# Test api : create business card


class VacationCardTestCase(APITestCase):
    client = APIClient()

    fixtures = ['default']

    user_token = ''

    vacation_card_data = ''

    vacation_card_id = 0

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

        """ Create the vacation card """
        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token)
        }

        self.vacation_card_data = {
            "vacation_name": "Us vacation",
            "vacation_trips": [
                {
                    "country": "india",
                    "vacation_type": "confrence",
                    "contact_no": "8800362589",
                    "state": "Haryana",
                    "city": "gurgaon",
                    "notes": "hsfdjdfjfsed",
                    "trip_start_date": "2016-08-10",
                    "trip_end_date": "2016-11-28"}]}

        url = '/api/vacationcard/'
        response = self.client.post(
            url, self.vacation_card_data, format='json', **auth_headers)
        self.vacation_card_id = response.data["data"][0]["vacationcard_id"]

        """ End """

    def test_list_of_vacation_card(self):

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token),
        }
        """ call vacation card api list """
        response = self.client.get(
            '/api/vacationcard/', '', format='json', **auth_headers)

        self.assertEqual(response.status_code, 200)

    def test_update_vacation_card(self):

        auth_headers = {
            'HTTP_AUTHORIZATION': 'Token ' + str(self.user_token),
        }

        """ call update vacation card """
        response = self.client.put(
            '/api/vacationcard/%s/' %
            (self.vacation_card_id),
            self.vacation_card_data,
            format='json',
            **auth_headers)

        self.assertEqual(response.status_code, 200)
