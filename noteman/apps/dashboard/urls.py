from django.urls import path

from . import views

app_name = 'dashboard'
# same problem as in stakler app

urlpatterns = [
    path('', views.index, name='index'),
    path('notes/', views.all_notes, name='all_notes'),
    # better to add a trailing slash
    path('notes/<int:note_id>/', views.note_detail, name='note_detail'),
]
