from rest_framework import permissions
from apps.folders.models import FolderContact

import logging
# ---------------------------End------------- #
logger = logging.getLogger(__name__)


class IsUserContactData(permissions.BasePermission):

    def has_permission(self, request, view):
    	return True
        # if view.action == 'retrieve':
        # 	# included object level permission here
        #     try:
        #         obj.link = FolderContact.objects.get(contact_id=view.kwargs['pk'])
        #         if obj.link_status == 2 OR  
        #     except FolderContact.DoesNotExist as e:
        #         logger.errors(
        #             "Object Does Not Exist: FolderContact: {}, {}".format(
        #                 view.kwargs['pk'], e))
        #         return False

               

    # def check_object_permission(self, user, obj):
    #     return (user and user.is_authenticated() and
    #             (user.is_staff or obj == user))

    # def has_object_permission(self, request, view, obj):
    # 	print ">>>>>>>>>>>>>>>>>>>>>>>"
    #     return self.check_object_permission(request.user, obj)
