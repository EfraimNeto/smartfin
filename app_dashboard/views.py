from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm
from django.contrib import messages
from django.db.models import Sum  # Corrigido: importar Sum de models
from .models import Pagamento, Recebimento
from django.utils.dateparse import parse_date
from .models import Recebimento, RECEBIMENTO_STATUS
from datetime import date
import json

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
    # Dados para gráficos
    receitas_por_loja = {
        'Loja A': {'total_receitas': 5000},
        'Loja B': {'total_receitas': 3000}
    }
    custos_por_loja = {
        'Loja A': {'total_custos': 2000},
        'Loja B': {'total_custos': 1000}
    }
    lucro_liquido_por_loja = {
        'Loja A': {'lucro_liquido': 3000},
        'Loja B': {'lucro_liquido': 2000}
    }
    
    # Transformar dados em JSON
    dados_json = json.dumps({
        'receitasPorLoja': receitas_por_loja,
        'custosPorLoja': custos_por_loja,
        'lucroLiquidoPorLoja': lucro_liquido_por_loja
    })

    # Dados para os cartões principais
    pagamentos = Pagamento.objects.order_by('data_vencimento')[:3]
    recebimentos = Recebimento.objects.order_by('data_vencimento')[:3]

    total_pagamento = Pagamento.objects.aggregate(total=Sum('valor'))['total'] or 0
    total_recebimento = Recebimento.objects.aggregate(total=Sum('valor'))['total'] or 0

    # Garantir que os cartões principais exibam 0 se não existirem dados
    if total_pagamento is None:
        total_pagamento = 0
    if total_recebimento is None:
        total_recebimento = 0

    # Dados para o resumo por loja
    resumo_por_loja = {}
    lojas = Pagamento.objects.values_list('loja', flat=True).distinct()
    total_lucro_liquido = 0

    for loja in lojas:
        custos_por_centro = Pagamento.objects.filter(loja=loja).values('centro_custo').annotate(total=Sum('valor')).order_by('centro_custo')
        receitas_por_centro = Recebimento.objects.filter(loja=loja).values('centro_custo').annotate(total=Sum('valor')).order_by('centro_custo')

        total_custos = custos_por_centro.aggregate(total=Sum('total'))['total'] or 0
        total_receitas = receitas_por_centro.aggregate(total=Sum('total'))['total'] or 0
        lucro_liquido = total_receitas - total_custos

        resumo_por_loja[loja] = {
            'total_custos': total_custos,
            'total_receitas': total_receitas,
            'lucro_liquido': lucro_liquido,
            'custos_por_centro': {item['centro_custo']: item['total'] for item in custos_por_centro},
            'receitas_por_centro': {item['centro_custo']: item['total'] for item in receitas_por_centro}
        }

        total_lucro_liquido += lucro_liquido

    return render(request, 'dashboard/home.html', {
        'title': 'Dashboard',
        'pagamentos': pagamentos,
        'recebimentos': recebimentos,
        'total_pagamento': total_pagamento,
        'total_recebimento': total_recebimento,
        'resumo_por_loja': resumo_por_loja,
        'total_lucro_liquido': total_lucro_liquido,
        'dados_json': dados_json,
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
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    data_pagamento_inicio = request.GET.get('data_pagamento_inicio')
    data_pagamento_fim = request.GET.get('data_pagamento_fim')
    loja_filter = request.GET.get('loja')
    centro_custo_filter = request.GET.get('centro_custo')
    status_filter = request.GET.get('status')

    # Converte as datas de início e fim para objetos datetime.date, se válidas
    if data_inicio:
        data_inicio = parse_date(data_inicio)
    if data_fim:
        data_fim = parse_date(data_fim)
    
    if data_pagamento_inicio:
        data_pagamento_inicio = parse_date(data_pagamento_inicio)
    if data_pagamento_fim:
        data_pagamento_fim = parse_date(data_pagamento_fim)

    # Filtra os pagamentos com base nas datas, loja, centro de custo e status fornecidos
    pagamentos = Pagamento.objects.all()
    
    if data_inicio and data_fim:
        pagamentos = pagamentos.filter(data_vencimento__range=[data_inicio, data_fim])
    elif data_inicio:
        pagamentos = pagamentos.filter(data_vencimento__gte=data_inicio)
    elif data_fim:
        pagamentos = pagamentos.filter(data_vencimento__lte=data_fim)

    if data_pagamento_inicio and data_pagamento_fim:
        pagamentos = pagamentos.filter(data_pagamento__range=[data_pagamento_inicio, data_pagamento_fim])
    elif data_pagamento_inicio:
        pagamentos = pagamentos.filter(data_pagamento__gte=data_pagamento_inicio)
    elif data_pagamento_fim:
        pagamentos = pagamentos.filter(data_pagamento__lte=data_pagamento_fim)

    if loja_filter:
        pagamentos = pagamentos.filter(loja=loja_filter)

    if centro_custo_filter:
        pagamentos = pagamentos.filter(centro_custo=centro_custo_filter)

    if status_filter:
        pagamentos = pagamentos.filter(status=status_filter)

    # Obtém todas as lojas distintas e centros de custo para o filtro
    lojas = Pagamento.objects.values_list('loja', flat=True).distinct()
    centros_custo = Pagamento.objects.values_list('centro_custo', flat=True).distinct()

    # Calcula o total dos pagamentos
    total_pagamento = pagamentos.aggregate(Sum('valor'))['valor__sum'] or 0

    # Calcula os totais por status
    total_pendente = Pagamento.objects.filter(status='pendente').aggregate(Sum('valor'))['valor__sum'] or 0
    total_pago = Pagamento.objects.filter(status='pago').aggregate(Sum('valor'))['valor__sum'] or 0
    total_vencido = Pagamento.objects.filter(status='vencido').aggregate(Sum('valor'))['valor__sum'] or 0

    # Ajusta os totais com base no filtro de data
    if data_inicio or data_fim:
        total_pendente = Pagamento.objects.filter(status='pendente', data_vencimento__range=[data_inicio, data_fim] if data_inicio and data_fim else None).aggregate(Sum('valor'))['valor__sum'] or 0
        total_pago = Pagamento.objects.filter(status='pago', data_vencimento__range=[data_inicio, data_fim] if data_inicio and data_fim else None).aggregate(Sum('valor'))['valor__sum'] or 0
        total_vencido = Pagamento.objects.filter(status='vencido', data_vencimento__range=[data_inicio, data_fim] if data_inicio and data_fim else None).aggregate(Sum('valor'))['valor__sum'] or 0

    # Cálculo dos totais por centro de custo
    totais_por_centro_custo = pagamentos.values('centro_custo').annotate(total=Sum('valor')).filter(total__gt=0)

    # Cálculo dos totais por loja
    totais_por_loja = pagamentos.values('loja').annotate(total=Sum('valor')).filter(total__gt=0)
    totais_por_loja_dict = {item['loja']: item['total'] for item in totais_por_loja}

    return render(request, 'pagamentos/pagamentos.html', {
        'title': 'Pagamentos',
        'pagamentos': pagamentos,
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'lojas': lojas,
        'centros_custo': centros_custo,
        'loja_filter': loja_filter,
        'centro_custo_filter': centro_custo_filter,
        'status_filter': status_filter,
        'data_pagamento_inicio': data_pagamento_inicio,
        'data_pagamento_fim': data_pagamento_fim,
        'total_pagamento': total_pagamento,
        'total_pendente': total_pendente,
        'total_pago': total_pago,
        'total_vencido': total_vencido,
        'totais_por_centro_custo': totais_por_centro_custo,
        'totais_por_loja': totais_por_loja_dict,
        'today': date.today()
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
    return render(request, 'pagamentos/editar_pagamento.html', {
        'title': f'Editar Pagamento',
        'form': form
    })

def duplicar_pagamento(request, pagamento_id):
    # Recuperar o pagamento a ser duplicado
    pagamento = get_object_or_404(Pagamento, id=pagamento_id)
    
    # Criar um novo pagamento com os mesmos dados
    novo_pagamento = Pagamento(
        fornecedor=pagamento.fornecedor,
        loja=pagamento.loja,
        centro_custo=pagamento.centro_custo,
        descricao=pagamento.descricao,
        valor=pagamento.valor,
        data_emissao=pagamento.data_emissao,
        data_vencimento=pagamento.data_vencimento,
        status=pagamento.status,
        data_pagamento=pagamento.data_pagamento,
    )
    novo_pagamento.save()
    
    # Redirecionar de volta para a página de listagem com uma mensagem de sucesso
    return redirect('pagamentos')

@login_required
def deletar_pagamento(request, pagamento_id):
    pagamento = get_object_or_404(Pagamento, pk=pagamento_id)

    pagamento.delete()
    messages.success(request, f'Pagamento deletado com sucesso!')
    return redirect('pagamentos')

@login_required
def recebimentos(request):
    data_inicio = request.GET.get('data_inicio')
    data_fim = request.GET.get('data_fim')
    loja_filter = request.GET.get('loja')
    centro_custo_filter = request.GET.get('centro_custo')
    status_filter = request.GET.get('status')
    data_recebimento_inicio = request.GET.get('data_recebimento_inicio')
    data_recebimento_fim = request.GET.get('data_recebimento_fim')

    RECEBIMENTO_STATUS = [
    ('pendente', 'Pendente'),
    ('pago', 'Pago'),
    ('vencido', 'Vencido'),
    ]

    # Converte as datas de início e fim para objetos datetime.date
    if data_inicio:
        data_inicio = parse_date(data_inicio)
    if data_fim:
        data_fim = parse_date(data_fim)

    if data_recebimento_inicio:
        data_recebimento_inicio = parse_date(data_recebimento_inicio)
    if data_recebimento_fim:
        data_recebimento_fim = parse_date(data_recebimento_fim)

    # Filtra os recebimentos com base nas datas, loja e centro de custo fornecidos
    recebimentos = Recebimento.objects.all()
    
    if data_inicio and data_fim:
        recebimentos = recebimentos.filter(data_vencimento__range=[data_inicio, data_fim])
    elif data_inicio:
        recebimentos = recebimentos.filter(data_vencimento__gte=data_inicio)
    elif data_fim:
        recebimentos = recebimentos.filter(data_vencimento__lte=data_fim)

    if loja_filter:
        recebimentos = recebimentos.filter(loja=loja_filter)

    if centro_custo_filter:
        recebimentos = recebimentos.filter(centro_custo=centro_custo_filter)

    if status_filter:
        recebimentos = recebimentos.filter(status=status_filter)

    if data_recebimento_inicio and data_recebimento_fim:
        recebimentos = recebimentos.filter(data_recebimento__range=[data_recebimento_inicio, data_recebimento_fim])
    elif data_recebimento_inicio:
        recebimentos = recebimentos.filter(data_recebimento__gte=data_recebimento_inicio)
    elif data_recebimento_fim:
        recebimentos = recebimentos.filter(data_recebimento__lte=data_recebimento_fim)

    # Obtém todas as lojas distintas e centros de custo para o filtro
    lojas = Recebimento.objects.values_list('loja', flat=True).distinct()
    centros_custo = Recebimento.objects.values_list('centro_custo', flat=True).distinct()

    # Passar RECEBIMENTO_STATUS para o template
    status_options = RECEBIMENTO_STATUS

    # Calcular os totais
    total_recebimento = recebimentos.aggregate(total=Sum('valor'))['total'] or 0

    # Calcula os totais por status
    total_pendente = Recebimento.objects.filter(status='pendente').aggregate(Sum('valor'))['valor__sum'] or 0
    total_pago = Recebimento.objects.filter(status='pago').aggregate(Sum('valor'))['valor__sum'] or 0
    total_vencido = Recebimento.objects.filter(status='vencido').aggregate(Sum('valor'))['valor__sum'] or 0

    # Cálculo dos totais por centro de custo
    totais_por_centro_custo = recebimentos.values('centro_custo').annotate(total=Sum('valor')).filter(total__gt=0)

    # Cálculo dos totais por loja
    totais_por_loja = recebimentos.values('loja').annotate(total=Sum('valor')).filter(total__gt=0)
    totais_por_loja_dict = {item['loja']: item['total'] for item in totais_por_loja}
    

    return render(request, 'recebimentos/recebimentos.html', {
        'title': 'Recebimentos',
        'recebimentos': recebimentos,
        'total_recebimento': total_recebimento,
        'lojas': lojas,
        'centros_custo': centros_custo,  # Adicionado aqui
        'data_inicio': data_inicio,
        'data_fim': data_fim,
        'loja_filter': loja_filter,
        'centro_custo_filter': centro_custo_filter,  # Adicionado aqui
        'status_filter': status_filter,
        'total_pendente': total_pendente,
        'total_pago': total_pago,
        'total_vencido': total_vencido,
        'totais_por_centro_custo': totais_por_centro_custo,
        'totais_por_loja': totais_por_loja_dict,
        'data_recebimento_inicio': data_recebimento_inicio,
        'data_recebimento_fim': data_recebimento_fim,
        'today': date.today()
    })

def duplicar_recebimento(request, recebimento_id):
    # Recuperar o recebimento a ser duplicado
    recebimento = get_object_or_404(Recebimento, id=recebimento_id)
    
    # Criar um novo recebimento com os mesmos dados
    novo_recebimento = Recebimento(
        cliente=recebimento.cliente,
        loja=recebimento.loja,
        centro_custo=recebimento.centro_custo,
        descricao=recebimento.descricao,
        valor=recebimento.valor,
        data_emissao=recebimento.data_emissao,
        data_vencimento=recebimento.data_vencimento,
        status=recebimento.status,
        data_recebimento=recebimento.data_recebimento,  # Inclua data_recebimento se necessário
    )
    novo_recebimento.save()
    
    # Redirecionar de volta para a página de listagem com uma mensagem de sucesso
    messages.success(request, "Recebimento duplicado com sucesso.")
    return redirect('recebimentos')

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
    return render(request, 'recebimentos/editar_recebimento.html', {
        'title': f'Editar Recebimento',
        'form': form
    })

@login_required
def deletar_recebimento(request, recebimento_id):
    recebimento = get_object_or_404(Recebimento, pk=recebimento_id)

    recebimento.delete()
    messages.success(request, f'Recebimento deletado com sucesso!')
    return redirect('recebimentos')


def pagamentos_view(request):
    # Obtendo todos os valores únicos de loja dos pagamentos
    lojas = Pagamento.objects.values_list('loja', flat=True).distinct()
    
    # Filtrando os pagamentos com base nos parâmetros da requisição
    pagamentos = Pagamento.objects.all()
    
    loja_filter = request.GET.get('loja')
    if loja_filter:
        pagamentos = pagamentos.filter(loja=loja_filter)
    
    # Passando os pagamentos e a lista de lojas para o template
    context = {
        'pagamentos': pagamentos,
        'lojas': lojas,
        'total_pagamento': pagamentos.aggregate(Sum('valor'))['valor__sum'] or 0,
    }
    
    return render(request, 'pagamentos.html', context)