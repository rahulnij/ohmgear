from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    url(r'', include('apps.awsserver.urls')),
    url(r'', include('apps.businesscards.urls')),
    url(r'', include('apps.contacts.urls')),
    url(r'', include('apps.cron.urls')),
    url(r'', include('apps.feedbacks.urls')),
    url(r'', include('apps.folders.urls')),
    url(r'', include('apps.groups.urls')),
    url(r'', include('apps.identifiers.urls')),
    url(r'', include('apps.notes.urls')),
    url(r'', include('apps.offline.urls')),
    url(r'', include('apps.sendrequest.urls')),
    url(r'', include('apps.staticpages.urls')),
    #url(r'', include('apps.userlocation.urls')),
    url(r'', include('apps.users.urls')),
    url(r'', include('apps.usersetting.urls')),
    url(r'', include('apps.vacationcard.urls')),
    url(r'^admin/', include(admin.site.urls))
    
]


from django.contrib.staticfiles.urls import staticfiles_urlpatterns
urlpatterns += staticfiles_urlpatterns()

#------------- Only on Development to server media files otherwise we will disable -------------#
from django.conf import settings
urlpatterns += [
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
]

