from django.test import TestCase
import unittest
from PIL import Image
from StringIO import StringIO
from django.core.files.base import File
from apps.users.models import Profile
from apps.users.models import User
import datetime
from common.image_lib import resize_image
from django.conf import settings
import re


def create_image_file(name='test.png', ext='png', size=(5000, 5000), color=(256, 0, 0)):
    file_obj = StringIO()
    image = Image.new("RGBA", size=size, color=color)
    image.save(file_obj, ext)
    file_obj.seek(0)
    return File(file_obj, name=name)


class TestProfileImageResize(TestCase):
    def setUp(self):
        self.user = User(
            email="joe@test.com",
            password="qwerty"
        )
        self.user.save()
        self.profile = Profile(
            prefix="Mr",
            middle="Jim",
            suffix="Jr",
            first_name="Ben",
            last_name="Gilbertson",
            nick_name="Bengi",
            headline="Mr Bengil, Master of the Universe",
            dob=datetime.date(200, 1, 1),
            user=self.user,
            profile_image=create_image_file(),
            activation_key="ABCDEFGHIJK"
        )
        self.profile.save()

    # @unittest.skip("Takes too long, eats the CPU")
    def test_profile_valid(self):
        self.assertIsInstance(self.profile, Profile)
        self.assertTrue(self.profile.profile_image is not None)
        file_regex = re.compile(r'uploads/profile_img/test.*\.png')
        self.assertRegexpMatches(self.profile.profile_image.name, file_regex)
        # self.assertEqual(self.profile.profile_image.name, 'uploads/profile_img/test_*.png')

    # @unittest.skip("Takes Too Long, eats CPU")
    def test_profile_img_resize(self):
        path = settings.BASE_DIR + str(self.profile.profile_image.url)
        new_path = resize_image(path, 50, append_str="thumb")
        self.assertRegexpMatches(new_path, re.compile(r'.*thumb\.png'))
