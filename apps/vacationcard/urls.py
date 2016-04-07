from django.conf.urls import url, include
import views


urlpatterns = [
    url(r'^vacationcard/merge$', views.VacationCardMerge.as_view(),
        name='vacationcard_merge')
]
