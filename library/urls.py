from rest_framework import routers
from .views import AuthorViewSet

router = routers.DefaultRouter(trailing_slash=False)
router.register(r'authors/?', AuthorViewSet)

urlpatterns = router.urls
