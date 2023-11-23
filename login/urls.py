from django.urls import path
from .views import autenticar_login,login,sair

urlpatterns = [
    path('login/',login,name='login'),
    path('autenticando/',autenticar_login,name='autenticar'),
    path('sair/',sair,name='sair')
]
