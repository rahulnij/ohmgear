from django.conf.urls import include, url,patterns
from django.contrib import admin
import token_authentication as views
from rest_framework import routers
from rest_framework.urlpatterns import format_suffix_patterns

router = routers.DefaultRouter()

#-------------- Users app url registration ----------------------#
import apps.users.views as  users_views

router.register(r'api/users', users_views.UserViewSet)
router.register(r'api/profile', users_views.ProfileViewSet)
router.register(r'api/sociallogin',users_views.SocialLoginViewSet)
router.register(r'api/sociallogin',users_views.SocialLoginViewSet)
urlpatterns =patterns(
    '',    
    url(r'^api/useractivity/$','apps.users.views.useractivity',name='useractivity'),
    url(r'^api/account_confirmation/(?P<activation_key>\w+)/$','apps.users.views.useractivity',name='registration_confirm'),
    url(r'^api/forgot_password/(?P<reset_password_key>\w+)/$','apps.users.views.useractivity',name='forgot_password'),
)
#-------------- End ---------------------------------------------#

#-------------- Business app url registration ----------------------#
import apps.businesscards.views as  businesscards_views
router.register(r'api/businesscard', businesscards_views.BusinessViewSet)
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

urlpatterns += patterns('',
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += router.urls

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()
#handler404 = 'ohmgear.custom_exception_handler.custom404'
#handler500 = 'ohmgear.custom_exception_handler.custom404'
