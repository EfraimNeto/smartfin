from django.db import models

RECEBIMENTO_STATUS = [
    ('pendente', 'Pendente'),
    ('pago', 'Pago'),
    ('vencido', 'Vencido'),
]

PAGAMENTO_STATUS = [
    ('pendente', 'Pendente'),
    ('pago', 'Pago'),
    ('vencido', 'Vencido'),
]

LOJA_CHOICES = [
        ('BARBACOA', 'Barbacoa'),
        ('BARRA', 'Barra'),
        ('VILAS', 'Vilas'),
        ('SMART', 'Smart'),
        ('DIGITAL', 'Digital'),
        ('APP', 'App'),
]

CENTRO_CUSTO_CHOICES = [
    ('Locação', 'Locação'),
    ('Sistema', 'Sistema'),
    ('Folha de Pagamento', 'Folha de Pagamento'),
    ('Participação dos Lucros', 'Participação dos Lucros'),
    ('Tarifa', 'Tarifa'),
    ('Empréstimos', 'Empréstimos'),
    ('Investimentos', 'Investimentos'),
    ('Campanha', 'Campanha'),
    ('Comissão', 'Comissão'),
    ('Antecipação', 'Antecipação'),
    ('Imposto', 'Imposto'),
    ('Diferido', 'Diferido'),
    ('Extra', 'Extra'),
    ('Manutenção', 'Manutenção'),
    ('Comemoração', 'Comemoração'),
    ('Bonificação', 'Bonificação'),
]

class Fornecedor(models.Model):
    nome = models.CharField(max_length=120, verbose_name='Nome')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    documento = models.CharField(max_length=20, verbose_name='CPF/CNPJ')
    rua = models.CharField(max_length=250, verbose_name='Logradouro')
    numero = models.CharField(max_length=10, verbose_name='Número')
    bairro = models.CharField(max_length=100, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    estado = models.CharField(max_length=2, verbose_name='Estado')
    loja = models.CharField(max_length=10, choices=LOJA_CHOICES, default='BARBACOA', verbose_name='Loja')
    centro_custo = models.CharField(max_length=50, choices=CENTRO_CUSTO_CHOICES, default='', verbose_name='Centro de Custo')

    def __str__(self):
        return self.nome


class Cliente(models.Model):
    nome = models.CharField(max_length=120, verbose_name='Nome')
    telefone = models.CharField(max_length=20, verbose_name='Telefone')
    documento = models.CharField(max_length=20, verbose_name='CPF/CNPJ')
    rua = models.CharField(max_length=250, verbose_name='Logradouro')
    numero = models.CharField(max_length=10, verbose_name='Número')
    bairro = models.CharField(max_length=100, verbose_name='Bairro')
    cidade = models.CharField(max_length=100, verbose_name='Cidade')
    estado = models.CharField(max_length=2, verbose_name='Estado')
    loja = models.CharField(max_length=10, choices=LOJA_CHOICES, default='BARBACOA', verbose_name='Loja')
    centro_custo = models.CharField(max_length=50, choices=CENTRO_CUSTO_CHOICES, default='', verbose_name='Centro de Custo')

    def __str__(self):
        return self.nome


class Recebimento(models.Model):
    STATUS_CHOICES = [
        ('PAGO', 'Pago'),
        ('PENDENTE', 'Pendente'),
        ('VENCIDO', 'Vencido'),
    ]

    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True)
    descricao = models.CharField(max_length=255, verbose_name='Descrição')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    data_emissao = models.DateField(auto_now_add=True, verbose_name='Data de Emissão')
    data_vencimento = models.DateField(verbose_name='Data de Vencimento')
    status = models.CharField(max_length=30, choices=RECEBIMENTO_STATUS, default='pendente')
    loja = models.CharField(max_length=10, choices=LOJA_CHOICES, default='BARBACOA', verbose_name='Loja')
    centro_custo = models.CharField(max_length=50, choices=CENTRO_CUSTO_CHOICES, default='', verbose_name='Centro de Custo')
    data_recebimento = models.DateField(verbose_name='Data de Recebimento', null=True, blank=True)


class Pagamento(models.Model):
    STATUS_CHOICES = [
        ('PAGO', 'Pago'),
        ('PENDENTE', 'Pendente'),
        ('VENCIDO', 'Vencido'),
    ]

    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.SET_NULL, null=True)
    descricao = models.CharField(max_length=255, verbose_name='Descrição')
    valor = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Valor')
    data_emissao = models.DateField(auto_now_add=True, verbose_name='Data de Emissão')
    data_vencimento = models.DateField(verbose_name='Data de Vencimento')
    status = models.CharField(max_length=30, choices=PAGAMENTO_STATUS, default='pendente')
    loja = models.CharField(max_length=10, choices=LOJA_CHOICES, default='BARBACOA', verbose_name='Loja')
    centro_custo = models.CharField(max_length=50, choices=CENTRO_CUSTO_CHOICES, default='', verbose_name='Centro de Custo')
    data_pagamento = models.DateField(verbose_name='Data de Pagamento', null=True, blank=True)