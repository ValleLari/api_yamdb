from rest_framework import routers
from .views import ReviewViewSet, CommentViewSet

app_name = 'api'

router = routers.DefaultRouter()

router.register(
    r'^titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review')
router.register(
    r'^titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comments')
