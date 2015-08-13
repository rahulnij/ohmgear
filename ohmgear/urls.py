from django.conf.urls import include, url
from django.contrib import admin
import token_authentication as views

urlpatterns = [
    # Examples:
    # url(r'^$', 'ohmgear.views.home', name='home'),
    #url(r'^blog/', include('blog.urls')),
    url(r'^api/', include('apps.users.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^token/', views.obtain_expiring_auth_token)
]
