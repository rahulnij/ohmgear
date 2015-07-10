from django.conf.urls import include, url
from django.contrib import admin
from rest_framework.authtoken import views
urlpatterns = [
    # Examples:
    # url(r'^$', 'ohmgear.views.home', name='home'),
    #url(r'^blog/', include('blog.urls')),
    url(r'^api/', include('apps.users.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^api-token-auth/', views.obtain_auth_token)
]
