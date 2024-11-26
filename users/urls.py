from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    path('', openPQRS, name="home"),
    path('crearPQRS/', createdPQRS, name="createdpqrs"),
    path('pqrs-cerradas/', closePQRS, name="closedpqrs"),
    path('pqrs-expiradas/', expiredPQRS, name="expiredpqrs"),
    path('pqrs-en-espera/', waitResponsePQRS, name="waitingpqrs"),
    path('pqrs/<str:num>/', pqrs, name="findpqrs"),
    path('cerrarPQRS/<str:num>/', closedPQRS, name="closepqrs")
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
