from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework import routers

from .views import ConnectionViewSet, NoteTagViewSet, NoteViewSet, TagViewSet

router = routers.DefaultRouter()


# given how the router works all query params must come after
# slash, that is begin with '/?' string (excluding quotes)
# further reading: https://stackoverflow.com/questions/1617058/ok-to-skip-slash-before-query-string
router.register(r'notes', NoteViewSet)
router.register(r'tags', TagViewSet)
router.register(r'notetags', NoteTagViewSet)
router.register(r'connections', ConnectionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/', SpectacularSwaggerView.as_view(), name='swagger-ui'),
]
