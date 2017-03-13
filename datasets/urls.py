from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from datasets import views

urlpatterns = format_suffix_patterns([
    url(r'^datasets/$', views.DatasetList.as_view()),
    url(r'^datasets/(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
])

urlpatterns += [
    url(r'^media/(?P<pk>[0-9]+)/$', views.DatasetServe.as_view()),
]
