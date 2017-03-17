from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from datasets import views

urlpatterns = format_suffix_patterns([
    # Datasets
    url(r'^datasets/$', views.DatasetList.as_view()),
    url(r'^datasets/(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view()),
    
    # Users
    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    # Rating
    url(r'^datasets/rate/(?P<dataset>[0-9]+)/$', views.RatingList.as_view()),
    url(r'^ratings/(?P<pk>[0-9]+)/$', views.RatingDetail.as_view()),

    # Searches
    url(r'^search/users/(?P<username>.+)/$', views.DatasetByUser.as_view()),
    url(r'^search/title/(?P<title>.+)/$', views.DatasetByName.as_view()), 

    # Feed - need to check if this is really working
    url(r'^discover/$', views.DiscoverFeed.as_view()),
])

urlpatterns += [ 
    # Change this to follow MEDIA_URL
    url(r'^media/(?P<pk>[0-9]+)/$', views.DatasetServeById.as_view()),
    url(r'^media/(?P<filename>.+)/$', views.DatasetServeByFilename.as_view()),
]
