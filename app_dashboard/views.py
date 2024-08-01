from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib import messages

from app_dashboard.models import Fornecedor, Cliente, Recebimento, Pagamento
from app_dashboard.forms import FornecedorForm, clientesForm, RecebimentoForm, PagamentoForm, EditFornecedorForm, EditclientesForm, EditRecebimentoForm, EditPagamentoForm

from app_dashboard.forms import UsuarioForm, EditUsuarioForm

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            auth_login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()

    return render(request, 'autenticacao/login.html', {'form': form})


def logout(request):
    auth_logout(request)
    return redirect('login')


@login_required
def home(request):
    pagamento = Pagamento.objects.order_by('data_vencimento')[:3]
    recebimento = Recebimento.objects.order_by('data_vencimento')[:3]
    return render(request, 'dashboard/home.html', {
        'title': 'Dashboard',
        'pagamentos': pagamento,
        'recebimentos': recebimento
        })


@login_required
def fornecedores(request):
    fornecedores = Fornecedor.objects.all()

    return render(request, 'fornecedores/fornecedores.html', {
        'title': 'Fornecedores',
        'fornecedores': fornecedores
    })


@login_required
def adicionar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            novo_fornecedor = form.save()

            messages.success(request, f'Fornecedor "{novo_fornecedor.nome}" adicionado com sucesso!')
            return redirect('fornecedores')
    else:
        form = FornecedorForm()
    return render(request, 'fornecedores/adicionar.html', {
        'title': 'Cadastrar Fornecedor',
        'form': form
    })


@login_required
def editar_fornecedor(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, pk=fornecedor_id)
    if request.method == 'POST':
        form = EditFornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            fornecedor = form.save()
            messages.success(request, f'Fornecedor "{fornecedor.nome}" editado com sucesso!')
            return redirect('fornecedores')
    else:
        form = EditFornecedorForm(instance=fornecedor)
    return render(request, 'fornecedores/adicionar.html', {
        'title': f'Editar Fornecedor: {fornecedor.nome}',
        'form': form
    })

@login_required
def deletar_fornecedor(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, pk=fornecedor_id)

    fornecedor.delete()
    messages.success(request, f'Fornecedor "{fornecedor.nome}" deletado com sucesso!')
    return redirect('fornecedores')

@login_required
def usuarios(request):
    usuarios = User.objects.all()
    return render (request, 'usuarios/usuarios.html', {
        'title': 'Usuários',
        'usuarios': usuarios
    })

@login_required
def adicionar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            dados = form.cleaned_data
            user = form.save(commit=False)
            
            user.set_password(dados['password'])
            user.save()

            messages.success(request, f'Usuario "{user.username}" adicionado com sucesso!')
            return redirect('usuarios')
    else:
        form = UsuarioForm()
    return render(request, 'usuarios/adicionar_user.html', {
        'title': 'Cadastrar Usuario',
        'form': form
    })


