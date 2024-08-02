from django import forms
from app_dashboard.models import Fornecedor, Cliente, Recebimento, Pagamento

from django.contrib.auth.models import User

class FornecedorForm(forms.ModelForm):
    
    class Meta:
        model = Fornecedor
        fields = [
            'nome', 
            'telefone', 
            'documento', 
            'rua', 
            'numero', 
            'bairro', 
            'cidade', 
            'estado',
            'loja',
            'centro_custo'
        ]

class EditFornecedorForm(forms.ModelForm):
    
    class Meta:
        model = Fornecedor
        fields = [
            'nome', 
            'telefone', 
            'documento', 
            'rua', 
            'numero', 
            'bairro', 
            'cidade', 
            'estado',
            'loja',
            'centro_custo'
        ]


class UsuarioForm(forms.ModelForm):
    
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password',
            'is_superuser',
            'first_name',
            'last_name',
            'is_staff',
            'is_active'
        ]
        widgets = {
            'password': forms.widgets.PasswordInput
        }


class EditUsuarioForm(forms.ModelForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'is_superuser',
            'first_name',
            'last_name',
            'is_staff',
            'is_active'
        ]


class clientesForm(forms.ModelForm):
    
    class Meta:
        model = Cliente
        fields = [
            'nome', 
            'telefone', 
            'documento', 
            'rua', 
            'numero', 
            'bairro', 
            'cidade', 
            'estado',
            'loja',
            'centro_custo'
        ]

class EditclientesForm(forms.ModelForm):
    
    class Meta:
        model = Cliente
        fields = [
            'nome', 
            'telefone', 
            'documento', 
            'rua', 
            'numero', 
            'bairro', 
            'cidade', 
            'estado',
            'loja',
            'centro_custo'
        ]


class RecebimentoForm(forms.ModelForm):

    class Meta:
        model = Recebimento
        fields = '__all__'
        widgets = {
            'data_vencimento': forms.widgets.DateInput(attrs={'type': 'date'}),
            'data_recebimento': forms.DateInput(attrs={'type': 'date'})
        }


class EditRecebimentoForm(forms.ModelForm):

    class Meta:
        model = Recebimento
        fields = '__all__'
        widgets = {
            'data_vencimento': forms.widgets.DateInput(attrs={'type': 'date'}),
            'data_recebimento': forms.DateInput(attrs={'type': 'date'})
        }

class PagamentoForm(forms.ModelForm):

    class Meta:
        model = Pagamento
        fields = '__all__'
        widgets = {
            'data_vencimento': forms.widgets.DateInput(attrs={'type': 'date'}),
            'data_pagamento': forms.DateInput(attrs={'type': 'date'})
        }


class EditPagamentoForm(forms.ModelForm):

    class Meta:
        model = Pagamento
        fields = '__all__'
        widgets = {
            'data_vencimento': forms.widgets.DateInput(attrs={'type': 'date'}),
            'data_pagamento': forms.DateInput(attrs={'type': 'date'})
        }