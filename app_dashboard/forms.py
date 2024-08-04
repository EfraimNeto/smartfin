from django import forms
from app_dashboard.models import Fornecedor, Cliente, Recebimento, Pagamento, Loja, UsuarioPerfil, CentroCusto

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
            'loja'
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
            'loja'
        ]


class UsuarioForm(forms.ModelForm):
    lojas = forms.ModelMultipleChoiceField(
        queryset=Loja.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    
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

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.set_password(self.cleaned_data['password'])
            user.save()
            perfil, created = UsuarioPerfil.objects.get_or_create(user=user)
            perfil.lojas.set(self.cleaned_data.get('lojas', []))
            perfil.save()
        return user


class EditUsuarioForm(forms.ModelForm):
    lojas = forms.ModelMultipleChoiceField(
        queryset=Loja.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

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

    def __init__(self, *args, **kwargs):
        # Passar o perfil do usuário para o formulário
        perfil = kwargs.pop('perfil', None)
        super().__init__(*args, **kwargs)
        if perfil:
            self.fields['lojas'].initial = perfil.lojas.all()

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            perfil, created = UsuarioPerfil.objects.get_or_create(user=user)
            perfil.lojas.set(self.cleaned_data.get('lojas', []))
            perfil.save()
        return user


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
            'loja'
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
            'loja'
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
    cliente = forms.ModelChoiceField(queryset=Cliente.objects.all(), empty_label="Selecione um Fornecedor")

    class Meta:
        model = Recebimento
        fields = '__all__'
        widgets = {
            'data_vencimento': forms.widgets.DateInput(attrs={'type': 'date'}),
            'data_recebimento': forms.DateInput(attrs={'type': 'date'}),
            'valor': forms.NumberInput(attrs={'step': '0.01'}),  # Configuração para campos decimais
        }

class PagamentoForm(forms.ModelForm):

    class Meta:
        model = Pagamento
        fields = '__all__'
        widgets = {
            'loja': forms.Select(choices=[(loja.id, loja.nome) for loja in Loja.objects.all()], attrs={'class': 'form-control'}),
            'data_vencimento': forms.widgets.DateInput(attrs={'type': 'date'}),
            'data_pagamento': forms.DateInput(attrs={'type': 'date'})
        }


class EditPagamentoForm(forms.ModelForm):
    fornecedor = forms.ModelChoiceField(queryset=Fornecedor.objects.all(), empty_label="Selecione um Fornecedor")

    class Meta:
        model = Pagamento
        fields = '__all__'
        widgets = {
            'data_vencimento': forms.widgets.DateInput(attrs={'type': 'date'}),
            'data_pagamento': forms.DateInput(attrs={'type': 'date'}),
            'valor': forms.NumberInput(attrs={'step': '0.01'}),  # Configuração para campos decimais
        }

class LojaForm(forms.ModelForm):
    class Meta:
        model = Loja
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        # Formatar o nome: Primeira letra maiúscula e demais minúsculas
        nome_formatado = nome.capitalize().strip()
        # Remover caracteres especiais e acentos
        nome_formatado = nome_formatado.replace('ç', 'c')
        return nome_formatado
    

class CentroCustoForm(forms.ModelForm):
    class Meta:
        model = CentroCusto
        fields = ['nome']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean_nome(self):
        nome = self.cleaned_data.get('nome')
        # Formatar o nome: Primeira letra maiúscula e demais minúsculas
        nome_formatado = nome.capitalize().strip()
        # Remover caracteres especiais e acentos
        nome_formatado = nome_formatado.replace('ç', 'c')
        return nome_formatado