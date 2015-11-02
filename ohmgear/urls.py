from django.conf.urls import include, url,patterns
from django.contrib import admin
import token_authentication as views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

admin.site.site_header = 'ohmgear'

router = routers.DefaultRouter()

#-------------- test app for local testing ----------------------#
from apps.test_purposes.test_view import  FtestViewSet
router.register(r'api/test_purposes', FtestViewSet)
#-------------- End ---------------------------------------------#

#-------------- Users app url registration ----------------------#
import apps.users.views as  users_views

router.register(r'api/users', users_views.UserViewSet)
router.register(r'api/profile', users_views.ProfileViewSet)
router.register(r'api/sociallogin',users_views.SocialLoginViewSet)
router.register(r'api/sociallogin',users_views.SocialLoginViewSet)
urlpatterns =patterns(
    '',  
   # url(r'^grappelli/', include('grappelli.urls')), 
    url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')), 
 
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/useractivity/$','apps.users.views.useractivity',name='useractivity'),
    url(r'^api/cron/$','apps.cron.views.updateidentifierstatus',name='updateidentifierstatus'),
    url(r'^api/account_confirmation/(?P<activation_key>\w+)/$','apps.users.views.useractivity',name='registration_confirm'),
    url(r'^api/forgot_password/(?P<reset_password_key>\w+)/$','apps.users.views.useractivity',name='forgot_password'),
)
from apps.users.signals import *
#-------------- End ---------------------------------------------#

#-------------- Business app url registration ----------------------#
import apps.businesscards.views as  businesscards_views
router.register(r'api/businesscard', businesscards_views.BusinessViewSet)
#-------------- End ---------------------------------------------#


#------------------BusinessCard Idnetifier-----------------------#
import apps.businesscards.views as businesscardidentifier_views
router.register(r'api/businesscardidentifier',businesscardidentifier_views.BusinessCardIdentifierViewSet)
#----------------End---------------------------------------------#

#-------------- Identifiers app url ----------------------#
import apps.identifiers.views as  identifiers_views
router.register(r'api/identifiers', identifiers_views.IdentifierViewSet)
#-------------- End ---------------------------------------------#


#-------------- Notes app url registration ----------------------#
import apps.notes.views as  notes_views
router.register(r'api/notes', notes_views.NotesViewSet)
#-------------- End ---------------------------------------------#


#-------------- Contacts app url registration ----------------------#
import apps.contacts.views as  contacts_views

urlpatterns += [
    url(r'^api/upload_contacs/$', contacts_views.storeContacts),    
]

urlpatterns += format_suffix_patterns(urlpatterns)
#-------------- End ---------------------------------------------#


#---------------Vacation Card app url-------------------------------#
import apps.vacationcard.views as vacationcard_views
router.register(r'api/vacationcard',vacationcard_views.VacationCardViewSet)
#---------------End ------------------------------------------------#


urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += router.urls

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

#------------- Only on Development to server media files otherwise we will disable -------------#
from django.conf import settings
urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
#handler404 = 'ohmgear.custom_exception_handler.custom404'
#handler500 = 'ohmgear.custom_exception_handler.custom404'
