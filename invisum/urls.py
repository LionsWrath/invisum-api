from django.conf.urls import url, include

urlpatterns = [
    url(r'^', include('datasets.urls')),
    url(r'^authentication/', include('rest_framework.urls', namespace='rest_framework')),
]
