from django.contrib import admin
from app_dashboard.models import Fornecedor, Cliente, Recebimento, Pagamento, UsuarioPerfil, Loja, CentroCusto


admin.site.register(Fornecedor)
admin.site.register(Cliente)
admin.site.register(Recebimento)
admin.site.register(Pagamento)
admin.site.register(UsuarioPerfil)
admin.site.register(Loja)
admin.site.register(CentroCusto)