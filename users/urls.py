from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from .views import *

urlpatterns = [
    path('', openPQRS, name="home"),
    path('crearPQRS/', createdPQRS, name="createdpqrs"),
    path('pqrs-cerradas/', closePQRS, name="closedpqrs"),
    path('pqrs-cerradas-por-asociado/', closeForUserPQRS, name="closedforuserpqrs"),
    path('pqrs-expiradas/', expiredPQRS, name="expiredpqrs"),
    path('pqrs-en-espera/', waitResponsePQRS, name="waitingpqrs"),
    path('pqrs/<str:num>/', pqrs, name="findpqrs"),
    path('cerrarPQRS/<str:num>/', closedPQRS, name="closepqrs"),
    path('solicitud-pqrs/<str:num>/<str:token>/', checkSuccessfull, name="checkSuccess"),
    path('solicitud-finalizada-sin-exito/<str:num>/<str:token>/', checkBad, name="checkfailed"),
    path('solicitud-finalizada', success, name="success"),
    path('solicitud-pendiente', failed, name="failed"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
