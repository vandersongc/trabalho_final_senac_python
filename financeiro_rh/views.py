from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login as auth_login
from datetime import datetime
# Importações dos módulos locais
from .forms import ContrachequeForm, RescisaoForm, ContatoForm, CadastroForm
from .models import HistoricoCalculo
from .utils import calcular_inss, calcular_irrf, calcular_fgts


def home(request):
    return render(request,'home.html')

def sobre(request):
    return render(request, 'sobre.html')

def login(request):
    if request.method == 'POST':
        usuario = request.POST.get('username')
        senha = request.POST.get('password')
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'E-mail ou senha inválidos.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request) 
    return redirect('home') 

def calcular_rh(request):
    return render(request, 'calcular_rh.html')

def cadastro(request):
    if request.method == 'POST':
        form = CadastroForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            messages.success(request, f'Conta criada para {email}! Faça login.')
            return redirect('login') 
    else:
        form = CadastroForm()
    return render(request, 'cadastro.html', {'form': form})

def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            nome = form.cleaned_data['name']
            messages.success(request, f'Obrigado, {nome}! Sua mensagem foi enviada.')
            return redirect('contato')
    return render(request, 'contato.html')

# --- VIEWS DE CÁLCULO ---

@login_required
def contracheque(request):
    context = {}
    if request.method == 'POST':
        form = ContrachequeForm(request.POST)
        if form.is_valid():
            # Captura os dados do formulário
            nome = form.cleaned_data['nome_completo']
            salario_base = float(form.cleaned_data['venc_salario'])
            
            # Cálculos
            val_inss = calcular_inss(salario_base)
            val_irrf = calcular_irrf(salario_base, val_inss)
            val_fgts = calcular_fgts(salario_base)
            
            total_descontos = val_inss + val_irrf
            salario_liquido = salario_base - total_descontos
            
            porc_inss = round((val_inss / salario_base) * 100, 2)
            porc_irrf = round((val_irrf / salario_base) * 100, 2)

            # Salva no histórico
            HistoricoCalculo.objects.create(
                usuario=request.user,
                tipo='contracheque',
                nome_funcionario=nome,
                salario_base=salario_base,
                resultado_liquido=salario_liquido
            )

            # Define o contexto devolvendo os dados para o template
            context = {
                'calculado': True,
                'nome_completo': nome,          # PERSISTÊNCIA: Nome
                'salario_base': f"{salario_base:.2f}", # PERSISTÊNCIA: Valor digitado (formatado)
                
                # Resultados
                'val_inss': f"{val_inss:.2f}",
                'porc_inss': porc_inss,
                'val_irrf': f"{val_irrf:.2f}",
                'porc_irrf': porc_irrf,
                'val_fgts': f"{val_fgts:.2f}",
                'total_descontos': f"{total_descontos:.2f}",
                'salario_liquido': f"{salario_liquido:.2f}"
            }
    return render(request, 'contracheque.html', context)

@login_required
def rescisao(request):
    context = {}
    if request.method == 'POST':
        try:
            # Captura os dados brutos do POST
            nome = request.POST.get('nome_completo')
            data_admissao = request.POST.get('data_admissao')
            data_demissao = request.POST.get('data_demissao')
            motivo = request.POST.get('motivo')
            ultimo_salario_str = request.POST.get('ultimo_salario', '0')
            ultimo_salario = float(ultimo_salario_str) if ultimo_salario_str else 0.0

            if data_admissao and data_demissao and ultimo_salario > 0:
                dt_adm = datetime.strptime(data_admissao, '%Y-%m-%d')
                dt_dem = datetime.strptime(data_demissao, '%Y-%m-%d')
                
                # Lógica de cálculo de datas
                diff_days = (dt_dem - dt_adm).days
                meses_proporcionais = int((dt_dem.month - dt_adm.month) + 1) if dt_dem.year == dt_adm.year else dt_dem.month
                if dt_dem.day < 15: meses_proporcionais -= 1
                if meses_proporcionais < 0: meses_proporcionais = 0

                # Cálculos financeiros
                saldo_salario = (ultimo_salario / 30) * dt_dem.day
                decimo_terceiro = (ultimo_salario / 12) * meses_proporcionais
                ferias_proporcionais = (ultimo_salario / 12) * meses_proporcionais
                terco_ferias = ferias_proporcionais / 3
                
                total_ferias = ferias_proporcionais + terco_ferias

                meses_totais_trabalhados = (dt_dem.year - dt_adm.year) * 12 + dt_dem.month - dt_adm.month
                saldo_fgts_estimado = (ultimo_salario * 0.08) * meses_totais_trabalhados
                multa_fgts = 0.0

                if motivo == 'sem_justa_causa':
                    multa_fgts = saldo_fgts_estimado * 0.40
                elif motivo == 'justa_causa':
                    decimo_terceiro = 0.0
                    total_ferias = 0.0
                    multa_fgts = 0.0
                
                total_rescisao = saldo_salario + decimo_terceiro + total_ferias + multa_fgts

                # Salva no histórico
                HistoricoCalculo.objects.create(
                    usuario=request.user,
                    tipo='rescisao',
                    nome_funcionario=nome,
                    salario_base=ultimo_salario,
                    resultado_liquido=total_rescisao
                )

                # Define o contexto devolvendo TUDO para o template
                context = {
                    'calculado': True,
                    'nome_completo': nome,      # PERSISTÊNCIA
                    'data_admissao': data_admissao, # PERSISTÊNCIA
                    'data_demissao': data_demissao, # PERSISTÊNCIA
                    'ultimo_salario': ultimo_salario, # PERSISTÊNCIA
                    'motivo': motivo,           # PERSISTÊNCIA (para o select)
                    
                    # Resultados
                    'saldo_salario': f"{saldo_salario:.2f}",
                    'decimo_terceiro': f"{decimo_terceiro:.2f}",
                    'total_ferias': f"{total_ferias:.2f}",
                    'multa_fgts': f"{multa_fgts:.2f}",
                    'total_rescisao': f"{total_rescisao:.2f}"
                }

        except ValueError:
            # Em caso de erro, devolve o que foi possível capturar para não limpar tudo
            context['erro'] = "Dados inválidos."
            context['nome_completo'] = request.POST.get('nome_completo')
            context['data_admissao'] = request.POST.get('data_admissao')
            context['data_demissao'] = request.POST.get('data_demissao')
            context['ultimo_salario'] = request.POST.get('ultimo_salario')

    return render(request, 'rescisao.html', context)