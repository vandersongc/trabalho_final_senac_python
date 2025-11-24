from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from datetime import datetime
# Importações dos nossos novos arquivos
from .forms import ContrachequeForm, RescisaoForm, ContatoForm
from .models import HistoricoCalculo
from .utils import calcular_inss, calcular_irrf, calcular_fgts

def home(request):
    return render(request,'home.html')

def sobre(request):
    return render(request, 'sobre.html')

def login(request):
    return render(request, 'login.html')

def admin(request):
    return render(request, 'admin.html')

def calcular_rh(request):
    return render(request, 'calcular_rh.html')

# --- Views Atualizadas com Melhorias ---

def contato(request):
    if request.method == 'POST':
        form = ContatoForm(request.POST)
        if form.is_valid():
            # Aqui você poderia salvar no banco ou enviar e-mail
            nome = form.cleaned_data['name']
            # Simulação de envio
            messages.success(request, f'Obrigado, {nome}! Sua mensagem foi enviada.')
            return redirect('contato')
    return render(request, 'contato.html')

@login_required
def contracheque(request):
    context = {}
    if request.method == 'POST':
        form = ContrachequeForm(request.POST)
        if form.is_valid():
            salario_base = float(form.cleaned_data['venc_salario'])
            
            # Cálculos via Utils
            val_inss = calcular_inss(salario_base)
            val_irrf = calcular_irrf(salario_base, val_inss)
            val_fgts = calcular_fgts(salario_base)
            
            total_descontos = val_inss + val_irrf
            salario_liquido = salario_base - total_descontos
            
            porc_inss = round((val_inss / salario_base) * 100, 2)
            porc_irrf = round((val_irrf / salario_base) * 100, 2)

            # Salvar Histórico no Banco
            HistoricoCalculo.objects.create(
                usuario=request.user,
                tipo='contracheque',
                salario_base=salario_base,
                resultado_liquido=salario_liquido
            )

            context = {
                'calculado': True,
                'salario_base': f"{salario_base:.2f}",
                'val_inss': f"{val_inss:.2f}",
                'porc_inss': porc_inss,
                'val_irrf': f"{val_irrf:.2f}",
                'porc_irrf': porc_irrf,
                'val_fgts': f"{val_fgts:.2f}", # Novo campo FGTS
                'total_descontos': f"{total_descontos:.2f}",
                'salario_liquido': f"{salario_liquido:.2f}"
            }
    return render(request, 'contracheque.html', context)

@login_required
def rescisao(request):
    context = {}
    if request.method == 'POST':
        # Usamos o form apenas para limpar/validar dados, 
        # mas a lógica manual de request.POST ainda funciona bem para datas se preferir
        # Para manter compatibilidade com seu template atual, vamos extrair direto:
        try:
            data_admissao = request.POST.get('data_admissao')
            data_demissao = request.POST.get('data_demissao')
            motivo = request.POST.get('motivo')
            ultimo_salario = float(request.POST.get('ultimo_salario', 0))

            if data_admissao and data_demissao and ultimo_salario > 0:
                dt_adm = datetime.strptime(data_admissao, '%Y-%m-%d')
                dt_dem = datetime.strptime(data_demissao, '%Y-%m-%d')
                
                # Lógica de Meses
                diff_days = (dt_dem - dt_adm).days
                meses_proporcionais = int((dt_dem.month - dt_adm.month) + 1) if dt_dem.year == dt_adm.year else dt_dem.month
                if dt_dem.day < 15: meses_proporcionais -= 1
                if meses_proporcionais < 0: meses_proporcionais = 0

                # Cálculos Financeiros
                saldo_salario = (ultimo_salario / 30) * dt_dem.day
                decimo_terceiro = (ultimo_salario / 12) * meses_proporcionais
                ferias_proporcionais = (ultimo_salario / 12) * meses_proporcionais
                terco_ferias = ferias_proporcionais / 3
                
                total_ferias = ferias_proporcionais + terco_ferias

                # Multa FGTS (40% sobre o total depositado estimado - Simplificação)
                # Em um sistema real, buscaríamos o saldo real do FGTS. 
                # Aqui estimamos o FGTS total do período para calcular a multa.
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

                # Salvar Histórico
                HistoricoCalculo.objects.create(
                    usuario=request.user,
                    tipo='rescisao',
                    salario_base=ultimo_salario,
                    resultado_liquido=total_rescisao
                )

                context = {
                    'calculado': True,
                    'data_admissao': data_admissao,
                    'data_demissao': data_demissao,
                    'ultimo_salario': ultimo_salario,
                    'motivo': motivo,
                    'saldo_salario': f"{saldo_salario:.2f}",
                    'decimo_terceiro': f"{decimo_terceiro:.2f}",
                    'total_ferias': f"{total_ferias:.2f}",
                    'multa_fgts': f"{multa_fgts:.2f}", # Exibir Multa
                    'total_rescisao': f"{total_rescisao:.2f}"
                }

        except ValueError:
            context['erro'] = "Dados inválidos."

    return render(request, 'rescisao.html', context)