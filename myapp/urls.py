__author__ = 'jyoti'
from django.conf.urls import url, include
from myapp import views

urlpatterns = [
    url(r'^users/$', views.user_list),
    url(r'^users/(?P<pk>[0-9]+)/$', views.user_detail),
    url(r'^api-auth/',include('rest_framework.urls', namespace='rest_framework')),
]