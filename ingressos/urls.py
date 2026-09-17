from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('jogos/', views.jogos, name='jogos'),
    path('jogos/<int:jogo_id>/comprar/', views.comprar, name='comprar'),
    path('setor/<int:setor_id>/', views.selecionar_setor, name='selecionar_setor'),
    path('resumo/<int:setor_id>/', views.resumo, name='resumo'),

    path(
        'verificacao-facial/<int:setor_id>/',
        views.verificacao_facial,
        name='verificacao_facial'
    ),

    path('finalizar/<int:setor_id>/', views.finalizar_compra, name='finalizar_compra'),
    path('cadastro/', views.cadastro, name='cadastro'),
    path('login/', views.entrar, name='login'),
    path('logout/', views.sair, name='logout'),
    path('meus-pedidos/', views.meus_pedidos, name='meus_pedidos'),
]