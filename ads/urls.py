from django.urls import include, path
from rest_framework.routers import DefaultRouter

from ads.apps import AdsConfig
from ads.views import AdViewSet, CommentViewSet


app_name = AdsConfig.name

router = DefaultRouter()
router.register(r'ads', AdViewSet, basename='ads')
router.register(r'ads/(?P<ad_pk>\d+)/comments', CommentViewSet, basename='reviews')

urlpatterns = [path("", include(router.urls))]
