from django.urls import path
from .views import login_contacto,guardar,regiones_comunas

urlpatterns = [
    path('',login_contacto, name='login'),
    path('save/', guardar, name='guardar'),
    path('comuna/', regiones_comunas,name='comunas' )
]
