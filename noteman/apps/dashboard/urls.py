from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'dashboard'
# same problem as in stakler app

urlpatterns = [
    path('', views.index, name='index'),
    path('notes/', views.all_notes, name='all_notes'),
    # better to add a trailing slash
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
    path('tags/', views.all_tags, name='all_tags'),
    path('notes/add/', views.add_note, name='add_note'),
    path('note-autocomplete/', views.NoteAutocomplete.as_view(), name='note-autocomplete'),
    path('tag-autocomplete/', views.TagAutocomplete.as_view(), name='tag-autocomplete'),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

