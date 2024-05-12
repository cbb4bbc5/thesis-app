from rest_framework import routers

from .views import NoteTagViewSet, NoteViewSet, TagViewSet

# for now router is unused
router = routers.DefaultRouter()

router.register(r'notes', NoteViewSet)
router.register(r'tags', TagViewSet)
router.register(r'notetags', NoteTagViewSet)
