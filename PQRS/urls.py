from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('controls/', include('account.urls')),
    path('adminUser/', include('adminUser.urls')),
    path('__reload__/', include('django_browser_reload.urls')),
    path('api-auth/', include('rest_framework.urls')) # Para la autenticación de la API, actualizacion
]
# Servir archivos estáticos en desarrollo
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Servir archivos de medios en desarrollo
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)