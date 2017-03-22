from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls import url
from datasets import views

urlpatterns = format_suffix_patterns([
    # Datasets
    url(r'^datasets/$', views.DatasetList.as_view(), name='dataset-list'),
    url(r'^datasets/(?P<pk>[0-9]+)/$', views.DatasetDetail.as_view(), name='dataset-detail'),

    # Personal Datasets
    url(r'^datasets/personal/(?P<dataset>[0-9]+)/$', views.PersonalDatasetCreate.as_view(), 
        name='personal-create'),
    url(r'^personal/$', views.PersonalDatasetList.as_view(), name='personal-list'),
    url(r'^personal/(?P<pk>[0-9]+)/$', views.PersonalDatasetDetail.as_view(), name='personal-detail'),
    
    # Users
    url(r'^users/$', views.UserList.as_view(), name='user-list'),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view(), name='user-detail'),

    # Rating
    url(r'^datasets/rate/(?P<dataset>[0-9]+)/$', views.RatingList.as_view(), name='rating-list'),
    url(r'^ratings/(?P<pk>[0-9]+)/$', views.RatingDetail.as_view(), name='rating-detail'),

    # Searches
    url(r'^search/users/(?P<username>.+)/$', views.DatasetByUser.as_view(), name='search-users'),
    url(r'^search/title/(?P<title>.+)/$', views.DatasetByName.as_view(), name='search-title'), 

    # Feed - need to check if this is really working
    url(r'^discover/$', views.DiscoverFeed.as_view(), name='discover-feed'),

    # Testing operations
    url(r'^personal/operation/(?P<op>[0-9]+)/(?P<pk>[0-9]+)/$', views.PersonalOperation.as_view()),
])

urlpatterns += [ 
    # Change this to follow MEDIA_URL
    url(r'^media/(?P<pk>[0-9]+)/$', views.DatasetServeById.as_view(), name='media-dataset'),
    url(r'^media/(?P<filename>.+)/$', views.DatasetServeByFilename.as_view(), name='media-filename'),
]
