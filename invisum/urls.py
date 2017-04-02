from django.conf.urls import url, include
from rest_framework_jwt.views import obtain_jwt_token
from rest_framework_jwt.views import verify_jwt_token

urlpatterns = [
    url(r'^', include('datasets.urls')),
    url(r'^auth/', obtain_jwt_token, name='jwt_login'),
    url(r'^auth-verify/', verify_jwt_token, name='jwt_verify'),
    url(r'^authentication/', include('rest_framework.urls', namespace='rest_framework')),
]
