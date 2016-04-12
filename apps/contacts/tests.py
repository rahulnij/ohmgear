from django.test import TestCase
from .models import(
    Contacts,
    ContactMedia,
    FavoriteContact,
    AssociateContact
)
from apps.businesscards.models import BusinessCard
from apps.users.models import User, UserType


class TestContactModel(TestCase):
    def setUp(self):
        # self.user_type = UserType(7)
        # self.user_type.save()
        self.user = User(
            email="joe@test.com",
            password="qwerty"
        )
        self.user.save()

    def test_user_create(self):
        self.assertIsInstance(self.user, User)

    def test_contact_create(self):
        biz_card = BusinessCard(user_id=self.user)
        biz_card.save()
        self.assertIsInstance(biz_card, BusinessCard)
        contact = Contacts(businesscard_id=biz_card)
        # contact.save()
        self.assertIsInstance(contact, Contacts)

    def test_contact_media_create(self):
        biz_card = BusinessCard(user_id=self.user)
        contact = Contacts(businesscard_id=biz_card)
        contact_media = ContactMedia(user_id=self.user,
            contact_id=contact, img_url='')
        self.assertIsInstance(contact_media, ContactMedia)
