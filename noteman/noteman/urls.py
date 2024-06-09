"""
URL configuration for noteman project.
"""
from apps.api.urls import router as api_router
from django.contrib import admin
from django.urls import include, path

# include and providing the module are both valid ways to configure
# urls, include seems better for more than 1 route, I will see in
# the future which one suits particular app better and reorganize
# accoringly
urlpatterns = [
    path('', include('apps.dashboard.urls')),
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/', include(api_router.urls)),
    path('api/', include('apps.api.urls')),
]
