from django.contrib import messages
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from datetime import datetime
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import constants as message_constants


# --- Funções Auxiliares de Cálculo (Tabelas Vigentes) ---

def calcular_inss(salario_bruto):
    # Tabela INSS 2024 (Progressiva)
    teto_inss = 7786.02
    
    if salario_bruto > teto_inss:
        return 908.85  # Teto máximo de desconto (aprox, base 14% da faixa final)
    
    desconto = 0.0
    # Faixa 1: 7,5% até 1.412,00
    faixa1 = 1412.00
    # Faixa 2: 9% de 1.412,01 até 2.666,68
    faixa2 = 2666.68
    # Faixa 3: 12% de 2.666,69 até 4.000,03
    faixa3 = 4000.03
    # Faixa 4: 14% de 4.000,04 até 7.786,02
    
    calc_salario = salario_bruto

    # 1ª Faixa
    base = min(calc_salario, faixa1)
    desconto += base * 0.075
    
    # 2ª Faixa
    if calc_salario > faixa1:
        base = min(calc_salario, faixa2) - faixa1
        desconto += base * 0.09
        
    # 3ª Faixa
    if calc_salario > faixa2:
        base = min(calc_salario, faixa3) - faixa2
        desconto += base * 0.12
        
    # 4ª Faixa
    if calc_salario > faixa3:
        base = calc_salario - faixa3
        desconto += base * 0.14
        
    return round(desconto, 2)

def calcular_irrf(salario_bruto, desconto_inss, dependentes=0):
    # Base de cálculo = Salário Bruto - INSS - (Dependentes * 189.59)
    base_calculo = salario_bruto - desconto_inss - (dependentes * 189.59)
    
    # Tabela IRRF 2024 (Progressiva Mensal)
    # Até 2.259,20: Isento
    # 2.259,21 até 2.826,65: 7,5% (Dedução 169,44)
    # 2.826,66 até 3.751,05: 15% (Dedução 381,44)
    # 3.751,06 até 4.664,68: 22,5% (Dedução 662,77)
    # Acima de 4.664,68: 27,5% (Dedução 896,00)

    irrf = 0.0
    
    if base_calculo <= 2259.20:
        return 0.0
    elif base_calculo <= 2826.65:
        irrf = (base_calculo * 0.075) - 169.44
    elif base_calculo <= 3751.05:
        irrf = (base_calculo * 0.15) - 381.44
    elif base_calculo <= 4664.68:
        irrf = (base_calculo * 0.225) - 662.77
    else:
        irrf = (base_calculo * 0.275) - 896.00
        
    # O desconto simplificado de R$ 564,80 pode ser aplicado se for mais vantajoso,
    # mas manteremos a lógica padrão para este exemplo.
    
    return max(round(irrf, 2), 0.0)


# --- Views do Projeto ---

def home(request):
    return render(request,'home.html')

def sobre(request):
    return render(request, 'sobre.html')

def login(request):
    return render(request, 'login.html')

def contato(request):
    return render(request, 'contato.html')

def admin(request):
    return render(request, 'admin.html')

def calcular_rh(request):
    return render(request, 'calcular_rh.html')

def contracheque(request):
    context = {}
    if request.method == 'POST':
        try:
            salario_base = float(request.POST.get('venc_salario', 0))
            if salario_base > 0:
                # Realiza os cálculos
                val_inss = calcular_inss(salario_base)
                val_irrf = calcular_irrf(salario_base, val_inss)
                total_descontos = val_inss + val_irrf
                salario_liquido = salario_base - total_descontos
                
                # Calcula porcentagens efetivas para exibição (apenas informativo)
                porc_inss = round((val_inss / salario_base) * 100, 2)
                porc_irrf = round((val_irrf / salario_base) * 100, 2)

                context = {
                    'calculado': True,
                    'salario_base': f"{salario_base:.2f}",
                    'val_inss': f"{val_inss:.2f}",
                    'porc_inss': porc_inss,
                    'val_irrf': f"{val_irrf:.2f}",
                    'porc_irrf': porc_irrf,
                    'total_descontos': f"{total_descontos:.2f}",
                    'salario_liquido': f"{salario_liquido:.2f}"
                }
        except ValueError:
            context['erro'] = "Valor inválido inserido."

    return render(request, 'contracheque.html', context)

def rescisao(request):
    context = {}
    if request.method == 'POST':
        try:
            data_admissao = request.POST.get('data_admissao')
            data_demissao = request.POST.get('data_demissao')
            motivo = request.POST.get('motivo')
            ultimo_salario = float(request.POST.get('ultimo_salario', 0))

            if data_admissao and data_demissao and ultimo_salario > 0:
                dt_adm = datetime.strptime(data_admissao, '%Y-%m-%d')
                dt_dem = datetime.strptime(data_demissao, '%Y-%m-%d')
                
                # Cálculo simplificado de meses trabalhados no ano (para 13º)
                # Assume-se proporcionalidade do ano corrente ou total se < 1 ano
                # Para simplificar este exemplo escolar: calculamos meses entre as datas
                diff_days = (dt_dem - dt_adm).days
                meses_trabalhados = diff_days / 30 # Aproximação
                meses_proporcionais = int((dt_dem.month - dt_adm.month) + 1) if dt_dem.year == dt_adm.year else dt_dem.month
                
                # Regra de fração superior a 15 dias conta como mês
                if dt_dem.day < 15:
                    meses_proporcionais -= 1
                if meses_proporcionais < 0: meses_proporcionais = 0

                # Cálculos
                saldo_salario = (ultimo_salario / 30) * dt_dem.day
                decimo_terceiro = (ultimo_salario / 12) * meses_proporcionais
                ferias_proporcionais = (ultimo_salario / 12) * meses_proporcionais
                terco_ferias = ferias_proporcionais / 3
                
                total_ferias = ferias_proporcionais + terco_ferias

                # Regras do Motivo
                if motivo == 'justa_causa':
                    decimo_terceiro = 0.0
                    total_ferias = 0.0 # Perde proporcionais
                    # (Férias vencidas continuariam devidas, mas vamos simplificar)
                
                total_rescisao = saldo_salario + decimo_terceiro + total_ferias

                context = {
                    'calculado': True,
                    'data_admissao': data_admissao,
                    'data_demissao': data_demissao,
                    'ultimo_salario': ultimo_salario,
                    'motivo': motivo,
                    'saldo_salario': f"{saldo_salario:.2f}",
                    'decimo_terceiro': f"{decimo_terceiro:.2f}",
                    'total_ferias': f"{total_ferias:.2f}", # Inclui 1/3
                    'total_rescisao': f"{total_rescisao:.2f}"
                }

        except ValueError:
            context['erro'] = "Dados inválidos."

    return render(request, 'rescisao.html', context)