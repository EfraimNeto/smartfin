from django.contrib import admin
from app_dashboard.models import Fornecedor, Cliente, Recebimento, Pagamento


admin.site.register(Fornecedor)
admin.site.register(Cliente)
admin.site.register(Recebimento)
admin.site.register(Pagamento)