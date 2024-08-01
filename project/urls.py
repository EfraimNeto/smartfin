from django.contrib import admin
from django.urls import path
from app_dashboard import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', views.home, name='home'),
    
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    
    path('fornecedores/', views.fornecedores, name='fornecedores'),
    path('fornecedores/adicionar/', views.adicionar_fornecedor, name='adicionar_fornecedor'),
    path('fornecedores/editar/<fornecedor_id>/', views.editar_fornecedor, name='editar_fornecedor'),
    path('fornecedores/deletar/<fornecedor_id>/', views.deletar_fornecedor, name='deletar_fornecedor'),

    path('clientes/', views.clientes, name='clientes'),
    path('clientes/adicionar/', views.adicionar_clientes, name='adicionar_clientes'),
    path('clientes/editar/<cliente_id>/', views.editar_clientes, name='editar_clientes'),
    path('clientes/deletar/<cliente_id>/', views.deletar_clientes, name='deletar_clientes'),

    path('usuarios/', views.usuarios, name='usuarios'),
    path('usuarios/adicionar/', views.adicionar_usuario, name='adicionar_user'),
    path('usuarios/editar/<user_id>/', views.editar_usuario, name='editar_user'),
    path('usuarios/alterar-senha/<user_id>/', views.editar_senha_usuario, name='alterar_senha_user'),
    path('usuarios/deletar/<user_id>/', views.deletar_usuario, name='deletar_user'),

    path('pagamentos/', views.pagamentos, name='pagamentos'),
    path('pagamentos/adicionar', views.adicionar_pagamento, name='adicionar_pagamento'),
    path('pagamentos/editar/<pagamento_id>/', views.editar_pagamento, name='editar_pagamento'),
    path('pagamentos/deletar/<pagamento_id>/', views.deletar_pagamento, name='deletar_pagamento'),

    path('recebimentos/', views.recebimentos, name='recebimentos'),
    path('recebimentos/adicionar', views.adicionar_recebimento, name='adicionar_recebimento'),
    path('recebimentos/editar/<recebimento_id>/', views.editar_recebimento, name='editar_recebimento'),
    path('recebimento/deletar/<recebimento_id>/', views.deletar_recebimento, name='deletar_recebimento'),
]