@login_required
def editar_usuario(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = EditUsuarioForm(request.POST, instance=user)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Usuario "{user.username}" editado com sucesso!')
            return redirect('usuarios')
    else:
        form = EditUsuarioForm(instance=user)
    return render(request, 'usuarios/adicionar_user.html', {
        'title': f'Editar Usuario: {user.username}',
        'form': form
    })


@login_required
def deletar_usuario(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    user.delete()
    messages.success(request, f'Usuario "{user.username}" deletado com sucesso!')
    return redirect('usuarios')


@login_required
def editar_senha_usuario(request, user_id):
    user = get_object_or_404(User, pk=user_id)

    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Senha do usuário "{user.username}" alterada com sucesso!')
            return redirect('usuarios')
    else:
        form = SetPasswordForm(user)
    return render(request, 'usuarios/adicionar_user.html', {
        'title': f'Alterar Senha do Usuario: {user.username}',
        'form': form
    })


@login_required
def clientes(request):
    clientes = Cliente.objects.all()
    return render(request, 'clientes/clientes.html', {
        'title': 'Cliente',
        'clientes': clientes
                                                      
    })

@login_required
def adicionar_clientes(request):
    if request.method == 'POST':
        form = clientesForm(request.POST)
        if form.is_valid():
            novo_cliente = form.save()

            messages.success(request, f'Cliente "{novo_cliente.nome}" adicionado com sucesso!')
            return redirect('clientes')
    else:
        form = clientesForm()
    return render(request, 'clientes/adicionar_clientes.html', {
        'title': 'Cadastrar Clientes',
        'form': form
    })

@login_required
def editar_clientes(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)
    if request.method == 'POST':
        form = EditclientesForm(request.POST, instance=cliente)
        if form.is_valid():
            cliente = form.save()
            messages.success(request, f'Cliente "{cliente.nome}" editado com sucesso!')
            return redirect('clientes')
    else:
        form = EditclientesForm(instance=cliente)
    return render(request, 'clientes/adicionar_clientes.html', {
        'title': f'Editar Cliente: {cliente.nome}',
        'form': form
    })

@login_required
def deletar_clientes(request, cliente_id):
    cliente = get_object_or_404(Cliente, pk=cliente_id)

    cliente.delete()
    messages.success(request, f'Cliente "{cliente.nome}" deletado com sucesso!')
    return redirect('clientes')


@login_required
def pagamentos(request):
    pagamento = Pagamento.objects.all()
    return render(request, 'pagamentos/pagamentos.html', {
        'title': 'Pagamentos',
        'pagamentos': pagamento
        })

@login_required
def adicionar_pagamento(request):
    if request.method == 'POST':
        form = PagamentoForm(request.POST)
        if form.is_valid():
            pagameento = form.save()
            messages.success(request, f'Pagamento adicionado com sucesso!')
            return redirect('pagamentos')
    else:
        form = PagamentoForm()
    return render(request, 'pagamentos/adicionar_pagamento.html', {
        'title': 'Adicionar Pagamento',
        'form': form
    })

@login_required
def editar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, pk=pagamento_id)
    if request.method == 'POST':
        form = EditPagamentoForm(request.POST, instance=pagamento)
        if form.is_valid():
            pagamento = form.save()
            messages.success(request, f'Pagamento editado com sucesso!')
            return redirect('pagamentos')
    else:
        form = EditPagamentoForm(instance=pagamento)
    return render(request, 'pagamentos/adicionar_pagamento.html', {
        'title': f'Editar Pagamento: ',
        'form': form
    })

@login_required
def deletar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, pk=pagamento_id)

    pagamento.delete()
    messages.success(request, f'Pagamento deletado com sucesso!')
    return redirect('pagamentos')

@login_required
def recebimentos(request):
    recebimentos = Recebimento.objects.all()

    return render(request, 'recebimentos/recebimentos.html', {
        'title': 'Recebimentos',
        'recebimentos': recebimentos
    })


@login_required
def adicionar_recebimento(request):
    if request.method == 'POST':
        form = RecebimentoForm(request.POST)
        if form.is_valid():
            recebimento = form.save()
            messages.success(request, f'Recebimento adicionado com sucesso!')
            return redirect('recebimentos')
    else:
        form = RecebimentoForm()
    return render(request, 'recebimentos/adicionar_recebimento.html', {
        'title': 'Adicionar Recebimento',
        'form': form
    })

@login_required
def editar_recebimento(request, recebimento_id):
    recebimento = get_object_or_404(Recebimento, pk=recebimento_id)
    if request.method == 'POST':
        form = EditRecebimentoForm(request.POST, instance=recebimento)
        if form.is_valid():
            recebimento = form.save()
            messages.success(request, f'Recebimento editado com sucesso!')
            return redirect('recebimentos')
    else:
        form = EditRecebimentoForm(instance=recebimento)
    return render(request, 'recebimentos/adicionar_recebimento.html', {
        'title': f'Editar Recimento: ',
        'form': form
    })

@login_required
def deletar_recebimento(request, recebimento_id):
    recebimento = get_object_or_404(Recebimento, pk=recebimento_id)

    recebimento.delete()
    messages.success(request, f'Recebimento deletado com sucesso!')
    return redirect('recebimentos')