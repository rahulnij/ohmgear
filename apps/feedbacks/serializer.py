from django.conf.urls import url, include
from rest_framework import routers, serializers, viewsets

from models import Feedbacks, FeedbackCategory, FeedbackCategorySubject, ContactUs


class FeedbacksSerializer(serializers.ModelSerializer):

    class Meta:
        model = Feedbacks


class FeedbackCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedbackCategory


class FeedbackCategorySubjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = FeedbackCategorySubject


class ContactusSerializer(serializers.ModelSerializer):

    class Meta:
        model = ContactUs
