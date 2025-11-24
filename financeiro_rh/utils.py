def calcular_inss(salario_bruto):
    # Teto máximo de contribuição do INSS (valores vigentes devem ser atualizados anualmente)
    teto_inss = 7786.02
    if salario_bruto > teto_inss:
        return 908.85
    
    desconto = 0.0
    # Faixas salariais para cálculo progressivo
    faixa1 = 1412.00
    faixa2 = 2666.68
    faixa3 = 4000.03
    
    calc_salario = salario_bruto

    # Cálculo progressivo: Desconta-se a porcentagem de cada fatia do salário
    
    # 1ª Faixa (7.5%)
    base = min(calc_salario, faixa1)
    desconto += base * 0.075
    
    # 2ª Faixa (9%) - incide sobre o que excede a faixa 1 até o limite da faixa 2
    if calc_salario > faixa1:
        base = min(calc_salario, faixa2) - faixa1
        desconto += base * 0.09
        
    # 3ª Faixa (12%)
    if calc_salario > faixa2:
        base = min(calc_salario, faixa3) - faixa2
        desconto += base * 0.12
        
    # 4ª Faixa (14%)
    if calc_salario > faixa3:
        base = calc_salario - faixa3
        desconto += base * 0.14
        
    return round(desconto, 2)

def calcular_irrf(salario_bruto, desconto_inss, dependentes=0):
    # A base de cálculo do IR é o Salário Bruto menos o INSS e desconto por dependentes
    base_calculo = salario_bruto - desconto_inss - (dependentes * 189.59)
    irrf = 0.0
    
    # Verificação das faixas de alíquota do Imposto de Renda
    if base_calculo <= 2259.20:
        return 0.0 # Isento
    elif base_calculo <= 2826.65:
        irrf = (base_calculo * 0.075) - 169.44 # Alíquota 7.5% - Dedução
    elif base_calculo <= 3751.05:
        irrf = (base_calculo * 0.15) - 381.44  # Alíquota 15% - Dedução
    elif base_calculo <= 4664.68:
        irrf = (base_calculo * 0.225) - 662.77 # Alíquota 22.5% - Dedução
    else:
        irrf = (base_calculo * 0.275) - 896.00 # Alíquota 27.5% - Dedução
        
    # Retorna o maior valor entre o cálculo e 0 (evita valores negativos)
    return max(round(irrf, 2), 0.0)

def calcular_fgts(salario_bruto):
    """Calcula o FGTS (8%) apenas para referência, não é descontado do salário líquido."""
    return round(salario_bruto * 0.08, 2)