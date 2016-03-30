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
    #url(r'^docs/', include('rest_framework_swagger.urls')),
   # url(r'^grappelli/', include('grappelli.urls')), 
    #url(r'^jet/', include('jet.urls', 'jet')),  # Django JET URLS
    #url(r'^jet/dashboard/', include('jet.dashboard.urls', 'jet-dashboard')), 
    url(r'^api/', include('apps.users.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api/', include('apps.userlocation.urls')),
    url(r'^api/', include('apps.vacationcard.urls')),
    url(r'^api/useractivity/$','apps.users.views.useractivity',name='useractivity'),
    #url(r'^api/cron/$','apps.cron.views.updateidentifierstatus',name='updateidentifierstatus'),
    url(r'^api/account_confirmation/(?P<activation_key>\w+)/$','apps.users.views.useractivity',name='registration_confirm'),
    url(r'^api/forgot_password/(?P<reset_password_key>\w+)/$','apps.users.views.useractivity',name='forgot_password'),
    #url(r'^users/emails/verify_email/(?P<activation_code>\w+)/$', 'apps.users.views.UserEmailViewSet',name='verify_email')
)
from apps.users.signals import *
import apps.businesscards.views as  businesscards_views
#-------------- End ---------------------------------------------#

#-------------- Business app url registration ----------------------#
router.register(r'api/businesscard', businesscards_views.BusinessViewSet)
#------------------BusinessCard Idnetifier-----------------------#
import apps.businesscards.views as businesscardidentifier_views
router.register(r'api/businesscardidentifier',businesscards_views.BusinessCardIdentifierViewSet)

#-------------- Business card Media  ----------------------#
#router.register(r'api/businesscardmedia', businesscards_views.BusinessCardMediaViewSet)

#-------------- Add Skills ----------------------#
router.register(r'api/businesscardaddskill', businesscards_views.BusinessCardAddSkillViewSet)

#-------------- Available Skills in the database  ----------------------#
router.register(r'api/businesscardskillavailable', businesscards_views.BusinessCardSkillAvailableViewSet)

#-------------- Business card Summary  ----------------------#
#router.register(r'api/businesscardsummary', businesscards_views.CardSummary)
urlpatterns += [
    url(r'^api/businesscardsummary/$', businesscards_views.CardSummary.as_view()),    
]

#-------------- End ---------------------------------------------#

#-------------- BusinessCard History  ----------------------#
import apps.businesscards.views as  businesscards_views
router.register(r'api/businesscardshistory', businesscards_views.BusinessCardHistoryViewSet)
#-------------- End ---------------------------------------------#


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
#----------Contact media------------------------#
router.register(r'api/contactmedia', contacts_views.ContactMediaViewSet)
#
#urlpatterns += [
#    url(r'api/upload_contacs', contacts_views.storeContactsViewSet),    
#]
router.register(r'api/contacts',contacts_views.storeContactsViewSet)
#urlpatterns += format_suffix_patterns(urlpatterns)
#-------------- End ---------------------------------------------#


#-------------- folders app url registration ---------------------------------#
import apps.folders.views as folder_view
router.register(r'api/folder',folder_view.FolderViewSet)
#-------------- End: folders app ---------------------------------------------#


#---------------Vacation Card app url-------------------------------#
import apps.vacationcard.views as vacationcard_views
router.register(r'api/vacationcard',vacationcard_views.VacationCardViewSet)

#--------------Feedback App url-------------------------------------#
import apps.feedbacks.views as feebacks_views
router.register(r'api/feedbacks',feebacks_views.FeedbackViewSet)


import apps.feedbacks.views as feebackcategory_views
router.register(r'api/feedbackcategory',feebackcategory_views.FeedbackCategoryViewSet)

import apps.feedbacks.views as feebackcategorysubject_views
router.register(r'api/feedbackcategorysubject',feebackcategorysubject_views.FeedbackCategorySubjectViewSet)

import apps.feedbacks.views as contactus_views
router.register(r'api/contactus',contactus_views.ContactusViewSet)

#-----------------End-------------------------------------------------#

#---------------------userSetting------------------------------------#
import apps.usersetting.views as setting_views
router.register(r'api/usersetting',setting_views.UserSettingViewSet)

import apps.usersetting.views as languagesetting_views
router.register(r'api/languagesetting',languagesetting_views.LanguageSettingViewSet)

import apps.usersetting.views as displaycontactsetting_views
router.register(r'api/displaycontactsetting',displaycontactsetting_views.DisplayContactNameAsViewSet)


#----------------Businesscard Vacation url ---------------------------#
import apps.vacationcard.views as businesscardvacation_views
router.register(r'api/businesscardvacation',businesscardvacation_views.BusinessCardVacationViewSet)
#-----------------End-------------------------------------------------#

#-------------- Static pages url--- ---------------------------------#
import apps.staticpages.views as staticpages_view
router.register(r'api/staticpages',staticpages_view.StaticPagesViewSet)
#-------------- End: Stattic pages app ---------------------------------------------#

#----------------Group------------------------------------------------#
import apps.groups.views as groups_view
router.register(r'api/group',groups_view.GroupViewSet)
router.register(r'api/groupcontacts',groups_view.GroupContactsViewSet)


#----------------- Verification email -------------------------#

#router.register(r'api/emails', users_views.UserEmailViewSet,base_name='verify_email')
#router.register(r'api/emails/verify_email/(?P<activation_code>\w+)', users_views.UserEmailViewSet,'verify_email')

#--------------------- OFFLINE --------------------------------------#
import apps.offline.views as offline_view
router.register(r'api/offline',offline_view.OfflineSendReceiveDataViewSet)
#_-------------------------------------------------------------------#

#--------------------- CRON --------------------------------------#
import apps.cron.views as cron_view
router.register(r'api/cron/update_contact_link_status',cron_view.UpdateContactLinkStatusCron)
#_-------------------------------------------------------------------#

#--------------------- SEND REQUEST(NOTIFICATION) --------------------------------------#
import apps.sendrequest.views as notification_view
router.register(r'api/send_accept_request',notification_view.SendAcceptRequest)
router.register(r'api/sendrequest',notification_view.SendNotification)
import apps.sendrequest.views as grey_view
router.register(r'api/greyrequest',grey_view.GreyInvitationViewSet)
#_-------------------------------------------------------------------#
#_-------------------------------------------------------------------#


#--------------------- AWS Activity --------------------------------------#
from  apps.awsserver.views import AWSActivity
router.register(r'api/aws',AWSActivity)
#_-------------------------------------------------------------------#

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
    
#------------------------------------------------------------------------------------------------------ #


#handler404 = 'ohmgear.custom_exception_handler.custom404'
#handler500 = 'ohmgear.custom_exception_handler.custom404'
