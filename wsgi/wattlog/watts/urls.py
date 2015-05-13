from django.conf.urls import patterns, include, url
# from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework import routers, serializers, viewsets

from . import views


# Routers provide an easy way of automatically determining the URL conf.
router = routers.SimpleRouter()
router.register(r'measurements', views.MeasurementViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.

urlpatterns = patterns('',
    url(r'^usage/?$', views.total_watt_hours, name='total_watt_hours'),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
)

