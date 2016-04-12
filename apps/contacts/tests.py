from django.test import TestCase
from .models import(
    Contacts,
    ContactMedia,
    # FavoriteContact,
    # AssociateContact
)
from apps.businesscards.models import BusinessCard
from apps.users.models import User  # UserType


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
            contact_id=self.contact, img_url='')
        self.assertIsInstance(contact_media, ContactMedia)

    def tearDown(self):
        self.user.delete()
        self.biz_card.delete()
        self.contact.delete()