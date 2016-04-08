from django.shortcuts import render
from rest_framework import routers, serializers, viewsets
from models import Feedbacks, FeedbackCategory, FeedbackCategorySubject, ContactUs
from serializer import FeedbacksSerializer, FeedbackCategorySerializer, FeedbackCategorySubjectSerializer, ContactusSerializer
from ohmgear.functions import CustomeResponse
import rest_framework.status as status

from ohmgear.token_authentication import ExpiringTokenAuthentication
from rest_framework.permissions import IsAuthenticated


# Create your views here.
class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedbacks.objects.all()
    serializer_class = FeedbacksSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        userid = request.user.id
        tempData = request.data.copy()
        tempData['user_id'] = userid
        serializer = FeedbacksSerializer(
            data=tempData, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return CustomeResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)


class FeedbackCategoryViewSet(viewsets.ModelViewSet):
    queryset = FeedbackCategory.objects.all()
    serializer_class = FeedbackCategorySerializer

    def list(self, request):
        queryset = self.queryset
        serializer = FeedbackCategorySerializer(queryset, many=True)
        if queryset:
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)


class FeedbackCategorySubjectViewSet(viewsets.ModelViewSet):
    queryset = FeedbackCategorySubject.objects.all()
    serializer_class = FeedbackCategorySubjectSerializer

    def list(self, request, pk=None):
        queryset = self.queryset
        category_id = self.request.QUERY_PARAMS.get('category_id', None)

        if category_id is not None:
            queryset = FeedbackCategorySubject.objects.filter(
                feedback_category_id=category_id)
            if not queryset:
                return CustomeResponse({"msg": "Category id not found"}, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)
        serializer = FeedbackCategorySubjectSerializer(queryset, many=True)

        if queryset:
            return CustomeResponse(serializer.data, status=status.HTTP_200_OK)
        else:
            return CustomeResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST, validate_errors=1)


class ContactusViewSet(viewsets.ModelViewSet):
    queryset = ContactUs.objects.all()
    serializer_class = ContactusSerializer
    authentication_classes = (ExpiringTokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def create(self, request):
        userid = request.user.id
        tempData = {}
        mutable = request.POST._mutable
        request.POST._mutable = True
        request.POST['user_id'] = userid
        serializer = ContactusSerializer(
            data=request.data, context={'request': request})

        if serializer.is_valid():
            serializer.save()
            return CustomeResponse(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return CustomeResponse(serializer.errors, status=status.HTTP_201_CREATED)
