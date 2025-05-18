from django.urls import path, include
from rest_framework.routers import DefaultRouter
from apps.review.api.views import ReviewViewSet

router = DefaultRouter()
router.register('reviews', ReviewViewSet, basename='review')


urlpatterns = [
    path('', include(router.urls))
]
