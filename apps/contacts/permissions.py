from rest_framework import permissions


class IsUserContactData(permissions.BasePermission):
    def has_permission(self, request, view):
        print ">>>>>>"
        pass

    def has_object_permission(self, request, view, obj):
        print ">>>>>>>>>>>>>>>>>>>>>>"
        return request.user == obj.user_id
