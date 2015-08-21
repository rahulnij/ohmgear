from django.test import TestCase
from models import User

class User(TestCase):
    def setUp(self):
        User.objects.create(first_name="sazid",)
        User.objects.create(name="cat", sound="meow")

    def get_user(self):
        lion = Animal.objects.get(name="lion")
        cat = Animal.objects.get(name="cat")
        self.assertEqual(lion.speak(), 'The lion says "roar"')
        self.assertEqual(cat.speak(), 'The cat says "meow"')