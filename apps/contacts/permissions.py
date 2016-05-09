from rest_framework import permissions


class IsUserContactData(permissions.BasePermission):
    def has_permission(self, request, view):
        print ">>>>>>"
        return True
    def get_object(self, request, obj, format):
        print self.check_object_permissions(self, request, view, obj)  
    def check_object_permissions(self, request, view, obj):
        print ">>>>>>>>>>>>>>>>>>>>>>"
        return request.user == obj.user_id
