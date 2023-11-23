from django.urls import path
from .views import index,cadastro_contrato,delete,update,gerador_contrato,gera_nota_servico,gera_nota_remessa,fechar

urlpatterns = [
    path('home/',index,name='index'),
    path('cadastro/',cadastro_contrato,name="insert"),
    path('delete/<int:seq_contrato>',delete,name='delete'),
    path('fechar/<int:seq_contrato>',fechar,name='fechar'),
    path('update/<int:seq_contrato>',update,name='update'),
    path('gera-contrato/<int:seq_contrato>',gerador_contrato,name='gera-contrato'),
    path('gera-nota-serv/<int:seq_contrato>',gera_nota_servico,name='gera-nota-serv'),
    path('gera-nota-remessa/<int:seq_contrato>',gera_nota_remessa,name='gera-nota-remessa')
]

    
