from rest_framework import routers
from .views import AuthorViewSet

router = routers.DefaultRouter()
router.register('authors', AuthorViewSet)

urlpatterns = router.urls
